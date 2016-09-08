import os
import time
import json_utils
import json
import ConfigParser
import datetime
from movement import Movement
from workout_user import WorkoutUser
from workout import Workout
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# set config
config = ConfigParser.ConfigParser()
config.readfp(open('settings.cfg'))


# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# write to json file
with open("memory.json", "w") as outfile:
    json.dump({'numbers':2, 'strings':'test', 'x':'x', 'y':'y'}, outfile)

def print_commands():
    return ("\n/set \n" 
    "\tminminutes\n"  
    "\tmaxminutes\n"  
    "\tstarttime\n" 
    "\tendtime\n" 
    "/view \n" 
    "\tsettings\n"  
    "\tworkouts\n" 
    "\tstats\n" 
    "\t\tmonth\n"  
    "\t\tweek\n" 
    "\t\tdatetimeformat\n"  
    "/workouts \n" 
    "\tadd\n" 
    "\tremove\n" 
    "\tview") 

def get_settings_string():
    s_string = ''
    for each_section in config.sections():
        for (each_key, each_val) in config.items(each_section):
            s_string += (each_key + ' = ')
            s_string += (each_val + '\n')
    return s_string

def set_setting(setting, value):
    config.set('Settings',setting, value)

def set_config():
    with open('settings.cfg', 'wb') as configfile:
        config.write(configfile)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean." + print_commands();
    print command
    command = command['text']
    list_of_words = command.split()

    if '/set' in command:
        if 'minminutes' in command:
            minminutes = list_of_words[list_of_words.index("minminutes") + 1]
            set_setting('minminutes', minminutes)
            response = 'setting min minutes'
        if 'maxminutes' in command:
            maxminutes = list_of_words[list_of_words.index("maxminutes") + 1]
            set_setting('maxminutes', maxminutes)
            response = 'setting max minutes'
        elif 'starttime' in command:
            starttime = list_of_words[list_of_words.index("starttime") + 1]
            set_setting('starttime', starttime)
            response = 'setting start time'
        elif 'endtime' in command:
            endtime = list_of_words[list_of_words.index("endtime") + 1]
            set_setting('endtime', endtime)
            response = 'setting end time'
        set_config()
    elif '/view' in command:
        if 'settings' in command:
            response = get_settings_string()
        elif 'workouts' in command:
            response = 'all available workouts'
        elif 'stats' in command:
            if 'month' in command:
                response = 'aggregate of current month'
            elif 'week' in command:
                response = 'aggregate of current week'
            elif 'datetimeformat' in command:
                response = 'specific date'
            else:
                response = 'all user stats'
    elif '/workouts'in command:
        if 'add' in command:
            movement = list_of_words[list_of_words.index("add") + 1]
            newMov = Movement(movement)
            json_utils.append_json_to_file("Movement.json", newMov.t_json)
            response = 'adding ...'
        elif 'remove' in command:
            movement = list_of_words[list_of_words.index("remove") + 1]
            json_utils.remove_movement(movement)
            response = 'removing ...'
        elif 'view' in command:
            response = json_utils.get_movements_string()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output:
                if 'text' in output:
                    if AT_BOT in output['text']:
                        # return text after the @ mention, whitespace removed
                        return output,output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
