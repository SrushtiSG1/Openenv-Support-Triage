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

from app.models import Action

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info
    }