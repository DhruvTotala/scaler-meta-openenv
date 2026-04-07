class BaseGrader:
    def grade(self, env) -> float:
        raise NotImplementedError

class EasyTask(BaseGrader):
    def grade(self, env) -> float:
        final_temp = env.state().indoor_temp
        if 20.0 <= final_temp <= 24.0:
            return 1.0
        deviation = abs(final_temp - 22.0)
        return max(0.0, 1.0 - (deviation / 10.0))

class MediumTask(BaseGrader):
    def grade(self, env) -> float:
        temp_score = EasyTask().grade(env)
        cost_score = max(0.0, 1.0 - (env.cumulative_cost / 20.0))
        return (temp_score * 0.5) + (cost_score * 0.5)

class HardTask(BaseGrader):
    def grade(self, env) -> float:
        med_score = MediumTask().grade(env)
        battery = env.state().battery_level
        battery_score = 1.0 if battery >= 80.0 else (battery / 80.0)
        return (med_score * 0.6) + (battery_score * 0.4)