from fastapi import FastAPI
from app.env import CustomerSupportEnv

app = FastAPI()
env = CustomerSupportEnv()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    obs = env.reset(0)
    return obs.dict()


def main():
    return app