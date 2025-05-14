from unittest.mock import patch

import pytest  # type: ignore
from psycopg2 import OperationalError

from db_utils.config.config import Config
from db_utils.connect import connect

config = Config()


def test_connect_to_db():
    conn = connect(config)
    assert conn is not None
    conn.close()


def test_successful_connection_first_try():
    with patch("psycopg2.connect", return_value="mock_conn") as mock_connect:
        conn = connect(config)
        assert conn == "mock_conn"
        assert mock_connect.call_count == 1


def test_successful_connection_after_retries():
    # 1. a 2. pokus selže, 3. projde
    side_effects = [OperationalError("fail 1"), OperationalError("fail 2"), "mock_conn"]
    with (
        patch("psycopg2.connect", side_effect=side_effects) as mock_connect,
        patch("time.sleep") as mock_sleep,
    ):
        conn = connect(config)
        assert conn == "mock_conn"
        assert mock_connect.call_count == 3
        assert mock_sleep.call_count == 2


def test_connection_fails_all_attempts():
    with (
        patch("psycopg2.connect", side_effect=OperationalError("fail")),
        patch("time.sleep") as mock_sleep,
    ):
        with pytest.raises(OperationalError):
            connect(config)
        assert mock_sleep.call_count == config.retries - 1


def test_unexpected_exception_propagates():
    with patch("psycopg2.connect", side_effect=TypeError("unexpected")):
        with pytest.raises(TypeError):
            connect(config)


def test_retry_delay_calculation():
    # Zkontrolujeme, že se delay správně násobí backoffem
    with (
        patch(
            "psycopg2.connect",
            side_effect=[OperationalError(), OperationalError(), "ok"],
        ),
        patch("time.sleep") as mock_sleep,
    ):
        connect(config)
        expected_delays = [1, 2]  # delay * backoff^0, delay * backoff^1
        actual_delays = [call.args[0] for call in mock_sleep.call_args_list]
        assert actual_delays == expected_delays
