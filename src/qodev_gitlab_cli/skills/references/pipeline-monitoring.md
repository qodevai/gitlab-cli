# Pipeline Monitoring

## Check Pipeline Status

```bash
# List recent pipelines
qodev-gitlab pipelines list

# List pipelines for a specific branch
qodev-gitlab pipelines list --ref main --limit 5

# Get details for a specific pipeline
qodev-gitlab pipelines get 12345
```

## Inspect Pipeline Jobs

```bash
# List all jobs in a pipeline
qodev-gitlab pipelines jobs 12345

# Get details for a specific job
qodev-gitlab jobs get 67890

# Read job logs (useful for debugging failures)
qodev-gitlab jobs log 67890
```

## Wait for Pipeline Completion

```bash
# Wait with default timeout (1 hour)
qodev-gitlab pipelines wait 12345

# Wait with custom timeout and check interval
qodev-gitlab pipelines wait 12345 --timeout 600 --interval 30
```

## Handle Failures

```bash
# 1. Check which jobs failed
qodev-gitlab --json pipelines jobs 12345 | jq '.items[] | select(.status == "failed")'

# 2. Read the failed job's log
qodev-gitlab jobs log 67890

# 3. Retry a failed job
qodev-gitlab jobs retry 67890
```

## MR Pipeline Monitoring

```bash
# List pipelines associated with an MR
qodev-gitlab mrs pipelines 42

# Combine with wait: get latest pipeline ID then wait
PIPELINE_ID=$(qodev-gitlab --json mrs pipelines 42 | jq '.items[0].id')
qodev-gitlab pipelines wait "$PIPELINE_ID"
```

## JSON Automation Patterns

```bash
# Get pipeline status for scripting
STATUS=$(qodev-gitlab --json pipelines get 12345 | jq -r '.status')

# Count failed jobs
qodev-gitlab --json pipelines jobs 12345 | jq '[.items[] | select(.status == "failed")] | length'

# Get all job names and statuses
qodev-gitlab --json pipelines jobs 12345 | jq '.items[] | {name, status}'
```
