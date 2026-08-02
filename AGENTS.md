# AGENTS.md — AI Agent Project Instructions

## Project Overview

This repository is a Docker Compose environment that provides an Open WebUI service on an internal network.
It integrates AI models on AWS Bedrock via LiteLLM and connects GitHub / GitLab MCP servers.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Browser (http://<server>:3000)                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              open-webui (v0.11.0)                 │  │
│  └──────────────────────┬────────────────────────────┘  │
│                         │  OpenAI-compatible API        │
│  ┌──────────────────────▼────────────────────────────┐  │
│  │              litellm (v1.94.1)                    │  │
│  │  Bedrock model wrapper                            │  │
│  └──┬──────────┬──────────┬──────────┬──────────────┘  │
│     │          │          │          │                 │
│  Bedrock   Bedrock   Bedrock   Bedrock                 │
│  (Tokyo Region)                                         │
│  ┌──────────┬──────────┬──────────┬──────────┐       │
│  │Claude    │Claude    │Claude    │Amazon     │       │
│  │Sonnet 4.6│Opus 4.8 │Haiku 4.5 │Nova 2 Lite│       │
│  └──────────┴──────────┴──────────┴──────────┘       │
│                                                       │
│  ┌──────────────┐  ┌──────────────────────────┐      │
│  │ github-mcp   │  │ gitlab-mcp / readonly    │      │
│  │ (read-only)  │  │ (glab-cli / FastAPI)     │      │
│  └──────────────┘  └──────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

## Key Files

| File | Description |
| -------- | ---- |
| `docker-compose.yml` | Main Docker Compose configuration |
| `litellm-config.yaml` | Bedrock model definitions (LiteLLM) |
| `filter-openapi.py` | GitLab OpenAPI endpoint filter |
| `gitlab-mcp-readonly/main.py` | GitLab read-only proxy (FastAPI) |
| `gitlab-mcp/glab-cli/config.yml` | GitLab connection configuration |

## Constraints

- **No Secret Leakage**: Do not include `.env` contents, the Client Secret in `github-openwebui-mcp-app.txt`,
  or the GitLab token in `config.yml` in code or commit messages.
- **GitLab Read-Only**: `gitlab-mcp-readonly` only allows GET/HEAD. Write operations return 403.
- **GitHub MCP Read-Only**: Launched with the `--read-only` flag.
- **Internal Network**: Services are configured for internal IP (e.g., `10.11.196.84`).

## Verification Steps After Changes

1. Run `docker compose config` to verify configuration integrity
2. If `litellm-config.yaml` changed, run `docker compose restart litellm`
3. If `gitlab-mcp-readonly` changed, run `docker compose up -d --build gitlab-mcp-readonly`
4. If `filter-openapi.py` changed, re-run it to regenerate `glab-openapi-readonly.json`

## Development Commands

```bash
# Start services
docker compose up -d

# Check logs
docker compose logs -f open-webui
docker compose logs -f litellm

# Restart
docker compose restart litellm

# Stop
docker compose down

# Rebuild read-only proxy
docker compose up -d --build gitlab-mcp-readonly
```
