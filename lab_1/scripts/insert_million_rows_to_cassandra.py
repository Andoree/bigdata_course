from argparse import ArgumentParser

from cassandra.cluster import Cluster


def main():
    parser = ArgumentParser()
    parser.add_argument('--server_ip', default="3.235.52.110")
    args = parser.parse_args()
    server_ip = args.server_ip
    num_rows = 1000000
    cluster = Cluster([server_ip, ], )
    session = cluster.connect()

    session.execute(
        """
        CREATE TABLE IF NOT EXISTS test(
            id int PRIMARY KEY,    
            name str
        );
        """
    )

    user_lookup_stmt = session.prepare(
        """
        INSERT INTO test (id, name,)
        VALUES (?, ?);
        """)

    for i in range(num_rows):
        session.execute(user_lookup_stmt, [i, f"name_{i}"])


if __name__ == '__main__':
    main()
