#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 19:16:09 2018

COMS 4705: Natural language Processing
Programming Assignment 1
Question - 5.2
@author: apoorv purwar (UNI - ap3644)
"""

"""
Evaluation Result of Viterbi: 
    
Found 4704 NEs. Expected 5931 NEs; Correct: 3643.

        	 precision 	recall 		F1-Score
Total:	 0.774447	0.614230	    0.685096
PER:	     0.759749  	0.593580	    0.666463
ORG:	     0.611855	     0.478326	    0.536913
LOC:	     0.876458  	0.696292	    0.776056
MISC:	 0.830065	0.689468	    0.753262

"""

import math

# String literals -
__fname__ = "ner_dev.dat" 
f_rare = "ner_rare.counts"
__bigram_tag__ = "2-GRAM"
__trigram_tag__ = "3-GRAM"
__word_tag__ = "WORDTAG"
__unigram_tag__ = "1-GRAM"
__RARE__ = "_RARE_"

# Function to get the bigram and trigram count and calculate q
def getQCount(content_rare):
    
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
     
    # Get and store the q value for all the trigrams    
    q = dict()
    for (u, v, w) in count_tri:
        q[(u, v, w)] = float(count_tri[(u, v, w)]/count_bi[(u, v)])
     
    return q

# Function to calculate emission probabilities
def calcEmissionProb(count_xy, count_uni):
    emission = dict()
    #Iterate over count_xy dictionary
    for key, value in  count_xy.items():
        if key[0] not in emission:
            emission[key[0]] = dict()
        
        emission[key[0]][key[1]] = value/count_uni[key[1]]
      
    return emission

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

# Function to get tag sequence
def getTags(sentence, emission_dict, k):
    
    if(k < 0):
       tags = '*'
    else:
       tags = emission_dict[sentence[k]].keys()
        
    return tags

# Fetch q values from dictionary
def getQVal(q, u, v, w):
    if((u, v, w) in q):
        return q[(u, v, w)]
    else:
        return None

def getTagFromSeq(tag_seq, k):
    if(k < 0):
        tag = '*'
    else:
        tag = tag_seq[k]     
        
    return tag
 
# Function to calculate max log likelihood    
def calcLogLikelihood(sentence, tag_seq, pi):
    log_likelihood = []
    for k in range(len(sentence)):
        log_prob = math.log(pi[(k, getTagFromSeq(tag_seq, k-1), getTagFromSeq(tag_seq, k))])
        log_likelihood.append(log_prob)
    
    return log_likelihood

# Function to wrire the log prob and tags using Viterbi Algorithm
def writeViterbiTags(sentence, q, emission_dict, f_viterbi, clone_sentence):
    
    # pi values and the backpointer dictionary
    pi = dict()
    bp = dict()
    
    # Initialization of the base case
    pi[(-1, '*', '*')] = 1
    
    
    # Loop over tags 
    for k in range(len(sentence)):
    
        for u in  getTags(sentence, emission_dict, k-1):
            for v in getTags(sentence, emission_dict, k):
                # Setting default pi value to -1
                pi[(k, u, v)] = -1
                for w in getTags(sentence, emission_dict, k-2):
                    
                    q_maxLikelihood = getQVal(q, w, u, v)
                    
                    if(q_maxLikelihood is not None and pi[(k - 1, w, u)] > 0):
                        
                        if(pi[(k - 1, w, u)] == -1):
                            print("yes")
                        curr_probability = pi[(k - 1, w, u)] * q_maxLikelihood * emission_dict[sentence[k]][v]                        
                        
                        # Store max probabilities and the backpointers
                        if(pi[(k, u, v)]  < curr_probability):
                            pi[(k, u, v)] = curr_probability
                            bp[(k, u, v)] = w
                    #else:
                     #   print(pi[(k-1, w, u)])
                                
    
    # Tagged sequence 
    tag_seq = sentence[:]
    
    max_prob = -1
    n = len(sentence)
    
    # Generate the tag sequence for the current sentence
    for u in getTags(sentence, emission_dict, n-2):
        for v in getTags(sentence, emission_dict, n-1):
            q_maxLikelihood = getQVal(q, u, v, 'STOP')
            if(q_maxLikelihood != None):
                if(max_prob < pi[(n - 1, u, v)] * getQVal(q, u, v, 'STOP')):
                    max_prob = pi[(n - 1, u, v)] * getQVal(q, u, v, 'STOP')
                    tag_seq[n - 2] = u
                    tag_seq[n - 1] = v
    
    for k in range(n - 3, -1, -1):
        tag_seq[k] = bp[(k + 2, tag_seq[k + 1], tag_seq[k + 2])]
    
    # Calculate the log likelihood for given tag sequence
    log_likelihood = calcLogLikelihood(sentence, tag_seq, pi)
    
    
    
    # Write the words into the file
    for (word, tag, prob) in zip(clone_sentence, tag_seq, log_likelihood):
        f_viterbi.write(word + " " + tag + " " + str(prob) + "\n")
    f_viterbi.write("\n")    


                    
    

if __name__ == "__main__":  
        
    #Open file with word counts
    with open(f_rare) as frare:
        content_rare = frare.readlines()
    
    content_rare = [x.strip() for x in content_rare]
    
    q = getQCount(content_rare)
    
    # Calculate emission and unigram counts
    count_xy, count_uni = countEmissionAndUnigram(content_rare)
      
    # Calculate emission probabilities
    emission_dict = calcEmissionProb(count_xy, count_uni) 
    
    with open(__fname__) as f:
        content = f.readlines()
        
    content = [x.strip() for x in content]  
    
    f_viterbi = open("5_2.txt","w+") 
    
    # Formulate sentences and pass to Viterbi to get log probabilities
    sentence = list()
    clone_sentence = list()
    for word in content:
        if word == '':
            writeViterbiTags(sentence, q, emission_dict, f_viterbi, clone_sentence)
            sentence[:] = []
            clone_sentence[:] = []
        else:
            if word in emission_dict:
                sentence.append(word)
                clone_sentence.append(word)
            else:
                sentence.append(__RARE__)
                clone_sentence.append(word)
            
    f_viterbi.close()      
    
    
    