from fastapi import FastAPI

from insights.features.gaps import router as gaps
from insights.settings import settings
from insights.version import __version__

app = FastAPI(
    title="WattMaven Insights",
    description="A simple analytics microservice for PV systems.",
    version=__version__,
    servers=[
        server
        for server in [
            {"url": "http://localhost:8000", "description": "Local"}
            # If the python environment is not production, add the local server.
            if settings.python_env != "production"
            else None,
            {
                "url": f"https://{settings.insights_domain}",
                "description": "Production",
            },
        ]
        if server is not None
    ],
    license_info={
        "name": "MIT",
        "identifier": "MIT",
        "url": "https://opensource.org/licenses/apache-2.0",
    },
    contact={
        "name": "WattMaven",
        "url": "https://wattmaven.com",
        "email": "support@wattmaven.com",
    },
)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(gaps.router)
