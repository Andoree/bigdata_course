from argparse import ArgumentParser
import happybase


def main():
    parser = ArgumentParser()
    parser.add_argument('--host', )
    parser.add_argument('--table_name', default='hbase_task_table')
    args = parser.parse_args()

    hbase_host = args.host
    table_name = args.table_name

    connection = happybase.Connection(hbase_host)
    connection.open()
    connection.create_table(
        table_name,
        {'f1': dict(max_versions=10),
         'f2': dict(max_versions=5, ),
         }
    )


if __name__ == '__main__':
    main()
