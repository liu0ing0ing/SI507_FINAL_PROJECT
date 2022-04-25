import json

f = open("tree_json.json", "r")
print(json.loads(f.read()))
