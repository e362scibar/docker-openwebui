import json

keep_paths = {
#    "/glab_repo_list",
#    "/glab_repo_view",
#    "/glab_repo_search",
#
#    "/glab_issue_list",
#    "/glab_issue_view",
#
#    "/glab_mr_list",
#    "/glab_mr_diff",
#    "/glab_mr_issues",
#
#    "/glab_ci_trace",
#    "/glab_ci_artifact",

    "/glab_api"
}

with open("glab-openapi.json") as f:
    spec = json.load(f)

spec["paths"] = {
    k: v for k, v in spec["paths"].items()
    if k in keep_paths
}

with open("glab-openapi-readonly.json", "w") as f:
    json.dump(spec, f, indent=2)
