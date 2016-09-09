import sched
import time
from json_utils import update_channel_members 

#constants
s = sched.scheduler(time.time, time.sleep)

def update_member_list():
    s.enter(5, 1, update_channel_members, argument=('quick-workout',)) 
    s.enter(5, 1, update_member_list, argument=())
    s.run()

