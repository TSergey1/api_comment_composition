import datetime
import os
import sqlite3
import pandas as pd

from django.core.management.base import BaseCommand


current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file) + '/../../..'
path_to_csv = current_directory + '/static/data/'


class Command(BaseCommand):
    help = """
    Use 'python3 manage.py upload_csv -u' if you want
    update data base from csv file.
    Attention! It's can drop table in your DB!
    """

    def handle(self, *args, **options):
        if options['upgrade_db']:
            files = os.listdir(path_to_csv)
            conn = sqlite3.connect(current_directory + '/db.sqlite3')
            for csv_file in files:
                if 'genre_' in csv_file:
                    table = ('reviews_'
                             + csv_file.split('_')[1].rstrip('s.csv')
                             + '_' + csv_file.split('_')[0]
                             )
                else:
                    table = 'reviews_' + csv_file.rstrip('s.csv')
                conn.execute(f'''DELETE FROM {table};''')
                cursor = conn.execute(f'select * from {table}')
                names = list(map(lambda x: x[0], cursor.description))
                data = pd.read_csv(
                    path_to_csv + csv_file,
                    header=0,
                    keep_default_na=False
                )
                new_data = pd.DataFrame()
                for n in names:
                    regular = fr"^{n.split('_')[0]}.*$"
                    if data.columns.str.contains(regular).any():
                        new_data[n] = data.filter(regex=regular)
                    else:
                        new_data[n] = ''

                if table == 'reviews_user':
                    new_data.loc[new_data['role']
                                 == 'admin', ('is_superuser', 'is_staff')] = 1
                    new_data.loc[new_data['role']
                                 == 'moderator', 'is_staff'] = 1
                    new_data.loc[
                        new_data['id'] > 0, ('is_active', 'date_joined')
                    ] = (1, datetime.datetime.now())
                new_data.to_sql(table, conn, if_exists='append', index=False)
            conn.commit()
            conn.close()
        else:
            print("""
Use:
'python3 manage.py upload_csv -u'
if you want update data base from csv file.
Be attention! It's drop table in your DB!
    """)

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--upgrade_db',
            action='store_true',
            default=False,
            help='Обновление базы данных'
        )
