from fastapi import FastAPI
from routers.rows import router as rows_router

app = FastAPI(title="Athena-backed API")
app.include_router(rows_router)