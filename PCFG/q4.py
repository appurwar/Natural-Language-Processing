#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:10:56 2018
COMS 4705: Natural Language Processing
Programming Assignemnt 2 - Question 4
@Author - Apoorv Purwar (ap3644)
"""

import json
import sys

# String Literals
__ftrain__ = sys.argv[1]
__ftrainRare__ = sys.argv[2]
__unary__ = 'UNARYRULE'
__RARE__ = '_RARE_'
# Generated cfg.counts file
__cfgCount__ = 'cfg.counts'

# Function to get the word counts
def getWordCounts():
    
    # Open and read cfg counts
    with open(__cfgCount__) as f:
        content = f.readlines()
    
    # Remove the new line character
    count_lines = [x.strip() for x in content]
    
    # Split each line based on blank space
    count_lines = [x.split() for x in count_lines]
    
    # Dictionary to keep a word count
    word_count = dict()
    
    # Iterate over all the lines with different counts
    for row in count_lines:
        # Check if it is a unary rule
        if(row[1] == __unary__):
            # Sum all the appearances of a paricular word
            if(word_count.get(row[3]) is None):
                word_count[row[3]] = int(row[0])
            else:
                word_count[row[3]] = int(word_count.get(row[3])) + int(row[0])

    return word_count 

# Function to create the list of rare words
def getRareWordList(word_count_dict):
    
    # List to store all the rare words
    rare_list = []
    
    # Loop over count dictionary to get rare words
    for key, value in word_count_dict.items():
        # Count < 5 implies rare word
        if(value < 5): 
            rare_list.append(key)
            
    return rare_list

# Recursive function to replace with rare words
def replaceList(curr_list, rare_list):
    if(len(curr_list) == 3):
        # Recursive call on 1 and 2 position of current list
        replaceList(curr_list[1], rare_list)
        replaceList(curr_list[2], rare_list)
    elif(len(curr_list) == 2):
        # Check for rare word
        if(curr_list[1] in  rare_list):
            # Replace with RARE 
            curr_list[1] = __RARE__
    

# Functiont to replace rare words with _RARE_
def replaceWithRare(rare_list):
    
    # Open and read the training file
    with open(__ftrain__) as f:
        content = f.readlines()
        
    # Open a new file to write rare words
    f_rare = open(__ftrainRare__, 'w+')
    
    # Remove the new line character
    content = [x.strip() for x in content]
    
    # Iterare over each line in content
    for line in content:
        curr_list = json.loads(line)
        if(len(curr_list) == 3):   
            # Function to recursively replace the rare words (by reference)
            replaceList(curr_list, rare_list)
            # Write the replaced list to file
            f_rare.write(json.dumps(curr_list) + '\n')
        elif(curr_list[2] in rare_list):
            # Replace with RARE 
            curr_list[2] = __RARE__
            # Write the replaced list to file
            f_rare.write(json.dumps(curr_list) + '\n')
    
    # Close the file
    f_rare.close()

# Main driver function
if __name__ == "__main__": 
    
    # Get the individual word counts
    word_count_dict = getWordCounts()
    
    # Create list of rare words
    rare_list = getRareWordList(word_count_dict)
    
    replaceWithRare(rare_list)
   
    
    
    
    