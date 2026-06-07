import json
import os
with open("vulnerabilities.json") as file:
    data = json.load(file)
print(data["Apache"])
