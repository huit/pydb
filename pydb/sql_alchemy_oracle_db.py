#!/usr/bin/env python3
import cx_Oracle
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker

from pylog.pylog import get_common_logger_for_module


class SqlAlchemyOracleUtil:
    def __init__(self, host: str, port: int, service: str, user: str, pwd: str, 
                 logging_level: int = 50, logging_format: logging.Formatter = None):
        self.logger = get_common_logger_for_module(module_name=__name__, level=logging_level, log_format=logging_format)
        self.host = host
        self.port = port
        self.service = service
        self.user = user
        self.pwd = pwd
        self.engine = self.setup_engine()

    def setup_engine(self):
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
        Session = sessionmaker(bind=self.get_engine())
        return Session()

    def create_connection(self):
        return self.engine.connect()

    def health_check(self):
        with self.create_connection() as conn:
            return conn.scalar("select 1 from dual")

    def execute_query(self, query_string: str, args: dict):
        with self.create_connection() as conn:
            statement = text(query_string)
            if args is not None and len(args.keys()) > 0:
                return conn.execute(statement, args)
            else:
                return conn.execute(statement)

    def execute_update(self, query_string: str, args: dict):
        with self.create_connection() as conn:
            statement = text(query_string)
            trans = conn.begin()
            if args is not None and len(args.keys()) > 0:
                conn.execute(statement, args)
            else:
                conn.execute(statement)
            trans.commit()

    def cleanup(self):
        if self.engine is not None:
            self.logger.info("sql alchemy engine found")
            try:
                self.engine.dispose()
            except Exception as err:
                obj, = err.args
                self.logger.critical("Cannot dispose sql alchemy engine")
                self.logger.error("Context: %s", obj.context)
                self.logger.error("Message: %s", obj.message)
