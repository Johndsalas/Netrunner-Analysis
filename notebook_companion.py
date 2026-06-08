''' Stores code imported to Netrunner Analysis: Access Threshold notebook to reduce clutter '''

# imports
import pandas as pd
import regex as re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def get_my_data():
    '''
    read in agenda matrix data
    return full dataframe 
    and two subset dataframes seperating 
    normal and let them dream agenda types 
    '''

    # read in data
    df = pd.read_excel('agenda_matrix.xlsx')

    # exclude let them dream type builds where no replacements occured
    df = df[~((df.agenda_type == 'Let Them Dream') & (df.let_them_dream_count == 0))]

    # rename columns for ease of understanding
    df = df.rename(columns={'old_col2' : 'new_col2',
                            'let_them_dream_count' : 'ltd_count',
                            'average_accesses' : 'access_threshold'})
    
    # add seperate columns for count of one, two, and three point agendas 
    df['three_point_agendas'] = df.agenda_counts.apply(lambda x: int(re.search('\[(\d+),', x).group(1)))
    df['two_point_agendas'] = df.agenda_counts.apply(lambda x: int(re.search(', (\d+),', x).group(1)))
    df['one_point_agendas'] = df.agenda_counts.apply(lambda x: int(re.search(', (\d+)\]', x).group(1)))

    # data validation
    # add column calculating agenda point total 
    df['calc_agenda_points'] = (df['three_point_agendas'] * 3) + (df['two_point_agendas'] * 2) + (df['one_point_agendas']) + (df['ltd_count'])

    # check that calculated agenda point total matches assigned agenda point total
    # if yes drop redundant columns
    # if no raise exception
    if (df.agenda_points == df.calc_agenda_points).all():

        df.drop(columns = ['agenda_counts', 'agenda_points', 'calc_agenda_points'])
        
    else:
        
        raise Exception("Agenda Point Mismatch!!!")
    
    # add agenda density column
    df['agenda_density'] = df['agenda_points'] / df['deck_size']
    
    # split data into normal and Let Them Dream data sets
    df_normal = df[df.agenda_type == 'Normal']
    df_ltd = df[df.agenda_type == 'Let Them Dream']

    return df, df_normal, df_ltd


def get_my_thresholds(df_normal, df_ltd):

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)

    colors1 = { '14' :   'skyblue',
                '15' : '#779ECB',
                '16' : '#779ECB',
                '17' : '#779ECB',
                '18' :   'skyblue',
                '19' :   'skyblue',}
    
    sns.countplot(x='access_threshold', data=df_normal, ax=ax1, palette=colors1)
    ax1.set_title('Normal Agendas')

    colors2 = { '15' :   'skyblue',
                '16' :   'skyblue',
                '17' : '#779ECB',
                '18' : '#779ECB',
                '19' : '#779ECB',
                '20' : '#779ECB',}

    sns.countplot(x='access_threshold', data=df_ltd, ax=ax2, palette=colors2)
    ax2.set_title('Let Them Dream')



    plt.tight_layout()
    plt.show()