#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


def create():
    try:
        # Create and connect to file
        conn = sqlite3.connect('replied.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE entries
                     (id text, post text, reply text)''')

        # Commit and close
        conn.commit()
        conn.close()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    create()
