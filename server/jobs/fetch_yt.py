import json
import requests
import datetime
import random

from sqlalchemy.orm.session import Session

from env import API_KEYS
from models import models

keys = {k: v for (k, v) in zip(API_KEYS, [True]*len(API_KEYS))}
time_delta_mult = 1


def get_valid_api_key():
    active_keys = [k for (k, v) in keys.items() if v]
    if not active_keys:
        message = "No Valid API key available"
        print(message)
        raise Exception(message)
    return random.choice(active_keys)


def make_request(api_key):
    API_URL = 'https://youtube.googleapis.com/youtube/v3/search'
    published_after = datetime.datetime.now(
        datetime.timezone.utc) - datetime.timedelta(seconds=60*time_delta_mult)
    published_after_iso = published_after.isoformat().replace('+00:00', 'Z')
    query = "football"
    response = requests.get(
        f'{API_URL}?part=snippet&maxResults=500&order=date&publishedAfter={published_after_iso}&q={query}&type=video&key={api_key}')
    return response


def add_to_db(response, db: Session):
    data = response.json().get('items')
    print(
        f"Found: {response.json().get('pageInfo').get('resultsPerPage')} video(s)")
    for x in data:
        video_id = x.get("id").get("videoId")
        snippet = x.get('snippet')
        title = snippet.get('title')
        description = snippet.get('description')
        published_at = snippet.get('publishedAt')
        thumbnails = json.dumps(snippet.get('thumbnails'))
        channel_name = snippet.get('channelTitle')

        new_video = models.Video(
            video_id=video_id,
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


def req_yt_api(db: Session):
    api_key = get_valid_api_key()
    response = make_request(api_key)
    if response.ok:
        add_to_db(response, db)

    elif response.status_code == 403:
        print(
            f"API Key - {api_key[:4]}...{api_key[-4:]} : Quota Exceeded, Trying Different Key")
        keys[api_key] = False
        api_key = get_valid_api_key()
        response = make_request(api_key)
        if response.ok:
            add_to_db(response, db)

    else:
        print("Error Occured")
        print(response.json())
        return []
