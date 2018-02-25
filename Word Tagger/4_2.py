#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:07:54 2018


COMS 4705: Natural language Processing
Programming Assignment 1
Question - 4.2
@author: apoorv purwar (UNI - ap3644)
"""

"""
Evaluation Results:

python eval_ne_tagger.py ner_dev.key 4_2.txt:
    
Found 14043 NEs. Expected 5931 NEs; Correct: 3117.

        	 precision 	recall 		F1-Score
Total:	 0.221961	0.525544	    0.312106
PER:	     0.435451	     0.231230	    0.302061
ORG:	     0.475936  	0.399103	    0.434146
LOC:	     0.147750	    0.870229	    0.252612
MISC:	 0.491689	0.610206	    0.544574
"""

import math

#Execute this file only after executint 4_1.py and 
# the script - python count_freqs.py ner_train_rare.dat > ner_rare.counts

# String literals -

__word_tag__ = "WORDTAG"
__unigram_tag__ = "1-GRAM"
__RARE__ = "_RARE_"
# File name for ner_dev dat file 
__fname__ = "ner_dev.dat" 
__fname_rare__ = "ner_rare.counts"


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


# Find tag and calculate log prob for RARE tag
def getArgMaxValues(emission_dict, tag):
    # Calculate max log rare prob and tage
    rare_probs = emission_dict[tag]
    max_rare_prob = 0
    # Iterate through dictionary of rare probs to get max
    for key, value in rare_probs.items():
        if(value > max_rare_prob):
            max_rare_prob = value
            max_rare_tag = key
            
    return math.log(max_rare_prob), max_rare_tag
     
if __name__ == "__main__": 
    
    # Open rare count and calcuate emission prob with rare count
    with open(__fname_rare__) as f_rare:
        content_rare = f_rare.readlines()
    
    content_rare = [x.strip() for x in content_rare]
    
    # Calculate emission and unigram counts
    count_xy, count_uni = countEmissionAndUnigram(content_rare)
      
    # Calculate emission probabilities
    emission_dict = calcEmissionProb(count_xy, count_uni)    
    
    # Open and read the file with counts
    with open(__fname__) as f:
        content = f.readlines()
    
    content = [x.strip() for x in content]
    
    # Get max rare prob details
    max_rare_prob, max_rare_tag = getArgMaxValues(emission_dict, __RARE__)
    
    # Open file to write argmax values:
    f_argmax = open("4_2.txt","w+")    
        
    for word in content:            # Iterate over the cotnents file containing words
        if word == '':
            f_argmax.write("\n")
        else:
            
            if word not in emission_dict:    # If word not in dictionary its a RARE word
                f_argmax.write(word + " " + max_rare_tag + " " + str(max_rare_prob) + "\n")
            else:
                max_prob, max_tag = getArgMaxValues(emission_dict, word)
                f_argmax.write(word + " " + max_tag + " " + str(max_prob) + "\n")
    
    # Close the file with rare count        
    f.close()
    f_rare.close() 