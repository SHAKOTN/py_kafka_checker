import logging

from consumer.database.database_session import Session

logger = logging.getLogger(__name__)

def migrate_metrics_table():
    create_table_query = """
        create table if not exists 
        website_metrics(
            id serial primary key,  
            created_on timestamp default current_timestamp, 
            url varchar (256) not null, 
            content varchar (4096), 
            response_time float not null, 
            code int not null
        );
    """

    create_index_query = """
        create index if not exists url_status_code_idx
        on website_metrics (url, code);
    """
    with Session() as session:
        session.execute(create_table_query)
        session.execute(create_index_query)
        session.commit()

def drop_metrics_table():
    with Session() as session:
        session.execute("drop table if exists website_metrics;")
        session.execute("drop index if exists url_status_code_idx;")
        session.commit()

if __name__ == '__main__':
    logger.warning("!!!Migrating database!!!")
    migrate_metrics_table()
