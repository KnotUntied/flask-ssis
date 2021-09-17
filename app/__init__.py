from flask import Flask

app = Flask(__name__)

# Circular imports
from app import routes
