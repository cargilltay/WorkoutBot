import os
import time
import json_utils
import json
import ConfigParser
import datetime
from workoutbot.custom.json.commands import *
from movement import Movement
from workout_user import WorkoutUser
from workout import Workout
from slackclient import SlackClient
import scheduler 

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
#with open("memory.json", "w") as outfile:
    #json.dump({'numbers':2, 'strings':'test', 'x':'x', 'y':'y'}, outfile)

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
    with open('settings.cfg', 'wb') as configfile:
        config.write(configfile)

def get_command_value(word_list, keyword):
    return word_list[word_list.index(keyword) + 1]

def obtain_time(word_list, command_type):
    
    #print word_list.index(command_type)
    whole_input = word_list[word_list.index(command_type) + 1:]
    pm_am = whole_input[1].upper()
    time = whole_input[0].split(':')

    try:
        hours = int(time[0])
        minutes = int(time[1])
        if hours > 12 or hours <= 0 or minutes > 60 or minutes < 0:
            return 'Please valid hours and minutes.'
    except ValueError:
        return 'Invalid time format... Use: "hr:min am"'
                

    if pm_am != 'PM' and pm_am != 'AM':
        return  'Specify "am" or "pm" after your time entry.'
        
    #scheduler.        
    set_setting(command_type, whole_input)
    return 'Setting %s' % command_type

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean." + print_commands();
    command = command['text']
    list_of_words = command.split()

    #move all to json file
    time_commands = ['minminutes','maxminutes','starttime','endtime']
    workout_commands = ['add', 'remove','view']

    #stats needs own sub-object for view
    view_commands = ['settings','workouts','stats']
    stats = ['month','week','datetimeformat','default']


    if '/set' in command:
        command_value = get_command_value(list_of_words, "/set")
        if command_value in commands['time']:
            time = obtain_time(list_of_words, command_value)
            response = time
    elif '/view' in command:
        if 'settings' in command:
            response = get_settings_string()
        elif 'workouts' in command:
            response = json_utils.get_movements_string()
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
            newMov = Movement(get_command_value(list_of_words, "add"))
            json_utils.append_json_to_file("Movement.json", newMov.t_json)
            response = 'adding ...'
        elif 'remove' in command:
            json_utils.remove_movement(get_command_value(list_of_words, "remove"))
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
        #Going to have to use threading not this:
        #scheduler.update_member_list()
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
