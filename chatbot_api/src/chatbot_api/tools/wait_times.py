from __future__ import annotations
from typing import Type

import numpy as np

from chatbot_api.utils.neo4j_graph import GraphConnector

class WaitTime:

    def __init__(self, neo4j_connector: Type[GraphConnector]) -> None:
        self.neo4j_connector = neo4j_connector

    def get_current_wait_times(self, hospital: str) -> str:
        """
        Get the current wait time at a hospital formatted as a string.
        """
        wait_time_in_minutes = self.__get_current_wait_time_minutes(hospital)

        if wait_time_in_minutes == -1:
            return f"Hospital '{hospital}' does not exist."

        hours, minutes = divmod(wait_time_in_minutes, 60)

        if hours > 0:
            formatted_wait_time = f"{hours} hours {minutes} minutes"
        else:
            formatted_wait_time = f"{minutes} minutes"

        return formatted_wait_time

    def get_most_available_hospital(self) -> str:
        """
        Find the hospital with the shortest wait time.
        """
        current_hospitals = self.__get_current_hospitals()

        current_wait_times = [
            self.__get_current_wait_time_minutes(h) for h in current_hospitals
        ]

        best_time_idx = np.argmin(current_wait_times)
        best_hospital = current_hospitals[best_time_idx]
        best_wait_time = current_wait_times[best_time_idx]

        return f'Hospital "{best_hospital}" with best wait time - {best_wait_time} minutes.'

    def __get_current_hospitals(self) -> list[str]:
        """
        Fetch a list of current hospital names from a Neo4j database.
        """
        current_hospitals = self.neo4j_connector.query(
            """
            MATCH (h:Hospital)
            RETURN h.name AS hospital_name
            """
        )
        
        current_hospitals = [d["hospital_name"].lower() for d in current_hospitals]

        return current_hospitals


    def __get_current_wait_time_minutes(self, hospital: str) -> int:
        """
        Get the current wait time at a hospital in minutes.
        """
        current_hospitals = self.__get_current_hospitals()

        if hospital.lower() not in current_hospitals:
            return -1

        return np.random.randint(low=0, high=600)
