import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from awsguardduty_security import (
    record_pagination_token,
    severity_criterion,
    severity_label,
    unresolved_finding_ids,
    utc_milliseconds,
)


def test_context_menu_values_escape_javascript() -> None:
    template = Path("awsguardduty_run_query.html").read_text()
    values = re.findall(r"context_menu\(.*?'value'\s*:\s*'\s*({{.*?}})", template)

    assert values
    assert all("|escapejs" in value for value in values)


@pytest.mark.parametrize(
    ("numeric_value", "expected"),
    [(1.0, "Low"), (3.9, "Low"), (4.0, "Medium"), (8.9, "High"), (9.0, "Critical"), (10.0, "Critical")],
)
def test_severity_ranges_cover_documented_values(numeric_value, expected) -> None:
    assert severity_label(numeric_value) == expected


def test_severity_filter_uses_range() -> None:
    assert severity_criterion("High") == {"Gte": 7.0, "Lt": 9.0}
    assert severity_criterion("Critical") == {"Gte": 9.0, "Lt": 10.1}


def test_utc_checkpoint_is_independent_of_local_timezone() -> None:
    assert utc_milliseconds("1970-01-01T00:00:01.000Z") == 1000


def test_repeated_pagination_token_is_rejected() -> None:
    seen_tokens = set()
    record_pagination_token("token", seen_tokens)
    with pytest.raises(ValueError, match="did not advance"):
        record_pagination_token("token", seen_tokens)


def test_unresolved_finding_ids_are_reported() -> None:
    assert unresolved_finding_ids(["finding-1", "finding-2"], [{"Id": "finding-1"}]) == ["finding-2"]
