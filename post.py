import requests
import time
from datetime import datetime
from json import JSONDecodeError
import os
from dotenv import load_dotenv
import json

load_dotenv()


def convert_datetime_to_unix_timestamp(datetime_value):
    return time.mktime(datetime_value.timetuple())


def post_data(
    post_content: str,
    post_time: str,
    access_token: str,
    scheduled_publish_time: datetime = None,
    post_url: str = None,
) -> dict:
    data = {"message": post_content, "access_token": access_token}
    if post_url:
        data["url"] = post_url
    if post_time != "immediate":
        data["published"] = "false"
        data["scheduled_publish_time"] = scheduled_publish_time  # UNIX timestamp
    else:
        data["published"] = "true"
    return json.dumps(data)


def send_post(data: dict, page_id: str) -> dict:
    """
    successfull output would be like this:
    {'id': 'pageid_postid'}
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=data, headers=headers)
        response_message = response.json()
        return response_message
    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}


def verify_post(version: str, page_post_id: str, access_token: str) -> dict:
    """
    successfull output would be like this:
    {'id': '100448962975781_324363867245501', 'message': 'content', 'created_time': '2024-01-19T06:18:35+0000'}
    """
    url = f"https://graph.facebook.com/{version}/{page_post_id}?fields=id,message,created_time&access_token={access_token}"
    try:
        response = requests.get(url)
        response_message = response.json()
        return response_message
    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}


def update_post(
    version: str, page_post_id: str, access_token: str, new_message: str
) -> dict:
    """
    successfull output would be like this:
    {
    "success": true
    }
    """
    headers = {"Content-Type": "application/json"}
    url = f"https://graph.facebook.com/{version}/{page_post_id}"
    data = {"message": new_message, "access_token": access_token}
    try:
        response = requests.post(url, headers=headers, data=data)
        response_message = response.json()
        return response_message
    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}


def delete_post(version: str, page_post_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/{version}/{page_post_id}?access_token={access_token}"
    try:
        response = requests.delete(url)
        response_message = response.json()
        return response_message
    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}
