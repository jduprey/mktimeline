import os
import tempfile

from mktimeline.events.event import Event


def test_read_event():
    ev = Event(
        "./test-data/test-events/events/1876--_west_publishing_company/1876--_west_publishing_company.md"
    )
    print(ev.event_data)
    assert ev.event_data["text"]["headline"] == "West Publishing Company"
    assert (
        "The nation’s most innovative and most successful"
        in ev.event_data["text"]["text"]
    )
    assert "media" in ev.event_data, "Event should have media"


def test_write_event():
    # read in an event, orig_ev
    orig_ev = Event(
        "./test-data/test-events/events/1876--_west_publishing_company/1876--_west_publishing_company.md"
    )

    # now write to a new location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as temp_file:
        temp_file_path = temp_file.name
        print(f"temp_file_path: {temp_file_path}")
    orig_ev.mdfile = temp_file_path
    orig_ev.write_markdown()

    # read in the new event, new_ev and verify its the same as 
    new_ev = Event(temp_file_path)
    assert orig_ev.event_data == new_ev.event_data
    assert orig_ev.mdfile == new_ev.mdfile

    os.remove(temp_file_path)
