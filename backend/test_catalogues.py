import urllib.request
import json

try:
    req = urllib.request.Request("http://localhost:5000/api/catalogues")
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print(e)
