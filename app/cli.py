import os
import click

from flask import current_app

from app import db

# Neither command works as intended for now

def register(app):
    @app.cli.command('init-db')
    def init_db():
        cursor = db.connection.cursor()
        with open('init.sql') as f:
            read_data = f.read()
            iterator = cursor.execute(read_data)

    @app.cli.command('sample')
    def populate_sample():
        cursor = db.connection.cursor()
        with open('sample.sql') as f:
            read_data = f.read()
            iterator = cursor.execute(read_data)