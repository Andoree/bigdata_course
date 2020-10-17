from argparse import ArgumentParser

from cassandra.cluster import Cluster


def main():
    parser = ArgumentParser()
    parser.add_argument('--server_ip', )
    args = parser.parse_args()
    server_ip = args.server_ip
    cluster = Cluster([server_ip, ], )
    session = cluster.connect(None)
    print("Connected!")
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS task_5
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' };
        """
    )
    print("Succesfully created schema!")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS task_5.task_5_table(
            id int PRIMARY KEY,    
            name text
        );
        """
    )
    print("Succesfully created table!")
    user_lookup_stmt = session.prepare(
        """
        INSERT INTO task_5.task_5_table (id, name)
        VALUES (?, ?);
        """)
    print("Created a statement")
    i = 0
    while True:
        session.execute(user_lookup_stmt, [i, f"name_{i}"])
        i += 1


if __name__ == '__main__':
    main()
