import random
from .models import GridState, AgentAction

class SmartGridEnv:
    def __init__(self, target_temp=22.0):
        self.target_temp = target_temp
        self.max_steps = 24
        self.reset()

    def reset(self) -> GridState:
        self.current_step = 0
        self.cumulative_cost = 0.0
        self._state = GridState(
            time_step=0,
            indoor_temp=random.uniform(18.0, 26.0),
            battery_level=50.0,
            grid_price=self._get_price(0)
        )
        return self.state()

    def state(self) -> GridState:
        return self._state

    def _get_price(self, hour: int) -> float:
        # Simulate peak pricing (e.g., expensive in the evening)
        return 0.5 + 0.5 * (hour / 24.0) if hour < 18 else 1.5

    def step(self, action: AgentAction):
        # Update Temperature
        self._state.indoor_temp += action.hvac_power * 2.0 
        self._state.indoor_temp += random.uniform(-0.5, 0.5) 
        
        # Update Battery
        self._state.battery_level += action.battery_action * 10.0
        self._state.battery_level = max(0.0, min(100.0, self._state.battery_level))

        # Calculate Costs
        hvac_cost = abs(action.hvac_power) * self._state.grid_price
        battery_cost = action.battery_action * self._state.grid_price
        step_cost = hvac_cost + battery_cost
        self.cumulative_cost += step_cost

        # Advance time
        self.current_step += 1
        self._state.time_step = self.current_step
        self._state.grid_price = self._get_price(self.current_step)

        # Reward Function (Penalty for cost and discomfort)
        temp_penalty = abs(self._state.indoor_temp - self.target_temp)
        reward = -(step_cost + temp_penalty)

        done = self.current_step >= self.max_steps
        
        return self.state(), reward, done, {"step_cost": step_cost}