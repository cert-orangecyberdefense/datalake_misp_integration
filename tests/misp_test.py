from unittest import mock
from src.misp import Misp


@mock.patch("pymisp.ExpandedPyMISP")
def test_add_empty_events(mocked_misp_backend):
    misp = Misp()
    events = []

    misp.add_events(events)

    assert not mocked_misp_backend.return_value.add_event.called  # No event added


@mock.patch("pymisp.ExpandedPyMISP")
def test_add_single_event(mocked_misp_backend):
    mocked_misp_backend.return_value.event_exists.return_value = False

    misp = Misp()
    event = {'Event': {'uuid': '123', 'info': 'hash1'}}
    events = [event]

    misp.add_events(events)

    assert mocked_misp_backend.return_value.event_exists.called
    assert mocked_misp_backend.return_value.add_event.called
    event_added = mocked_misp_backend.return_value.add_event.call_args[0][0]
    assert event_added.uuid == '123'


@mock.patch("pymisp.ExpandedPyMISP")
def test_add_multiple_event(mocked_misp_backend):
    mocked_misp_backend.return_value.event_exists.return_value = False

    misp = Misp()
    event1 = {'Event': {'uuid': '123', 'info': 'hash1'}}
    event2 = {'Event': {'uuid': '456', 'info': 'hash2'}}
    events = [event1, event2]

    misp.add_events(events)

    # 2 events checked then added
    assert mocked_misp_backend.return_value.event_exists.call_count == 2
    assert mocked_misp_backend.return_value.add_event.call_count == 2
    # But the insertion order is not guaranteed
    event1_added = mocked_misp_backend.return_value.add_event.call_args_list[0][0][0]
    event2_added = mocked_misp_backend.return_value.add_event.call_args_list[1][0][0]
    assert {event1_added.uuid, event2_added.uuid} == {'123', '456'}


@mock.patch("pymisp.ExpandedPyMISP")
def test_add_duplicate_events(mocked_misp_backend):
    mocked_misp_backend.return_value.event_exists.side_effect = [False, True]
    misp = Misp()
    event = {'Event': {'uuid': '123', 'info': 'hash1'}}
    event_duplicate = {'Event': {'uuid': '123', 'info': 'hash1'}}
    events = [event, event_duplicate]

    misp.add_events(events)

    assert mocked_misp_backend.return_value.event_exists.call_count == 2  # 2 events checked
    assert mocked_misp_backend.return_value.add_event.call_count == 1  # Only 1 event added
    event_added = mocked_misp_backend.return_value.add_event.call_args[0][0]
    assert event_added.uuid == '123'
