"""Security-focused helpers for the AWS GuardDuty connector."""

from datetime import datetime, timezone


SEVERITY_RANGES = {
    "Low": (1.0, 4.0),
    "Medium": (4.0, 7.0),
    "High": (7.0, 9.0),
    "Critical": (9.0, 10.1),
}


def severity_label(value):
    """Map the full documented numeric GuardDuty severity range to a label."""
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None
    for label, (minimum, maximum) in SEVERITY_RANGES.items():
        if minimum <= numeric_value < maximum:
            return label
    return None


def severity_criterion(label):
    """Build GuardDuty range criteria for a user-facing severity label."""
    bounds = SEVERITY_RANGES.get(label)
    if not bounds:
        return None
    minimum, maximum = bounds
    return {"Gte": minimum, "Lt": maximum}


def utc_milliseconds(value):
    """Convert a GuardDuty UTC timestamp to epoch milliseconds without local skew."""
    parsed = datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    return int(parsed.timestamp() * 1000)


def record_pagination_token(next_token, seen_tokens):
    """Record an advancing pagination token and reject repeated tokens."""
    if not next_token:
        return
    if next_token in seen_tokens:
        raise ValueError("The upstream pagination token did not advance")
    seen_tokens.add(next_token)


def unresolved_finding_ids(requested_ids, findings):
    """Return requested finding IDs omitted from a GetFindings response."""
    returned_ids = {finding.get("Id") for finding in findings if finding.get("Id")}
    return sorted(set(requested_ids) - returned_ids)
