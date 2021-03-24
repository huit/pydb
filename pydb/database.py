import abc

from enum import Enum


class DatabaseType(Enum):
    """
    not implemented: other databases
    """
    ORACLE = "oracle"
    SQL_ALCHEMY_ORACLE = "sql_alchemy_oracle"


class DBInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'execute_query') and
                callable(subclass.execute_query) and
                hasattr(subclass, 'execute_update') and
                callable(subclass.execute_update) and
                hasattr(subclass, 'health_check') and
                callable(subclass.health_check) and
                hasattr(subclass, 'cleanup') and
                callable(subclass.cleanup) and
                hasattr(subclass, 'create_connection') and
                callable(subclass.create_connection) and
                hasattr(subclass, 'get_session') and
                callable(subclass.get_session)
                or NotImplemented)

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
