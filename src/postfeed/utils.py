from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from postfeed.models import Posts


async def get_last_post(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    """Return last posts"""
    print(user)
    if user:
        try:
            query = select(Posts).options(subqueryload(Posts.user), subqueryload(Posts.like))\
                .order_by(Posts.add_message_at).limit(limit=10)
            resp = await session.execute(query)
            r = resp.scalars().all()

            return {
                "status": "success",
                "data": r,
                "detail": "Posts add!"
            }
        except Exception:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": "Wrong query to DB"
            })
    else:
        try:
            query = select(Posts).options(subqueryload(Posts.user), subqueryload(Posts.like))\
                .order_by(Posts.add_message_at).limit(limit=10)
            resp = await session.execute(query)
            r = resp.scalars().all()

            return {
                "status": "success",
                "data": r,
                "detail": None
            }
        except Exception:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": "Wrong query to DB"
            })