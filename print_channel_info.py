import os
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
api_call = slack_client.api_call('channels.list')
channels = api_call.get('channels')

def print_channel_names_and_ids():
    for channel in channels:
        #print channel.get('name') + ' ' + channel.get('id')
        print channel.get('name') + ' ' + channel.get('id')

