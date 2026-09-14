**Unreleased**

* Prevent action-scoped AWS credentials from being retained in action results.
* Keep action-scoped AWS credentials isolated from the asset credential state.
* Migrate scheduled polling checkpoints to UTC with a conservative overlap.
* Retry failed GuardDuty findings without advancing the checkpoint past them.
* Bound GuardDuty pagination pages and retained item counts before accumulation.
