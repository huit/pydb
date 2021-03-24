#!/usr/bin/env python3
import cx_Oracle
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

from pylog.pylog import get_common_logger_for_module


class SqlAlchemyOracleDB:
    """
    Module for interacting with an Oracle DB via SQL Alchemy
    """
    def __init__(self, host: str, port: int, service: str, user: str, pwd: str, 
                 logging_level: int = 50, logging_format: logging.Formatter = None):
        """
        initialize object with values required to create a connection to an Oracle DB
        :param host:
        :param port:
        :param service:
        :param user:
        :param pwd:
        :param logging_level:
        :param logging_format:
        """
        self.logger = get_common_logger_for_module(module_name=__name__, level=logging_level, log_format=logging_format)
        self.host = host
        self.port = port
        self.service = service
        self.user = user
        self.pwd = pwd
        self.engine = self.setup_engine()

    def setup_engine(self):
        """
        Create a SQL Alchemy engine to connect to Oracle DB with a connection pool
        :return:
        """
        try:
            dsn_str = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)
            pool = cx_Oracle.SessionPool(
                user=self.user, password=self.pwd, dsn=dsn_str,
                min=2, max=5, increment=1, threaded=True
            )
            engine = create_engine("oracle://",
                                   creator=pool.acquire,
                                   poolclass=NullPool,
                                   echo=True,
                                   max_identifier_length=128)

            self.logger.info("Setup sqlalchemy engine successfully")
            return engine
        except Exception as err:
            obj, = err.args
            self.logger.critical("Cannot create sql alchemy engine")
            self.logger.error("Context: %s", obj.context)
            self.logger.error("Message: %s", obj.message)
            raise Exception(f"Cannot create sql alchemy engine: {obj.message}")

    def get_engine(self):
        if self.engine is None:
            self.engine = self.setup_engine()
        return self.engine

    def get_session(self):
        """
        Specific to SQL Alchemy; allows interaction with SQL Alchemy entities
        :return:
        """
        Session = sessionmaker(bind=self.get_engine())
        return Session()

    def create_connection(self):
        """
        provides a connection to the db host for more 'direct' access
        :return:
        """
        return self.get_engine().connect()

    def health_check(self):
        """
        Performs a basic query against the db to ensure connectivity
        """
        with self.create_connection() as conn:
            return conn.scalar("select 1 from dual")

    def execute_query(self, query_string: str, args: dict = None) -> list:
        """
        executes a sql query, return a list of dictionaries representing rows

        :param query_string: str
        :param args: dict
        :return: list of dict
        """
        with self.create_connection() as conn:
            statement = text(query_string)

            if args is not None and len(args.keys()) > 0:
                query_result = conn.execute(statement, args).fetchall()
            else:
                query_result = conn.execute(statement).fetchall()

            return [dict(row) for row in query_result]

    def execute_update(self, query_string: str, args: dict):
        """
        used to execute an insert, update, or delete sql statement

        :param query_string: str
        :param args: dict
        :return:
        """
        with self.create_connection() as conn:
            statement = text(query_string)
            trans = conn.begin()
            if args is not None and len(args.keys()) > 0:
                conn.execute(statement, args)
            else:
                conn.execute(statement)
            trans.commit()

    def cleanup(self):
        """
        release any existing connections; to be called prior to exiting program
        :return:
        """
        if self.engine is not None:
            self.logger.info("sql alchemy engine found")
            try:
                self.engine.dispose()
            except Exception as err:
                obj, = err.args
                self.logger.critical("Cannot dispose sql alchemy engine")
                self.logger.error("Context: %s", obj.context)
                self.logger.error("Message: %s", obj.message)
