import requests

port = 65000
host = 'localhost'

req1 = """{
    "term": "time",
    "nresults": 47
}"""

url = "http://" + host + ":" + str(port) + "/gsearch"
r = requests.post(url, data=req1, headers={'Content-Type': 'application/json'})
print(r.text, r.status_code)
