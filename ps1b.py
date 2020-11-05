###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
#top down 
def dp_make_weight(egg_weights, target_weight, memo = {0:0}): #for a target weight of 0, add 0 eggs 
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    if target_weight in memo:
        return memo[target_weight] #check if target weight is already in memo 
    value = 1 + min(
        dp_make_weight(egg_weights, target_weight - weight, memo)#add 1 egg of optimal weight from the list of available weights 
        for weight in egg_weights
        if  weight <= target_weight)#if the egg weight is greater than the target weight, don't execute 
    memo[target_weight] = value #store value for each target weight 
    return memo[target_weight]
#bottom up
def tab_make_weight(egg_weights, target_weight):
    opt_eggs = [0 for i in range(target_weight+1)] #make a list representing the optimal number of eggs where the index is the target weight
    for i in range (1, target_weight+1): #for a target weight of 0, add 0 eggs
        for j in egg_weights:
            if j <= i: 
                opt_eggs[i] = opt_eggs[i-j] + 1
    return opt_eggs[target_weight]
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print(dp_make_weight(egg_weights, n))
    print(tab_make_weight(egg_weights, n))

