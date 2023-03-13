import datetime
from dataclasses import dataclass


@dataclass
class Score:
    id: int = 0
    score: int = 0
    date_create: datetime.datetime = datetime.datetime.now()

    def __str__(self):
        return f"id={self.id}\nscore={self.score}\ndate_create={self.date_create_str()}"

    def __repr__(self):
        return self.__str__()

    def select_placeholder(self, *args) -> bool:
        if len(args) < 3:
            return False

        self.id = args[0]
        self.score = args[1]
        self.date_create = datetime.datetime.fromtimestamp(args[2])

        return True

    def insert_placeholder(self) -> tuple:
        return self.score,

    def date_create_str(self) -> str:
        return self.date_create.strftime("%d-%m-%Y %H:%M")

    def date_create_timestamp(self) -> int:
        return self.date_create.timetuple()

    def score_str(self) -> str:
        return str(self.score)
