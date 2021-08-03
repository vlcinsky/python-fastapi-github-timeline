import pendulum
import requests
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from yarl import URL

app = FastAPI()
GITHUB_REPOS_PER_PAGE = 30


def format_date(val: str):
    """Jinja2 filter formatting datetime string"""
    dt = pendulum.parse(val)
    return dt.format("DD MMM YYYY")


templates = Jinja2Templates(directory="templates")
templates.env.filters["format_date"] = format_date


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def repos_response(request: Request, user: str, page: int = 1):
    per_page = GITHUB_REPOS_PER_PAGE
    url = f"https://api.github.com/users/{user}/repos"
    params = {
        "sort": "created",
        "direction": "desc",
        "page": page,
        "per_page": per_page,
    }
    resp = requests.get(url, params=params)
    next_page = None
    if resp.ok:
        if resp.links:
            next_url = resp.links.get("next", {}).get("url")
            if next_url:
                next_page = URL(next_url).query.get("page")
        repos = resp.json()
        user_not_found = False
    else:
        repos = []
        user_not_found = True
    return templates.TemplateResponse(
        "_timeline.html",
        {
            "request": request,
            "user": user,
            "repos": repos,
            "next_page": next_page,
            "per_page": per_page,
            "user_not_found": user_not_found,
        },
    )


@app.post("/repos", response_class=HTMLResponse)
def repos(request: Request, user: str = Form(...)):
    return repos_response(request, user, page=1)


@app.get("/more", response_class=HTMLResponse)
def more(request: Request, user: str, page: int):
    return repos_response(request, user, page)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
