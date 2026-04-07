''' Script for simulating random acceses during a Netrunner game'''

# imports
import random
import pandas as pd
import matplotlib.pyplot as plt

# get list of every possible agenda point combination

agenda_point_total = 20
max_ones = 15
max_twos = 36
max_threes = 12

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


agenda_counts = get_agenda_counts(agenda_point_total, max_ones, max_twos, max_threes)

# get agenda point deck list

agenda_count = agenda_counts[-3]

threes = agenda_count[0]

twos = agenda_count[1]

ones = agenda_count[2]

# 40-44/45-49/50-54

deck_size = 49

deck_list = []

deck_list.extend([3] * threes)

deck_list.extend([2] * twos)

deck_list.extend([1] * ones)

deck_list.extend([0] * (deck_size - len(deck_list)))


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


tests = []

for r in range(10_001):

    tests.append(get_accesses(deck_list))

chart = pd.Series(tests).value_counts()

tests = pd.Series(tests)

frequency_table = tests.value_counts().sort_index()

# 4. Plot the results
frequency_table.plot.bar(
    xlabel='Number', 
    ylabel='Frequency', 
    title='Frequency Distribution'
)
plt.show()