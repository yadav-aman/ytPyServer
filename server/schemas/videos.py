from datetime import datetime
from pydantic import BaseModel


class Video(BaseModel):
    video_id: str
    channel_name: str
    title: str
    description: str
    published_at: datetime
    thumbnails: str


class Show_Video(Video):

    class Config():
        orm_mode = True
