import sqlite3

from models.score import Score

INSERT_SCORE = """
INSERT INTO scores (score)
VALUES (?)
RETURNING id;
"""

SELECT_SCORES = """
SELECT id,
       score,
       date_create
FROM scores
ORDER BY score DESC
LIMIT 3;
"""


class Store:
    db = None

    def __new__(cls, *args, **kwargs):
        if cls.db is None:
            cls.db = super().__new__(cls)
        return cls.db

    def __init__(self, path_db: str):
        self._connect = sqlite3.connect(path_db)
        self._connect.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with open("./store/init_db.sql") as sql_script:
            self._connect.executescript(sql_script.read())

    def add_score(self, score: Score) -> int:
        try:
            with self._connect:
                cur = self._connect.execute(INSERT_SCORE, score.insert_placeholder())
                data: sqlite3.Row = cur.fetchone()
                if data is None:
                    return 0
                return data[0]
        except sqlite3.Error as err:
            print(err)
            return 0

    def get_scores(self) -> list[Score]:
        scores_lst: list[Score] = list()

        try:
            with self._connect:
                cur = self._connect.execute(SELECT_SCORES)
                for item in cur:
                    score = Score()
                    score.select_placeholder(*item)
                    scores_lst.append(score)
        except sqlite3.Error as err:
            print(err)
        return scores_lst

    def __del__(self):
        self._connect.close()
