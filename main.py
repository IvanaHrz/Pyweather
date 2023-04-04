from flask import Flask
import sys
from Controller import Controller

app = Flask(__name__,static_folder="Assets",template_folder="Views")


if __name__=="__main__":
    Controller.setup(app)