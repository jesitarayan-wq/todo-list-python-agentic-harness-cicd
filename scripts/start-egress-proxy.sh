#!/usr/bin/env bash
# start-egress-proxy.sh: start (or stop) the allow-list egress proxy for restricted network mode.
# Usage: ./scripts/start-egress-proxy.sh [enforce|learn|stop]
#   enforce  (default) only hosts in config/egress-allow-list.txt are reachable.
#   learn    every HTTPS host is allowed and logged, to discover what an agent needs.
set -euo pipefail
export MSYS_NO_PATHCONV=1

ACTION="${1:-enforce}"
IMAGE="${AGENT_IMAGE:-todo-agent-m4}"

if [ "$ACTION" = "stop" ]; then
  docker rm -f egress-proxy >/dev/null 2>&1 || true
  echo "egress-proxy stopped"
  exit 0
fi

case "$ACTION" in
  enforce|learn) ;;
  *) echo "Usage: $0 [enforce|learn|stop]" >&2; exit 1 ;;
esac

# The internal network has no route to the internet; only the proxy is attached to both networks.
docker network inspect agent-internal >/dev/null 2>&1 || docker network create --internal agent-internal >/dev/null
docker rm -f egress-proxy >/dev/null 2>&1 || true
mkdir -p logs
docker run -d --name egress-proxy --network bridge \
  -e "EGRESS_MODE=${ACTION}" \
  -v "$(pwd):/workspace:ro" -v "$(pwd)/logs:/logs:rw" \
  --entrypoint python3 "$IMAGE" /workspace/scripts/egress_proxy.py >/dev/null
docker network connect agent-internal egress-proxy
echo "egress-proxy running in ${ACTION} mode; log: logs/egress-proxy-log.jsonl"
