from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from operations.models import Operation
from operations.schemas import OperationCreate
from postfeed.models import Posts, LikePost
from fastapi_cache.decorator import cache
from fastapi_cache.key_builder import default_key_builder

from postfeed.schemas import PostsGet

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.post("/add_to_db")
async def add_to_db(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/add_like")
async def add_like(session: AsyncSession = Depends(get_async_session)):
    pass
