#!/usr/bin/env python3
# -*- coding: utf8 -*-
import sys
import os
import traceback
import argparse
import time
import logging
import random
import numpy

def main():
  P_SIZE = 500 # population size
  # user id as index with desirability scores according to gaussian distribution
  # divided into straight men and women marriage market 
  male_scores = [random.gauss(5, 1.5) for i in range(P_SIZE/2)]
  female_scores = [random.gauss(5, 1.5) for i in range(P_SIZE)]

  
  # male proposing deferred acceptance
  def deferred_acc(male_scores, female_scores): 

    # return top preferred female in list of females
    def top_fem(fems):
      f_max_score = 0 
      f_id = None
      for f in fems:
        if female_scores[f] > f_max_score:
          f_max_score = female_scores[f]
          f_id = f
      return f_id

    matches = {} # dict of matches, stored as f: m

    male_prefs = [set(range(len(female_scores))) for m in male_scores] # set of females remaining for each male to propose to
    single_males = list(range(len(male_scores))) # queue of single males

    # cycle through all the single males until there are no more single males
    while single_males:
        male = single_males.pop()
        # propose to top female and remove it from options
        fem = top_fem(male_prefs[male])
        if not fem: # no more females for male to propose to, male remains single
          continue
        male_prefs[male].remove(fem)

        # unmatched female accepts, male is removed from single males
        if fem not in matches: 
          matches[fem] = male

        # if female's match has lower desirability than proposing male, female accepts
        elif male_scores[male] > male_scores[matches[fem]]:
          single_males.append(matches[fem])
          matches[fem] = male  

        # female rejects, add male to end of queue and go to next male
        else:
          single_males.append(male)

    return matches

  # calculate utility of matches based on scores representing utility
  def utility(matches):
    male_utility = 0 
    female_utility = 0
    for f in matches:
      male_utility += female_scores[f]
      female_utility += male_scores[matches[f]]

    return male_utility, female_utility

  # baseline
  
  print(utility(deferred_acc(male_scores, female_scores)))

  # tinder algorithm where people are matched by only being shown people within 10 people of their own scores
  def blocked(male_scores, female_scores): 

    # return top preferred female in list of females
    def top_fem(fems):
      f_max_score = 0 
      f_id = None
      for f in fems:
        if female_scores[f] > f_max_score:
          f_max_score = female_scores[f]
          f_id = f
      return f_id

    matches = {} # dict of matches, stored as f: m

    LIMIT = 0.5
    male_prefs = [set(female_scores.index(f) for f in female_scores if abs(f-m) <  LIMIT) for m in male_scores] # set of females remaining for each male to propose to
    single_males = list(range(len(male_scores))) # queue of single males

    # cycle through all the single males until there are no more single males
    while single_males:
        male = single_males.pop()
        # propose to top female and remove it from options
        fem = top_fem(male_prefs[male])
        if not fem: # no more females for male to propose to, male remains single
          continue
        male_prefs[male].remove(fem)

        # unmatched female accepts, male is removed from single males
        if fem not in matches: 
          matches[fem] = male

        # if female's match has lower desirability than proposing male, female accepts
        elif male_scores[male] > male_scores[matches[fem]]:
          single_males.append(matches[fem])
          matches[fem] = male  

        # female rejects, add male to end of queue and go to next male
        else:
          single_males.append(male)


    return matches

  # print(utility(blocked(male_scores, female_scores)))

  # female proposing
  # print(utility(deferred_acc(female_scores, male_scores)))

if __name__ == '__main__':
 for i in range(50):
    main ()