import requests
import uuid

# Constants
TELEGRAM_API_URL = "https://api.telegram.org/bot6139635960:AAHLm6Zg3sYAVA_3UWwe4RW4wzInZQ_PumE/"
BLIP_API_URL = "https://msging.net/messages"
BLIP_API_KEY = "77d74707a1e5fdb73c828a26d4e2012a36db2dad"

def receive_photo(update):
    photo = update["message"]["photo"][-1]["file_id"]
    photo_url = f"{TELEGRAM_API_URL}getFile?file_id={photo}"
    photo_response = requests.get(photo_url)
    photo_path = photo_response.json()["result"]["file_path"]
    full_photo_url = f"https://api.telegram.org/file/bot6139635960:AAHLm6Zg3sYAVA_3UWwe4RW4wzInZQ_PumE/{photo_path}"

    # Send the photo to the BLiP API
    headers = {
        'Authorization': f'Key {BLIP_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "id": str(uuid.uuid4()),
        "to": "postmaster@msging.net",
        "method": "post",
        "uri": "/buckets/your_blip_bucket_id/collections/your_blip_collection_id/documents",
        "type": "application/json",
        "body": {
            "url": full_photo_url
        }
    }
    response = requests.post(BLIP_API_URL, headers=headers, json=data)
    description = response.json()["body"]["description"]

    # Send the description back to the user
    chat_id = update["message"]["chat"]["id"]
    send_message_url = f"{TELEGRAM_API_URL}sendMessage?chat_id={chat_id}&text={description}"
    requests.get(send_message_url)
