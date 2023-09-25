'''
This is the configuration file for RouteRover
'''
import os
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''
    This class sets configuration values
    C
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')\
        or 'postgresql:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
