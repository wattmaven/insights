from datetime import datetime
from typing import Annotated

import pandas as pd
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, field_validator

from insights.common.validators import is_in_the_future


class NormalizedValueAndTimestamp(BaseModel):
    """
    A normalized value and timestamp.
    """

    model_config = ConfigDict(extra="forbid")

    """
    The normalized value.
    """
    value: float = Field(
        ...,
        description="The normalized value.",
        examples=[0.5],
    )

    """
    The timestamp.
    """
    timestamp: datetime = Field(
        ...,
        description="The timestamp of the value.",
        examples=[datetime(2023, 6, 21, 12, 0, 0)],
    )


def create_normalized_value_and_timestamp_series(
    data: list[NormalizedValueAndTimestamp], data_frequency: str
) -> pd.Series:
    """
    Create a normalized value and timestamp series.

    Args:
        data: The list of normalized value and timestamp.
        data_frequency: The frequency of the data.

    Returns:
        The normalized value and timestamp series.
    """
    series = pd.Series(
        [item.value for item in data],
        index=pd.to_datetime([item.timestamp for item in data]),
    )

    # Reindex the data to ensure it has a proper frequency
    if len(series) > 0:
        full_range = pd.date_range(
            start=series.index.min(), end=series.index.max(), freq=data_frequency
        )
        series = series.reindex(full_range)

    return series


class DataPeriod(BaseModel):
    """
    A period of time.
    """

    model_config = ConfigDict(extra="forbid")

    """
    The start date.
    """
    start_date: datetime = Field(
        ...,
        description="The start date of the data period.",
        examples=[datetime(2023, 6, 21, 12, 0, 0)],
    )

    """
    The end date.
    """
    end_date: Annotated[datetime, AfterValidator(is_in_the_future)] = Field(
        ...,
        description="The end date of the data period.",
        examples=[datetime(2023, 6, 21, 12, 0, 0)],
    )
