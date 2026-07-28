import re
from dataclasses import dataclass

ACTION_PREFIXES = ("todo:", "action:", "task:", "fixme:", "follow up:", "followup:")
IMPERATIVE_STARTERS = ("please ", "need to ", "needs to ", "must ", "should ", "let's ", "make sure ")
PRIORITY_KEYWORDS = ("urgent", "asap", "critical", "immediately", "high priority")

BULLET_PATTERN = re.compile(r"^[-*•]\s+")
NUMBERED_PATTERN = re.compile(r"^\d+[.)]\s+")
CHECKBOX_PATTERN = re.compile(r"^\[([ xX])\]\s*")
MENTION_PATTERN = re.compile(r"@(\w+)")
DUE_DATE_PATTERN = re.compile(r"\b(?:by|due(?:\s+by)?)\s+(.+?)[.!]*$", re.IGNORECASE)


@dataclass
class ActionItem:
    text: str
    priority: str = "normal"
    assignee: str | None = None
    due_date: str | None = None


def _strip_list_marker(line: str) -> str:
    line = BULLET_PATTERN.sub("", line)
    line = NUMBERED_PATTERN.sub("", line)
    return line


def _has_action_prefix(text: str) -> bool:
    return text.lower().startswith(ACTION_PREFIXES)


def _has_imperative_start(text: str) -> bool:
    return text.lower().startswith(IMPERATIVE_STARTERS)


def _priority(text: str) -> str:
    normalized = text.lower()
    if text.count("!") >= 2 or any(keyword in normalized for keyword in PRIORITY_KEYWORDS):
        return "high"
    return "normal"


def _assignee(text: str) -> str | None:
    match = MENTION_PATTERN.search(text)
    return match.group(1) if match else None


def _due_date(text: str) -> str | None:
    match = DUE_DATE_PATTERN.search(text)
    return match.group(1).strip() if match else None


def analyze_action_items(text: str) -> list[ActionItem]:
    """Scan free-form text for actionable lines and their metadata.

    Recognizes explicit markers (TODO:/ACTION:/TASK:/FIXME:/FOLLOW UP:),
    markdown checkboxes (open checkboxes are actionable, checked ones are
    treated as already done and skipped), exclamations, and imperative
    sentences (e.g. "Please review the PR"). A bare @mention is not on its
    own enough to flag a line - it only enriches an already-actionable
    line's `assignee`, since a mention alone (e.g. "Thanks @alice for
    the update") is not necessarily a task.
    """
    results: list[ActionItem] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        line = _strip_list_marker(line)
        checkbox_match = CHECKBOX_PATTERN.match(line)
        if checkbox_match:
            if checkbox_match.group(1).lower() == "x":
                continue
            content = CHECKBOX_PATTERN.sub("", line).strip()
        elif _has_action_prefix(line) or line.endswith("!") or _has_imperative_start(line):
            content = line
        else:
            continue

        if not content:
            continue

        results.append(
            ActionItem(
                text=content,
                priority=_priority(content),
                assignee=_assignee(content),
                due_date=_due_date(content),
            )
        )
    return results


def extract_action_items(text: str) -> list[str]:
    return [item.text for item in analyze_action_items(text)]
