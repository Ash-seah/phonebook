import requests

url = "http://localhost:8000/"
data = {
    "name": "John Doe",
    "number": "1234567890",
    "email": "john.doe@example.com"
}

response = requests.put(url, json=data)

if response.status_code == 200:
    print("Record added successfully")
else:
    print(f"Failed to add record: {response.status_code} - {response.text}")