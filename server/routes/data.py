from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic.networks import HttpUrl
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import desc

from database.main import get_db
from schemas import videos as videoSchema
from models import models

router = APIRouter(prefix='/data', tags=["Data"])


@router.get('/', response_model=Page[videoSchema.Show_Video])
async def get_data(db: Session = Depends(get_db), sort: Optional[str] = '-time'):
    data = None
    # Default sorting is Reverse chronological order
    if sort == '-time':
        data = db.query(models.Video).order_by(
            desc(models.Video.published_at)).all()
    # sort in chronological order
    elif sort == '+time':
        data = db.query(models.Video).order_by(models.Video.published_at).all()
    # sorting by ascending titles
    elif sort == '+title':
        data = db.query(models.Video).order_by(models.Video.title).all()
    # sorting by descending titles
    elif sort == '-title':
        data = db.query(models.Video).order_by(desc(models.Video.title)).all()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return paginate(data)

add_pagination(router)
