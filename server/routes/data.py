from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate

from database.main import get_db
from schemas import videos as videoSchema
from models import models

router = APIRouter(prefix='/data', tags=["Data"])


@router.get('/', response_model=Page[videoSchema.Show_Video])
async def get_data(page: int, db: Session = Depends(get_db)):
    data = db.query(models.Video).all()
    return paginate(data)


@router.post('/')
async def post_data(request: videoSchema.Video, db: Session = Depends(get_db)):
    new_video = models.Video(
        title=request.title,
        description=request.description
    )
    try:
        db.add(new_video)
        db.commit()
        db.refresh(new_video)
        return {"detail": "Video Added to database"}
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

add_pagination(router)
