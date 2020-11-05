###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time


#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
FILENAME = "ps1_cow_data_2.txt"
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = {}
    file = open(filename, "r")
    for line in file:
        data = file.readline()
        data = data.strip().split(",")
        cow_dict.update ({data[0]:int(data[1])})
    return cow_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_by_wt = sorted (cows.items(), key = lambda x: x[1], reverse = True)

    trips = []
    total_wt = 0
    trip = []
    for i in range (0, len(cows_by_wt)):
        if (total_wt + cows_by_wt[i][1]) <= limit:
            trip.append (cows_by_wt[i][0])
            total_wt += cows_by_wt[i][1]
        else:
            trips.append(trip)
            trip = []
            total_wt = 0
            trip.append(cows_by_wt[i][0])
            total_wt += cows_by_wt[i][1]
    trips.append(trip)
    return trips
# Problem 3
print(greedy_cow_transport(load_cows(FILENAME)))
    
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    best_trip = cows
    for partition in get_partitions(cows):
        all_trip_wts = []
        for i in range (0, len(partition)):
            total_wt = 0
            for j in range (0, len(partition[i])):
                wt = cows.get(partition[i][j])
                total_wt += wt
            all_trip_wts.append(total_wt)
        
        if all(wt <= limit for wt in all_trip_wts):
            if len(partition) < len(best_trip ):
                best_trip = partition
    return best_trip            
print(brute_force_cow_transport(load_cows(FILENAME)))       
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows (FILENAME)
    start1 = time.time()
    greedy = greedy_cow_transport(cows)
    end1 = time.time()
    start2 = time.time()
    brute = brute_force_cow_transport(cows)
    end2 = time.time()
    print("Greedy returned ", len(greedy), " trips and took ", end1 - start1 , " seconds")
    print("Brute force returned ", len(brute), " trips and took ", end2 - start2 , " seconds")
    
compare_cow_transport_algorithms()