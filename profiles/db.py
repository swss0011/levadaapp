from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from neomodel import config
from dotenv import dotenv_values
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def neo4j_driver(self):
        return self.driver

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_person(self, person1_name, male=True):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            res_for_sql = ""
            result = session.write_transaction(
                self._create_and_return_person, person1_name, male)
            print("Created friendship between: {p1}".format(p1=result))
            res_for_sql = result[0]['p1']


            return res_for_sql

    @staticmethod
    def _create_and_return_person(tx, person1_name, is_male):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = ""
        if is_male:
            query = (
                "CREATE (p1:Male { name: $person1_name }) "
                "RETURN ID(p1)"
            )
        else:
            query = (
                "CREATE (p1:Female { name: $person1_name }) "
                "RETURN ID(p1)"
            )
        result = tx.run(query, person1_name=person1_name)
        try:
            return [{"p1": row["ID(p1)"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


config_credentials = dotenv_values(".env")

print("Starting database...")
config.DATABASE_URL = 'bolt://neo4j:123456@127.0.0.1:7687'

DB_URL = 'sqlite:///./profile.db'

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
neo4j_app = None

def get_neo4j():
    uri = config_credentials["NEO4J_URI"]
    user = config_credentials["NEO4JUSER"]
    password = config_credentials["NEO4J-AURA"]
    neo4j_app = App(uri, user, password)
    return neo4j_app

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()