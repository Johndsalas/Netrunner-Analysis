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
    
    # add agenda density column round to 5 decimals for color mapping
    df['agenda_density'] = round(df['agenda_points'] / df['deck_size'], 6)
    
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
    ax1.set(xlabel='', ylabel='')

    colors2 = { '15' :   'skyblue',
                '16' :   'skyblue',
                '17' : '#779ECB',
                '18' : '#779ECB',
                '19' : '#779ECB',
                '20' : '#779ECB',}

    sns.countplot(x='access_threshold', data=df_ltd, ax=ax2, palette=colors2)
    ax2.set_title('Let Them Dream')
    ax2.set(xlabel='', ylabel='')

    fig.suptitle("Strong Contrast Between Common and Uncommon Access Threshold Values", fontweight='bold')
    fig.supxlabel('Access Threshold')
    fig.supylabel('Count of Distinct Legal Builds')

    plt.tight_layout()
    plt.show()


def get_my_density_chart(df):
    '''
        Plots agenda density chart using dataframe
    '''
    #lable colors by clusters
    colors = {
                0.407407 : '#FFB5E8',
                0.408163 : '#FFB5E8',
                0.409091 : '#FFB5E8',   
        
                0.425926 : '#FFB347',   
                0.428571 : '#FFB347',   
                0.431818 : '#FFB347',   
        
                0.440000 : '#FFD166',   
        
                0.444444 : '#54D29C',   
                0.450000 : '#54D29C',   
        
                0.460000 : '#4AAAD1',   
        
                0.466667 : '#D99BFF',   
        
                0.475000 : '#2D3142'
            }

    # plot chart
    sns.scatterplot(data=df, x='agenda_density', y='access_threshold', hue='agenda_density', palette=colors)
    
    plt.title('Agenda Density Sets a Range of 3-4 Values for Access Threshold', fontweight='bold')

    plt.xlabel("Agenda Density")
    plt.ylabel("Access Threshold")

    plt.legend([], [], frameon=False)

    plt.show()

def get_min_deck_chart(df):

    df_min = df[df.deck_size.isin([40, 45, 50])]

    df_min.plot.scatter(x='deck_size', y='access_threshold',figsize=(4, 5), color='#779ECB')
    plt.title('Minimum Deck Size Caps Builds Maximum Access Threshold', fontweight='bold', pad=15)
    plt.xticks([40, 45, 50])
    plt.xlim(37.5, 52.5)

    plt.yticks(range(14, 20)) 
    plt.ylim(13, 19.5)  

    plt.xlabel("Agenda Density")
    plt.ylabel("Access Threshold")

    plt.tight_layout()
    plt.show()


def get_margin_chart(df):

    df_small = df[df['deck_size'].between(40,44)]
    df_mid = df[df.deck_size.between(45,49)]
    df_lg = df[df.deck_size.between(50,54)]

    fig, axes = plt.subplots(ncols=3, figsize=(6,5), constrained_layout=True, sharey=True)

    df_small.plot.scatter(x='deck_size', y='access_threshold', title='40-44', xlabel='', ylabel='', color='#779ECB', ax=axes[0])
    axes[0].set_xticks([40, 44])
    axes[0].set_xlim(39, 45)
    axes[0].set_ylim(13, 21)
    axes[0].set_yticks(range(14, 21))

    df_mid.plot.scatter(x='deck_size', y='access_threshold', title='45-49', xlabel='', ylabel='', color='#779ECB', ax=axes[1])
    axes[1].set_xticks([45, 49])
    axes[1].set_xlim(44, 50)

    df_lg.plot.scatter(x='deck_size', y='access_threshold', title='50-54', xlabel='', ylabel='', color='#779ECB', ax=axes[2])
    axes[2].set_xticks([50, 54])
    axes[2].set_xlim(49, 55)

    fig.suptitle('Access Threshold Range Shifts Up When Using the Four Card Margin', fontweight='bold')

    fig.supxlabel('Deck Size')
    fig.supylabel('Access Threshold')

    fig.align_ylabels()

    plt.tight_layout()
    plt.show()