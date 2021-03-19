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
        def execute_query(self, query_string: str, args=None) -> dict:
            raise NotImplementedError

        @abc.abstractmethod
        def execute_update(self, query_string, args=None):
            raise NotImplementedError

        @abc.abstractmethod
        def health_check():
            raise NotImplementedError

        @abc.abstractmethod
        def cleanup():
            raise NotImplementedError

        @abc.abstractmethod
        def create_connection():
            raise NotImplementedError

        @abc.abstractmethod
        def get_session():
            raise NotImplementedError
