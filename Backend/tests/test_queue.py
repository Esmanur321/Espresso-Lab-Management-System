"""
Test: Asynchronous Queue Consumer
Validates the callback function and event processing logic.
"""
import json
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# We need to handle the case that pika might not be available in test env
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_callback_payment_processed(caplog, db_session):
    """Test that payment_processed event is handled correctly."""
    import logging
    from queue_consumer import callback

    ch = MagicMock()
    method = MagicMock()
    properties = MagicMock()

    event = {
        "event": "payment_processed",
        "order_id": 42,
        "status": "success"
    }
    body = json.dumps(event).encode()

    with caplog.at_level(logging.INFO, logger="QueueConsumer"):
        with patch("time.sleep"):  # skip actual sleep
            callback(ch, method, properties, body)

    ch.basic_ack.assert_called_once()
    assert "42" in caplog.text or "payment" in caplog.text.lower()


def test_callback_payment_failed(caplog, db_session):
    """Test that payment_failed event is handled correctly."""
    import logging
    from queue_consumer import callback

    ch = MagicMock()
    method = MagicMock()
    properties = MagicMock()

    event = {
        "event": "payment_failed",
        "order_id": 99,
        "error": "Card declined"
    }
    body = json.dumps(event).encode()

    with caplog.at_level(logging.WARNING, logger="QueueConsumer"):
        with patch("time.sleep"):
            callback(ch, method, properties, body)

    ch.basic_ack.assert_called_once()


def test_callback_offline_payment_reviewed(db_session):
    """Test that offline_payment_reviewed event is handled correctly."""
    from queue_consumer import callback

    ch = MagicMock()
    method = MagicMock()
    properties = MagicMock()

    event = {
        "event": "offline_payment_reviewed",
        "order_id": 55,
        "status": "confirmed",
        "admin_id": 1
    }
    body = json.dumps(event).encode()
    callback(ch, method, properties, body)
    ch.basic_ack.assert_called_once()


def test_callback_unknown_event():
    """Test that unknown events are handled gracefully without crashing."""
    from queue_consumer import callback

    ch = MagicMock()
    method = MagicMock()
    properties = MagicMock()

    event = {"event": "some_unknown_event", "data": "test"}
    body = json.dumps(event).encode()
    callback(ch, method, properties, body)
    ch.basic_ack.assert_called_once()


def test_callback_invalid_json():
    """Test that malformed JSON is handled without crashing (error path)."""
    from queue_consumer import callback

    ch = MagicMock()
    method = MagicMock()
    properties = MagicMock()

    body = b"this is not valid json {{{"
    # Should NOT raise an exception — error is logged
    callback(ch, method, properties, body)
    # basic_ack should NOT be called on error
    ch.basic_ack.assert_not_called()


def test_queue_service_mock_mode():
    """Test that QueueService falls back to mock mode when RabbitMQ is unavailable."""
    from queue_service import QueueService

    # Force mock mode by patching pika to be unavailable
    with patch.dict("sys.modules", {"pika": None}):
        # Import a fresh instance — since HAS_PIKA is checked at import time,
        # we test the publish_message fallback by creating instance without connection
        qs = QueueService(queue_name="test_queue")
        qs.connection = None  # Force mock mode
        qs.channel = None

        result = qs.publish_message({"event": "test_event", "order_id": 1})
        assert result is True  # Mock mode should still return True
