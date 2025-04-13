import sqlite3
from datetime import datetime
from flask import g

DATABASE = './db/database.db'


class Db:
    @staticmethod
    def get_connection():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db

    @staticmethod
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @staticmethod
    def get_record(code):

        db = Db.get_connection()
        cur = db.cursor()
        cur.execute(
            '''SELECT id, code_type, code, description, item_count, registered_at
            FROM items
            WHERE code=?''',
            (code,)
        )
        record = cur.fetchone()
        cur.close()

        return {
            'id': record[0],
            'code_type': record[1],
            'code': record[2],
            'description': record[3],
            'count': record[4],
            'registered_at': record[5]
        }

    @ staticmethod
    def list_items():
        db = Db.get_connection()
        cur = db.cursor()
        cur.execute(
            'SELECT id, code_type, code, description, item_count, registered_at FROM items')
        rows = cur.fetchall()
        cur.close()

        return [
            {
                'id': row[0],
                'code_type': row[1],
                'code': row[2],
                'description': row[3],
                'count': row[4],
                'registered_at': row[5]
            } for row in rows
        ]

    @ staticmethod
    def item_exists(code):
        db = Db.get_connection()
        cur = db.cursor()
        cur.execute(
            'SELECT item_count FROM items WHERE code=? LIMIT 1', (code,))
        result = cur.fetchone()
        cur.close()
        return result[0] if result else None

    @ staticmethod
    def add_count(code, amount, timestamp):

        count = amount + 1
        db = Db.get_connection()
        cur = db.cursor()
        cur.execute('''
            UPDATE items
            SET item_count=?, timestamp=?
            WHERE code=?
        ''', (count, timestamp, code,))

        db.commit()
        cur.close()
        return 200

    @ staticmethod
    def substract_count(code, amount, timestamp):
        count = amount - 1
        db = Db.get_connection()
        cur = db.cursor()
        cur.execute('''
            UPDATE items
            SET item_count=?, timestamp=?
            WHERE code=?
        ''', (count, timestamp, code))
        db.commit()
        cur.close()
        return 200

    @ staticmethod
    def add_item(item):
        code_type = item.get("type")
        code = item.get("data")
        timestamp_iso = datetime.strptime(
            item.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = timestamp_iso.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        amount = Db.item_exists(code)
        db = Db.get_connection()
        cur = db.cursor()

        if amount is None:
            cur.execute('''
                INSERT INTO items (code_type, code, timestamp, item_count)
                VALUES (?, ?, ?, ?)
            ''', (code_type, code, timestamp, 1))
            db.commit()
            cur.close()
            return 201
        else:
            cur.close()
            return Db.add_count(code, amount, timestamp)

    @ staticmethod
    def remove_item(item):
        code = item.get("data")
        timestamp_iso = datetime.strptime(
            item.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = timestamp_iso.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        amount = Db.item_exists(code)

        if amount is None or amount <= 0:
            return 304
        else:
            return Db.substract_count(code, amount, timestamp)
