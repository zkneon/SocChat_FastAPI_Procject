from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth_pages",
    tags=["pages"]
)

templates = Jinja2Templates(directory="templates/auth_templates")


@router.get("/register")
def get_register_page(request: Request):
    """Return page with register Form"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
def get_login_page(request: Request):
    """Return page with login Form"""

    return templates.TemplateResponse("login.html", context={"request": request})
