from argparse import ArgumentParser

from cassandra.cluster import Cluster


def main():
    parser = ArgumentParser()
    parser.add_argument('--server_ip', default="3.235.52.110")
    args = parser.parse_args()
    server_ip = args.server_ip
    num_rows = 1000000
    cluster = Cluster([server_ip, ], )
    session = cluster.connect(None)
    print("Connected!")
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS test
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' };
        """
    )
    print("Succesfully created schema!")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS test.test(
            id int PRIMARY KEY,    
            name text
        );
        """
    )
    print("Succesfully created table!")
    user_lookup_stmt = session.prepare(
        """
        INSERT INTO test.test (id, name)
        VALUES (?, ?);
        """)
    print("Created a statement")
    for i in range(num_rows):
        session.execute(user_lookup_stmt, [i, f"name_{i}"])


if __name__ == '__main__':
    main()
