from fastapi import FastAPI # type: ignore
from app.env import CustomerSupportEnv

app = FastAPI()
env = CustomerSupportEnv()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/reset")
def reset():
    obs = env.reset(0)
    return obs.dict()