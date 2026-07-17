# Copyright (c) 2026 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import sys
from pathlib import Path


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


def test_severity_ranges_cover_documented_values() -> None:
    expected_values = [(1.0, "Low"), (3.9, "Low"), (4.0, "Medium"), (8.9, "High"), (9.0, "Critical"), (10.0, "Critical")]
    for numeric_value, expected in expected_values:
        assert severity_label(numeric_value) == expected


def test_severity_filter_uses_range() -> None:
    assert severity_criterion("High") == {"Gte": 7.0, "Lt": 9.0}
    assert severity_criterion("Critical") == {"Gte": 9.0, "Lt": 10.1}


def test_utc_checkpoint_is_independent_of_local_timezone() -> None:
    assert utc_milliseconds("1970-01-01T00:00:01.000Z") == 1000


def test_repeated_pagination_token_is_rejected() -> None:
    seen_tokens = set()
    record_pagination_token("token", seen_tokens)
    try:
        record_pagination_token("token", seen_tokens)
    except ValueError as exc:
        assert "did not advance" in str(exc)
    else:
        raise AssertionError("Repeated pagination token was accepted")


def test_unresolved_finding_ids_are_reported() -> None:
    assert unresolved_finding_ids(["finding-1", "finding-2"], [{"Id": "finding-1"}]) == ["finding-2"]
