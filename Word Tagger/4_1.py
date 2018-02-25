#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:33:41 2018

COMS 4705: Natural language Processing
Programming Assignment 1
Question - 4.1
@author: apoorv purwar (UNI - ap3644)
"""

# String literals -
__word_tag__ = "WORDTAG"
__unigram_tag__ = "1-GRAM"
__rareword__ = '_RARE_'

#File with emission probabilities
fname = "ner.counts"    

# Function to calculate emission and unigram counts
def countEmissionAndUnigram(content):
    
    # Dictionaries to store counts
    count_xy = dict()
    count_uni = dict()
    # Tuple to store word and tags
    word_tag_tuple = tuple()

    for line in content:
        
        words = line.split()
    
        if(words[1]==__word_tag__):
            word_tag_tuple = (words[3], words[2])
            # Stores {(word, tag): count} emission count 
            count_xy[word_tag_tuple] = int(words[0])
        elif(words[1]==__unigram_tag__):
            # Stores {tag:tag_count} for unigrams 
            count_uni[words[2]] = int(words[0])  
    
    return count_xy, count_uni

# Function to calculate emission probabilities
def calcEmissionProb(count_xy, count_uni):
    emission = dict()
    #Iterate over count_xy dictionary
    for key, value in  count_xy.items():
        if key[0] not in emission:
            emission[key[0]] = dict()
        
        emission[key[0]][key[1]] = value/count_uni[key[1]]
      
    return emission

def calcRare(count_xy):
    
    f_train_rare = open("ner_train_rare.dat","w+")
    f_train = open("ner_train.dat")
     # Replace RARE words 
    word_count = dict()         # Dictionary to store total count per word - {word: count}
    
    for key, value in count_xy.items():
      #  print(word_count[key[0]])
        if(key[0] in word_count):
            word_count[key[0]] += value
        else:
            word_count[key[0]] = value
    
    
    for line in f_train.readlines():
        if(line.strip() != ''):
            
            word, tag = line.strip().split()
            if(word_count[word] < 5):
                word = __rareword__
                
            f_train_rare.write(word + " " + tag + "\n")
        else:
            f_train_rare.write("\n")           
            
        
if __name__ == "__main__": 

    # Open and read the file with counts
    with open(fname) as f:
        content = f.readlines()
    
    content = [x.strip() for x in content]
    
    # Calculate emission and unigram counts
    count_xy, count_uni = countEmissionAndUnigram(content)
      
    # Calculate emission probabilities   
    emission_prob = calcEmissionProb(count_xy, count_uni)    
            
   # Call RARE function here
    calcRare(count_xy)
    
    f.close()
    
    
    
        