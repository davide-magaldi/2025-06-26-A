class Circuito:
    circuitId:int
    circuitRef:str
    name:str
    location:str
    country:str
    lat:float
    lng:float
    alt:int
    url: str
    ris: dict

    def __init__(self, id, ref, n, l, co, lat, lng, alt, url):
        self.circuitId=id
        self.circuitRef=ref
        self.name=n
        self.location=l
        self.country=co
        self.lat=lat
        self.lng=lng
        self.alt=alt
        self.url=url
        self.ris = {}

    def __hash__(self):
        return hash(self.circuitId)

    def __eq__(self, other):
        return self.circuitId == other.circuitId

    def addPiazzamenti(self, k, v):
        self.ris[k] = v

    def __str__(self):
        return f"{self.circuitRef}"
