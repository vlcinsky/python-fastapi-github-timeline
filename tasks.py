from invoke import task


@task
def app_run(c):
    """Run web app in development mode"""
    c.run(
        "uvicorn app:app --reload --port=8000",
        pty=True,
    )
