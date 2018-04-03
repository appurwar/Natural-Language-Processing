#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:10:56 2018
COMS 4705: Natural Language Processing
Programming Assignemnt 2 - Question 5
@Author - Apoorv Purwar (ap3644)
"""

import json
import sys

# String Literals
__unary__ = 'UNARYRULE'
__binary__ = 'BINARYRULE'
__nonTerminal__ = 'NONTERMINAL'

__RARE__ = '_RARE_'

# Generated cfg.counts file
__cfgCount__ = 'cfg_rare_q5.counts'
__parseDev__ = sys.argv[2]
__result__ = sys.argv[3]


# Function to get Unary, Binary and Non Terminal Counts
def getCounts():
    
    # Open and read the count frequency file
    with open(__cfgCount__) as f:
        content = f.readlines()
        
    # Remove the new line character
    content = [x.strip() for x in content]
    
    # Split each line based on blank space
    count_lines = [x.split() for x in content]
    
    # Declare Unary, Binary, Non Terminal and word Dict
    count_nt = dict()
    count_uni = dict()
    count_bi = dict()
    count_word = dict()
    words_list = []
    
    # Iterate over all the lines with different counts
    for row in count_lines:
        # Check if it is a unary rule
        if(row[1] == __unary__):
            # Store Unary counts
            if(count_uni.get(row[2]) is None):
                #count_uni[row[2]] = [{row[3]:int(row[0])}]
                count_uni[row[2]] = dict()
                count_uni[row[2]][row[3]] = int(row[0])
                if(row[3] not in words_list):
                    words_list.append(row[3])
            else:
                count_uni[row[2]][row[3]] = int(row[0])
                if(row[3] not in words_list):
                    words_list.append(row[3])
                
            # Sum all the appearances of a paricular word
            if(count_word.get(row[3]) is None):
                count_word[row[3]] = int(row[0])
            else:
                count_word[row[3]] = int(count_word.get(row[3])) + int(row[0])
        elif(row[1] == __nonTerminal__):
             # Create dictionary of count of unary rules
             if(count_nt.get(row[2]) is None):
                count_nt[row[2]] = int(row[0])
             else:
                count_nt[row[2]] = int(count_nt.get(row[2])) + int(row[0])
        elif(row[1] == __binary__):    
            # Create dictionary of count of binary rules
            if(count_bi.get(row[2]) is None):
                count_bi[row[2]] = dict()
                count_bi[row[2]][(row[3], row[4])] = int(row[0])
            else:
                count_bi[row[2]][(row[3], row[4])] = int(row[0])
    
    # Calculate the Params for Unary and Binary Rules
    for key,value in count_nt.items():
        if(key in count_uni):
            uni_dict = count_uni.get(key)
            # Iterate over all keys in count_uni
            for uni, uni_val in uni_dict.items():
                count_uni[key][uni] = uni_val/value
        
        if(key in count_bi):
            bi_dict = count_bi.get(key)
            # Iterate over all keys in count_uni
            for bi, bi_val in bi_dict.items():
                count_bi[key][bi] = bi_val/value
    
    return count_nt, count_word, count_bi, count_uni, words_list

def recurseTree(parent, i, j, bp):
    
    final_tree = []
    
    if(type(bp[(i,j,parent)]) == str):
        final_tree.append(parent)
        final_tree.append(bp[(i,j,parent)])
    else:
        s, Y, Z = bp[(i,j,parent)]
        left_tree = recurseTree(Y, i, s, bp)
        right_tree = recurseTree(Z, s+1, j, bp)
        final_tree.append(parent)
        final_tree.append(left_tree)
        final_tree.append(right_tree)
      
    return final_tree
    

def generate_tree(parent, bp, line_len):
    
    return recurseTree(parent, 0, line_len-1, bp)
    
    
# Main driver function
if __name__ == "__main__": 
    
    # Get the required counts of words
    count_nt, count_word, count_bi, count_uni, words_list = getCounts()
    
    #print(count_bi)
    with open(__parseDev__) as f:
        content = f.readlines()
        
    # Open the output files to write the results
    f_result = open(__result__, 'w+')
    
    # Remove the new line character
    content = [x.strip() for x in content]
    
    # Split each line based on blank space
    content = [x.split() for x in content]
    
    # Replace file with RARE words
    for i in range(len(content)):
        for j in range(len(content[i])):
            if content[i][j] not in words_list:
                content[i][j] = __RARE__
    
    # Iterate over all lines
    for line in content:
        line_len = len(line)
             
        # Dictionaries to store prob. and back pointers
        pi = dict()
        bp  = dict()
        
        # Create the base case of the tree (Unary Rules)
        for index in range(0,line_len):
            for X in count_uni:
                if line[index] not in count_uni[X]:
                    pi[(index, index, X)] = 0
                else:
                    pi[(index, index, X)] = count_uni[X][line[index]]
                    bp[(index, index, X)] = line[index]

        # CKY Algorithm
        for l in range(2,line_len+1):
            for i in range(0, line_len - l + 1):
                # Iniitalize j
                j = i + l - 1
                
                # Iterate over all non terminals
                for X in count_bi:
                    max_pi = 0
                    split_point = 0 
                    Y = None
                    Z = None
                    for birule in count_bi[X]:
                        for s in range(i,j):
                            # Dynamicaly build the dictionary
                            if((i,s,birule[0]) not in pi or (s+1,j, birule[1]) not in pi):
                                pi_curr = 0
                            else:   
                                pi_curr = count_bi[X][birule] * pi[i,s,birule[0]] * pi[s+1,j, birule[1]]
                                if(pi_curr > max_pi):
                                    max_pi = pi_curr
                                    split_point = s
                                    Y = birule[0]
                                    Z = birule[1]
                    
                    # Update pi for this location
                    pi[(i,j,X)] = max_pi
                    # Back Pointers
                    bp[(i,j,X)] = (split_point,Y,Z)
            
        parent = None
        # Finds the parent of the tree
        if(pi[(0,line_len-1,'S')] != 0):
            parent = 'S'
        else:
            max_prob = 0
            for X in count_bi:
                if(pi[(0,line_len-1,X)] > max_prob):
                    parent = X
                    max_prob = pi[(0,line_len-1,X)] 
        
        # Formulate the sentence from parse tree
        final_tree = generate_tree(parent, bp, line_len)
        f_result.write(json.dumps(final_tree) +'\n')
        
    
    f_result.close()
    
    
    