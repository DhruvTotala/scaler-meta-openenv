from pydantic import BaseModel, Field

class GridState(BaseModel):
    time_step: int = Field(0, description="Current hour of the day (0-23)")
    indoor_temp: float = Field(22.0, description="Current indoor temperature in Celsius")
    battery_level: float = Field(50.0, description="Battery charge percentage (0-100)")
    grid_price: float = Field(..., description="Current electricity price per kWh")

class AgentAction(BaseModel):
    hvac_power: float = Field(0.0, ge=-1.0, le=1.0, description="-1.0 (Full AC) to 1.0 (Full Heat)")
    battery_action: float = Field(0.0, ge=-1.0, le=1.0, description="-1.0 (Sell to grid) to 1.0 (Buy from grid)")