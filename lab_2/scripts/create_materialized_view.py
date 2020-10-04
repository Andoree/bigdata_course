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
        CREATE MATERIALIZED VIEW task_4.task_4_mview 
        AS SELECT id, dept_name, name 
        FROM task_4.task_4_table
        WHERE name IS NOT NULL AND id IS NOT NULL
        PRIMARY KEY ((name), id, dept_name);
        """
    )
    print("Successfully created materialized view!")


if __name__ == '__main__':
    main()
