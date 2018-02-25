#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 16:31:58 2018

COMS 4705: Natural language Processing
Programming Assignment 1
Question - 5.1
@author: apoorv purwar (UNI - ap3644)
"""

import math

# String literals -
f_trigram = "trigrams.txt"
f_rare = "ner_rare.counts"
__bigram_tag__ = "2-GRAM"
__trigram_tag__ = "3-GRAM"

# Function to get the bigram and trigram count
def getBiAndTriGramCount(content_rare):
    
    count_bi = dict()
    count_tri = dict()
    
    for line in content_rare:   
        words = line.split()
        key = ()
        if(words[1]==__bigram_tag__):
            key = (words[2], words[3]) 
            # Stores {tag:tag_count} for bigrams 
            count_bi[key] = int(words[0])  
        elif(words[1]==__trigram_tag__):
            key = (words[2], words[3], words[4]) 
            # Stores {tag:tag_count} for trigrams 
            count_tri[key] = int(words[0])  
     
    return count_bi, count_tri

# Function to get the log emission prob for given trigrams 
def getLogProb(content, count_bi, count_tri):
    
    # File to write the emission probs of given trigrams
    f_emission = open("5_1.txt","w+") 
    
    for trigram in content:
        trigram = trigram.split()
        yi_2 = trigram[0]
        yi_1 = trigram[1]
        yi = trigram[2]
        
        # Create the keys for trigram and bigrams to be used to get counts
        trigram_key = (yi_2, yi_1, yi)
        bigram_key = (yi_2, yi_1)
        
        # Emission Prob = q(y(i) | y(i-1), y(i-2))
        emission_prob = math.log(count_tri[trigram_key]/count_bi[bigram_key])
        
        f_emission.write(yi_2 + " " + yi_1 + " " + yi + " " + str(emission_prob) + "\n")
        
    f_emission.close()
        

if __name__ == "__main__": 
    
    #Open file with word counts
    with open(f_rare) as frare:
        content_rare = frare.readlines()
    
    content_rare = [x.strip() for x in content_rare]
    
    count_bi, count_tri = getBiAndTriGramCount(content_rare)
    
    # Open and read the file with trigrams
    with open(f_trigram) as f:
        content = f.readlines()
    
    content = [x.strip() for x in content]
    
    getLogProb(content, count_bi, count_tri)
    
    frare.close()
    f.close()
    
    
        
        
    