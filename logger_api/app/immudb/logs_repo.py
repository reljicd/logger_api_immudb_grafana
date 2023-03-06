from dataclasses import asdict
from typing import List, Tuple

from app.immudb.database import immu_db
from app.immudb.models import Log


class LogsRepo(object):

    @staticmethod
    def insert_one(log: Log) -> int:
        insert_sql = ("INSERT INTO logs (user, device, app, log) "
                      "VALUES (@user, @device, @app, @log);")
        response = immu_db.sqlExec(insert_sql, asdict(log))
        return response.txs[0].header.id

    @staticmethod
    def insert_batch(logs: List[Log]) -> None:
        values = ', '.join([f"('{log.user}', '{log.device}', "
                            f"'{log.app}', '{log.log}')" for log in logs])
        insert_sql = ("INSERT INTO logs (user, device, app, log) "
                      f"VALUES {values};")
        response = immu_db.sqlExec(insert_sql)
        return response.txs[0].header.id

    @staticmethod
    def select_all(offset: int = 0, limit: int = 0) -> List[Log]:
        pass

    @staticmethod
    def select_last_n(n: int) -> List[Log]:
        pass

    @staticmethod
    def select_bucket(user: str, device: str = None, app: str = None,
                      offset: int = 0, limit: int = 0) -> List[Log]:
        pass

    @staticmethod
    def count() -> int:
        count_sql = 'SELECT COUNT(*) FROM logs;'
        return immu_db.sqlQuery(count_sql)[0][0]

    @staticmethod
    def verified_select_one(log_id: int) -> Tuple[Log, bool]:
        pass
