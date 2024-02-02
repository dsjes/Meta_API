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
        # 不立即發佈貼文，需要設定貼文發佈時間，時間落在傳送 API 要求時間起 10 分鐘至 30 天
        data["published"] = "false"
        data["scheduled_publish_time"] = scheduled_publish_time  # 格式為整數 UNIX 時間戳記
    else:
        data["published"] = "true"
    return json.dumps(data)


def send_post(data: dict, page_id: str) -> dict:
    """
    成功的 output 如下:
    {'id': '100448962975781_326324867049401'}
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
    成功的 output 如下:
    {'id': '100448962975781_324363867245501', 'message': '測試貼文', 'created_time': '2024-01-19T06:18:35+0000'}
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
    成功的 output 如下:
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


if __name__ == "__main__":
    # ---- post
    # data = post_data(
    #     post_content="2024/1/23 9.01發文",
    #     post_time="immediate",
    #     access_token=os.getenv("ACCESS_TOKEN"),
    #     scheduled_publish_time=None,
    #     post_url=None,
    # )
    # result = send_post(data=data, page_id=os.getenv("PAGE_ID"))
    # print(result)

    # ---- verify
    # result = verify_post(
    #     version="v18.0",
    #     page_post_id="100448962975781_326793533669201",
    #     access_token=os.getenv("ACCESS_TOKEN"),
    # )
    # print(result)

    # ---- update
    # result = update_post(
    #     version="v18.0",
    #     page_post_id="100448962975781_326793533669201",
    #     access_token=os.getenv("ACCESS_TOKEN"),
    #     new_message="2024/1/23 9.01發文 -> 10.34",
    # )
    # print(result)

    # ---- delete
    result = delete_post(
        version="v18.0",
        page_post_id="100448962975781_326793533669201",
        access_token=os.getenv("ACCESS_TOKEN"),
    )
    print(result)
