from datetime import date, datetime, timezone
from typing import Optional

import pandas as pd
from fastapi import APIRouter
from pvanalytics.quality import gaps
from pydantic import BaseModel, ConfigDict, Field

from insights.common.models import (
    NormalizedStreamValueAndTimestamp,
    create_normalized_value_and_timestamp_series,
)

router = APIRouter(
    prefix="/gaps",
    tags=["gaps"],
)


class IdentifyMissingDataRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """
    The data to detect missing data in.
    """
    data: list[NormalizedStreamValueAndTimestamp] = Field(
        ...,
        description="The data to detect missing data in.",
        examples=[
            [
                # Create a data series with 15 minute intervals.
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
                NormalizedStreamValueAndTimestamp(
                    value=0.3,
                    timestamp=datetime(2023, 6, 21, 12, 30, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
            ]
        ],
    )

    """
    The frequency of the data.
    """
    data_frequency: str = Field(
        ...,
        description="The frequency of the data.",
        examples=["15min"],
    )


class IdentifyMissingDataResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """
    The completeness score.
    """
    completeness_score_by_day: dict[date, float] = Field(
        ...,
        description="The completeness score by day.",
        examples=[
            {
                date(2023, 6, 21): 0.03125,
            }
        ],
    )


@router.post("/identify-missing-data")
async def identify_missing_data(
    request_body: IdentifyMissingDataRequestBody,
) -> IdentifyMissingDataResponse:
    """
    Detect missing data in a given period.
    """

    data = create_normalized_value_and_timestamp_series(
        request_body.data, request_body.data_frequency
    )

    # Identify the missing data
    # This will give a series of completeness scores for each day.
    completeness_score_series = gaps.completeness_score(
        data, freq=request_body.data_frequency
    )

    # Create a dictionary of each day's completeness score.
    completeness_score_by_day = (
        completeness_score_series.groupby(completeness_score_series.index.date)
        .mean()
        .round(5)  # Round to 5 decimal places for consistency
        .to_dict()
    )

    return IdentifyMissingDataResponse(
        completeness_score_by_day=completeness_score_by_day
    )
