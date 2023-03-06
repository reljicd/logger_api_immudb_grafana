from dataclasses import dataclass


@dataclass
class Log:
    user: str
    device: str
    app: str
    log: str
