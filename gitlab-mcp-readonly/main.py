from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import httpx


UPSTREAM = "http://gitlab-mcp:8083"

ALLOWED_PATHS = {
    #"glab_ci_artifact",
    #"glab_ci_trace",
    #"glab_issue_list",
    #"glab_issue_view",
    #"glab_mr_diff",
    #"glab_mr_issues",
    #"glab_mr_list",
    #"glab_repo_list",
    #"glab_repo_search",
    #"glab_repo_view",
    "glab_api"
}

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


with open("/app/glab-openapi-readonly.json") as f:
    OPENAPI = json.load(f)


@app.get("/openapi.json")
async def openapi_json():
    return JSONResponse(OPENAPI)


@app.api_route(
    "/{path:path}",
    methods=["POST", "GET"]
)
async def proxy(path: str, request: Request):

    if path not in ALLOWED_PATHS:
        return JSONResponse(
            {
                "error": "Tool disabled in readonly mode"
            },
            status_code=403,
        )

    if path == "glab_api":
        try:
            data = json.loads(body.decode())
        except Exception:
            data = {}
        method = (
            data.get("flags", {})
            .get("method", "GET")
            .upper()
        )
        if method not in ("GET", "HEAD"):
            return JSONResponse(
                {
                    "error": "Only GET is allowed for glab_api"
                },
                status_code=403,
            )

    async with httpx.AsyncClient() as client:

        body = await request.body()

        response = await client.request(
            request.method,
            f"{UPSTREAM}/{path}",
            content=body,
            headers={
                k: v
                for k, v in request.headers.items()
                if k.lower() != "host"
            },
        )

    return JSONResponse(
        content=response.json(),
        status_code=response.status_code,
    )

