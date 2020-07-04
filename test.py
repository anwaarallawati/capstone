import os
import unittest
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app

casting_assistant = os.environ.get('casting_assistant')

print (casting_assistant)