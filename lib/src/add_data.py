import requests

names = [
    "Max",
    "Jayden",
    "Tim",
    "Marcus",
    "Eddie",
    "Chelsea",
    "Chi",
    "Andrew",
    "Steve",
    "Sam",
]
url = "https://iasrapy4gj.execute-api.ap-southeast-2.amazonaws.com/createtask"
for i in range(10):
    payload = {"phoneNumber": "+61478613323", "patientName": names[i]}
    requests.request("POST", url, json=payload)
