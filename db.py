import sqlite3
import datetime

class db:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')

        self.conn.executescript('''
            create table if not exists messages (
                id integer primary key autoincrement not null,
                name text,
                phone text not null,
                message_type text,
                timeStamp text not null,
                campaign_id text not null
            );

            create table if not exists users (
                id integer primary key autoincrement not null,
                name text not null,
                phone text not null,
                user_type text not null,
                created_at text not null
            );
        ''')
    
    def isEntryMade(self, name, number, campaign_id):
        cur = self.conn.cursor()
        rows = cur.execute('''
            select count(*) from messages where (name = ? or phone = ?) and campaign_id = ?
        ''', (name, number, campaign_id))

        flag = False
        
        for row in rows:
            if row[0] > 0:
                flag = True

        return flag

    def makeMessageEntry(self, message, t, name, phone, campaign_id):
        now = str(datetime.datetime.now())
        self.conn.execute('''
            insert into messages
            (name, phone, message_type, timeStamp, campaign_id)
            values (?, ?, ?, ?, ?)
        ''', (name, phone, t, now, campaign_id))
        self.conn.commit()

    def createUser(self, name, phone, user_type):
        now = str(datetime.datetime.now())
        self.conn.execute('''
            insert into users
            (name, phone, user_type, created_at)
            values (?, ?, ?, ?)
        ''', (name, phone, user_type, now))
        self.conn.commit()
