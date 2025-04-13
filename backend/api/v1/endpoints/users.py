from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException

import schemas
from db import models
from api.v1 import deps

router = APIRouter()

@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
) -> Any:
    """
    Get current logged-in user's details.
    """
    return current_user
