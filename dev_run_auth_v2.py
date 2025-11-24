import uvicorn
from fastapi import FastAPI
from backend.routers import auth_v2

app = FastAPI(title="AUTH_V2_DEV")

# include only the new auth_v2 router for isolated testing
app.include_router(auth_v2.router)

if __name__ == "__main__":
    uvicorn.run("dev_run_auth_v2:app", host="127.0.0.1", port=8001, reload=True)
