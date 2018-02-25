#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 21:34:20 2018

COMS 4705: Natural language Processing
Programming Assignment 1
Question - 6
@author: apoorv purwar (UNI - ap3644)
"""

"""

Evaluation Results (with Parser) - 

Found 5822 NEs. Expected 5931 NEs; Correct: 4328.

        	 precision 	recall 		F1-Score
Total:	 0.743387	0.729725	     0.736493
PER:	      0.805886	0.774755	     0.790014
ORG:	      0.541162	0.668161	     0.597993
LOC:	      0.840826	0.754635	     0.795402
MISC:	 0.826948	0.679696	     0.746126
"""

import datetime, math

# String literals -
__word_tag__ = "WORDTAG"
__unigram_tag__ = "1-GRAM"
__rareword__ = '_RARE_'
__fname__ = "ner.counts" 
__bigram_tag__ = "2-GRAM"
__trigram_tag__ = "3-GRAM"
__fname__dev = "ner_dev.dat" 


# Functions to parse rare words
def rareWordParser(emission_dict, word):
        #is word is not rare, it need not be replaced
        if(emission_dict is not None and word in emission_dict):
            return word
        

        #classify as if numbers only
        if(word.isnumeric() and len(word) == 2):
           return "2_Digit_Num"
        if(word.isnumeric() and len(word) == 4):
           return "4_Digit_Num"
        if(not word.isalpha() and word.isalnum()):
           return "Digit_And_Alphabet"
 
        tokens = word.split("-")
        if(len(tokens) == 2 and len(tokens[0]) > 1 and len(tokens[1]) > 1 and tokens[0].isnumeric() and tokens[1].isnumeric()):
            return "Digit_And_Dash"
        
        tokens = word.split(".")
        if(len(tokens) == 2 and len(tokens[0]) > 1 and len(tokens[1]) > 1 and tokens[0].isnumeric() and tokens[1].isnumeric()):
            return "Digit_And_Period"
        
        tokens = word.split(",")
        if(len(tokens) == 2 and len(tokens[0]) > 1 and len(tokens[1]) > 1 and tokens[0].isnumeric()):
            return "Digit_And_Period"
        
        if(word.isnumeric()):
            return "Other_Number"
        
        if(word.istitle()):
            return "Init_Cap"
        
        if(word.isupper()):
            return "All_Caps"
        
        if(word.islower()):
            return "Lower_Case"
        
        if(len(word) == 2 and word[1]=='.'):
            return "Cap_Period"
        
        #check for date in month/day/year format (2 digit year)
        try:
            datetime.datetime.strptime(word, "%m/%d/%y")
            return "Digit_And_Slash"
        except Exception as e:
            pass

        #check for date in month/day/Year format (4 digit year)
        try:
            datetime.datetime.strptime(word, "%m/%d/%Y")
            return "Digit_And_Slash"
        except Exception as e:
            pass
        
        #if(word not in self.count_of_words):
        
        return "_OTHERS_"

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



def calcRare(count_xy):
    
    f_train_rare = open("ner_train_rare_new.dat","w+")
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
                word = rareWordParser(None, word)
                
            f_train_rare.write(word + " " + tag + "\n")
        else:
            f_train_rare.write("\n")    
        
if __name__ == "__main__":  
    
    # Open and read the file with counts
    with open(__fname__) as f:
        content = f.readlines()
    
    content = [x.strip() for x in content]
    
    # Calculate emission and unigram counts
    count_xy, count_uni = countEmissionAndUnigram(content)
      
   # Call RARE function here
    calcRare(count_xy)
    
    
    f_rare_new = open("ner_rare_new.counts", "r")
    content_rare_new = f_rare_new.readlines()
    
    q = getQCount(content_rare_new)
    
    # Calculate emission and unigram counts
    count_xy, count_uni = countEmissionAndUnigram(content_rare_new)
      
    # Calculate emission probabilities
    emission_dict = calcEmissionProb(count_xy, count_uni) 
    
    
    with open(__fname__dev) as f:
        content = f.readlines()
        
    content = [x.strip() for x in content]  
    
    f_viterbi = open("6.txt","w+") 
    
    
    # Formulate sentences and pass to Viterbi to get log probabilities
    sentence = list()
    clone_sentence = list()
    for word in content:
        if word == '':
            # Comment the line below to generate rare counts, run the count script - 
            # then uncomment the line below and rerun this code and run the evaluation script
            writeViterbiTags(sentence, q, emission_dict, f_viterbi, clone_sentence)
            sentence[:] = []
            clone_sentence[:] = []
        else:
            sentence.append(rareWordParser(emission_dict, word))
            clone_sentence.append(word)
            
    f_viterbi.close()      
    
    
    f.close()
    
    
    


