from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import desc

from database.main import get_db
from schemas import videos as videoSchema
from models import models

router = APIRouter(prefix='/data', tags=["Data"])


@router.get('/', response_model=Page[videoSchema.Show_Video])
async def get_data(db: Session = Depends(get_db)):
    data = db.query(models.Video).order_by(
        desc(models.Video.published_at)).all()
    return paginate(data)

add_pagination(router)
