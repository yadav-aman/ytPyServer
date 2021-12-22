from database.main import Base
from sqlalchemy import Column, String, DateTime


class Video(Base):
    __tablename__ = "videos"
    # using videoID as primary key to avoid duplicates in the database
    video_id = Column(String, primary_key=True)
    channel_name = Column(String)
    title = Column(String)
    description = Column(String)
    published_at = Column(DateTime)
    thumbnails = Column(String)
