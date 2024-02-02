import requests
from json import JSONDecodeError
import os
from dotenv import load_dotenv
import json

load_dotenv()


def get_user_id_conversion_id(
    version: str, page_id: str, access_token: str, message=False
) -> dict:
    """
    用來取得用戶 id 與 對話 id
    """
    messages_info = "messages{id,message}"
    url = f"https://graph.facebook.com/{version}/{page_id}/conversations?fields=participants,{messages_info}&access_token={access_token}"
    try:
        response = requests.get(url)
        response_message = response.json()
        user_id = response_message["data"][0]["participants"]["data"][0]["id"]
        conversion_id = response_message["data"][0]["id"]
        return {"user_id": user_id, "conversion_id": conversion_id}

    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}


def message_data(user_id: str, message: str) -> dict:
    data = {"recipient": {"id": user_id}, "message": {"text": message}}
    return json.dumps(data)


def send_message(user_id: str, message: str, access_token) -> dict:
    """
    成功的 output 如下:
    {
    "recipient_id": "24522651050715780",
    "message_id": "m_vkWuL501BoHy0IFig1imW2kI-ix8Dj7nvFNlk8rZGBxTl-Pt1vDysfvWbNvR0fJ3tjBaUy1HA4zpqjUbcrpuVg"
    }
    """
    url = f"https://graph.facebook.com/v2.6/me/messages?access_token={access_token}"
    headers = {"Content-Type": "application/json"}
    data = message_data(user_id=user_id, message=message)
    try:
        response = requests.post(url, data=data, headers=headers)
        response_message = response.json()
        return response_message
    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}


def get_all_messages_info(version: str, conversion_id: str, access_token: str) -> dict:
    url = f"https://graph.facebook.com/{version}/{conversion_id}?fields=messages&access_token={access_token}"
    try:
        response = requests.get(url)
        response_message = response.json()
        return response_message
    except JSONDecodeError:
        return {"error": "Response could not be serialized"}
    except Exception as e:
        return {"error": e}


if __name__ == "__main__":
    result = get_user_id_conversion_id(
        version="v18.0",
        page_id="100448962975781",
        access_token=os.getenv("ACCESS_TOKEN"),
    )

    if "error" not in result.keys():
        # result = get_all_messages_info(
        #     version="v18.0",
        #     conversion_id=result["conversion_id"],
        #     access_token=os.getenv("ACCESS_TOKEN"),
        # )

        # result = send_message(
        #     user_id=result["user_id"],
        #     message="寫詩嗎?",
        #     access_token=os.getenv("ACCESS_TOKEN"),
        # )

        print(result)
