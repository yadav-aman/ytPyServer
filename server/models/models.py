from sqlalchemy.sql.sqltypes import DateTime
from database.main import Base
from sqlalchemy import Column, Integer, String


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    published_at = Column(String)
    thumbnails = Column(String)
    channel_name = Column(String)
