import json
import os

def write_json_to_file(fileName,tJson):
    if os.path.isfile(fileName) is False:
        with open(fileName, mode='w') as f:
            json.dump([], f)
    with open(fileName, "w") as outfile:
        json.dump(tJson, outfile)



def append_json_to_file(fileName,tJson):
    if os.path.isfile(fileName) is False:
        with open(fileName, mode='w') as f:
            json.dump([], f)

    with open(fileName, mode='r') as feedsjson:
        feeds = json.load(feedsjson)

    with open(fileName, "w") as outfile:
        feeds.append(tJson)
        json.dump(feeds, outfile)

def remove_movement(movement):
    fileName = "Movement.json"
    if os.path.isfile(fileName) is False:
        return

    obj  = json.load(open(fileName))
    for i in xrange(len(obj)):
        if obj[i]["MovementName"] == movement:
            obj.pop(i)
            break
    write_json_to_file(fileName, obj)

