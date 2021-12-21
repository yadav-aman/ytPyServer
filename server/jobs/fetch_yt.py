import json
import requests
import datetime

from sqlalchemy.orm.session import Session

from env import API_KEY
from models import models


def req_yt_api(db: Session):
    API_URL = 'https://youtube.googleapis.com/youtube/v3/search'
    currentTime = datetime.datetime.now().isoformat()
    response = requests.get(
        f'{API_URL}?part=snippet&order=date&publishedAfter=2021-01-01T00%3A00%3A00Z&q=cricket&key={API_KEY}')
    if response.ok:
        data = response.json().get('items')
        for x in data:
            snippet = x.get('snippet')
            title = snippet.get('title')
            description = snippet.get('description')
            published_at = snippet.get('publishedAt')
            thumbnails = json.dumps(snippet.get('thumbnails'))
            channel_name = snippet.get('channelTitle')

            new_video = models.Video(
                title=title,
                description=description,
                published_at=published_at,
                thumbnails=thumbnails,
                channel_name=channel_name
            )

            try:
                db.add(new_video)
                db.commit()
                db.refresh(new_video)
            except:
                print("Error Occured in adding Video to DB")
    else:
        print("Error Occured")
        return []
