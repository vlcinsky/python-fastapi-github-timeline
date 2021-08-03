import pendulum
import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
GITHUB_REPOS_PER_PAGE = 30


def format_date(val: str):
    """Jinja2 filter formatting datetime string"""
    dt = pendulum.parse(val)
    return dt.format("DD MMM YYYY")


templates = Jinja2Templates(directory="templates")
templates.env.filters["format_date"] = format_date


def get_repos(user, page=1, per_page=GITHUB_REPOS_PER_PAGE):
    """Fetch info about GitHub user repos"""
    print(f"get_repos: user: {user} page: {page}")
    url = f"https://api.github.com/users/{user}/repos"
    params = {
        "sort": "created",
        "direction": "desc",
        "page": page,
        "per_page": per_page,
    }
    return requests.get(url, params=params).json()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/repos", response_class=HTMLResponse)
def repos(request: Request, user: str = Form(...)):
    page = 1
    per_page = GITHUB_REPOS_PER_PAGE
    repos = get_repos(user, page)
    return templates.TemplateResponse(
        "_timeline.html",
        {
            "request": request,
            "user": user,
            "repos": repos,
            "page": page + 1,
            "per_page": per_page,
        },
    )


@app.get("/more", response_class=HTMLResponse)
def more(request: Request, user: str, page: int):
    per_page = GITHUB_REPOS_PER_PAGE
    repos = get_repos(user, page, per_page)
    return templates.TemplateResponse(
        "_timeline.html",
        {
            "request": request,
            "user": user,
            "repos": repos,
            "page": page + 1,
            "per_page": per_page,
        },
    )
