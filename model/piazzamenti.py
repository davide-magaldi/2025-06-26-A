class Piazzamento:
    driverId:int
    position:int

    def __init__(self, driverId, position):
        self.driverId=driverId
        self.position=position

    def __hash__(self):
        return hash(self.driverId)

    def __eq__(self, other):
        return self.driverId == other.driverId
