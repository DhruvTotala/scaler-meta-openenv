import os
import json
from openai import OpenAI
from env import SmartGridEnv
from models import AgentAction
from tasks import EasyTask, MediumTask, HardTask

# FIX 1: No trailing slash
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1")

# FIX 2: Ungated open model
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", os.getenv("HF_TOKEN", "dummy")), 
    base_url=API_BASE_URL
)

def get_agent_action(state_json: str) -> AgentAction:
    prompt = f"""
    You are a Smart Grid AI Agent.
    State: {state_json}
    Output JSON exactly matching: {{"hvac_power": float (-1 to 1), "battery_action": float (-1 to 1)}}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        action_dict = json.loads(response.choices[0].message.content)
        return AgentAction(**action_dict)
    except Exception:
        return AgentAction(hvac_power=0.0, battery_action=0.0)

def run_baseline():
    print("[START] Initializing Smart Grid Environment Baseline")
    env = SmartGridEnv()
    done = False
    step_count = 0
    
    while not done:
        state_json = env.state().model_dump_json()
        print(f"[STEP] Step {step_count} - State: {state_json}")
        
        action = get_agent_action(state_json)
        print(f"[STEP] Step {step_count} - Action Taken: {action.model_dump_json()}")
        
        _, _, done, _ = env.step(action)
        step_count += 1
    
    print(f"[END] Episode Finished. Cumulative Cost: {env.cumulative_cost:.2f}")
    print(f"[END] Easy Task Score: {EasyTask().grade(env)}")
    print(f"[END] Medium Task Score: {MediumTask().grade(env)}")
    print(f"[END] Hard Task Score: {HardTask().grade(env)}")

if __name__ == "__main__":
    run_baseline()
