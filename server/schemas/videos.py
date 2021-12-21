from datetime import datetime
from pydantic import BaseModel


class Video(BaseModel):
    title: str
    description: str
    published_at: str
    thumbnails: str
    channel_name: str


class Show_Video(Video):
    id: int

    class Config():
        orm_mode = True
