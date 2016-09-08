class WorkoutUser:
    WorkoutID = ""
    SlackUserID = ""
    Reaction = ""
    DateTimeStamp = ""
    t_json = {"WorkoutID": WorkoutID, "SlackUserID": SlackUserID, "Reaction": Reaction, "DateTimeStamp": DateTimeStamp}

    def __init__(self, SlackUserID):
        self.SlackUserID = SlackUserID
