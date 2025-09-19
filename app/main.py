import logging

from fastapi import FastAPI, Request
from app.api import router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from app.utils.logger import init_log

init_log(logging.INFO)

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

uvicorn.run(app, port=80)
