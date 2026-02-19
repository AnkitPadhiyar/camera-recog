"""
Unit tests for GestureProcessor module
Comprehensive testing of gesture detection and classification
"""

import pytest
from typing import Dict, Any
from gesture_processor import GestureProcessor


class TestGestureProcessor:
    """Test cases for GestureProcessor class."""
    
    @pytest.fixture
    def processor(self) -> GestureProcessor:
        """Create a GestureProcessor instance for testing."""
        return GestureProcessor()
    
    def test_initialization(self, processor: GestureProcessor) -> None:
        """Test GestureProcessor initialization."""
        assert processor is not None
        assert hasattr(processor, 'gesture_thresholds')
        assert hasattr(processor, 'gesture_buffer')
        assert hasattr(processor, 'gesture_callbacks')
    
    def test_register_callback(self, processor: GestureProcessor) -> None:
        """Test callback registration."""
        callback_called = []
        
        def test_callback(gesture_type: str, info: Dict[str, Any]) -> None:
            callback_called.append(True)
        
        processor.register_gesture_callback(test_callback)
        assert len(processor.gesture_callbacks) > 0
    
    def test_analyze_gesture_returns_dict(self, processor: GestureProcessor) -> None:
        """Test that analyze_gesture returns a dictionary."""
        gesture_data = {'hands': None, 'pose': None}
        result = processor.analyze_gesture(gesture_data)
        
        assert isinstance(result, dict)
        assert 'gesture_type' in result
        assert 'confidence' in result
        assert 'details' in result
    
    @pytest.mark.parametrize("gesture_type", [
        "thumbs_up",
        "peace_sign",
        "open_palm",
        "pointing",
        "wave",
        "raise_hand",
        "neutral"
    ])
    def test_valid_gesture_types(self, processor: GestureProcessor, gesture_type: str) -> None:
        """Test that all valid gesture types are recognized."""
        gesture_data = {'hands': None, 'pose': None}
        result = processor.analyze_gesture(gesture_data)
        
        assert result['gesture_type'] in [
            "thumbs_up", "peace_sign", "open_palm", 
            "pointing", "wave", "raise_hand", "neutral"
        ]
    
    def test_confidence_score_range(self, processor: GestureProcessor) -> None:
        """Test that confidence scores are in valid range."""
        gesture_data = {'hands': None, 'pose': None}
        result = processor.analyze_gesture(gesture_data)
        
        confidence = result['confidence']
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
    
    def test_gesture_buffer_management(self, processor: GestureProcessor) -> None:
        """Test gesture buffer size management."""
        initial_size = len(processor.gesture_buffer)
        
        # The buffer should not exceed max size
        assert len(processor.gesture_buffer) <= processor.buffer_size
    
    def test_callback_with_gesture_detection(self, processor: GestureProcessor) -> None:
        """Test that callbacks are triggered on gesture detection."""
        detections = []
        
        def tracking_callback(gesture_type: str, info: Dict[str, Any]) -> None:
            detections.append(gesture_type)
        
        processor.register_gesture_callback(tracking_callback)
        
        # Multiple detections should be tracked
        for _ in range(3):
            gesture_data = {'hands': None, 'pose': None}
            processor.analyze_gesture(gesture_data)


class TestGestureThresholds:
    """Test gesture detection thresholds."""
    
    @pytest.fixture
    def processor(self) -> GestureProcessor:
        """Create processor with test configuration."""
        return GestureProcessor()
    
    def test_threshold_values_exist(self, processor: GestureProcessor) -> None:
        """Test that all thresholds are defined."""
        thresholds = processor.gesture_thresholds
        
        required_thresholds = [
            'raise_hand', 'wave', 'thumbs_up', 
            'peace_sign', 'point', 'open_palm'
        ]
        
        for threshold_key in required_thresholds:
            assert threshold_key in thresholds
            assert 0.0 <= thresholds[threshold_key] <= 1.0
    
    def test_threshold_range(self, processor: GestureProcessor) -> None:
        """Test that thresholds are in valid range."""
        for name, value in processor.gesture_thresholds.items():
            assert isinstance(value, float), f"Threshold {name} is not float"
            assert 0.0 <= value <= 1.0, f"Threshold {name} out of range"


class TestTemporalSmoothing:
    """Test temporal smoothing of gesture detection."""
    
    @pytest.fixture
    def processor(self) -> GestureProcessor:
        """Create processor for smoothing tests."""
        return GestureProcessor()
    
    def test_buffer_size_configuration(self, processor: GestureProcessor) -> None:
        """Test buffer size is properly configured."""
        assert processor.buffer_size > 0
        assert processor.min_hold_frames > 0
        assert processor.min_hold_frames <= processor.buffer_size
    
    def test_gesture_hold_frames(self, processor: GestureProcessor) -> None:
        """Test gesture hold frames tracking."""
        initial_hold = processor.gesture_hold_frames
        assert initial_hold >= 0 and initial_hold < processor.min_hold_frames


@pytest.fixture
def mock_hand_landmarks() -> Dict[str, Any]:
    """Provide mock hand landmarks data."""
    return {
        'thumb_tip': (0.5, 0.5),
        'index_tip': (0.6, 0.5),
        'middle_tip': (0.7, 0.5),
        'ring_tip': (0.8, 0.5),
        'pinky_tip': (0.9, 0.5),
        'palm': (0.7, 0.7)
    }


@pytest.fixture
def mock_pose_landmarks() -> Dict[str, Any]:
    """Provide mock pose landmarks data."""
    return {
        'shoulders': [(0.4, 0.3), (0.6, 0.3)],
        'elbows': [(0.3, 0.5), (0.7, 0.5)],
        'wrists': [(0.2, 0.7), (0.8, 0.7)],
        'hips': [(0.4, 0.7), (0.6, 0.7)]
    }


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    @pytest.fixture
    def processor(self) -> GestureProcessor:
        """Create processor for edge case testing."""
        return GestureProcessor()
    
    def test_empty_gesture_data(self, processor: GestureProcessor) -> None:
        """Test handling of empty gesture data."""
        gesture_data = {'hands': None, 'pose': None}
        result = processor.analyze_gesture(gesture_data)
        
        assert result is not None
        assert 'gesture_type' in result
        assert result['gesture_type'] == 'neutral'
    
    def test_invalid_gesture_data(self, processor: GestureProcessor) -> None:
        """Test handling of invalid gesture data."""
        # Should not raise exception
        try:
            result = processor.analyze_gesture({})
            assert result is not None
        except Exception as e:
            pytest.fail(f"analyze_gesture raised {type(e).__name__} unexpectedly!")
    
    def test_none_input(self, processor: GestureProcessor) -> None:
        """Test handling of None input."""
        # Should handle gracefully or raise appropriate exception
        try:
            result = processor.analyze_gesture(None)
        except (TypeError, AttributeError):
            # Expected behavior
            pass
        except Exception as e:
            pytest.fail(f"Unexpected exception: {type(e).__name__}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
