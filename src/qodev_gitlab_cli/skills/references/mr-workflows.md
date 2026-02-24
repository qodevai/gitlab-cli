# Merge Request Workflows

## Create and Submit MR

```bash
# Create MR from current branch targeting main
qodev-gitlab mrs create --title "feat: add user auth"

# Create MR with full details
qodev-gitlab mrs create \
  --title "fix: resolve login timeout" \
  --source feature-branch \
  --target main \
  --description "Fixes #42. Increases timeout from 5s to 30s." \
  --labels "bug,priority::high"

# Create MR with squash enabled
qodev-gitlab mrs create --title "refactor: clean up utils" --squash
```

## Review MR

```bash
# Get MR overview
qodev-gitlab mrs get 42

# Check what changed
qodev-gitlab mrs changes 42

# Read discussions/review comments
qodev-gitlab mrs discussions 42

# Check approval status
qodev-gitlab mrs approvals 42

# Check associated pipelines
qodev-gitlab mrs pipelines 42
```

## Update and Respond

```bash
# Update MR title or description
qodev-gitlab mrs update 42 --title "feat: improved title"
qodev-gitlab mrs update 42 --description "Updated description with more context"

# Add labels
qodev-gitlab mrs update 42 --labels "reviewed,ready-to-merge"

# Leave a comment
qodev-gitlab mrs comment 42 --body "Addressed all review comments"
```

## Merge

```bash
# Merge immediately
qodev-gitlab mrs merge 42

# Squash and merge
qodev-gitlab mrs merge 42 --squash

# Merge when pipeline succeeds
qodev-gitlab mrs merge 42 --when-pipeline-succeeds
```

## Full Lifecycle Example

```bash
# 1. Create MR
qodev-gitlab mrs create --title "feat: add caching layer" --labels "enhancement"

# 2. Check pipeline status
qodev-gitlab mrs pipelines 1

# 3. Review feedback
qodev-gitlab mrs discussions 1

# 4. Address feedback and comment
qodev-gitlab mrs comment 1 --body "Fixed the race condition in cache invalidation"

# 5. Check approvals
qodev-gitlab mrs approvals 1

# 6. Merge when pipeline passes
qodev-gitlab mrs merge 1 --when-pipeline-succeeds
```

## JSON Workflows (for Automation)

```bash
# Get MR state for conditional logic
STATE=$(qodev-gitlab --json mrs get 42 | jq -r '.state')

# List all open MRs as JSON
qodev-gitlab --json mrs list --state opened

# Check if MR has conflicts
qodev-gitlab --json mrs get 42 | jq '.has_conflicts'
```
