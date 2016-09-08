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
    movement = movement.lower()
    if os.path.isfile(fileName) is False:
        return

    obj  = json.load(open(fileName))
    for i in xrange(len(obj)):
        if obj[i]["MovementName"].lower() == movement:
            obj.pop(i)
            break
    write_json_to_file(fileName, obj)

def get_movements_string():
    fileName = "Movement.json"
    err_mov = "No Workout Movements"

    if os.path.isfile(fileName) is False:
        return err_mov

    counter = 0
    s_string = 'Here are your workouts:\n'
    obj  = json.load(open(fileName))

    if not obj:
        return err_mov

    for i in xrange(len(obj)):
        counter += 1
        s_string += (str(counter) + ': ' + obj[i]["MovementName"] + '\n')

    return s_string
