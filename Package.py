"""
Package.py
Defines the Package class and helper functions for package management, loading, and filtering.
"""

# Author: Zack Mathias | 010868562
# Course: C950 - Data Structures and Algorithms II
# Project: WGUPS Routing Program
# File: Package.py
# Purpose: Holds all the package info and has helper
#          functions related to the packages

# Standard Library
import csv
import datetime
from typing import List, Tuple

# Created Imports
from HashTable import HashTable


# Used to help format the Package string for consistent width
def left_pad(value: any, width: int, pad_char: str = " ") -> str:
    """
    Pads a value on the left with a specified character to a given width.
    Args:
        value (any): Value to pad.
        width (int): Desired width.
        pad_char (str): Padding character.
    Returns:
        str: Padded string.
    """
    result = ""

    # Check if the length of the value is less than the desired width
    if len(str(value)) < width:

        # The padding to add is the width minus the length of the value
        added_padding = width - len(str(value))

        # Adds the padding character
        for i in range(added_padding):
            result += pad_char

    # Adds the value string to the result
    result += str(value)
    return result


# Wraps all the Package info into a single object
class Package:
    """
    Represents a delivery package with all relevant information and status.
    """
    def __init__(self, package_id: int = -1, address: str = "", city: str = "", state: str = "", zip_code: int = -1,
                 deadline: datetime.datetime = datetime.datetime(year=1, month=1, day=1, hour=0, minute=0),
                 weight: int = 0,
                 special_notes: str = "",
                 status: str = "None",
                 delivery_time: datetime.datetime = datetime.datetime(year=1, month=1, day=1, hour=0, minute=0)):
        """
        Initializes a Package object.
        Args:
            package_id (int): Package ID.
            address (str): Delivery address.
            city (str): Delivery city.
            state (str): Delivery state.
            zip_code (int): Delivery zip code.
            deadline (datetime.datetime): Delivery deadline.
            weight (int): Package weight.
            special_notes (str): Special notes or constraints.
            status (str): Current status.
            delivery_time (datetime.datetime): Delivery time.
        """
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = status
        self.delivery_time = delivery_time

    # Prints the deadline in a hh:mm format
    def print_deadline(self) -> None:
        """
        Prints the package deadline in hh:mm format.
        """
        print(str(self.deadline.hour) + ":" + str(self.deadline.minute).zfill(2))

    # Prints the delivery time in a hh:mm:ss format
    def print_delivery_time(self) -> None:
        """
        Prints the package delivery time in hh:mm:ss format.
        """
        print(str(self.delivery_time.hour) + ":" + str(self.delivery_time.minute).zfill(2) + ":" + str(
            self.delivery_time.second).zfill(2))

    # Returns a formatted string with all the package info
    def __str__(self) -> str:
        """
        Returns a formatted string with all package info.
        Returns:
            str: Formatted package information.
        """
        pid = left_pad(self.id, 2)
        address = left_pad(self.address, 38)
        city = left_pad(self.city, 16)
        status = left_pad(self.status, 16)
        weight = left_pad(self.weight, 2)

        delivery_time = "Not delivered"
        if self.delivery_time.hour != 0:
            delivery_time = str(self.delivery_time.hour).zfill(2) + ":" + str(self.delivery_time.minute).zfill(2)
        delivery_time = left_pad(delivery_time, len("Not delivered"))

        string = "[" + pid + ", "
        string += address + ", "
        string += city + ", "
        string += self.state + ", "
        string += str(self.zip_code) + ", "
        string += weight + "kg, "
        string += status + ", "
        string += "Deadline: " + str(self.deadline.hour).zfill(2) + ":" + str(self.deadline.minute).zfill(2) + ", "
        string += "Delivery Time: " + delivery_time + "]"

        return string


# Reads packages in from a CSV file and returns a hash table containing
# all packages.
def read_packages(package_file: str) -> HashTable:
    """
    Reads packages from a CSV file and returns a hash table containing all packages.
    Args:
        package_file (str): Path to the package CSV file.
    Returns:
        HashTable: Hash table of packages.
    """
    hash_table = HashTable()
    with open(package_file, mode='r') as file:
        csv_file = csv.reader(file)
        skip = True

        # Read every line in the file, skipping the first line
        for line in csv_file:
            if not skip:

                # The time format is in hh:mm [am|pm].
                # If time read is EOD change it to 5:00 pm
                time_format = "%I:%M %p"
                time_string = line[5]
                if time_string == "EOD":
                    time_string = "5:00 PM"

                # Create a new package
                deadline = datetime.datetime.strptime(time_string, time_format)
                p = Package(int(line[0]), line[1], line[2], line[3], int(line[4]), deadline, int(line[6]), line[7])

                # in this section, I use unique words in the special notes to standardize the special notes
                # and status

                # Hard coded for wrong address
                if "Wrong" in line[7]:
                    p.status = "Updating Address"
                    p.special_notes = "Arriving 10:20 am"

                # If a package is delayed, we combined Arriving with the end of the line which
                # has the time it'll arrive.
                elif "Delayed" in line[7]:
                    p.status = "Delayed"
                    string = "Arriving "
                    index = 0
                    for char in line[7]:
                        if char.isdigit():
                            string += line[7][index:]
                            break
                        index += 1

                    p.special_notes = string

                # If the package needs to be in a certain truck, we combine the word truck with
                # the number located at the end of the truck
                elif "truck" in line[7]:
                    p.status = "At the Hub"
                    p.special_notes = "Truck "
                    p.special_notes += line[7][len(line[7]) - 1]

                # If the package must be with other packages, we combine package with
                # the packages listed at the end of the line. We replace commas with
                # spaces to make parsing easier
                elif "Must be" in line[7]:
                    p.status = "At the Hub"
                    string = "Package "
                    index = 0
                    for char in line[7]:
                        if char.isdigit():
                            string += line[7][index:]
                            string = string.replace(",", "")
                            break
                        index += 1

                    p.special_notes = string

                # Otherwise, the package doesn't have any constraints
                else:
                    p.status = "At the Hub"

                hash_table.insert(int(line[0]), p)

            else:
                skip = False

    return hash_table


# Helper function that splits packages loosely by their constraints.
# This doesn't account for packages that need to be with other packages.
def separate_packages(hash_table: HashTable) -> Tuple[List[Package], List[Package]]:
    """
    Splits packages by constraints into normal and constrained lists.
    Args:
        hash_table (HashTable): Hash table of packages.
    Returns:
        tuple[list[Package], list[Package]]: (normal_packages, constrained_packages)
    """
    normal_packages = []
    constrained_packages = []
    for i in range(1, hash_table.num_keys + 1):
        package = hash_table.lookup(i)
        if package.status == "At the Hub" and package.special_notes == "":
            normal_packages.append(package)

        else:
            constrained_packages.append(package)

    return normal_packages, constrained_packages


# Separate normal and constrained packages into the three trucks
def filter_constrained_packages(normal_packages: List[Package], constrained_packages: List[Package],
                                hash_table: HashTable, max_packages_per_truck: int) -> Tuple[
    List[Package], List[Package], List[Package]]:
    """
    Separates normal and constrained packages into three trucks based on constraints.
    Args:
        normal_packages (list[Package]): List of normal packages.
        constrained_packages (list[Package]): List of constrained packages.
        hash_table (HashTable): Hash table of packages.
        max_packages_per_truck (int): Maximum packages per truck.
    Returns:
        tuple[list[Package], list[Package], list[Package]]: (truck_1, truck_2, truck_3)
    """
    # Create three empty trucks
    truck_1: list[Package] = []
    truck_2: list[Package] = []
    truck_3: list[Package] = []

    # Loops through each constrained package from a copied list, so we
    # can remove the package after we sort it
    for package in list(constrained_packages):

        # Checks to see if the package needs to be in a certain truck.
        if "Truck" in package.special_notes:
            if package.special_notes[len(package.special_notes) - 1] == "1" and len(truck_1) < max_packages_per_truck:
                truck_1.append(package)
                constrained_packages.remove(package)

            elif package.special_notes[len(package.special_notes) - 1] == "2" and len(truck_2) < max_packages_per_truck:
                truck_2.append(package)
                constrained_packages.remove(package)

            elif package.special_notes[len(package.special_notes) - 1] == "3" and len(truck_3) < max_packages_per_truck:
                truck_3.append(package)
                constrained_packages.remove(package)

        # Checks if the package needs to be with other packages. If they do, check to see
        # if the package is in the normal packages list. If it is, remove it and add it to truck 1
        elif "Package" in package.special_notes:
            line = package.special_notes[len("Package "):]
            package_ids = line.split(" ")
            for package_id in package_ids:
                temp_package = hash_table.lookup(int(package_id))
                if package and normal_packages.count(temp_package) >= 1:
                    normal_packages.remove(temp_package)
                    truck_1.append(temp_package)

            constrained_packages.remove(package)
            truck_1.append(package)

    return truck_1, truck_2, truck_3


# Loads packages onto the truck until the truck is full, or we run out of packages.
def load_truck(truck: List[Package], packages: List[Package], max_packages_per_truck: int) -> List[Package]:
    """
    Loads packages onto a truck until full or out of packages.
    Args:
        truck (list[Package]): Truck to load.
        packages (list[Package]): Packages to load.
        max_packages_per_truck (int): Maximum packages per truck.
    Returns:
        list[Package]: Loaded truck.
    """
    index = 0
    temp_list = list(packages)
    while len(truck) < max_packages_per_truck and len(packages) > 0:
        truck.append(temp_list[index])
        packages.remove(temp_list[index])
        index += 1

    return truck
