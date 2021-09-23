import os
import click

from flask import current_app

from app import db

def register(app):
    @app.cli.command("create-db")
    def create_db():
        cursor = db.connection.cursor()
        # cursor.execute("CREATE DATABASE ssis")