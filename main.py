from fastapi import HTTPException, status, Request, Form, FastAPI, Query, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from Fanction import FanctionData
from pathlib import Path
import os


# إعداد التطبيق
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="Asdwq423vbDW54r566rtrbff2352")

# إعداد الباسورد
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# رابط الملف
url = 'https://www.dropbox.com/scl/fi/d332anc7id7z24x9u2y12/Workshop.xlsx?rlkey=f4yaaz7euil4o2xqogwt3qcxm&dl=1'
FileJSON = "data.json"

get_usre = FanctionData()
users = get_usre.load_json("user.json")

# إعداد المجلدات
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# تعريف المستخدم
class User(BaseModel):
    username: str
    password: str


# دالة لفحص كلمة المرور
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# دالة لتشفير كلمة المرور
def get_password_hash(password):
    return pwd_context.hash(password)

#اسم المستخدم وكلمة المرور
fake_users_db = {
    "ALAMIN_A": {
        "username": users["username"],
        "hashed_password": get_password_hash(users["password"])
    }
}

# تحديد مسار مجلد لحفظ الصور المرفوعة
UPLOAD_DIR = Path("static/image")
UPLOAD_DIR.mkdir(exist_ok=True)
UPLOAD_FOLDER = "static/image"

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file:
        file_location = UPLOAD_DIR / file.filename
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return {"status": "success", "message": f"File '{file.filename}' uploaded successfully."}
    else:
        return {"status": "error", "message": "No file provided"}


@app.delete("/delete_image")
async def delete_image(name: str = Query(...)):
    image_path = os.path.join(UPLOAD_FOLDER, f"{name}.jpg")
    if os.path.exists(image_path):
        os.remove(image_path)
        return {"success": True}
    else:
        return {"success": False, "error": "File not found"}


# الصفحة الرئيسية
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):

    if "username" not in request.session:
        return RedirectResponse(url="/login")

    openTitle = FanctionData()
    TitleOpen = openTitle.load_json(FileJSON)
    title = TitleOpen.get("title", "معلومات الطقوم")

    images1 = [f.split('.')[0] for f in os.listdir('static/uploads') if
              os.path.isfile(os.path.join('static/uploads', f))]
    return templates.TemplateResponse("index.html", {"request": request, "images": images1, "title": title})


#التحديث بناء على الطقوم الجاهزة
@app.get("/update-images")
async def update_images():
    try:
        updateP = FanctionData()
        updateP.update('الجاهز',
                        'اسم الموديل',
                        'الصفحة الرئيسية',
                        'عدد الطقوم',
                        url,
                        "الطقوم الجاهزة")

        return JSONResponse(content={"success": True})
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return JSONResponse(content={"success": False})


#التحديث بناء على الطقوم الموجودة
@app.get("/update-available-images")
async def update_available_images():
    try:
        updateP = FanctionData()
        updateP.update('الموجود',
                        'اسم الموديل',
                        'الصفحة الرئيسية',
                        'عدد الطقوم',
                        url,
                        "الطقوم الموجودة")
        return JSONResponse(content={"success": True})
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return JSONResponse(content={"success": False})


#التحديث بناء على نقص الطقوم
@app.get("/update-price-nazm-images1")
async def update_available_images2():
    try:
        updateP = FanctionData()
        updateP.update('النقص',
                        'اسم الموديل',
                        'الصفحة الرئيسية',
                        'عدد الطقوم',
                        url,
                        "نقص الطقوم")
        return JSONResponse(content={"success": True})
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return JSONResponse(content={"success": False})


#التحديث بيناء على أسعار الطقوم
@app.get("/update-price-images")
async def update_price_images():
    try:
        updateP = FanctionData()
        updateP.update('السعر',
                        'اسم الموديل',
                        'الصفحة الرئيسية',
                        'سعر',
                        url,
                        "أسعار الطقوم")
        return JSONResponse(content={"success": True})
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return JSONResponse(content={"success": False})


# التحديث بناءً على رأس المال
@app.get("/update-pric-images")
async def update_pric_images():
    try:
        updateP = FanctionData()
        updateP.update('صافي التكلفة',
                        'الرقم',
                        'بيانات رأس المال',
                        'التكلفة',
                        url,
                        "رأس المال")
        return JSONResponse(content={"success": True})
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return JSONResponse(content={"success": False})


# التحديث بناء على الأسعار لمحل ناظم
@app.get("/update-price-nazm-images")
async def update_price_nazm_images():
    try:
        updateP = FanctionData()
        updateP.update('الأسعار لمحل ناظم',
                        'اسم الموديل',
                        'الصفحة الرئيسية',
                        'السعر لمحل ناظم',
                        url,
                        "الأسعار لمحل ناظم")
        return JSONResponse(content={"success": True})
    except Exception as e:
        print(f"حدث خطأ: {e}")
        return JSONResponse(content={"success": False})


# صفحة تسجيل الدخول
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login_for_access(request: Request, username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)
    if user and verify_password(password, user['hashed_password']):
        request.session["username"] = username
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    raise HTTPException(status_code=400, detail="Invalid credentials")


# صفحة تسجيل الخروج
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


# صفحة الملخص
@app.get("/summary", response_class=HTMLResponse)
async def read_summary(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'ملخص',
        'Table33'
    )
    titleTable = "الملخص"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html , "title_table": titleTable})

#ملخص البيع
@app.get("/summary1", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'ملخص البيع',
        'Table1021'
    )
    titleTable = "ملخص البيع"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html , "title_table": titleTable})

#المصروف
@app.get("/summary2", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'المصروف',
        'Table15'
    )
    titleTable = "المصروف"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html ,"title_table": titleTable})

#الزكاة
@app.get("/summary3", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'الزكاة',
        'Table7'
    )
    titleTable = "الزكاة"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#بيانات رأس المال
@app.get("/summary4", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'بيانات رأس المال',
        'الجدول1'
    )
    titleTable = "بيانات رأس المال"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#بيانات البيع
@app.get("/summary5", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'البيانات',
        'Table4'
    )
    titleTable = "بيانات البيع"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#الأمانات
@app.get("/summary6", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'الأمانات',
        'Table19'
    )
    titleTable = "الأمانات"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#بيانات عبد الملك
@app.get("/summary7", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'عبد العظيم',
        'Table18'
    )
    titleTable = "بيانات عبد الملك"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#بيانات عبد العظيم
@app.get("/summary8", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'عبد العظيم',
        'Table17'
    )
    titleTable = "بيانات عبد العظيم"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#بيانات أحمد أحمدية
@app.get("/summary9", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'أحمد أحمدية',
        'الجدول16'
    )
    titleTable = "بيانات أحمد أحمدية"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#الدفعات
@app.get("/summary10", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'الدفعات',
        'Table3'
    )
    titleTable = "الدفعات"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#الإنتاج
@app.get("/summary11", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'الإنتاج',
        'Table2'
    )
    titleTable = "الإنتاج"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#حساب خارجي
@app.get("/summary12", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'حساب خارجي',
        'Table12'
    )
    titleTable = "حساب خارجي"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#جدول الدفعات الشهرية
@app.get("/summary13", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'صفحة الشباب الرئيسية',
        'Table28'
    )
    titleTable = "جدول الدفعات الشهرية"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#الصفحة الرئيسية
@app.get("/summary14", response_class=HTMLResponse)
async def view_data(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    view = FanctionData()
    data_html = view.viwe(
        url,
        'الصفحة الرئيسية',
        'Table11'
    )
    titleTable = "الصفحة الرئيسية"
    return templates.TemplateResponse("data_table.html", {"request": request, "summary_html": data_html, "title_table": titleTable})

#رفع صورة
@app.get("/upload_page", response_class=HTMLResponse)
async def upload_page(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")
    with open("templates/upload.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# صفحة الصور
@app.get("/images", response_class=HTMLResponse)
async def images(request: Request):
    if "username" not in request.session:
        return RedirectResponse(url="/login")

    images2 = sorted(
        [int(f.split('.')[0]) for f in os.listdir('static/image') if os.path.isfile(os.path.join('static/image', f))],
        reverse=True)
    return templates.TemplateResponse("images.html", {"request": request, "images": images2})
