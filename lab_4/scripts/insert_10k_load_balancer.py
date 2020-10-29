from argparse import ArgumentParser

from cassandra.cluster import Cluster


def main():
    parser = ArgumentParser()
    parser.add_argument('--load_balancer_dns', )
    parser.add_argument('--num_rows', type=int)
    args = parser.parse_args()
    load_balancer_dns = args.load_balancer_dns
    num_rows = args.num_rows
    cluster = Cluster([load_balancer_dns, ], )
    session = cluster.connect(None)
    print("Connected!")
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS task_6
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' };
        """
    )
    print("Succesfully created schema!")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS task_6.task_6_table(
            id int PRIMARY KEY,    
            name text
        );
        """
    )
    print("Succesfully created table!")
    user_lookup_stmt = session.prepare(
        """
        INSERT INTO task_6.task_6_table (id, name)
        VALUES (?, ?);
        """)
    print("Created a statement")
    for i in range(num_rows):
        session.execute(user_lookup_stmt, [i, f"name_{i}"])
        i += 1


if __name__ == '__main__':
    main()
