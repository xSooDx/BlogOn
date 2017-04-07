from flask import Flask, render_template;
from os import environ

app = Flask(__name__)

import blogon_views
import apis
import blogon_tasks


