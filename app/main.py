from fastapi import FastAPI, Request
from app.version_a import router as version_a
from app.version_b import router as version_b
from app.metrics import (
    router as metrics_router,
    REQUEST_COUNT,
    REQUEST_LATENCY,
)
import time

app = FastAPI(title="OS Concurrency Demo")

# Routers
app.include_router(version_a, prefix="/v1")
app.include_router(version_b, prefix="/v2")
app.include_router(metrics_router)

# Metrics middleware 
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(duration)

    return response

@app.get("/")
def root():
    return {"message": "OS Concurrency Project Running"}
