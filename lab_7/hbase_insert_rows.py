import random
from argparse import ArgumentParser

import happybase


def main():
    parser = ArgumentParser()
    parser.add_argument('--host', )
    parser.add_argument('--num_rows', default=10000, type=int)
    parser.add_argument('--num_region_servers', default=3, type=int)
    args = parser.parse_args()

    hbase_host = args.host
    num_rows = args.num_rows
    num_region_servers = args.num_region_servers

    connection = happybase.Connection(hbase_host)
    connection.open()
    table = connection.table('hbase_task_table')

    for i in range(num_rows):
        region_server_id = random.randint(1, num_region_servers)
        key = f"{region_server_id}_key_{i}"
        table.put(key, {'f1': f'value_{i % 100}',
                        'f2': f'value_{i % 1000}'})


if __name__ == '__main__':
    main()
