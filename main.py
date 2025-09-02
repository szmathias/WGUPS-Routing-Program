"""
main.py
WGUPS Routing Program main entry point.
Handles user interaction, package loading, truck routing, and delivery simulation.
"""

# Author: Zack Mathias | 010868562
# Course: C950 - Data Structures and Algorithms II
# Project: WGUPS Routing Program
# Purpose: Create a Hash Table and load packages from a CSV file into it.
#          Then, use an algorithm to pick which package to deliver next,
#          while meeting all constraints given in the package CSV.

# Standard Library
import datetime
from typing import List, Tuple

# Created Imports
import Graph
import Package

# Our constants
MAX_BINS = 10
MAX_PACKAGES_PER_TRUCK = 16
TRUCK_SPEED = 18

# Create our graph and address dictionaries from the distance table
graph, address_to_ids, ids_to_address = Graph.read_distances_to_graph("WGUPS Distance Table.csv")

# Set our start and current time
start_time = "08:00"
start_of_day = datetime.datetime.strptime(start_time, "%H:%M")
current_time = start_of_day

# prints the help menu containing all the possible commands
def print_menu() -> None:
    """
    Prints the help menu containing all possible commands for the WGUPS Routing Program.
    """
    # Program logo printed at the beginning
    print("+---------------------------------------------------+")
    print("|                       WGUPS                       |")
    print("|                 By: Zack Mathias                  |")
    print("+---------------------------------------------------+\n")
    print("Welcome to the WGUPS Routing Program! Our goal")
    print("is to efficiently distribute all packages by")
    print("their promised deadline.\n")
    print("Commands:")
    print("\t- time <hh:mm>           Sets current time")
    print("\t- reset                  Resets program to the start of day")
    print("\t- truck <number>         Prints truck info")
    print("\t- package <id>           Prints packages info")
    print("\t- print                  Prints everything")
    print("\t- quit                   Quit this program")
    print()


def get_input() -> list[str]:
    """
    Reads a line from user input, splits it into a list by whitespace, and transforms commands to lowercase.
    Returns:
        list[str]: List of command arguments.
    """
    line: list[str] = input("===> ").split()
    while not line:
        print()
        print("Please enter a command.")
        print("- Type \"quit\" to leave")
        print()
        line = input("===> ").split()

    for position in range(len(line)):
        line[position] = line[position].lower()

    return line


def validate_time(time_to_validate: str) -> bool:
    """
    Validates a time string in the format <hh:mm>.
    Args:
        time_to_validate (str): Time string to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    is_valid_time = True

    # Loops through each character making sure it's a digit or colon
    for char in range(len(time_to_validate)):
        if not time_to_validate[char].isdigit() and not time_to_validate[char] == ":":
            is_valid_time = False
            break

    # If it's still valid, we make sure only one colon is used as a seperator
    if is_valid_time and time_to_validate.count(":") != 1:
        is_valid_time = False

    if is_valid_time:
        # Split the string into two parts and make sure they aren't empty
        time_values = time_to_validate.split(":")
        for time in time_values:
            if not time:
                is_valid_time = False

        # Lastly, check to make sure the hour is between [0, 23] and minute is between [0, 59]
        if is_valid_time and (int(time_values[0]) < 0 or int(time_values[0]) > 23 or int(time_values[1]) < 0 or int(
                time_values[1]) > 59):
            is_valid_time = False

    return is_valid_time


def change_time(time_input: list[str], time_to_change: datetime.datetime) -> datetime.datetime:
    """
    Changes the current time to a new datetime object if valid.
    Args:
        time_input (list[str]): Command arguments for time.
        time_to_change (datetime.datetime): Current time.
    Returns:
        datetime.datetime: New time if valid, else original time.
    """
    num_arguments = len(time_input)
    new_time: datetime = time_to_change

    # Check to see if we have the right argument count and it's a valid time
    if num_arguments == 2 and validate_time(time_input[1]):

        # Converts the time to a new datetime object then makes sure the time is in a range between the start
        # of day and end of day.
        new_time = datetime.datetime.strptime(time_input[1], "%H:%M")
        if new_time < start_of_day or new_time > datetime.datetime.strptime("17:00", "%H:%M"):
            new_time = time_to_change
            print("Please enter a time between 08:00 and 17:00\n")

    # If the number of arguments or the time isn't valid, then print error messages to guide the user
    # to the proper format
    else:
        if len(time_input) != 2:
            print("Time requires one argument.")

        else:
            print("\"" + time_input[1] + "\" is not a valid time.")
        print("Please enter as \"time <hh:mm>\"")
        print()

    return new_time


# The main algorithm we use to find our next package location.
def find_next_location(current_truck: List[Package], current_location: int) -> Tuple[int, float, Package]:
    """
    Finds the next closest package location for delivery.
    Args:
        current_truck (List[Package]): List of packages on the truck.
        current_location (int): Current location ID.
    Returns:
        Tuple[int, float, Package]: Next location ID, distance, and package to deliver.
    """
    # next_location holds the index of our next location from our graph.
    # closest_distance with hold the mileage of the closest location, it's set to infinity to ensure any distance is closer.
    # package_to_deliver is the package of the closest location which we return to deliver.
    next_location = 0
    closest_distance = float("inf")
    package_to_deliver: Package = None

    # Loop through each package left in the truck
    for next_package in current_truck:

        # If a path between the current location and the next address exists and the distance between location is
        # less then the current closest distance, then we update all of our variables
        if graph.has_edge(current_location, address_to_ids[next_package.address]) and graph.get_edge(current_location,
                                                                                                     address_to_ids[
                                                                                                         next_package.address]) < closest_distance:
            closest_distance = graph.get_edge(current_location, address_to_ids[next_package.address])
            next_location = address_to_ids[next_package.address]
            package_to_deliver = next_package

    return next_location, closest_distance, package_to_deliver


# Delivers packages from the current truck starting from a start time and ending deliveries when
# the finish time specified is reached.
def deliver_packages(current_truck: List[Package], start_run: datetime.datetime,
                     finish_time: datetime.datetime) -> Tuple[float, bool, datetime.datetime]:
    """
    Delivers packages from the current truck, simulating delivery until finish_time is reached.
    Args:
        current_truck (List[Package]): List of packages on the truck.
        start_run (datetime.datetime): Start time of delivery run.
        finish_time (datetime.datetime): Time to stop delivery simulation.
    Returns:
        Tuple[float, bool, datetime.datetime]: Total distance traveled, whether truck is at hub, and current time.
    """
    # Safety check: if start_run >= finish_time, return immediately
    if start_run >= finish_time:
        return 0.0, True, start_run
    
    # Safety check: if no packages, return immediately
    if not current_truck:
        return 0.0, True, start_run
    # Change the status of all trucks to en route
    for next_package in current_truck:
        next_package.status = "En route"

    # The truck starts at the hub.
    # Truck time is the time elapsed since start_run
    truck_location = address_to_ids["HUB"]
    distance = 0.0
    truck_time: datetime.datetime = start_run
    done_deliveries = False

    # While we have packages to deliver, continue to deliver packages.
    while current_truck and not done_deliveries:
        truck_location, next_distance, package_to_deliver = find_next_location(current_truck, truck_location)

        # Makes sure the truck isn't at the hub
        if truck_location != 0:
            delivery_time = truck_time + datetime.timedelta(minutes=(next_distance / (TRUCK_SPEED / 60)))

            # If our current time is less than the finish time:
            # - set package delivery time
            # - set package delivery time to Delivered
            # - update the trucks current time
            # - remove the package from the truck
            # - add the distance traveled to our total distance
            if delivery_time <= finish_time:
                package_to_deliver.delivery_time = delivery_time
                package_to_deliver.status = "Delivered"
                truck_time = delivery_time
                current_truck.remove(package_to_deliver)
                distance += next_distance

            # If the delivery time exceeds the finish time, then the truck is en route to another location but
            # can't reach the delivery location before the finish time:
            # - calculate the time left between the current time and finish time
            # - add the distance the truck traveled so far
            # - we're delivering
            elif current_truck:
                interim_time = (finish_time - truck_time) / datetime.timedelta(minutes=60)
                distance += TRUCK_SPEED * interim_time
                done_deliveries = True

    # Get the distance from the current location to the Hub and calculate the time
    next_distance = graph.get_edge(truck_location, address_to_ids["HUB"])
    time = truck_time + datetime.timedelta(minutes=(next_distance / (TRUCK_SPEED / 60)))
    at_hub = False

    # Check if the truck is empty
    if not current_truck:

        # If the time to get to the Hub is less than the finish time, then we made
        # it to the hub after delivering all the packages
        if time < finish_time:
            distance += next_distance
            at_hub = True

        # Otherwise, we're still traveling to the Hub, but we won't make it back
        # before the finish time, so we get the distance traveled so far.
        else:
            interim_time = (finish_time - truck_time) / datetime.timedelta(minutes=60)
            distance += TRUCK_SPEED * interim_time

    return distance, at_hub, time

def main():
    """
    Main entry point for the WGUPS Routing Program. Handles user interaction and simulation loop.
    """
    # Create the initial hash table, graph, address to id dict, and id to address dict
    global current_time
    hash_table = Package.read_packages("WGUPS Package File.csv")


    # Initialize distances to 0
    truck_1_distance = 0.0
    truck_2_distance = 0.0
    truck_3_distance = 0.0
    total_distance = 0.0

    # Separate normal and constrained packages
    normal_packages, constrained_packages = Package.separate_packages(hash_table)

    # Filter packages into the three trucks
    truck_1, truck_2, truck_3 = Package.filter_constrained_packages(normal_packages, constrained_packages,
                                                                    hash_table,
                                                                    MAX_PACKAGES_PER_TRUCK)

    # Sort the packages by deadline so the packages with the shortest deadline get loaded first.
    normal_packages.sort(key=lambda package_to_sort: package_to_sort.deadline)

    # Load truck 1 and 2
    truck_1 = Package.load_truck(truck_1, normal_packages, MAX_PACKAGES_PER_TRUCK)
    truck_2 = Package.load_truck(truck_2, normal_packages, MAX_PACKAGES_PER_TRUCK)

    done = False
    while not done:

        print_menu()
        # Print the current time set and wait for user input
        print("Current time is " + str(current_time.hour).zfill(2) + ":" + str(current_time.minute).zfill(2))
        user_input = get_input()
        print()

        # Used to quit
        if user_input[0] == "quit":
            done = True

        # Resets the time to the start of the day or to the specified time
        elif user_input[0] == "time" or user_input[0] == "reset":

            # Choose what to set the current time to
            if user_input[0] == "reset":
                current_time = start_of_day

            else:
                current_time = change_time(user_input, current_time)

            # Reset all packages, trucks, and the hash table
            normal_packages.clear()
            constrained_packages.clear()

            truck_1.clear()
            truck_2.clear()
            truck_3.clear()

            hash_table = Package.read_packages("WGUPS Package File.csv")

            # Reseparate and filter the packages
            normal_packages, constrained_packages = Package.separate_packages(hash_table)

            truck_1, truck_2, truck_3 = Package.filter_constrained_packages(normal_packages, constrained_packages,
                                                                            hash_table,
                                                                            MAX_PACKAGES_PER_TRUCK)

            # Sort packages based on deadline and load them into truck 1 and 2
            normal_packages.sort(key=lambda package_to_sort: package_to_sort.deadline)
            truck_1 = Package.load_truck(truck_1, normal_packages, MAX_PACKAGES_PER_TRUCK)
            truck_2 = Package.load_truck(truck_2, normal_packages, MAX_PACKAGES_PER_TRUCK)

            # Send both trucks out to deliver packages (only if current_time is after start_of_day)
            if current_time > start_of_day:
                truck_1_distance, truck_1_at_hub, truck_1_time = deliver_packages(truck_1, start_of_day, current_time)
                truck_2_distance, truck_2_at_hub, truck_2_time = deliver_packages(truck_2, start_of_day, current_time)
            else:
                # At start of day, trucks haven't moved yet
                truck_1_distance, truck_1_at_hub, truck_1_time = 0.0, True, start_of_day
                truck_2_distance, truck_2_at_hub, truck_2_time = 0.0, True, start_of_day

            # If the current time given is different then the start of day, we check if the delayed or package with
            # the wording address are at the Hub
            if current_time > start_of_day:
                for package in list(constrained_packages):
                    if package.status == "Delayed" or package.status == "Updating Address":

                        # Get the time specified in the special notes
                        time_string = package.special_notes.split()
                        arrival_time = datetime.datetime.strptime(time_string[1] + " " + time_string[2], "%I:%M %p")

                        # If the time the user gave is after the arrival time of the package, we update the status and
                        # add the package to normal packages
                        if arrival_time <= current_time:

                            # This updates the address for the package with the wrong address
                            if package.status == "Updating Address":
                                package.address = "410 S State St"
                                package.city = "Salt Lake City"
                                package.state = "UT"
                                package.zip_code = 84111

                            # Set a new deadline and status
                            package.deadline = datetime.datetime.strptime("5:00 pm", "%I:%M %p")
                            package.status = "At the Hub"
                            normal_packages.append(package)
                            constrained_packages.remove(package)

            # If truck 1 made it back to the hub, we load it with the available packages and send it back out
            if truck_1_at_hub:
                leftover_packages = []

                # Iterate over all the unconstrained packages
                for package in list(normal_packages):

                    # If it was arriving late we check to make sure the truck made it back to the hub
                    # after the package got to the hub
                    if "Arriving" in package.special_notes:
                        time_string = package.special_notes.split()
                        arrival_time = datetime.datetime.strptime(time_string[1] + " " + time_string[2], "%I:%M %p")
                        if truck_1_time >= arrival_time:
                            leftover_packages.append(package)
                            normal_packages.remove(package)

                    # Otherwise, add it to the packages to load into truck 3
                    else:
                        leftover_packages.append(package)
                        normal_packages.remove(package)

                # Load truck 3 with the available packages leftover
                truck_3 = Package.load_truck(truck_3, leftover_packages, MAX_PACKAGES_PER_TRUCK)

                # If truck 3 has packages, we send it out to deliver them
                if truck_3:
                    truck_3_distance, truck_3_at_hub, truck_3_time = deliver_packages(truck_3, truck_1_time, current_time)

            # If truck 2 made it back to the hub, we load it with the available packages and send it back out
            if truck_2_at_hub:
                leftover_packages = []

                # Iterate over all the unconstrained packages
                for package in list(normal_packages):

                    # If it was arriving late we check to make sure the truck made it back to the hub
                    # after the package got to the hub
                    if "Arriving" in package.special_notes:
                        time_string = package.special_notes.split()
                        arrival_time = datetime.datetime.strptime(time_string[1] + " " + time_string[2], "%I:%M %p")
                        if truck_2_time >= arrival_time:
                            leftover_packages.append(package)
                            normal_packages.remove(package)

                    # Otherwise, add it to the packages to load into truck 1
                    else:
                        leftover_packages.append(package)
                        normal_packages.remove(package)

                # Load truck 1 with the available packages leftover
                truck_1 = Package.load_truck(truck_1, leftover_packages, MAX_PACKAGES_PER_TRUCK)

                # If truck 1 has packages, we send it out to deliver them
                if truck_1:
                    truck_1_distance2, truck_1_at_hub, truck_1_time = deliver_packages(truck_1, truck_2_time, current_time)
                    truck_1_distance += truck_1_distance2

            # Add the distances together for the total
            total_distance = truck_1_distance + truck_2_distance + truck_3_distance

        # Prints the specified package
        elif user_input[0] == "package":

            # Make sure the user gave an id
            if len(user_input) == 2:

                # Verify it's a number
                is_valid = True
                for i in range(len(user_input[1])):
                    if not user_input[1][i].isdigit():
                        is_valid = False

                # verify the number is between 1 and the number of keys in the hash table
                if is_valid and hash_table.num_keys >= int(user_input[1]) >= 1:
                    print(hash_table.lookup(int(user_input[1])))

                # The user didn't give a valid id
                else:
                    print("\"" + str(user_input[1]) + "\" is not a valid package id.")
                    print("Please enter \"package <id>\" with an <id> between 1 and " + str(hash_table.num_keys) + ".")

            # The user didn't give one argument
            else:
                print("package requires one argument.")
                print("Please enter \"package <id>\" with an <id> between 1 and " + str(hash_table.num_keys) + ".")

            print()

        # Print specified truck info
        elif user_input[0] == "truck":

            # Make sure the user gave a number
            if len(user_input) == 2:

                # Verify it's a number
                is_valid = True
                for i in range(len(user_input[1])):
                    if not user_input[1][i].isdigit():
                        is_valid = False

                # verify the number is between 1 and 3
                if is_valid and 3 >= int(user_input[1]) >= 1:
                    print("Truck " + user_input[1])
                    if user_input[1] == "1":
                        truck = truck_1
                        truck_distance = truck_1_distance

                    elif user_input[1] == "2":
                        truck = truck_2
                        truck_distance = truck_2_distance

                    else:
                        truck = truck_3
                        truck_distance = truck_3_distance

                    # Print the truck mileage and packages left to deliver.
                    print(f"- Current distance: {truck_distance:.1f} miles")
                    print("- Packages to deliver: " + str(len(truck)))
                    for package in truck:
                        print(package)

                # The user didn't give a valid truck number
                else:
                    print("\"" + str(user_input[1]) + "\" is not a valid truck number.")
                    print("Please enter \"truck <number>\" with an <number> between 1 and 3.")

            # The user didn't give one argument
            else:
                print("truck requires one argument.")
                print("Please enter \"truck <number>\" with a <number> between 1 and 3.")

            print()

        # Prints all info
        elif user_input[0] == "print":

            # Prints the total distance and packages that haven't been loaded yet
            print(f"- Total distance traveled so far: {total_distance:.1f} miles")
            print("- Packages not loaded yet: " + str(len(normal_packages) + len(constrained_packages)))
            for package in normal_packages:
                print(package)

            for package in constrained_packages:
                print(package)

            print()

            # Print truck 1, 2, and 3
            for number in range(1, 4):
                print("Truck " + str(number) + ":")
                truck = truck_1
                truck_distance = truck_1_distance
                if number == 2:
                    truck = truck_2
                    truck_distance = truck_2_distance

                elif number == 3:
                    truck = truck_3
                    truck_distance = truck_3_distance

                # Prints the mileage and packages left to deliver
                print(f"- Current distance: {truck_distance:.1f} miles")
                print("- Packages to deliver: " + str(len(truck)))
                if not truck:
                    print("No packages to deliver.")
                for package in truck:
                    print(package)

                print()

            # Get the number of packages delivered
            count = 0
            for index in range(1, hash_table.num_keys + 1):
                if hash_table.lookup(index).status == "Delivered":
                    count += 1

            # Print the packages delivered so far
            print("Packages delivered: " + str(count))
            for index in range(1, hash_table.num_keys + 1):
                temp = hash_table.lookup(index)
                if temp.status == "Delivered":
                    print(temp)

            if count == 0:
                print("No packages delivered yet.")

            print()


        # The user didn't give a valid command
        else:
            print("\"" + user_input[0] + "\" is not a valid command.")
            print()



    print(f"Total distance traveled: {total_distance:.1f} miles")

if __name__ == "__main__":
    main()
    main()