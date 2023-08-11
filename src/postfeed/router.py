import json

from fastapi import APIRouter, Depends, HTTPException, Request, WebSocketDisconnect
from fastapi.responses import Response, JSONResponse, HTMLResponse, RedirectResponse


from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session

from fastapi.templating import Jinja2Templates

from auth.utils import AuthGuard
from auth.base_config import current_user
from postfeed.service import ConnectionManager, WebSocket
from postfeed.models import Posts, LikePost
from postfeed.schemas import PostsAdd, PostsGet
from postfeed.utils import get_last_post
# manager = ConnectionManager()

router = APIRouter(
    prefix="/postfeed",
    tags=['PostFeed']
)

templates = Jinja2Templates(directory="templates")
auth_post_page = AuthGuard("post_page")


@router.get("")
async def get_post_page(request: Request,
                        resp: PostsGet = Depends(get_last_post),
                        user: User = Depends(current_user)) -> Response:
    """Return last posts for authorized Users. It's security page"""
    if user:
        return templates.TemplateResponse("posts_page.html", {"request": request, "user": user,
                                                              "post_data": resp["data"]})
    else:
        return RedirectResponse(url='auth_pages/login', status_code=307)


@router.get("/lastpost")
async def get_last_post_page(request: Request, resp: PostsGet = Depends(get_last_post)) -> Response:
    """Return last posts for all User"""
    user = False
    return templates.TemplateResponse("posts_page.html", {"request": request,
                                                          "user": user,
                                                          "post_data": resp["data"]})


@router.post("/add_post", dependencies=[Depends(current_user)])
async def add_post_page(new_post_data: PostsAdd, session: AsyncSession = Depends(get_async_session)):
    """Add New Post. Only for authorized users"""
    try:
        stmt = insert(LikePost).returning(LikePost)
        like_post = await session.execute(stmt)
        like_id = like_post.scalar_one().id
        data = new_post_data.dict()
        print(like_id)

        print(data)
        stmt = insert(Posts).values({**data, 'like_post_id': like_id}).returning(Posts)
        post = await session.execute(stmt)
        post = post.scalar_one()
        await session.commit()
        return {
            "status": "success",
            "data": {
                "post_id": post.id,
                "user_id": post.user_id,
                 },
            "detail": "Posts add!"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "Bad Response Data",
            "data": None,
            "details": "Wrong query to DB"
        })
#
#
# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
