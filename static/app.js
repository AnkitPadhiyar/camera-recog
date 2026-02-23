// Gesture AI Agent Dashboard - Frontend Logic

// Configuration
const API_BASE = '/api';
const UPDATE_INTERVAL = 500; // milliseconds
const STATS_UPDATE_INTERVAL = 2000;

// State
let agentState = {
    running: false,
    voiceEnabled: false,
    logs: []
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Gesture AI Agent Dashboard');
    
    // Initialize the agent
    fetch(`${API_BASE}/init`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Agent initialized:', data);
            addLog('System initialized', 'info');
            
            // Check voice availability
            checkVoiceAvailability();
        })
        .catch(error => {
            console.error('Initialization error:', error);
            addLog('Failed to initialize agent', 'error');
        });
    
    // Start video stream handler
    handleVideoStream();
    
    // Start status updates
    startStatusUpdates();
    startStatsUpdates();
    updateSystemTime();
    setInterval(updateSystemTime, 1000);
    
    // Auto-refresh gesture history
    setInterval(updateGestureHistory, 3000);
});

// ==================== Control Functions ====================

function startAgent() {
    console.log('Starting agent...');
    
    fetch(`${API_BASE}/start`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Agent started successfully');
                agentState.running = true;
                updateControlButtons();
                addLog('Agent started', 'success');
            } else {
                console.error('Failed to start agent:', data.error);
                addLog(`Failed to start: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            console.error('Start error:', error);
            addLog('Connection error', 'error');
        });
}

function stopAgent() {
    console.log('Stopping agent...');
    
    fetch(`${API_BASE}/stop`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Agent stopped successfully');
                agentState.running = false;
                updateControlButtons();
                addLog('Agent stopped', 'warning');
            } else {
                console.error('Failed to stop agent:', data.error);
                addLog(`Failed to stop: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            console.error('Stop error:', error);
            addLog('Connection error', 'error');
        });
}

function toggleVoice() {
    console.log('Toggling voice commands...');
    
    fetch(`${API_BASE}/voice/toggle`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                agentState.voiceEnabled = data.enabled;
                updateVoiceButton();
                addLog(data.message, 'info');
            } else {
                console.error('Failed to toggle voice:', data.error);
                addLog(`Voice error: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            console.error('Voice toggle error:', error);
            addLog('Voice command error', 'error');
        });
}

// ==================== Video Stream Handler ====================

function handleVideoStream() {
    const videoImg = document.getElementById('videoFeed');
    const streamStatus = document.getElementById('streamStatus');
    
    if (!videoImg) return;
    
    // Function to refresh video frame
    function refreshVideoFrame() {
        // Add timestamp to prevent caching
        const timestamp = new Date().getTime();
        const frameUrl = `${API_BASE}/video_feed?t=${timestamp}`;
        
        // Try to fetch directly for mjpeg stream
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/api/video_feed', true);
        xhr.responseType = 'blob';
        
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Create object URL from blob
                const blob = xhr.response;
                const url = URL.createObjectURL(blob);
                videoImg.src = url;
                
                // Update status
                if (streamStatus) {
                    streamStatus.innerHTML = '<i class="bi bi-circle-fill"></i> Live';
                    streamStatus.className = 'badge bg-success position-absolute top-0 end-0 m-2';
                }
            }
        };
        
        xhr.onerror = function() {
            if (streamStatus) {
                streamStatus.innerHTML = '<i class="bi bi-circle-fill"></i> Offline';
                streamStatus.className = 'badge bg-danger position-absolute top-0 end-0 m-2';
            }
        };
        
        xhr.send();
    }
    
    // Try alternative approach: use img src with mjpeg directly
    try {
        videoImg.src = '/api/video_feed';
        if (streamStatus) {
            streamStatus.className = 'badge bg-success position-absolute top-0 end-0 m-2';
            streamStatus.innerHTML = '<i class="bi bi-circle-fill"></i> Live';
        }
    } catch (e) {
        console.error('Video stream error:', e);
        if (streamStatus) {
            streamStatus.className = 'badge bg-danger position-absolute top-0 end-0 m-2';
            streamStatus.innerHTML = '<i class="bi bi-circle-fill"></i> Error';
        }
    }
    
    // Poll for updates every second
    setInterval(refreshVideoFrame, 1000);
}

// ==================== Status Updates ====================

function startStatusUpdates() {
    // Update status every UPDATE_INTERVAL
    setInterval(updateStatus, UPDATE_INTERVAL);
    updateStatus(); // Initial update
}

function updateStatus() {
    fetch(`${API_BASE}/status`)
        .then(response => response.json())
        .then(data => {
            // Update agent status
            document.getElementById('agentStatus').textContent = 
                data.running ? 'Running' : 'Stopped';
            
            // Update frame count
            document.getElementById('frameCount').textContent = data.frame_count;
            
            // Update gesture detection
            const gestureType = document.getElementById('gestureType');
            if (data.current_gesture) {
                gestureType.textContent = data.current_gesture;
                gestureType.className = 'badge bg-primary fs-5';
            } else {
                gestureType.textContent = 'None';
                gestureType.className = 'badge bg-secondary fs-5';
            }
            
            // Update gesture confidence
            const gestureConfidence = Math.round(data.gesture_confidence * 100);
            updateProgressBar('gestureConfidence', gestureConfidence);
            document.getElementById('gestureConfidenceText').textContent = gestureConfidence + '%';
            
            // Update emotion detection
            const emotionType = document.getElementById('emotionType');
            if (data.current_emotion) {
                emotionType.textContent = data.current_emotion;
                emotionType.className = `badge bg-${getEmotionColor(data.current_emotion)} fs-5`;
            } else {
                emotionType.textContent = 'None';
                emotionType.className = 'badge bg-secondary fs-5';
            }
            
            // Update emotion confidence
            const emotionConfidence = Math.round(data.emotion_confidence * 100);
            updateProgressBar('emotionConfidence', emotionConfidence);
            document.getElementById('emotionConfidenceText').textContent = emotionConfidence + '%';
            
            // Update last action
            if (data.last_action) {
                document.getElementById('lastAction').textContent = data.last_action;
                if (data.last_action_time) {
                    const actionTime = new Date(data.last_action_time);
                    document.getElementById('lastActionTime').textContent = 
                        'At ' + actionTime.toLocaleTimeString();
                }
            }
            
            // Update voice status
            const voiceStatus = document.getElementById('voiceStatus');
            voiceStatus.textContent = data.voice_enabled ? 'Enabled' : 'Disabled';
            voiceStatus.className = data.voice_enabled ? 'badge bg-success' : 'badge bg-danger';
            
        })
        .catch(error => {
            console.error('Status update error:', error);
            updateHealthIndicator(false);
        });
}

function startStatsUpdates() {
    setInterval(updateStats, STATS_UPDATE_INTERVAL);
    updateStats(); // Initial update
}

function updateStats() {
    fetch(`${API_BASE}/gesture_stats`)
        .then(response => response.json())
        .then(data => {
            // Update total gestures
            document.getElementById('totalGestures').textContent = data.total_gestures;
            
            // Update average confidence
            const avgConf = Math.round(data.average_confidence * 100);
            document.getElementById('avgConfidence').textContent = avgConf + '%';
            
            // Update most common gesture
            const mostCommon = document.getElementById('mostCommon');
            mostCommon.textContent = data.most_common || '—';
            
            // Update gesture breakdown
            updateGestureBreakdown(data.gesture_types);
        })
        .catch(error => {
            console.error('Stats update error:', error);
        });
}

// ==================== History Functions ====================

function updateGestureHistory() {
    fetch(`${API_BASE}/gesture_history?limit=20`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('gestureHistoryBody');
            
            if (data.history.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No gesture history yet</td></tr>';
                return;
            }
            
            // Sort by timestamp (newest first)
            const sorted = data.history.sort((a, b) => 
                new Date(b.timestamp) - new Date(a.timestamp)
            );
            
            tbody.innerHTML = sorted.map(entry => `
                <tr>
                    <td class="text-muted small">${formatTime(entry.timestamp)}</td>
                    <td><span class="badge bg-primary">${entry.gesture}</span></td>
                    <td>${Math.round(entry.confidence * 100)}%</td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('History update error:', error);
        });
}

function updateGestureBreakdown(gestureTypes) {
    const container = document.getElementById('gestureBreakdown');
    
    if (Object.keys(gestureTypes).length === 0) {
        container.innerHTML = '<p class="text-muted small">No data yet</p>';
        return;
    }
    
    // Sort by count (descending)
    const sorted = Object.entries(gestureTypes)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5); // Top 5
    
    container.innerHTML = sorted.map(([gesture, count]) => `
        <div class="gesture-breakdown-item">
            <span>${gesture}</span>
            <span class="badge bg-info">${count}</span>
        </div>
    `).join('');
}

// ==================== UI Helper Functions ====================

function updateControlButtons() {
    const btnStart = document.getElementById('btnStart');
    const btnStop = document.getElementById('btnStop');
    
    if (agentState.running) {
        btnStart.disabled = true;
        btnStop.disabled = false;
    } else {
        btnStart.disabled = false;
        btnStop.disabled = true;
    }
}

function updateVoiceButton() {
    const btnVoice = document.getElementById('btnVoice');
    
    if (agentState.voiceEnabled) {
        btnVoice.className = 'btn btn-danger btn-lg';
        btnVoice.innerHTML = '<i class="bi bi-mic-mute"></i> Disable Voice';
    } else {
        btnVoice.className = 'btn btn-warning btn-lg';
        btnVoice.innerHTML = '<i class="bi bi-mic"></i> Enable Voice';
    }
}

function updateProgressBar(elementId, percentage) {
    const bar = document.getElementById(elementId);
    const clampedPercent = Math.min(100, Math.max(0, percentage));
    bar.style.width = clampedPercent + '%';
    
    // Change color based on percentage
    if (clampedPercent >= 80) {
        bar.className = 'progress-bar bg-success';
    } else if (clampedPercent >= 50) {
        bar.className = 'progress-bar bg-info';
    } else {
        bar.className = 'progress-bar bg-warning';
    }
}

function updateHealthIndicator(healthy) {
    const status = document.getElementById('healthStatus');
    
    if (healthy) {
        status.className = 'badge bg-success me-2';
        status.innerHTML = '<i class="bi bi-circle-fill"></i> Connected';
    } else {
        status.className = 'badge bg-danger me-2';
        status.innerHTML = '<i class="bi bi-circle-fill"></i> Disconnected';
    }
}

function updateSystemTime() {
    const time = new Date().toLocaleTimeString();
    document.getElementById('systemTime').textContent = time;
}

function getEmotionColor(emotion) {
    const colors = {
        'happy': 'success',
        'sad': 'danger',
        'angry': 'danger',
        'surprised': 'warning',
        'neutral': 'secondary',
        'fearful': 'danger',
        'disgusted': 'warning'
    };
    return colors[emotion] || 'secondary';
}

// ==================== Logging Functions ====================

function addLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = {
        message,
        type,
        timestamp
    };
    
    agentState.logs.push(logEntry);
    
    // Keep only last 50 logs
    if (agentState.logs.length > 50) {
        agentState.logs.shift();
    }
    
    updateLogsDisplay();
    console.log(`[${type.toUpperCase()}] ${message}`);
}

function updateLogsDisplay() {
    const logsList = document.getElementById('logsList');
    
    if (agentState.logs.length === 0) {
        logsList.innerHTML = '<p class="text-muted small p-2">No events yet</p>';
        return;
    }
    
    // Show newest logs first
    logsList.innerHTML = agentState.logs
        .reverse()
        .map(log => {
            let badgeClass = 'bg-info';
            if (log.type === 'error') badgeClass = 'bg-danger';
            else if (log.type === 'warning') badgeClass = 'bg-warning text-dark';
            else if (log.type === 'success') badgeClass = 'bg-success';
            
            return `
                <div class="list-group-item d-flex justify-content-between align-items-start">
                    <div>
                        <span class="badge ${badgeClass} me-2">${log.type.toUpperCase()}</span>
                        <span>${log.message}</span>
                    </div>
                    <span class="text-muted small">${log.timestamp}</span>
                </div>
            `;
        })
        .join('');
}

// ==================== Utility Functions ====================

function formatTime(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleTimeString();
    } catch (e) {
        return 'N/A';
    }
}

function formatTimestamp(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleString();
    } catch (e) {
        return 'N/A';
    }
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    addLog(`Error: ${event.message}`, 'error');
});

// Network error handling
window.addEventListener('offline', function() {
    console.warn('Network connection lost');
    addLog('Network connection lost', 'error');
    updateHealthIndicator(false);
});

window.addEventListener('online', function() {
    console.log('Network connection restored');
    addLog('Network connection restored', 'success');
    updateHealthIndicator(true);
});

// ==================== Screenshot Functions ====================

function takeScreenshot() {
    console.log('Taking screenshot...');
    
    fetch(`${API_BASE}/screenshot`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addLog(`Screenshot saved: ${data.filename}`, 'success');
            } else {
                addLog(`Failed to take screenshot: ${data.error}`, 'error');
            }
        })
        .catch(error => {
            console.error('Screenshot error:', error);
            addLog('Screenshot error', 'error');
        });
}

function toggleAutoScreenshot() {
    console.log('Toggling auto-screenshot...');
    
    const payload = { interval: 5 };
    
    fetch(`${API_BASE}/screenshot/auto`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        addLog(data.message, 'success');
        
        // Update button appearance
        const btn = document.getElementById('btnAutoScreenshot');
        if (data.enabled) {
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-primary');
        } else {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-secondary');
        }
    })
    .catch(error => {
        console.error('Auto-screenshot toggle error:', error);
        addLog('Auto-screenshot error', 'error');
    });
}

// ==================== Voice Availability Check ====================

function checkVoiceAvailability() {
    fetch(`${API_BASE}/voice/status`)
        .then(response => response.json())
        .then(data => {
            const btnVoice = document.getElementById('btnVoice');
            const btnVoiceText = document.getElementById('btnVoiceText');
            
            if (!data.available) {
                // Microphone not available
                btnVoice.disabled = true;
                btnVoice.className = 'btn btn-secondary btn-lg';
                btnVoiceText.textContent = 'Microphone Not Available';
                btnVoice.title = 'Microphone is not available on this system';
                addLog('Microphone not available - voice commands disabled', 'warning');
            } else {
                // Microphone is available
                btnVoice.disabled = false;
                updateVoiceButton();
            }
        })
        .catch(error => {
            console.error('Voice status check error:', error);
        });
}

// Log initial startup
addLog('Dashboard loaded successfully', 'success');
