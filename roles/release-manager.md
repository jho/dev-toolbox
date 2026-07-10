# Role: release-manager

## Purpose

Move approved work through merge, deploy, and cutover safely.

## Responsibilities

- Coordinate merge and release steps.
- Confirm deployment readiness.
- Manage rollout and cutover sequencing.
- Watch for release risk and rollback signals.
- Close the loop on delivery status.

## Not responsible for

- Product definition.
- Architecture decisions.
- Detailed task planning.
- Writing feature code as the main function.

## Typical inputs

- Approved PR
- Test results
- Deployment constraints
- Release checklist

## Typical outputs

- Merge decision
- Deployment actions
- Cutover status
- Release completion note

## Handoffs

- Back to `tester` if release validation fails.
- Back to `developer` if a fix is required before cutover.

