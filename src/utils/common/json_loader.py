import json

def load_json(fpath: str):
    if not fpath.exists():
        return []

    with open(fpath, encoding="utf-8") as f:
        return json.load(f)

def load_json_as_dict(fpath: str):
    if not fpath.exists():
        return {}
    
    with open(fpath, encoding="utf-8") as f:
        json_list = json.load(f)
        json_dict = {}
        for item in json_list:
            json_dict[item.id] = item
        
        return json_dict