from sqlmodel import SQLModel, Field


class Stop(SQLModel, table=True):
    stop_id: int = Field(default=None,primary_key=True)
    name_stop: str
    latitude: str
    longitude: str
    has_pavilion: bool