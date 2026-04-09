''' Script for simulating random accesses during a Netrunner game'''

# imports
import random
import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt

deck_size = 49
agenda_point_total = 20
max_ones = 15
max_twos = 36
max_threes = 12

def main(deck_size, agenda_point_total, max_ones, max_twos, max_threes):

    agenda_dict = {
                    "counts" : [],
                    #"total_number" : [],
                    "average_accesses" : []

    }
    
    # get list of every possible agenda point combination
    agenda_counts = get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes)

    #loop through all agenda counts
    for agenda_count in agenda_counts:

        # generate agenda points deck list  
        deck_list = get_deck_list(agenda_count, deck_size)

        accesses = round(mean([get_accesses(deck_list) for r in range(100_001)]))

        agenda_dict["counts"] = agenda_counts
        
        #agenda_dict["total_number"] = sum(agenda_counts)
        
        agenda_dict["average_accesses"].append(accesses)

    return pd.DataFrame(agenda_dict)


def get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes):

    counts_list = []

    for threes in range(agenda_point_total // 3 + 1):

        agenda_points_after_threes = agenda_point_total - (threes*3)

        for twos in range(agenda_points_after_threes // 2 + 1):

            agenda_points_after_twos = agenda_points_after_threes - (twos*2)

            for ones in range(agenda_points_after_twos + 1):

                if ((3*threes) + (2*twos) + ones == agenda_point_total and 
                    threes <= max_ones and
                    twos <= max_twos and
                    ones <= max_ones):

                    counts_list.append([threes, twos, ones])

    return counts_list


def get_deck_list(agenda_count, deck_size):

    deck_list = []

    threes = agenda_count[0]

    twos = agenda_count[1]

    ones = agenda_count[2]

    deck_list.extend([3] * threes)

    deck_list.extend([2] * twos)

    deck_list.extend([1] * ones)

    deck_list.extend([0] * (deck_size - len(deck_list)))

    return deck_list


def get_accesses(deck_list):

    points = 0

    accesses = 0

    temp_deck = deck_list.copy()

    while points < 7:

        accesses += 1

        card = random.choice(temp_deck)

        points += card

        temp_deck.remove(card)

    return accesses


if __name__ == "__main__":

    print(main(deck_size, agenda_point_total, max_ones, max_twos, max_threes))