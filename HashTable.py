"""
HashTable.py
Implements a Hash Table using Nodes with a singly linked list for package storage and lookup.
"""
# Author: Zack Mathias | 010868562
# Course: C950 - Data Structures and Algorithms II
# Project: WGUPS Routing Program
# File: HashTable.py
# Purpose: Implements a Hash Table using Nodes with a singly linked list

from typing import List


# Holds the key, value, and next object for each hash table implementation
class Node:
    """
    Represents a node in a singly linked list for hash table buckets.
    """

    def __init__(self, key=-1, value=None):
        """
        Initializes a Node.
        Args:
            key (int): Key for the node.
            value (any): Value stored in the node.
        """
        self.key = key
        self.value = value
        self.next = None

    # Prints the Node and all Nodes linked
    def __str__(self):
        """
        Returns a string representation of the node and its linked nodes.
        Returns:
            str: String representation of the node chain.
        """
        string = ""
        current = self
        while current:
            string += str(current.value)
            current = current.next
            if current:
                string += " -> "

        string += "\n"
        return string


# Hash Table implementation
class HashTable:
    """
    Implements a hash table with separate chaining using singly linked lists.
    """

    # Initializes values to default
    def __init__(self, capacity=10):
        """
        Initializes the hash table with a given capacity.
        Args:
            capacity (int): Number of buckets in the hash table.
        """
        self.table: List[Node] = []
        self.capacity = capacity
        self.num_keys = 0
        for i in range(0, self.capacity):
            self.table.append(Node())

    # Basic hash function using the capacity and the key
    def hash_function(self, key: int) -> int:
        """
        Basic hash function using the capacity and the key.
        Args:
            key (int): Key to hash.
        Returns:
            int: Bucket index.
        """
        return key % self.capacity

    # Inserts a Node into the hash table
    def insert(self, key: int, value: any) -> None:
        """
        Inserts a Node into the hash table.
        Args:
            key (int): Key for the node.
            value (any): Value to store.
        """
        index = self.hash_function(key)

        # If the location is empty, put the value in place
        if self.table[index].key == -1:
            self.table[index].key = key
            self.table[index].value = value
            self.num_keys += 1
            return

        # A Node exits, so iterate through the list until you get to the end or find the key
        current = self.table[index]
        while current.key != key and current.next is not None:
            current = current.next

        # If the current node has the same key, then update the value
        if current.key == key:
            current.value = value

        # Otherwise, add a new Node to the end of the list
        else:
            current.next = Node(key, value)
            self.num_keys += 1

    # Returns the value of the key found or None
    def lookup(self, key: int) -> any:
        """
        Returns the value of the key found or None.
        Args:
            key (int): Key to look up.
        Returns:
            any: Value associated with the key, or None if not found.
        """
        index = self.hash_function(key)

        # Nothing exists at that location yet
        if self.table[index].key == -1:
            return None

        # Iterate until we find a matching key or get to the end of the list
        current = self.table[index]
        while current.key != key and current.next is not None:
            current = current.next

        # We found the matching key, return the value
        if current.key == key:
            return current.value

        # The key didn't exist
        return None

    # Removes a node if it exists in the hash table
    def remove(self, key: int) -> Node | None:
        """
        Removes a node if it exists in the hash table.
        Args:
            key (int): Key to remove.
        Returns:
            Node | None: Removed node, or None if not found.
        """
        index = self.hash_function(key)

        # It doesn't exist.
        if self.table[index].key == -1:
            return None

        # Iterate through the list until we find the key or get to the end.
        # Keeping track of the previous node
        current = self.table[index]
        last = None
        while current.key != key and current.next is not None:
            last = current
            current = current.next

        # We found the key in the list
        if current.key == key:

            # The key was in the middle or at the end of the list
            if last is not None:
                last.next = current.next

            # The key was the head of the list
            else:
                self.table[index] = current.next

            # Return the removed node
            self.num_keys -= 1
            return current

        # The Node doesn't exist
        return None

    # Used to print the hash table into buckets
    def __str__(self):
        """
        Returns a string representation of the hash table buckets and their contents.
        Returns:
            str: String representation of the hash table.
        """
        string = ""
        bucket_num = 0
        for item in self.table:
            string += "Bucket " + str(bucket_num) + ": "
            string += str(item)
            bucket_num += 1

        string += "\n"
        return string
