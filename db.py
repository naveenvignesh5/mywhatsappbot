import sqlite3
import datetime

class db:
    def __init__(self):
        # open('data.db', 'w+') # create data.db
        self.conn = sqlite3.connect('data.db')
        self.conn.executescript('''
            create table if not exists messages (
                id integer primary key autoincrement not null,
                name text,
                phone text not null,
                message_type text,
                timeStamp text not null,
                campaign_id integer not null
            );

            create table if not exists users (
                id integer primary key autoincrement not null,
                name text not null,
                phone text not null,
                user_type text not null,
                created_at text not null
            );

            create table if not exists campaigns (
                id integer primary key autoincrement not null,
                name text not null,
                sent_at text
            );

            create table if not exists message (
                id integer primary key autoincrement not null,
                data text not null,
                type text not null
            );
        ''')
    
    def isEntryMade(self, number):
        today = str(datetime.datetime.now().date())
        cur = self.conn.cursor()
        rows = cur.execute('''
            select count(*) from messages where phone = ? and date(timeStamp) = ?
        ''', (number, today))
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

    def createCampaign(self,name):
        now = str(datetime.datetime.now())
        self.conn.execute('''
            insert into campaigns
            (name, sent_at)
            values (?, ?)
        ''', (name, now))
        self.conn.commit()
