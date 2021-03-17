#!/usr/bin/env python3
"""
Module for interacting with the database
"""
# -*- encoding: utf-8 -*-

#============================================================================================
# Imports
#============================================================================================
# Standard imports
import logging

# Third-party imports
import cx_Oracle

# Local imports


class PyDB:
    """
    Class for interacting with an oracle database
    """

    def __init__(self, oracle_config: dict, logging_formatter: logging.Formatter = None):
        """
        Setup for oracle db connections. oracle_config must be a python dictionary with the following fields:
        host
        port
        instance (service name)
        user
        pwd

        :param oracle_config:
        :param logging_formatter:
        """
        self.oracle_config = oracle_config
        self.pool = None

        self.logger = logging.getLogger(__name__)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        if logging_formatter:
            stream_handler.setFormatter(logging_formatter)
        else:
            stream_format = logging.Formatter(
                '{"log_level": "%(levelname)s", '
                '"app_file_line": "%(name)s:%(lineno)d", '
                '"message": %(message)s}'
            )
            stream_handler.setFormatter(stream_format)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)

    def get_session_pool(self):
        """
        Function for creating a session pool with the database
        """
        if self.pool:
            return self.pool
        else:
            host = self.oracle_config.get('host')
            port = self.oracle_config.get('port')
            instance = self.oracle_config.get('instance')

            try:
                dsn_str = cx_Oracle.makedsn(host, port, service_name=instance)
                pool = cx_Oracle.SessionPool(
                    user=self.oracle_config.get('user'),
                    password=self.oracle_config.get('pwd'),
                    dsn=dsn_str,
                    min=2,
                    max=5,
                    increment=1,
                    threaded=True,
                    encoding="UTF-8"
                    )
                self.pool = pool
                return pool

            except cx_Oracle.DatabaseError as err:
                obj, = err.args
                self.logger.error("Error creating pool")
                self.logger.error("Context: %s", obj.context)
                self.logger.error("Message: %s", obj.message)
                raise Exception(f"Error creating pool: {obj.message}")

    def create_connection(self, pool):
        """
        Function for creating a connection with the database from a session pool
        """
        try:
            connection = pool.acquire()
            return connection

        except cx_Oracle.DatabaseError as err:
            obj, = err.args
            self.logger.error("Error acquiring database connection from the session pool")
            self.logger.error("Context: %s", obj.context)
            self.logger.error("Message: %s", obj.message)
            raise Exception("Error acquiring database connection from the session pool")

    @staticmethod
    def make_dict(cursor):
        """
        Function for converting a query result row into a dictionary
        """
        column_names = [d[0] for d in cursor.description]

        def create_row(*args):
            return dict(zip(column_names, args))
        return create_row

    def execute_query(self, pool, query_string: str, args=None) -> dict:
        """
        Function for executing a query against the database via the session pool
        """
        try:
            connection = self.create_connection(pool)
            cursor = connection.cursor()
            if args is not None:
                cursor.execute(query_string, args)
            else:
                cursor.execute(query_string)
            cursor.rowfactory = self.make_dict(cursor)
            query_result = cursor.fetchall()
            return query_result

        except cx_Oracle.DatabaseError as err:
            obj, = err.args
            self.logger.error("Error in execute_query")
            self.logger.error("Context: %s", obj.context)
            self.logger.error("Message: %s", obj.message)
            raise Exception(f"Error executing query: {query_string}")

        finally:
            cursor.close()
            pool.release(connection)

    def execute_update(self, pool, query_string, args=None):
        """
        Function for executing an insert/update query against the database via the session pool
        """
        try:
            connection = self.create_connection(pool)
            cursor = connection.cursor()
            if args is not None:
                cursor.execute(query_string, args)
            else:
                cursor.execute(query_string)
            connection.commit()

        except cx_Oracle.DatabaseError as err:
            obj, = err.args
            self.logger.error("Error in execute_update")
            self.logger.error("Context: %s", obj.context)
            self.logger.error("Message: %s", obj.message)
            raise Exception(f"Error executing update: {query_string}")

        finally:
            cursor.close()
            pool.release(connection)
