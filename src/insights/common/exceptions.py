from fastapi import HTTPException

# This is a custom exception that is raised when a data frequency cannot be inferred from the data.
# This is only possible if the data is greater than 3 samples.
IncompleteInferrenceError = HTTPException(
    status_code=400,
    detail="Data frequency is required if the data is less than 3 samples.",
)
