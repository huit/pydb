# pydb

a tool for facilitating connection to databases with python and performing basic operations

## Requirements

    python >= 3.7
    (see setup.py for additional packages)

## Installation and setup

In a suitable python3 (>=3.7) virtual env, using pip:

    pip install https://github.com/huit/pydb/archive/v0.0.2.tar.gz#egg=pydb
    # import the module for the specific type of db you'd like to use
    from pydb.oracle_db import OracleDB

* creating an OracleDB instance requires host, port, service, user, pwd.
    * other db types may have other requirements - see specific module for details  
* logging_level is optional, and will default to `logging.CRITICAL`
* logging_format is optional, and will default to pylog default formatting
* see https://github.com/huit/pylog for details

    
    db = OracleDb(host="valid_host", port=8003, service="SERVICE_NAME", user="username", pwd="pwd")
    (where 8003 is a valid port)

## Basic operations

    create_connection()
        provides a connection to the db host for more 'direct' access

    get_session()
        Specific to SQL Alchemy; allows interaction with SQL Alchemy entities
        see https://docs.sqlalchemy.org/en/14/orm/session.html?highlight=session#module-sqlalchemy.orm.session

    execute_query(self, query_string: str, args=None) -> list
        executes a sql query, return a list of dictionaries representing rows

    execute_update(self, query_string, args=None)
        used to execute an insert, update, or delete sql statement
    
    health_check()
        Performs a basic query against the db to ensure connectivity

    cleanup()
        Attempts to release any 'live' objects/connections to the host

## Example

Given a valid connection, and a table called `EMP`...

To query the `EMP` table for all records:

    result = db.execute_query("select * from emp")

To query the `EMP` table for a specific record:

     result = db.execute_query("select * from emp where ename= :ename", {'ename':'JOHNSON'})

Results for the individual rows would be in the following form:

    {'EMPNO': 7935, 'ENAME': 'JOHNSON', 'JOB': 'CLERK', 'MGR': 7839, 'HIREDATE': datetime.datetime(1981, 5, 1, 0, 0), 'SAL': 2850.0, 'COMM': None, 'DEPTNO': 30}

Row results may vary somewhat depending on the exact module... e.g., for SqlAlchemyOracleDB the following would be received:

    {'empno': 7935, 'ename': 'JOHNSON', 'job': 'CLERK', 'mgr': 7839, 'hiredate': datetime.datetime(1981, 5, 1, 0, 0), 'sal': Decimal('2850'), 'comm': None, 'deptno': 30}