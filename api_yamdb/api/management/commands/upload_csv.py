import datetime
import os
import sqlite3
import pandas as pd

from django.core.management.base import BaseCommand


current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file) + '/../../..'
path_to_csv = current_directory + '/static/data/'
uploads_info = {
    'reviews_title': (
        'titles.csv',
        (
            'id', 'name', 'year', 'category_id', 'description'
        )
    ),
    'reviews_category': (
        'category.csv',
        (
            'id', 'name', 'slug'
        )
    ),
    'reviews_user': (
        'users.csv',
        (
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
            'password',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
        )
    ),
    'reviews_genre': (
        'genre.csv', ('id', 'name', 'slug')
    ),
    'reviews_review': (
        'review.csv',
        (
            'id', 'title_id', 'text', 'author_id', 'score', 'pub_date'
        )
    ),
    'reviews_comment': (
        'comments.csv',
        (
            'id', 'review_id', 'text', 'author_id', 'pub_date'
        )
    ),
    'reviews_title_genre': (
        'genre_title.csv', (
            'id', 'title_id', 'genre_id'
        )
    ),
}


class Command(BaseCommand):
    help = """
    Use 'python3 manage.py upload_csv -u' if you want
    update data base from csv file.
    Attention! It's can drop table in your DB!
    """

    def handle(self, *args, **options):
        if options['upgrade_db']:
            conn = sqlite3.connect(current_directory + '/db.sqlite3')
            for table, (csv_file, names) in uploads_info.items():
                conn.execute(f'''DELETE FROM {table};''')
                path = path_to_csv + csv_file
                data = pd.read_csv(
                    path,
                    header=None,
                    names=names,
                    skiprows=1,
                    keep_default_na=False
                )
                if table == 'reviews_user':
                    data = data.replace(
                        {
                            'is_active': {'': 1},
                            'date_joined': {'': datetime.datetime.now()}
                        }
                    )
                    for row in data.index:
                        if data.loc[row, 'role'] == 'admin':
                            data.loc[row, 'is_superuser'] = 1
                            data.loc[row, 'is_staff'] = 1
                        elif data.loc[row, 'role'] == 'moderator':
                            data.loc[row, 'is_staff'] = 1
                data.to_sql(table, conn, if_exists='append', index=False)
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
