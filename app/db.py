from neo4j import GraphDatabase
from dotenv import load_dotenv
import os 

class Database:
    def __init__(self):
        self.get_credentials()
        self._driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password), database=self.database)

    def get_credentials(self):
        if os.path.exists('credentials.env'):
            load_dotenv('credentials.env', override=True)
            self.uri = os.getenv('NEO4J_URI')
            self.username = os.getenv('NEO4J_USERNAME')
            self.password = os.getenv('NEO4J_PASSWORD')
            self.database = os.getenv('NEO4J_DATABASE')
            self.import_directory = os.getenv('NEO4j_IMPORT')
        else:
            print("File 'credentials.env' not found.")
        

    def close(self):
        self._driver.close()

    def get_session(self):
        return self._driver.session()

db = Database()