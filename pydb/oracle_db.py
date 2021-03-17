#!/usr/bin/env python3
"""
Module for interacting with an oracle database
"""
# -*- encoding: utf-8 -*-

#============================================================================================
# Imports
#============================================================================================
# Standard imports
import logging

# Third-party imports
import cx_Oracle

from pylog.pylog import get_common_logger_for_module

# Local imports


class OracleDB:
    """
    Class for interacting with an oracle database
    """

    def __init__(self, oracle_config: dict, logging_level: int = 50, logging_format: logging.Formatter = None):
        """
        Setup for oracle db connections. oracle_config must be a python dictionary with the following fields:
        host
        port
        instance (service name)
        user
        pwd

        :param oracle_config:
        :param logging_level: defaults to logging.CRITICAL
        :param logging_format: defaults to None here, which translates to the pylog.get_commong_logging_format
        """
        self.oracle_config = oracle_config
        self.pool = self.set_up_session_pool()

        self.logger = get_common_logger_for_module(module_name=__name__, level=logging_level, log_format=logging_format)

    def set_up_session_pool(self):
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

    def get_session_pool(self):
        """
        Function for creating a session pool with the database
        """
        if self.pool:
            return self.pool
        else:
            self.set_up_session_pool()

    def create_connection(self):
        """
        Function for creating a connection with the database from a session pool
        """
        try:
            connection = self.get_session_pool().acquire()
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

    def execute_query(self, query_string: str, args=None) -> dict:
        """
        Function for executing a query against the database via the session pool
        """
        try:
            connection = self.create_connection()
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
            self.get_session_pool().release(connection)

    def execute_update(self, query_string, args=None):
        """
        Function for executing an insert/update query against the database via the session pool
        """
        try:
            connection = self.create_connection()
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
            self.get_session_pool().release(connection)
