from datetime import date, datetime, timezone
from typing import Optional

import pandas as pd
from fastapi import APIRouter
from pvanalytics.quality import gaps
from pydantic import BaseModel, ConfigDict, Field

from insights.common.models import (
    NormalizedValueAndTimestamp,
    create_normalized_value_and_timestamp_series,
)

router = APIRouter(
    prefix="/gaps",
    tags=["gaps"],
)


class NormalizedACPowerAndTimestamp(NormalizedValueAndTimestamp):
    """
    A normalized AC power value and timestamp.
    """

    """
    The name of the stream.
    """
    stream_name: str = Field(
        ...,
        description="The name of the stream.",
        examples=["ac_power"],
    )


class IdentifyInterpolatedDataRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


@router.post("/identify-interpolated-data")
async def identify_interpolated_data(
    request_body: IdentifyInterpolatedDataRequestBody,
) -> list[NormalizedACPowerAndTimestamp]:
    """
    Identify interpolated data in a given period.
    """
    return []


class IdentifyStaleDataRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")


@router.post("/identify-stale-data")
async def identify_stale_data(
    request_body: IdentifyStaleDataRequestBody,
) -> list[NormalizedACPowerAndTimestamp]:
    """
    Identify stale data in a given period.
    """
    return []


class IdentifyMissingDataRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """
    The data to detect missing data in.
    """
    data: list[NormalizedACPowerAndTimestamp] = Field(
        ...,
        description="The data to detect missing data in.",
        examples=[
            [
                # Create a data series with 15 minute intervals.
                NormalizedACPowerAndTimestamp(
                    value=0.1,
                    timestamp=datetime(2023, 6, 21, 12, 0, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
                NormalizedACPowerAndTimestamp(
                    value=0.2,
                    timestamp=datetime(2023, 6, 21, 12, 15, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
                NormalizedACPowerAndTimestamp(
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
        description="The frequency of the data. If not provided, the data frequency will be inferred from the data.",
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


class TrimMissingDataRequestBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    """
    The data to detect missing data in.
    """
    data: list[NormalizedACPowerAndTimestamp] = Field(
        ...,
        description="The data to detect missing data in.",
        examples=[
            [
                # Create a data series with 15 minute intervals.
                NormalizedACPowerAndTimestamp(
                    value=0.1,
                    timestamp=datetime(2023, 6, 21, 12, 0, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
                NormalizedACPowerAndTimestamp(
                    value=0.2,
                    timestamp=datetime(2023, 6, 21, 12, 15, 0, tzinfo=timezone.utc),
                    stream_name="ac_power",
                ),
                NormalizedACPowerAndTimestamp(
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
        description="The frequency of the data. If not provided, the data frequency will be inferred from the data.",
        examples=["15min"],
    )

    """
    The minimum completeness to trim.
    """
    min_completeness: float = Field(
        0.333,
        description="The minimum completeness to trim.",
        ge=0,
        le=1,
        examples=[0.333],
    )

    """
    The number of consecutive days to trim. If not provided, any day that meets the minimum completeness will be included.
    """
    consecutive_days: int = Field(
        10,
        description="The number of consecutive days to trim. If not provided, any day that meets the minimum completeness will be included.",
        ge=0,
        examples=[10],
    )


class TrimMissingDataResponse(BaseModel):
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

    """
    The trimmed data. The data is trimmed to the minimum completeness.
    """
    trimmed_data: list[NormalizedACPowerAndTimestamp] = Field(
        ...,
        description="The trimmed data. The data is trimmed to the minimum completeness.",
        examples=[[]],
    )

    """
    The days that were excluded.
    """
    excluded_days: list[date] = Field(
        ...,
        description="The days that were excluded.",
        examples=[[date(2023, 6, 21)]],
    )


@router.post("/trim-missing-data")
async def trim_missing_data(
    request_body: TrimMissingDataRequestBody,
) -> TrimMissingDataResponse:
    """
    Trim missing data in a given period.
    """

    data = create_normalized_value_and_timestamp_series(
        request_body.data, request_body.data_frequency
    )

    # Identify the missing data
    # This will give a series of completeness scores for each day.
    completeness_score_series = gaps.completeness_score(
        data, freq=request_body.data_frequency
    )

    # Create a dictionary of each day's completeness score
    completeness_score_by_day = (
        completeness_score_series.groupby(completeness_score_series.index.date)
        .mean()
        .to_dict()
    )

    # Get the mask of complete days
    daily_completeness_mask = gaps.complete(
        completeness_score_series,
        minimum_completeness=request_body.min_completeness,
        freq=request_body.data_frequency,
    )

    keep_mask = daily_completeness_mask.reindex(data.index, method="ffill")
    trimmed_data = [item for item, keep in zip(request_body.data, keep_mask) if keep]

    excluded_days = [
        date
        for date, keep in daily_completeness_mask.groupby(
            daily_completeness_mask.index.date
        )
        .first()
        .items()
        if not keep
    ]

    return TrimMissingDataResponse(
        completeness_score_by_day=completeness_score_by_day,
        trimmed_data=trimmed_data,
        excluded_days=excluded_days,
    )
