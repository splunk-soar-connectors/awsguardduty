**Unreleased**

- Escaped dynamic JavaScript values in the run query widget.
- Converted polling checkpoints as UTC to prevent timezone skew.
- Mapped the complete GuardDuty severity range, including Critical findings.
- Advanced polling checkpoints only after containers and artifacts persist successfully.
- Bounded pagination and rejected repeated upstream page tokens.
- Reported failed container persistence and retried the affected finding on the next poll.
- Failed finding actions when any requested finding ID cannot be resolved.
