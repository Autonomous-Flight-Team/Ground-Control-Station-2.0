from datetime import datetime
from typing import Literal
from pydantic import BaseModel

class Attitude(BaseModel):
    q: tuple[float, float, float, float]      # w, x, y, z
    rates_rad_s: tuple[float, float, float]

class Position(BaseModel):
    lat_deg: float
    lon_deg: float
    alt_msl_m: float
    alt_agl_m: float | None = None
    vel_ned_m_s: tuple[float, float, float]
    heading_rad: float
    gps_fix: int

class Envelope(BaseModel):
    schema_version: int = 1
    vehicle_id: str
    msg_type: Literal["attitude", "position", "airdata", "power", "status", "link"]
    t_boot_us: int
    t_recv_utc: datetime
    seq: int
    payload: dict