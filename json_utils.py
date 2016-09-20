import json
import os
from slackclient import SlackClient

#constants
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def write_json_to_file(fileName,tJson):
    fileName = fileName
    if os.path.isfile(fileName) is False:
        with open(fileName, mode='w') as f:
            json.dump([], f)
    with open(fileName, 'w') as outfile:
        json.dump(tJson, outfile)

def append_json_to_file(fileName,tJson):
    fileName = fileName
    if os.path.isfile(fileName) is False:
        with open(fileName, mode='w') as f:
            json.dump([], f)

    with open(fileName, mode='r') as feedsjson:
        feeds = json.load(feedsjson)

    with open(fileName, 'w') as outfile:
        feeds.append(tJson)
        json.dump(feeds, outfile)

def remove_movement(movement):
    fileName = 'movement.json'
    movement = movement.lower()
    if os.path.isfile(fileName) is False:
        return

    obj  = json.load(open(fileName))
    for i in xrange(len(obj)):
        if obj[i]['MovementName'].lower() == movement:
            obj.pop(i)
            break
    write_json_to_file(fileName, obj)

def get_command_string():
    fileName = 'commands.json'
    err_mov = 'Commands file error. See commands.json'

    if os.path.isfile(fileName) is False:
        return err_mov

    counter = 0
    s_string = 'Here are your available commands:\n'
    obj  = json.load(open(fileName))

    if not obj:
        return err_mov

    for i in xrange(len(obj)):
        for cmd in obj[i]:
            s_string += (cmd + '\n')
            for scmd in obj[i][cmd]:
                s_string += ('\t' + scmd + '\n')

    return s_string


def get_movements_string():
    fileName = 'movement.json'
    err_mov = 'No Workout Movements'

    if os.path.isfile(fileName) is False:
        return err_mov

    counter = 0
    s_string = 'Here are your workouts:\n'
    obj  = json.load(open(fileName))

    if not obj:
        return err_mov

    for i in xrange(len(obj)):
        counter += 1
        s_string += (str(counter) + ': ' + obj[i]['MovementName'] + '\n')

    return s_string

def update_channel_members(channel_name):
    fileName = 'members.json'

    #get channels
    api_call = slack_client.api_call('channels.list')
    channels = api_call.get('channels')

    #get all users
    api_call = slack_client.api_call('users.list')
    users = api_call.get('members')

    #get channel members id
    member_IDs = ''
    for channel in channels:
        if channel.get('name') == channel_name:
            member_IDs = channel.get('members')
            
    #add names and id to json
    names = []
    for ID in member_IDs:
        for user in users:
            userID = user.get('id')
            if userID == ID:
                name_ID_pair = {'name': user.get('name'), 'id': userID}
                names.append(name_ID_pair)

    #check existing members json
    if os.path.isfile(fileName) is False:
        with open(fileName, mode='w') as f:
            json.dump([], f)

    obj = json.load(open(fileName))

    for i in xrange(len(obj)):
        is_old = False
        for j in xrange(len(names)):
            if (obj[i]['id']).lower() == (names[j]['id']).lower():
                is_old = True
                names.pop(j)
                break
        if is_old is False:
            print i 
            obj.pop(i)
    
    if names:
        for name in names:
            obj.append(name)
            slack_client.api_call("chat.postMessage", channel=channel_name,
                                  text="Welcome to quick-workout " + name['name'], as_user=True)
            
    write_json_to_file(fileName, obj)


    print obj


