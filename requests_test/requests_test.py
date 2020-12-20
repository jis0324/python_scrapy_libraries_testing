import os
import requests

base_dir = os.path.dirname(os.path.abspath(__file__))
response = requests.get("https://www.bcmitsubishiofsaltillo.com/new-vehicles/")

print(response)

with open("{}/requests_test.txt".format(base_dir), "w", encoding="utf-8") as ff:
    ff.write(response.text)