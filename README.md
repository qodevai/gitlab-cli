# qodev-gitlab-cli

Agent-friendly CLI for the GitLab API. Designed for both human and AI-agent workflows, with structured JSON output, consistent flags, and predictable error codes.

## Installation

```bash
pip install qodev-gitlab-cli
```

Or run directly without installing:

```bash
uvx qodev-gitlab-cli
```

## Quick Start

```bash
# Set your GitLab token
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"

# List open merge requests for a project
qodev-gitlab mrs list --project mygroup/myproject

# Get details of a specific issue
qodev-gitlab issues get 42 --project mygroup/myproject

# List pipelines, output as JSON for scripting
qodev-gitlab pipelines list --project mygroup/myproject --json

# Create a merge request from the current branch
qodev-gitlab mrs create --title "Add new feature" --project mygroup/myproject
```

## Commands

| Group | Subcommand | Description |
|---|---|---|
| **projects** | `list` | List projects (`--owned` for owned only) |
| | `get` | Get project details |
| **mrs** | `list` | List merge requests (`--state`) |
| | `get` | Get merge request details |
| | `create` | Create a merge request (`--title`, `--source`, `--target`, `--description`, `--labels`, `--squash`) |
| | `update` | Update a merge request (`--title`, `--description`, `--labels`, `--target`) |
| | `merge` | Merge a merge request (`--squash`, `--when-pipeline-succeeds`) |
| | `close` | Close a merge request |
| | `discussions` | List discussions on a merge request |
| | `changes` | Show diff for a merge request |
| | `commits` | List commits in a merge request |
| | `approvals` | Show approval status |
| | `comment` | Comment on a merge request (`--body`) |
| | `pipelines` | List pipelines for a merge request |
| **pipelines** | `list` | List pipelines (`--ref`, `--limit`) |
| | `get` | Get pipeline details |
| | `jobs` | List jobs for a pipeline |
| | `wait` | Wait for a pipeline to complete (`--timeout`, `--interval`) |
| **jobs** | `get` | Get job details |
| | `log` | Get job log output |
| | `retry` | Retry a failed job |
| **issues** | `list` | List issues (`--state`, `--labels`, `--milestone`) |
| | `get` | Get issue details |
| | `create` | Create an issue (`--title`, `--description`, `--labels`) |
| | `update` | Update an issue (`--title`, `--description`, `--labels`) |
| | `close` | Close an issue |
| | `comment` | Comment on an issue (`--body`) |
| | `notes` | List comments/notes on an issue |
| **releases** | `list` | List releases |
| | `get` | Get release details by tag |
| | `create` | Create a release (`--tag`, `--name`, `--description`, `--ref`) |
| **variables** | `list` | List CI/CD variables (values hidden) |
| | `get` | Get a CI/CD variable |
| | `set` | Set (create or update) a CI/CD variable (`--protected`, `--masked`) |

## Configuration

### Authentication

Set the `GITLAB_TOKEN` environment variable, or pass `--token` on each invocation:

```bash
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
```

### GitLab Instance

By default the CLI targets `https://gitlab.com`. Override with the `GITLAB_URL` environment variable or the `--url` flag:

```bash
export GITLAB_URL="https://gitlab.example.com"
```

### Global Options

| Flag | Description | Default |
|---|---|---|
| `--json` | Output as JSON (for scripting / agents) | `false` |
| `--project`, `-p` | Project ID or path | auto-detected from git remote |
| `--limit` | Results per page | `25` |
| `--page` | Page number | `1` |
| `--token` | GitLab token (overrides `GITLAB_TOKEN`) | |
| `--url` | GitLab URL (overrides `GITLAB_URL`) | |

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `80` | Authentication error |
| `81` | Not found |
| `82` | API error |
| `83` | Validation error |
| `84` | Configuration error |

## License

MIT -- see [LICENSE](LICENSE) for details.
