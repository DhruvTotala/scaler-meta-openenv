import sys
import os
import uvicorn
from fastapi import FastAPI

# This ensures Python can still find your env.py file in the main folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env import SmartGridEnv
from models import AgentAction

app = FastAPI()
env = SmartGridEnv()

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/reset")
@app.get("/reset")
def reset_env():
    return env.reset().model_dump()

@app.get("/state")
def get_state():
    return env.state().model_dump()

@app.post("/step")
def step_env(action: AgentAction):
    state, reward, done, info = env.step(action)
    return {
        "state": state.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

# The mandatory main function
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

# The mandatory callable block
if __name__ == "__main__":
    main()