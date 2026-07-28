from backend.app.services.extract import analyze_action_items, extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_recognizes_additional_prefixes_and_markers():
    text = """
    1. TASK: update the changelog
    FIXME: broken link on homepage
    Follow up: confirm with legal
    - [ ] write the release notes
    - [x] already merged the branch
    * please review the design doc
    Need to restart the worker
    """.strip()
    items = extract_action_items(text)
    assert "TASK: update the changelog" in items
    assert "FIXME: broken link on homepage" in items
    assert "Follow up: confirm with legal" in items
    assert "write the release notes" in items
    assert "already merged the branch" not in items
    assert "please review the design doc" in items
    assert "Need to restart the worker" in items


def test_analyze_action_items_extracts_assignee_due_date_and_priority():
    text = """
    - TODO: @alice send the report by Friday
    - ACTION: fix the outage now!! this is urgent
    - Ship it!
    """.strip()
    items = analyze_action_items(text)
    by_text = {item.text: item for item in items}

    report_item = by_text["TODO: @alice send the report by Friday"]
    assert report_item.assignee == "alice"
    assert report_item.due_date == "Friday"

    urgent_item = by_text["ACTION: fix the outage now!! this is urgent"]
    assert urgent_item.priority == "high"

    ship_item = by_text["Ship it!"]
    assert ship_item.priority == "normal"
    assert ship_item.assignee is None
    assert ship_item.due_date is None


def test_bare_mention_is_not_an_action_item():
    text = """
    Thanks @alice for the update
    Great work team @bob and @carol
    """.strip()
    items = extract_action_items(text)
    assert items == []


