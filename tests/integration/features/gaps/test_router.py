import json

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from insights.features.gaps.router import router

app = FastAPI()
app.include_router(router)


@pytest.mark.integration
@pytest.mark.anyio
async def test_simple_identity_missing_data(testdata_golden_dir):
    with open(
        testdata_golden_dir / "simple-identify-missing-data" / "request-body.json"
    ) as f:
        request_body = json.load(f)

    with open(
        testdata_golden_dir / "simple-identify-missing-data" / "response.json"
    ) as f:
        expected_response = json.load(f)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/gaps/identify-missing-data",
            json=request_body,
        )
        assert response.status_code == 200
        assert response.json() == expected_response
