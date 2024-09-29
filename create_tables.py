import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries
# modify

def drop_tables(cur, conn):
    """accepts connection parameters and drops all tables and returns nothing"""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """accepts connection parameters and creates all tables and returns nothing"""
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """STEP 1: Get the params of the created redshift cluster"""
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    DWH_DB= config.get("DWH","DWH_DB")  
    DWH_DB_USER= config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD= config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT = config.get("DWH","DWH_PORT")
    DWH_ENDPOINT=config.get("DWH","DWH_ENDPOINT")  # conn = psycopg2.connect("host={} dbname={} user={} password={} port=##{}".format(*config['CLUSTER'].values()))

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(DWH_ENDPOINT,DWH_DB,DWH_DB_USER,DWH_DB_PASSWORD,DWH_PORT))
    
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()