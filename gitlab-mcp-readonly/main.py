from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import httpx


UPSTREAM = "http://gitlab-mcp:8083"

ALLOWED_PATHS = {
    "glab_api",
    "glab_repo_view",
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
        body = await request.body()

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
    else:
        body = await request.body()

    async with httpx.AsyncClient() as client:

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

