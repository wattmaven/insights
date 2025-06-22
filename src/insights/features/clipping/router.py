from datetime import date, datetime, timezone
from typing import Optional

import pandas as pd
from fastapi import APIRouter
from pvanalytics.features.clipping import geometric
from pvanalytics.quality import gaps
from pydantic import BaseModel, ConfigDict, Field

from insights.common.models import (
    NormalizedStreamValueAndTimestamp,
    NormalizedValueAndTimestamp,
    create_normalized_value_and_timestamp_series,
)

router = APIRouter(
    prefix="/clipping",
    tags=["clipping"],
)


class DetectClippingRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """
    The data to detect clipping in.
    """
    data: list[NormalizedStreamValueAndTimestamp] = Field(
        ...,
        description="The data to detect clipping in.",
        examples=[
            [
                NormalizedStreamValueAndTimestamp(
                    value=0.1,
                    timestamp=datetime(2023, 6, 21, 12, 0, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
                NormalizedStreamValueAndTimestamp(
                    value=0.2,
                    timestamp=datetime(2023, 6, 21, 12, 15, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
            ]
        ],
    )

    data_frequency: str = Field(
        ...,
        description="The frequency of the data.",
        examples=["15min"],
    )


class DetectClippingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """
    The clipping data.
    """
    clipping_data: list[NormalizedStreamValueAndTimestamp] = Field(
        ...,
        description="The clipping data.",
    )


@router.post("/detect-clipping")
async def detect_clipping(
    request_body: DetectClippingRequestBody,
) -> DetectClippingResponse:
    """
    Detect clipping in a given period.
    """

    data = create_normalized_value_and_timestamp_series(
        request_body.data, request_body.data_frequency
    )

    # Detect clipping
    clipping_data = geometric(ac_power=data, freq=request_body.data_frequency)

    return DetectClippingResponse(clipping_data=[])
