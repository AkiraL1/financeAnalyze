from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from apps.api.routes import router
from finance_analyze.paths import WEB_ROOT

app = FastAPI(title="financeAnalyze", version="0.1.0")
app.include_router(router)
if WEB_ROOT.is_dir():
    app.mount("/static", StaticFiles(directory=WEB_ROOT), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_ROOT / "index.html")
