import os
from dotenv     import load_dotenv


class Config():
    def __init__(self):
        load_dotenv()

        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.DB_URI     = os.getenv('DB_URI')
      
        self.REDIS = False
        redis_host = os.getenv('REDIS_HOST')
        if len(redis_host) > 0:
            self.REDIS_HOST = redis_host
            self.REDIS_PORT = os.getenv('REDIS_PORT')
            self.REDIS = True

        #TODO 
        #look into environ for ConfigType or smth. Use 'Dev' as default.
        #rewrite defaults in .env.
    
