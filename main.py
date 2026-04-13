''' Script for simulating random accesses during a Netrunner game'''

# imports
import random
import numpy as np
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt

deck_sizes = [40, 44, 45, 49, 50, 54]
max_ones = 15
max_twos = 36
max_threes = 12

def main(deck_sizes, max_ones, max_twos, max_threes):


    # get empty dictionary
    agenda_dict = {

                    "deck_size" : [],
                    "agenda_points" : [],
                    "agenda_counts" : [],
                    "num_agendas" : [],
                    "average_accesses" : []

    }

    for deck_size in deck_sizes:

        agenda_point_totals = get_agenda_point_totals(deck_size)

        for agenda_point_total in agenda_point_totals:

            # get list of every possible agenda point combination
            agenda_counts = get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes)

            #loop through all agenda counts
            for agenda_count in agenda_counts:

                # generate agenda points deck list  
                deck_list = get_deck_list(agenda_count, deck_size)

                accesses = round(mean([get_accesses(deck_list) for r in range(100_001)]))

                agenda_dict["deck_size"].append(deck_size)

                agenda_dict["agenda_points"].append(agenda_point_total)

                agenda_dict["agenda_counts"].append(agenda_count)
                
                agenda_dict["num_agendas"].append(sum(agenda_count))
                
                agenda_dict["average_accesses"].append(accesses)

    return pd.DataFrame(agenda_dict)


def get_agenda_point_totals(deck_size):

    if deck_size >= 40 and deck_size <= 44:

        agenda_point_totals = [18, 19]

    if deck_size >= 45 and deck_size <= 49:

        agenda_point_totals = [20, 21]

    if deck_size >= 50 and deck_size <= 54:

        agenda_point_totals = [22, 23]

    return agenda_point_totals


def get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes):

    counts_list = []

    for threes in range(agenda_point_total // 3 + 1):

        agenda_points_after_threes = agenda_point_total - (threes*3)

        for twos in range(agenda_points_after_threes // 2 + 1):

            agenda_points_after_twos = agenda_points_after_threes - (twos*2)

            for ones in range(agenda_points_after_twos + 1):

                if ((3*threes) + (2*twos) + ones == agenda_point_total and 
                    threes <= max_threes and
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

    print(main(deck_sizes, max_ones, max_twos, max_threes))