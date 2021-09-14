import json


_status_map = {
    0: "Offline",
    1: "Online",
    2: "Starting",
    3: "Stopping",
    4: "Restarting",
    5: "Saving",
    6: "Loading",
    7: "Crashed",
    8: "Pending",
    10: "Preparing",
}


class List(list):
    """ Custom List Class to beautify output """
    __slots__ = []

    def __str__(self) -> None:
        return ExarotonType.__str__(self)

    def __repr__(self) -> None:
        return (
            f"exaroton.types.List([{','.join(ExarotonType.__repr__(i) for i in self)}])"
        )


class ExarotonType:
    def __init__(self) -> None:
        pass

    @staticmethod
    def default(obj: "ExarotonType"):
        if isinstance(obj, bytes):
            return repr(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: getattr(obj, attr)
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            },
        }

    def __str__(self) -> str:
        return json.dumps(self, indent=4, default=ExarotonType.default)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__dict__}>"


class Account(ExarotonType):
    name: str
    email: str
    verified: bool
    credits: int

    def __init__(self, name: str, email: str, verified: bool, credits: int) -> None:
        self.name = name
        self.email = email
        self.verified = verified
        self.credits = credits


class Server(ExarotonType):
    id: str
    name: str
    address: str
    motd: str
    status: str
    host: str
    port: int
    players: object
    software: object
    shared: bool

    def __init__(
        self,
        id: str,
        name: str,
        address: str,
        motd: str,
        status: str,
        host: str,
        port: int,
        players: "Players",
        software: "Software",
        shared: bool,
    ) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.motd = motd
        self.status = _status_map.get(status)
        self.host = host
        self.port = port
        self.players = Players(**players)
        self.software = Software(**software)
        self.shared = shared


class Software(ExarotonType):
    id: str
    name: str
    version: str

    def __init__(self, id: str, name: str, version: str) -> None:
        self.id = id
        self.name = name
        self.version = version


class Players(ExarotonType):
    max: int
    count: int
    list: list

    def __init__(self, max: int, count: int, list: list) -> None:
        self.max = max
        self.count = count
        self.list = list


class Logs(ExarotonType):
    id: str
    url: str
    raw: str

    def __init__(self, id: str, url: str, raw: str) -> None:
        self.id = id
        self.url = url
        self.raw = raw
