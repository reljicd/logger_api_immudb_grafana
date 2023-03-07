from typing import List, Tuple

from immudb.datatypesv2 import PrimaryKeyIntValue

from app.immudb.database import immu_db
from app.immudb.models import Log


class LogsRepo(object):

    @staticmethod
    def _log_to_values(log: Log) -> str:
        return (f"('{log.user}', '{log.device}', "
                f"'{log.app}', '{log.log}')")

    @classmethod
    def _logs_to_values(cls, logs: List[Log]) -> str:
        return ', '.join([cls._log_to_values(log) for log in logs])

    @staticmethod
    def _insert_into_logs_values(values: str) -> int:
        insert_sql = ("INSERT INTO logs (user, device, app, log) "
                      f"VALUES {values};")
        response = immu_db.sqlExec(insert_sql)
        return response.txs[0].lastInsertedPKs['logs'].n

    @classmethod
    def insert_one(cls, log: Log) -> int:
        return cls._insert_into_logs_values(cls._log_to_values(log))

    @classmethod
    def insert_batch(cls, logs: List[Log]) -> int:
        return cls._insert_into_logs_values(cls._logs_to_values(logs))

    @staticmethod
    def _result_to_log(result) -> Log:
        _, user, device, app, log = result
        return Log(user, device, app, log)

    @classmethod
    def _results_to_logs(cls, results) -> List[Log]:
        return [cls._result_to_log(result) for result in results]

    @classmethod
    def _sql_query_to_logs(cls, sql: str) -> List[Log]:
        results = immu_db.sqlQuery(sql)
        return cls._results_to_logs(results)

    @classmethod
    def select_one(cls, log_id: int) -> Log:
        select_query = f"SELECT * FROM logs WHERE id={log_id};"
        return cls._sql_query_to_logs(select_query)[0]

    @classmethod
    def select_all(cls, offset: int = 0, limit: int = 10) -> List[Log]:
        select_query = f"SELECT * FROM logs LIMIT {limit} OFFSET {offset};"
        return cls._sql_query_to_logs(select_query)

    @classmethod
    def select_last_n(cls, n: int) -> List[Log]:
        select_query = f"SELECT * FROM logs ORDER BY id DESC LIMIT {n};"
        return cls._sql_query_to_logs(select_query)

    @classmethod
    def select_bucket(cls, user: str, device: str = None, app: str = None,
                      offset: int = 0, limit: int = 10) -> List[Log]:
        where_device_sql = f" AND device='{device}'" if device else ""
        where_app_sql = f" AND app='{app}'" if app else ""

        select_query = (f"SELECT * FROM logs WHERE user='{user}'"
                        + where_device_sql
                        + where_app_sql
                        + f" LIMIT {limit} OFFSET {offset};")
        return cls._sql_query_to_logs(select_query)

    @staticmethod
    def count() -> int:
        count_sql = 'SELECT COUNT(*) FROM logs;'
        return immu_db.sqlQuery(count_sql)[0][0]

    @classmethod
    def verified_select_one(cls, log_id: int) -> Tuple[Log, bool]:
        verified_result = immu_db.verifiableSQLGet(
            table='logs',
            primaryKeys=[PrimaryKeyIntValue(log_id)])
        return cls.select_one(log_id), verified_result.verified
