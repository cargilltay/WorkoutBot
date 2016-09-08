class Movement:
    MovementID = ""
    MovementName = ""
    t_json = ""

    def __init__(self, MovementName):
        self.MovementName = MovementName
        self.t_json = {"MovementID": self.MovementID, "MovementName": self.MovementName}
