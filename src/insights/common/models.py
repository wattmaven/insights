from datetime import datetime
from typing import Annotated

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
