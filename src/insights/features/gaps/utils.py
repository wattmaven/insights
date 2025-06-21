import pandas as pd

from insights.common.models import NormalizedValueAndTimestamp


def create_data_series(
    data: list[NormalizedValueAndTimestamp], data_frequency: str
) -> pd.Series:
    """
    Create a data series from a list of normalized value and timestamp.

    Args:
        data: The list of normalized value and timestamp.
        data_frequency: The frequency of the data.

    Returns:
        The data series.
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
