from unittest import mock
from os import environ

with mock.patch.dict(
    environ,
    {
        "OCD_DTL_MISP_HOST": "localhost",
        "OCD_DTL_MISP_API_KEY": "mock_key",
        "OCD_DTL_MISP_USE_SSL": "false",
        "OCD_DTL_MISP_WORKER": "4",
    },
):
    from src.misp import Misp


@mock.patch("pymisp.PyMISP")
def test_add_empty_events(mocked_misp_backend):
    """Test that no events are added when an empty list is provided"""
    misp = Misp()
    events = []
    misp.add_events(events)
    assert not mocked_misp_backend.return_value.add_event.called
    assert not mocked_misp_backend.return_value.event_exists.called


@mock.patch("pymisp.PyMISP")
def test_add_single_event(mocked_misp_backend):
    """Test adding a single event that doesn't exist"""
    mocked_misp_backend.return_value.event_exists.return_value = False
    misp = Misp()
    event = {"Event": {"uuid": "123", "info": "hash1"}}
    events = [event]

    result = misp.add_events(events)

    assert mocked_misp_backend.return_value.event_exists.called
    assert mocked_misp_backend.return_value.add_event.called
    event_added = mocked_misp_backend.return_value.add_event.call_args[0][0]
    assert event_added.uuid == "123"
    assert event_added.info == "hash1"
    assert len(result) == 1


@mock.patch("pymisp.PyMISP")
def test_add_multiple_events(mocked_misp_backend):
    """Test adding multiple unique events"""
    mocked_misp_backend.return_value.event_exists.return_value = False
    misp = Misp()
    event1 = {"Event": {"uuid": "123", "info": "hash1"}}
    event2 = {"Event": {"uuid": "456", "info": "hash2"}}
    events = [event1, event2]

    result = misp.add_events(events)

    assert mocked_misp_backend.return_value.event_exists.call_count == 2
    assert mocked_misp_backend.return_value.add_event.call_count == 2
    added_uuids = {
        call[0][0].uuid
        for call in mocked_misp_backend.return_value.add_event.call_args_list
    }
    assert added_uuids == {"123", "456"}
    assert len(result) == 2


@mock.patch("pymisp.PyMISP")
def test_add_duplicate_events(mocked_misp_backend):
    """Test that duplicate events are not added multiple times"""
    mocked_misp_backend.return_value.event_exists.side_effect = [False, True]
    misp = Misp()
    event = {"Event": {"uuid": "123", "info": "hash1"}}
    event_duplicate = {"Event": {"uuid": "123", "info": "hash1"}}
    events = [event, event_duplicate]

    result = misp.add_events(events)

    assert mocked_misp_backend.return_value.event_exists.call_count == 2
    assert mocked_misp_backend.return_value.add_event.call_count == 1
    event_added = mocked_misp_backend.return_value.add_event.call_args[0][0]
    assert event_added.uuid == "123"
    assert len(result) == 2  # Results include None for skipped event


@mock.patch("pymisp.PyMISP")
def test_add_event_error_handling(mocked_misp_backend):
    """Test that errors during event addition are properly handled"""
    mocked_misp_backend.return_value.event_exists.return_value = False
    mocked_misp_backend.return_value.add_event.side_effect = Exception("MISP Error")
    misp = Misp()
    event = {"Event": {"uuid": "123", "info": "hash1"}}

    result = misp.add_events([event])

    assert mocked_misp_backend.return_value.event_exists.called
    assert mocked_misp_backend.return_value.add_event.called
    assert result == [None]  # Error should be caught and None returned


@mock.patch("pymisp.PyMISP")
def test_close(mocked_misp_backend):
    """Test proper shutdown of MISP connection"""
    misp = Misp()
    misp.close()

    assert misp.thread_pool is None

    # Verify add_events handles closed state
    events = [{"Event": {"uuid": "123", "info": "hash1"}}]
    result = misp.add_events(events)
    assert result is None
