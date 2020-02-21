from flask import Flask
from config import Config
import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.start_time = datetime.datetime.utcnow()

from app import routes
