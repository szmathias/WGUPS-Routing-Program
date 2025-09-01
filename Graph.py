# Author: Zack Mathias | 010868562
# Course: C950 - Data Structures and Algorithms II
# Project: WGUPS Routing Program
# File: Graph.py
# Purpose: Implements a Graph using an Adjacency Matrix to track relations

# Standard Library
import csv


# Creates a table with weights signifying a relation between two edges
class AdjacencyMatrix:
    def __init__(self, x: int, y: int, initial_value=-1.0):
        self.x = x
        self.y = y
        self.adjacency_matrix = [[initial_value] * x for _ in range(y)]

    # Returns the weight at the position (i, j) or None
    def get_weight(self, i: int, j: int) -> float | None:

        # Checks if the position is in the bounds of the matrix
        if i < 0 or j < 0 or i >= self.x or j >= self.y:
            return None

        return self.adjacency_matrix[i][j]

    # Sets the value at position (i, j) to value. Returns if it was successfully set
    def set_weight(self, i: int, j: int, value: float) -> bool:

        # Checks if the position is in the bounds of the matrix
        if i < 0 or j < 0 or i >= self.x or j >= self.y:
            return False

        self.adjacency_matrix[i][j] = value
        return True

    # Returns the Matrix as a grid
    def __str__(self) -> str:
        string = ""
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[i])):
                item = self.adjacency_matrix[i][j]
                string += f'{item:4}' + " "

            string += "\n"

        return string


# Graph implementation that uses the adjacency matrix above
class Graph:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adjacency_matrix = AdjacencyMatrix(num_vertices, num_vertices)

    # Checks to see if a relation exists between i and j
    def has_edge(self, i: int, j: int) -> bool | None:
        weight = self.adjacency_matrix.get_weight(i, j)
        if weight is None or weight == -1.0:
            return False

        return True

    # Returns the weight of the edge or None
    def get_edge(self, i: int, j: int) -> float | None:
        return self.adjacency_matrix.get_weight(i, j)

    # Adds an edge between two vertices and sets the weight
    def add_edge(self, i: int, j: int, weight: float = 1.0) -> None:
        self.adjacency_matrix.set_weight(i, j, weight)
        self.adjacency_matrix.set_weight(j, i, weight)

    # Gives a string showing the number of vertices and the matrix
    def __str__(self) -> str:
        return "Number of vertices: " + str(self.num_vertices) + "\n" + str(self.adjacency_matrix)


# Reads in a CSV file and returns a new graph with a dictionary of addresses to ids and
# ids to addresses
def read_distances_to_graph(filename: str) -> tuple[Graph, dict[str, int], dict[int, str]]:
    # Uses address as the key and id as the value
    address_ids: dict[str, int] = {}

    # Uses id as the key and address as the value
    ids_address: dict[int, str] = {}
    distances: list[list[float]] = []

    with open(filename, mode='r') as file:
        csv_file = csv.reader(file)
        temp_id = 0

        # Loops through every line in the file
        for line in csv_file:

            # Sets the addresses and ids
            address_ids.update({line[0]: temp_id})
            ids_address.update({temp_id: line[0]})
            temp_id += 1

            # Loops through all the distances for that location
            temp: list[float] = []
            for i in range(1, len(line)):
                temp.append(float(line[i]))

            distances.append(temp)

    # Creates the graph and sets the distance to each location as the weight between the edges
    vertices = len(address_ids)
    graph = Graph(vertices)
    for i in range(len(distances)):
        for j in range(len(distances[i])):
            graph.add_edge(j, i, distances[i][j])

    return graph, address_ids, ids_address
