# from azure.monitor.opentelemetry import configure_azure_monitor
# configure_azure_monitor()

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
from os import getenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount('/static', StaticFiles(directory=os.path.join(current_dir, 'static')), name='static')
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("index")
    logger.info("JEREVOSS: app.middleware: %s" % app.middleware)
    logger.info("JEREVOSS: app.middleware(opentelemetry): %s" % app.middleware("opentelemetry"))
    print('Request for index page received')
    return "fastapi test app"

@app.get('/favicon.ico')
async def favicon():
    logger.info("favicon")
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})

@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    logger.info("hello")
    if name:
        print('Request for hello page received with name=%s' % name)
        return templates.TemplateResponse('hello.html', {
            "request": request,
            'name':name,
            'pythonpath': getenv("PYTHONPATH"),
            'app_path': getenv("APP_PATH")
        })
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    logger.info("__main__")
    logger.warning("__main__")
    logger.error("__main__")
    print("__main__")
    uvicorn.run('main:app', host='0.0.0.0', port=3100)
