from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from neomodel import config
from dotenv import dotenv_values
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from fastapi import status, HTTPException
from dotenv import dotenv_values

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


    def create_from_father_to_son(self, father_id, son_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_from_father_to_son, father_id, son_id
            )

    @staticmethod
    def _create_from_father_to_son(tx, father_id, son_id):
        query = (
            f"MATCH(c1:Male)"
            f" WITH c1"
            f" MATCH(c2: Male)"
            f" WHERE ID(c1) = $father_id AND ID(c2) = $son_id"
            f" CREATE(c1) - [r: FROM_FATHER_TO_SON]->(c2)"
        )

        try:
            result = tx.run(query, father_id=father_id, son_id=son_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def delete_from_father_to_son(self, father_id, son_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._delete_from_father_to_son, father_id, son_id
            )

    @staticmethod
    def _delete_from_father_to_son(tx, father_id, son_id):
        query = (
            f"MATCH(c1:Male)"
            f" WITH c1"
            f" MATCH(c2: Male)"
            f" WHERE ID(c1) = $father_id AND ID(c2) = $son_id"
            f" MATCH (c1) - [r: FROM_FATHER_TO_SON]->(c2)"
            f" DELETE r"
        )

        try:
            result = tx.run(query, father_id=father_id, son_id=son_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def create_from_father_to_daughter(self, father_id, daughter_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_from_father_to_daughter, father_id, daughter_id
            )

    @staticmethod
    def _create_from_father_to_daughter(tx, father_id, daughter_id):
        query = (
            f"MATCH(c1:Male)"
            f" WITH c1"
            f" MATCH(c2: Female)"
            f" WHERE ID(c1) = $father_id AND ID(c2) = $daughter_id"
            f" CREATE(c1) - [r: FROM_FATHER_TO_DAUGHTER]->(c2)"
        )

        try:
            result = tx.run(query, father_id=father_id, daughter_id=daughter_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def delete_from_father_to_daughter(self, father_id, daughter_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._delete_from_father_to_daughter, father_id, daughter_id
            )

    @staticmethod
    def _delete_from_father_to_daughter(tx, father_id, daughter_id):
        query = (
            f"MATCH(c1:Male)"
            f" WITH c1"
            f" MATCH(c2: Female)"
            f" WHERE ID(c1) = $father_id AND ID(c2) = $daughter_id"
            f" MATCH (c1) - [r: FROM_FATHER_TO_DAUGHTER]->(c2)"
            f" DELETE r"
        )

        try:
            result = tx.run(query, father_id=father_id, daughter_id=daughter_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))


    def delete_from_mother_to_son(self, mother_id, son_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._delete_from_mother_to_son, mother_id, son_id
            )

    @staticmethod
    def _delete_from_mother_to_son(tx, mother_id, son_id):
        query = (
            f"MATCH(c1:Female)"
            f" WITH c1"
            f" MATCH(c2: Male)"
            f" WHERE ID(c1) = $mother_id AND ID(c2) = $son_id"
            f" MATCH (c1) - [r: FROM_MOTHER_TO_SON]->(c2)"
            f" DELETE r"
        )

        try:
            result = tx.run(query, mother_id=mother_id, son_id=son_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def delete_from_mother_to_daughter(self, mother_id, daughter_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._delete_from_mother_to_daughter, mother_id, daughter_id
            )

    @staticmethod
    def _delete_from_mother_to_daughter(tx, mother_id, daughter_id):
        query = (
            f"MATCH(c1:Female)"
            f" WITH c1"
            f" MATCH(c2: Female)"
            f" WHERE ID(c1) = $mother_id AND ID(c2) = $daughter_id"
            f" MATCH (c1) - [r: FROM_MOTHER_TO_DAUGHTER]->(c2)"
            f" DELETE r"
        )

        try:
            result = tx.run(query, mother_id=mother_id, daughter_id=daughter_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))


    def create_from_mother_to_son(self, mother_id, son_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_from_mother_to_son, mother_id, son_id
            )

    @staticmethod
    def _create_from_mother_to_son(tx, mother_id, son_id):
        query = (
            f"MATCH(c1:Female)"
            f" WITH c1"
            f" MATCH(c2: Male)"
            f" WHERE ID(c1) = $mother_id AND ID(c2) = $son_id"
            f" CREATE(c1) - [r: FROM_MOTHER_TO_SON]->(c2)"
        )

        try:
            result = tx.run(query, mother_id=mother_id, son_id=son_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def create_from_mother_to_daughter(self, mother_id, daughter_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_from_mother_to_daughter, mother_id, daughter_id
            )

    @staticmethod
    def _create_from_mother_to_daughter(tx, mother_id, daughter_id):
        query = (
            f"MATCH(c1:Female)"
            f" WITH c1"
            f" MATCH(c2: Female)"
            f" WHERE ID(c1) = $mother_id AND ID(c2) = $daughter_id"
            f" CREATE(c1) - [r: FROM_MOTHER_TO_DAUGHTER]->(c2)"
        )

        try:
            result = tx.run(query, mother_id=mother_id, daughter_id=daughter_id)
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def change_name(self, id, new_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._change_name, id, new_name
            )


    @staticmethod
    def _change_name(tx, id, new_name):
        query = (
            f"MATCH (c)"
            f" WHERE ID(c)=$id"
            f" SET c.name=$new_name"
        )

        try:
            result = tx.run(query, id=id, new_name=new_name)
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    def delete_person(self, id, male=True):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._delete_person, id, male)

    @staticmethod
    def _delete_person(tx, id, is_male):
        query = ""
        if is_male:
            query = (
                f"MATCH (p:Male) where ID(p)=$id"
                " OPTIONAL MATCH (p)-[r]-()"
                " DELETE r,p"
            )
        else:
            query = (
                f"MATCH (p:Female) where ID(p)=$id"
                " OPTIONAL MATCH (p)-[r]-()"
                " DELETE r,p"
            )


        try:
            result = tx.run(query, id=id)
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="{query} raised an error: \n {exception}".format(
                                    query=query, exception=exception))

    @staticmethod
    def _create_and_return_person(tx, person1_name, is_male):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = ""
        if is_male:
            query = (
                "CREATE (p1:Male { name: $person1_name }) "
                " RETURN ID(p1)"
            )
        else:
            query = (
                "CREATE (p1:Female { name: $person1_name }) "
                " RETURN ID(p1)"
            )

        try:
            result = tx.run(query, person1_name=person1_name)
            return [{"p1": row["ID(p1)"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="{query} raised an error: \n {exception}".format(
                query=query, exception=exception))


config_credentials = dotenv_values(".env")

print("Starting database...")
config.DATABASE_URL = 'bolt://neo4j:123456@127.0.0.1:7687'

config_credentials = dotenv_values(".env")

DB_URL = "postgresql://" + config_credentials["POSTGRES_USER"] + ":" + config_credentials["POSTGRES_PASSWORD"] + "@frankfurt-postgres.render.com/mypostgres" #'sqlite:///./profile.db'

engine = create_engine(DB_URL) #, connect_args={"check_same_thread": False})

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
        if neo4j_app:
            neo4j_app.close()