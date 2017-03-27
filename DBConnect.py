#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os.path
import DBCreate


class Connect(object):
    def __init__(self):
        self.dbFile = 'replied.db'

    def storeData(self, pID, post, reply):
        try:
            # Create db if it does not exist
            if not os.path.isfile(self.dbFile):
                DBCreate.create()

            # Create and connect to file
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()

            # Prepare and insert data
            data = [(pID, post, reply)]
            c.executemany('INSERT INTO entries VALUES (?,?,?)', data)

            # Test query
            c.execute('SELECT ID FROM entries')
            print ((c.fetchall()))

            # Commit and close
            conn.commit()
            conn.close()

        except Exception as e:
            print(e)

if __name__ == "__main__":
    Connect().run()
