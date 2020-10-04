import random
from argparse import ArgumentParser

from cassandra.cluster import Cluster

DEPARTMENTS = ["HR", "IT", "Support", "Sales", "Design", "Finance"]
NAMES = ["Ivan", "Andrey", "Azat", "Dmitriy", "Sergey", "Vladimir"]


def main():
    parser = ArgumentParser()
    parser.add_argument('--server_ip',)
    args = parser.parse_args()
    server_ip = args.server_ip
    num_rows = 1000000
    cluster = Cluster([server_ip, ], )
    session = cluster.connect(None)
    print("Connected!")
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS task_4
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' };
        """
    )
    print("Successfully created schema!")
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS task_4.task_4_table(
            id int,    
            dept_name text,
            name text,
            PRIMARY KEY((id), dept_name)
        );
        """
    )
    print("Successfully created table!")
    user_lookup_stmt = session.prepare(
        """
        INSERT INTO task_4.task_4_table (id, dept_name, name)
        VALUES (?, ?, ?);
        """)
    print("Created a statement")
    for i in range(num_rows):
        id_value = i % 1000
        department = random.choice(DEPARTMENTS)
        name = random.choice(NAMES)
        session.execute(user_lookup_stmt, [id_value, department, name])


if __name__ == '__main__':
    main()
