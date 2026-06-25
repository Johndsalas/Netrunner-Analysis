''' 
    Script for generating dataset for Netrunner Agendas and Accesses Study
       
    Data set includes:
    All legal combinations of studied deck building features where Let Them Dream is not included in the deck
    Additional rows simulating replacing the maximum number of 'normal' two-point agendas with Let Them Dream agendas for each of the previous builds containing two-point agendas
    Each combination saved as one row of data
    The access threshold was calculated and added to each row
    Data reflects the current standard legal card pool (April 21, 2026)
'''

# imports
import random
import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt

# max and min possible deck sizes for the corporation player
deck_sizes = [40, 44, 45, 49, 50, 54]

# maximum number of 1 2 and 3 point agendas that can be included based on current card pool and banned list (April 21)
max_ones = 15
max_twos = 36
max_threes = 12

def main(deck_sizes, max_ones, max_twos, max_threes):
    '''
        Takes in 
        List of all desired deck sizes
        Maximum number of one point agendas (by available card pool)
        Maximum number of three point agendas (by available card pool)
    
        Returns dataframe with all legal combinations of studied features 
        Adding Additional rows simulating replacing the maximum number of 
        'normal' two-point agendas with Let Them Dream agendas for each of 
        the previous builds containing two-point agendas
    '''

    # get empty dictionary
    agenda_dictionary = {

                        "agenda_type" : [],
                        "deck_size" : [],
                        "agenda_points" : [],
                        "let_them_dream_count": [],
                        "agenda_counts" : [],
                        "num_agendas" : [],
                        "average_accesses" : []
                        
                        }

    # for each deck size
    for deck_size in deck_sizes:

            # get normal agenda point total
            agenda_point_totals = get_agenda_point_totals(deck_size)

            # for each agenda point total
            for agenda_point_total in agenda_point_totals:

                # get list of every possible agenda point combination
                agenda_counts = get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes)

                # agenda count and number of Let Them Dream agendas in the deck
                ltd_agenda_counts, num_ltd = get_ltd_agenda_counts(agenda_counts)

                # add Let Them Dream agenda info to dictionary
                agenda_type = "Let Them Dream"

                agenda_dictionary = fill_dictionary(agenda_dictionary, agenda_point_total, ltd_agenda_counts, num_ltd, deck_size, agenda_type)

                # add normal agenda info to dictionary
                agenda_type = "Normal"
                num_ltd = [0] * len(agenda_counts)

                agenda_dictionary = fill_dictionary(agenda_dictionary, agenda_point_total, agenda_counts, num_ltd, deck_size, agenda_type)
            
    return pd.DataFrame(agenda_dictionary)


def get_agenda_point_totals(deck_size):
    '''
        Takes in deck size 
        Returns list of legal agenda point 
        totals for that deck size
    '''

    # check deck size and assign matching agenda point list
    if deck_size >= 40 and deck_size <= 44:

        agenda_point_totals = [18, 19]

    if deck_size >= 45 and deck_size <= 49:

        agenda_point_totals = [20, 21]

    if deck_size >= 50 and deck_size <= 54:

        agenda_point_totals = [22, 23]

    return agenda_point_totals


def get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes):
    '''
        Takes in agenda point total 
        Maximum number of one point agendas (by available card pool)
        Maximum number of two point agendas (by available card pool)
        Maximum number of three point agendas (by available card pool)

        Returns list of all possible combinations of three, two, and one point agendas where their total value equals the agenda point total
    '''


    counts_list = []

    # iterate through all possible combinations of one two and three point agendas
    # using a max number for each agenda value calculated by dividing the agenda point total by the value of the agenda
    for threes in range(agenda_point_total // 3 + 1):

        agenda_points_after_threes = agenda_point_total - (threes*3)

        for twos in range(agenda_points_after_threes // 2 + 1):

            agenda_points_after_twos = agenda_points_after_threes - (twos*2)

            for ones in range(agenda_points_after_twos + 1):

                # if the values of all of the agendas in the combination are equal to the agenda point total add that total to a list
                if ((3*threes) + (2*twos) + ones == agenda_point_total and 
                    threes <= max_threes and
                    twos <= max_twos and
                    ones <= max_ones):

                    counts_list.append([threes, twos, ones])

    # return the list of 
    return counts_list


def get_ltd_agenda_counts(agenda_counts):
    '''
        Takes in list of one, two, and three point agenda combinations

        Returns list of agenda counts simulating replacing the maximum number of two point agendas with Let Them Dream agendas (up to three)
        This is simulated by raising the number of one point agendas by one and lowering the number of two point agendas by one for each replacement
        Also returns number of replaced agendas
    '''

    ltd_agenda_counts = []
    num_ltd = []
    
    # iterate through list of agenda counts
    for agenda_count in agenda_counts:
        
        # unpack agenda numbers
        threes = agenda_count[0]
        twos = agenda_count[1]
        ones = agenda_count[2]

        # replace agenda values based on the number of two point agendas in the agenda count
        # and value after replacement values to list of values after replacement

        if twos == 0:

            ltd = 0

            ltd_agenda_counts.append([threes,twos,ones])
            num_ltd.append(ltd)
    
        elif twos > 0 and twos <= 3:

            ltd =  twos
            
            ones += ltd
            twos -= ltd
            
            ltd_agenda_counts.append([threes,twos,ones])
            num_ltd.append(ltd)

        elif twos > 3:

            ltd = 3

            ones += ltd
            twos -= ltd

            ltd_agenda_counts.append([threes,twos,ones])
            num_ltd.append(ltd)

  
    # return list of values with replacements and list of number of replacements
    return ltd_agenda_counts, num_ltd


def fill_dictionary(agenda_dictionary, agenda_point_total, agenda_counts, ltd_num,  deck_size, agenda_type):
    '''
        Takes in 
        Dictionary of agenda features
        Agenda point total
        List of agenda counts 
        Number list of count of Let Them Dream agendas 
        Deck size

        calls functions to get access threshold

        Fills dictionary with information for possibility matrix

        Returns filled dictionary
    '''

    #loop through normal agenda counts and add information to dictionary
    for agenda_count in agenda_counts:
    
        # generate agenda points deck list  
        deck_list = get_deck_list(agenda_count, deck_size)
    
        accesses = round(mean([get_accesses(deck_list) for r in range(100_001)]))
    
        # add information to dictionary
        agenda_dictionary["agenda_type"].append(agenda_type)
    
        agenda_dictionary["deck_size"].append(deck_size)
    
        agenda_dictionary["agenda_points"].append(agenda_point_total)
    
        agenda_dictionary["agenda_counts"].append(agenda_count)
        
        agenda_dictionary["num_agendas"].append(sum(agenda_count))
        
        agenda_dictionary["average_accesses"].append(accesses)

    for num in ltd_num:

        agenda_dictionary["let_them_dream_count"].append(num)
    
    return agenda_dictionary


def get_deck_list(agenda_count, deck_size):
    '''
    Takes in agenda count and deck size
    
    Returns list of agenda values for each card in a deck constructed using the input information 
    '''

    deck_list = []

    # unpack number of each agenda
    threes = agenda_count[0]

    twos = agenda_count[1]

    ones = agenda_count[2]

    # add the number of each agenda value in the deck to the deck list
    deck_list.extend([3] * threes)

    deck_list.extend([2] * twos)

    deck_list.extend([1] * ones)

    # fill the rest of the deck list with zeros (non-agenda cards have an agenda value of 0)
    deck_list.extend([0] * (deck_size - len(deck_list)))

    return deck_list


def get_accesses(deck_list):
    '''
    Takes in a list of agenda point values for a given deck
    Performs digital experiment to calculate access threshold for the deck
    Returns the access threshold for the deck
    '''

    points = 0

    access_threshold = 0

    temp_deck = deck_list.copy()

   # continue selecting cards until 7 points of cards are selected 
    while points < 7:

        # for each selection
        # choose a card value at random from the deck list
        card = random.choice(temp_deck)

        # add 1 to access threshold
        access_threshold += 1

        # add value of card to points
        points += card

        # remove selected card from deck
        temp_deck.remove(card)

    return access_threshold


if __name__ == "__main__":

    # generate data from script
    df = main(deck_sizes, max_ones, max_twos, max_threes)
    # export to excel file
    df.to_excel("accesses.xlsx", index=False)