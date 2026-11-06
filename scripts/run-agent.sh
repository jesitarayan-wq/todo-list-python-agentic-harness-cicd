#!/usr/bin/env bash
# run-agent.sh: launch a subagent container with only the permissions its
# governance policy allows. Pass the role name as the first argument.
#
# Network mode (environment variable AGENT_NETWORK):
#   open        (default) Docker's default network; the app ports are published.
#   restricted  the internal network (no route to the internet); all HTTPS goes through the
#               allow-list proxy that ./scripts/start-egress-proxy.sh starts.
set -euo pipefail
export MSYS_NO_PATHCONV=1

ROLE="${1:?Usage: run-agent.sh <role-name> [command]}"
shift

IMAGE="${AGENT_IMAGE:-todo-agent-m4}"
NETWORK_MODE="${AGENT_NETWORK:-open}"
WORKSPACE_MODE="ro"
MOUNT_MEMORY=0

case "$ROLE" in
  implementer|orchestrator)
    WORKSPACE_MODE="rw"
    MOUNT_MEMORY=1
    ;;
  security-reviewer|planner|test-coverage-analyzer|tester|project-manager|dependency-auditor)
    WORKSPACE_MODE="ro"
    MOUNT_MEMORY=0
    ;;
  *)
    echo "Unknown role: $ROLE" >&2
    echo "This role has no policy entry, so it cannot be launched." >&2
    exit 1
    ;;
esac

ARGS=( run --rm -it )

# Network boundary.
case "$NETWORK_MODE" in
  open)
    # Expose local application ports.
    ARGS+=( -p 8501:8501 )
    ARGS+=( -p 8502:8502 )
    ;;
  restricted)
    if ! docker ps --filter "name=^egress-proxy$" --filter "status=running" -q | grep -q .; then
      echo "Restricted network mode needs the egress proxy. Start it first: ./scripts/start-egress-proxy.sh" >&2
      exit 1
    fi
    ARGS+=( --network agent-internal )
    ARGS+=( -e "HTTPS_PROXY=http://egress-proxy:3128" -e "https_proxy=http://egress-proxy:3128" )
    ARGS+=( -e "HTTP_PROXY=http://egress-proxy:3128" -e "http_proxy=http://egress-proxy:3128" )
    ARGS+=( -e "NO_PROXY=localhost,127.0.0.1" -e "no_proxy=localhost,127.0.0.1" )
    ;;
  *)
    echo "Unknown AGENT_NETWORK: $NETWORK_MODE (use open or restricted)" >&2
    exit 1
    ;;
esac

# Slack configuration.
# These may be set in your shell before running this script.
ARGS+=( -e "SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN:-xoxb-your-token}" )
ARGS+=( -e "SLACK_TEAM_ID=${SLACK_TEAM_ID:-T0123456}" )

# Workspace and logs.
mkdir -p logs
ARGS+=( -v "$(pwd):/workspace:${WORKSPACE_MODE}" )
ARGS+=( -v "$(pwd)/logs:/logs:rw" )

# Audit log locations.
ARGS+=( -e "STORAGE_AUDIT_LOG=/logs/storage-audit-log.jsonl" )
ARGS+=( -e "RETRIEVAL_AUDIT_LOG=/logs/retrieval-audit-log.jsonl" )

# Mount persistent memory only for roles allowed by policy.
if [ "$MOUNT_MEMORY" -eq 1 ]; then
  ARGS+=( -v "$(pwd)/.memory:/memory:rw" )
fi

ARGS+=( -e OPENROUTER_API_KEY )
ARGS+=( -v claude-auth:/claude-auth )
ARGS+=( -v "$(pwd)/docker-entrypoint.sh:/usr/local/bin/docker-entrypoint.sh:ro" )
# Role identity.
ARGS+=( -e "AGENT_ROLE=${ROLE}" )

# Image and optional command.
ARGS+=( "$IMAGE" "$@" )

MEMORY_STATE=$([ "$MOUNT_MEMORY" -eq 1 ] && echo mounted || echo omitted)
echo "Launching '$ROLE': image=${IMAGE}, workspace=${WORKSPACE_MODE}, memory=${MEMORY_STATE}, network=${NETWORK_MODE}"
exec docker "${ARGS[@]}"
