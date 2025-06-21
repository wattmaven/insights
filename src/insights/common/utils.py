import pandas as pd


def can_infer_data_frequency(data: pd.Series) -> bool:
    """
    Check if the data frequency can be inferred from the data.

    Args:
        data: The data to check.

    Returns:
        True if the data frequency can be inferred, False otherwise.
    """
    return len(data) > 3
