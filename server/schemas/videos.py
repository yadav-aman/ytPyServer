from datetime import datetime
from pydantic import BaseModel


class Video(BaseModel):
    video_id: str
    channel_name: str
    title: str
    description: str
    published_at: datetime
    thumbnails: str


# response model to fetch video data
class Show_Video(Video):

    class Config():
        orm_mode = True
