from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId

from models.products import Product
from models.users import User

templates = Jinja2Templates(directory="templates")
web_router = APIRouter(include_in_schema=False)

# Вспомогательная функция получения текущего пользователя из Cookies
async def get_current_user(request: Request) -> Optional[User]:
    email = request.cookies.get("user_email")
    if email:
        return await User.find_one(User.email == email)
    return None

# ----------------- КАТАЛОГ И ТОВАРЫ -----------------

@web_router.get("/", response_class=HTMLResponse)
async def catalog_page(
    request: Request,
    brand: Optional[str] = None,
    category: Optional[str] = None
):
    current_user = await get_current_user(request)
    query = {}
    if brand:
        query["brand"] = {"$regex": f"^{brand}$", "$options": "i"}
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    products = await Product.find(query).to_list()
    all_products = await Product.find_all().to_list()
    categories = sorted(list({p.category for p in all_products if p.category}))
    brands = sorted(list({p.brand for p in all_products if p.brand}))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "products": products,
            "categories": categories,
            "brands": brands,
            "selected_brand": brand,
            "selected_category": category,
            "current_user": current_user
        }
    )

@web_router.get("/products/{id}", response_class=HTMLResponse)
async def product_detail_page(request: Request, id: str):
    current_user = await get_current_user(request)
    product = await Product.get(ObjectId(id))
    if not product:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse(
        request=request,
        name="product_detail.html",
        context={"product": product, "current_user": current_user}
    )

@web_router.get("/admin/products/new", response_class=HTMLResponse)
async def new_product_form(request: Request):
    current_user = await get_current_user(request)
    return templates.TemplateResponse(
        request=request,
        name="product_add.html",
        context={"error": None, "current_user": current_user}
    )

@web_router.post("/admin/products/new", response_class=HTMLResponse)
async def create_product_from_form(
    request: Request,
    sku: str = Form(...),
    name: str = Form(...),
    brand: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    spec_screen: Optional[str] = Form(None),
    spec_cpu: Optional[str] = Form(None),
    spec_ram: Optional[str] = Form(None),
    spec_storage: Optional[str] = Form(None),
):
    current_user = await get_current_user(request)
    existing = await Product.find_one(Product.sku == sku)
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="product_add.html",
            context={
                "error": f"Товар с артикулом (SKU) '{sku}' уже существует!",
                "current_user": current_user
            }
        )

    specs = {}
    if spec_screen:
        specs["Экран"] = spec_screen
    if spec_cpu:
        specs["Процессор"] = spec_cpu
    if spec_ram:
        specs["Оперативная память"] = spec_ram
    if spec_storage:
        specs["Встроенная память"] = spec_storage

    new_product = Product(
        sku=sku,
        name=name,
        brand=brand,
        category=category,
        price=price,
        description=description,
        specifications=specs
    )
    await new_product.create()

    return RedirectResponse(url=f"/products/{str(new_product.id)}", status_code=status.HTTP_303_SEE_OTHER)

# Страница формы редактирования
@web_router.get("/admin/products/{id}/edit", response_class=HTMLResponse)
async def edit_product_form(request: Request, id: str):
    current_user = await get_current_user(request)
    product = await Product.get(ObjectId(id))
    if not product:
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        request=request,
        name="product_edit.html",
        context={"product": product, "current_user": current_user}
    )

# Обработка сохранения изменений
@web_router.post("/admin/products/{id}/edit")
async def save_edited_product(
    id: str,
    sku: str = Form(...),
    name: str = Form(...),
    brand: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    description: str = Form(...),
    spec_screen: Optional[str] = Form(None),
    spec_cpu: Optional[str] = Form(None),
    spec_ram: Optional[str] = Form(None),
    spec_storage: Optional[str] = Form(None),
):
    product = await Product.get(ObjectId(id))
    if product:
        product.sku = sku
        product.name = name
        product.brand = brand
        product.category = category
        product.price = price
        product.description = description

        specs = {}
        if spec_screen:
            specs["Экран"] = spec_screen
        if spec_cpu:
            specs["Процессор"] = spec_cpu
        if spec_ram:
            specs["Оперативная память"] = spec_ram
        if spec_storage:
            specs["Встроенная память"] = spec_storage
        product.specifications = specs

        await product.save()

    return RedirectResponse(url=f"/products/{id}", status_code=status.HTTP_303_SEE_OTHER)

@web_router.post("/admin/products/{id}/delete")
async def delete_product_from_web(id: str):
    product = await Product.get(ObjectId(id))
    if product:
        await product.delete()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# ----------------- АВТОРИЗАЦИЯ И ПОЛЬЗОВАТЕЛИ -----------------

@web_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"error": None})

@web_router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    existing = await User.find_one(User.email == email)
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": f"Пользователь с email '{email}' уже существует в базе данных!"}
        )

    new_user = User(
        username=username,
        email=email,
        password=password,
        role=role
    )
    await new_user.create()

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_email", value=email, max_age=86400)
    return response

@web_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})

@web_router.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = await User.find_one(User.email == email)
    if not user or user.password != password:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Неверный адрес электронной почты или пароль"}
        )

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user_email", value=email, max_age=86400)
    return response

@web_router.get("/logout")
async def logout_user():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="user_email")
    return response
