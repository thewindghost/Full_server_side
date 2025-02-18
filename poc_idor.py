import requests

base_url = "http://192.168.1.164:4100/admin-panel-131315315211"

max_value = 100

for n in range(1, max_value + 1):
    paramenter = {'id': n}
    response = requests.get(base_url, params=paramenter)

    if response.status_code == 200:
        print(f"Here Information can get!: {n} ", response.text)
    else:
        print(f"Have't Information!")