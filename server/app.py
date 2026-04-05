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
if __name__ == "__main__":
        import uvicorn
        uvicorn.run("server.app:app", host="0.0.0.0", port=7860)