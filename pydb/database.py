import abc

from enum import Enum


class Database(Enum):
    """
    not implemented: other databases
    """
    ORACLE = "oracle"


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
                callable(subclass.cleanup))

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
