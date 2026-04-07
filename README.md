---
title: ScalerXMeta Smart Grid
emoji: ⚡
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 7860
---

# Smart Grid Energy Manager - OpenEnv

## Environment Description
This is a real-world Reinforcement Learning environment built for the Meta PyTorch OpenEnv Hackathon. An AI agent acts as a smart home controller. It must manage the house's HVAC system (temperature) and a home battery (like a Tesla Powerwall) against real-time fluctuating electricity prices. The goal is to maximize human comfort while minimizing the electricity bill and grid reliance.

## Observation Space (State)
The agent receives a `GridState` object containing:
* `time_step`: Current hour (0-23)
* `indoor_temp`: Current temperature in Celsius.
* `battery_level`: Battery percentage (0-100).
* `grid_price`: Real-time cost of electricity.

## Action Space
The agent outputs an `AgentAction` object containing:
* `hvac_power`: Float [-1.0 to 1.0] representing cooling/heating intensity.
* `battery_action`: Float [-1.0 to 1.0] representing selling/buying from the grid.

## Setup & Running Instructions
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Export your keys:
   `export HF_TOKEN="your_huggingface_token"`
   `export OPENAI_API_KEY="your_huggingface_token"`
4. Run inference: `python inference.py`
5. Or run via Docker: `docker build -t smartgrid . && docker run smartgrid`