import abc

from enum import Enum


class DatabaseType(Enum):
    """
    not implemented: other databases
    """
    ORACLE = "oracle"
    SQL_ALCHEMY_ORACLE = "sql_alchemy_oracle"


class DBInterface(metaclass=abc.ABCMeta):

        @abc.abstractmethod
        def execute_query(self, query_string: str, args=None) -> list:
            """
            executes a sql query, return a list of dictionaries representing rows
            :param self:
            :param query_string:
            :param args:
            :return:
            """
            raise NotImplementedError

        @abc.abstractmethod
        def execute_update(self, query_string, args=None):
            """
            used to execute an insert, update, or delete sql statement
            :param self:
            :param query_string:
            :param args:
            :return:
            """
            raise NotImplementedError

        @abc.abstractmethod
        def health_check():
            """
            Performs a basic query against the db to ensure connectivity
            :return:
            """
            raise NotImplementedError

        @abc.abstractmethod
        def cleanup():
            """
            Attempts to release any 'live' objects/connections to the host
            :return:
            """
            raise NotImplementedError

        @abc.abstractmethod
        def create_connection():
            """
            provides a connection to the db host for more 'direct' access
            :return:
            """
            raise NotImplementedError

        @abc.abstractmethod
        def get_session():
            """
            Specific to SQL Alchemy; allows interaction with SQL Alchemy entities
            :return:
            """
            raise NotImplementedError
