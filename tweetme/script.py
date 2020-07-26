import requests
import json
primary_URL = "http://127.0.0.1:8000/api/create/"
postData = {
    "content": "Content created from post"
}
check = requests.post(primary_URL,
                      data=postData)

print(check.text)
