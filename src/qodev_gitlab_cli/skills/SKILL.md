# qodev-gitlab CLI

Agent-friendly CLI for the GitLab API. Designed for AI coding agents with structured JSON output and predictable exit codes.

## Setup

```bash
pip install qodev-gitlab-cli
export GITLAB_TOKEN="glpat-..."

# Install skill files into the current workspace
qodev-gitlab install --skills
```

The CLI auto-detects the current GitLab project from the git remote. Override with `--project GROUP/NAME` or `-p GROUP/NAME`.

## Global Options

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON (default: rich Markdown) |
| `--project`, `-p` | Project ID or path (default: auto-detected) |
| `--limit` | Results per page (default: 25) |
| `--page` | Page number (default: 1) |
| `--token` | GitLab token (overrides GITLAB_TOKEN) |
| `--url` | GitLab URL (overrides GITLAB_URL) |

## Command Reference

### projects

| Command | Description |
|---------|-------------|
| `projects list [--owned]` | List projects |
| `projects get [ID]` | Get project details (default: current) |

### mrs (Merge Requests)

| Command | Description |
|---------|-------------|
| `mrs list [--state STATE]` | List MRs (default: opened) |
| `mrs get IID` | Get MR details |
| `mrs create --title TITLE [--source BRANCH] [--target BRANCH] [--description TEXT] [--labels L] [--squash]` | Create MR |
| `mrs update IID [--title T] [--description D] [--labels L] [--target B]` | Update MR |
| `mrs merge IID [--squash] [--when-pipeline-succeeds]` | Merge MR |
| `mrs close IID` | Close MR |
| `mrs discussions IID` | List MR discussions |
| `mrs changes IID` | Show MR diff |
| `mrs commits IID` | List MR commits |
| `mrs approvals IID` | Show approval status |
| `mrs comment IID --body TEXT` | Comment on MR |
| `mrs pipelines IID` | List MR pipelines |

### pipelines

| Command | Description |
|---------|-------------|
| `pipelines list [--ref BRANCH] [--limit N]` | List pipelines |
| `pipelines get ID` | Get pipeline details |
| `pipelines jobs ID` | List pipeline jobs |
| `pipelines wait ID [--timeout S] [--interval S]` | Wait for pipeline to complete |

### jobs

| Command | Description |
|---------|-------------|
| `jobs get ID` | Get job details |
| `jobs log ID` | Get job log output |
| `jobs retry ID` | Retry a failed job |

### issues

| Command | Description |
|---------|-------------|
| `issues list [--state STATE] [--labels L] [--milestone M]` | List issues |
| `issues get IID` | Get issue details |
| `issues create --title TITLE [--description D] [--labels L]` | Create issue |
| `issues update IID [--title T] [--description D] [--labels L]` | Update issue |
| `issues close IID` | Close issue |
| `issues comment IID --body TEXT` | Comment on issue |
| `issues notes IID` | List issue comments |

### releases

| Command | Description |
|---------|-------------|
| `releases list` | List releases |
| `releases get TAG` | Get release details |
| `releases create --tag TAG [--name N] [--description D] [--ref REF]` | Create release |

### variables

| Command | Description |
|---------|-------------|
| `variables list` | List CI/CD variables (values hidden) |
| `variables get KEY` | Get a CI/CD variable |
| `variables set KEY VALUE [--protected] [--masked]` | Set a CI/CD variable |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 80 | Authentication error (bad/missing token) |
| 81 | Not found |
| 82 | API error |
| 83 | Validation error |
| 84 | Configuration error |

## JSON Output

All commands support `--json` for structured output. Lists return:

```json
{"items": [...], "total": 10, "page": 1, "limit": 25}
```

Single resources return the raw API object. Errors return:

```json
{"error": "message", "code": "error_code"}
```

## Common Patterns

```bash
# Get current project info
qodev-gitlab projects get

# Create MR from current branch
qodev-gitlab mrs create --title "feat: add feature"

# Check pipeline status as JSON
qodev-gitlab --json pipelines list --limit 5

# Wait for pipeline then check result
qodev-gitlab pipelines wait 12345 --timeout 600

# Review MR discussions
qodev-gitlab mrs discussions 42
```

## References

For detailed workflow patterns, see:
- [MR Workflows](references/mr-workflows.md) — Create, review, and merge MRs
- [Pipeline Monitoring](references/pipeline-monitoring.md) — CI/CD monitoring patterns
