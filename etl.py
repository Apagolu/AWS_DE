import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
# modify1

def load_staging_tables(cur, conn):
    """ step: staging - Loading data from S3 into Staging tables - staging_events,staging_songs"""
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """ step: From staging - Loading data from S3 into Fact and Dim tables"""
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))
    
    DWH_DB= config.get("DWH","DWH_DB")  
    DWH_DB_USER= config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD= config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT = config.get("DWH","DWH_PORT")
    DWH_ENDPOINT=config.get("DWH","DWH_ENDPOINT")
   
    # Connect to the Database
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".
                            format(DWH_ENDPOINT,DWH_DB,DWH_DB_USER,DWH_DB_PASSWORD,DWH_PORT))
    
    #config.read('dwh.cfg')
   # conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
   
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()