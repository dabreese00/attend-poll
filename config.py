import os

class Config:
    DATABASE = os.environ.get('DATABASE') or 'attend-poll.sqlite'
