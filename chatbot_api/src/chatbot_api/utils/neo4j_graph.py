from __future__ import annotations
from typing import Type
from chatbot_api.utils.configuration import Configuration
from langchain_neo4j import Neo4jGraph


class GraphConnector:

    def __init__(self, app_conf: Type[Configuration]) -> None:
        self.app_conf = app_conf
        self.graph = Neo4jGraph(
            url = self.app_conf.neo4j_config['uri'],
            username = self.app_conf.neo4j_config['username'],
            password = self.app_conf.neo4j_config['password'],
        )

    def query(self, query: str) -> list[dict]:
        """
        Execute a Cypher query on the graph database.
        """
        return self.graph.query(query)

    def refresh_schema(self) -> None:
        """
        Refresh the schema of the graph database.
        """
        self.graph.refresh_schema()
    
    def get_neo4jgraph(self) -> Type[Neo4jGraph]:
        """
        Get the Neo4jGraph object.
        """
        return self.graph
