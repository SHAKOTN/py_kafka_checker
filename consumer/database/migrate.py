from consumer.database import Session


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
        create index url_ix
        on website_metrics (url, code);
    """
    with Session() as session:
        session.execute(create_table_query)
        session.execute(create_index_query)
