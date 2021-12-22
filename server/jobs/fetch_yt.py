import json
import requests
import datetime
import random

from sqlalchemy.orm.session import Session

from env import API_KEYS
from models import models

# store api-keys in dictionaries with bool value True
# this bool value is used to indicate if api key can request or not in case of quota limit exceed
keys = {k: v for (k, v) in zip(API_KEYS, [True]*len(API_KEYS))}


def get_valid_api_key():
    # get active api-keys from the available keys
    active_keys = [k for (k, v) in keys.items() if v]
    if not active_keys:
        message = "No Valid API key available"
        print(message)
        raise Exception(message)
    return random.choice(active_keys)


def make_request(api_key):
    API_URL = 'https://youtube.googleapis.com/youtube/v3/search'
    # set published time to get latest videos published within a minute
    published_after = datetime.datetime.now(
        datetime.timezone.utc) - datetime.timedelta(seconds=60)
    # convert time to RFC 3339 format supported by the api
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
        # converting json date-time to python date-time
        published_at = datetime.datetime.strptime(
            snippet.get('publishedAt'), '%Y-%m-%dT%H:%M:%SZ')
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
