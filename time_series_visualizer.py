import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]



def draw_line_plot():
    # Draw line plot
    fig,axes = plt.subplots(figsize=(18,7)) 
    df.plot(kind='line', y = 'value', ax=axes, color='r',
                  title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().reset_index()
    
    df_bar['year'] = pd.DatetimeIndex(df_bar['date']).year
    df_bar['month'] = pd.DatetimeIndex(df_bar['date']).month
    df_bar_group = df_bar.groupby(['year','month'])['value'].mean().unstack()

    # Draw bar plot
    ax = df_bar_group.plot(kind='bar', figsize=(14,5))
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(labels = [calendar.month_name[i] 
                         for i in sorted(df_bar.month.unique())])
    
    fig = ax.get_figure()   

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = pd.DatetimeIndex(df_box['date']).year
    df_box['month'] = pd.DatetimeIndex(df_box['date']).month_name().str[:3]
    df_box.sort_values(by=['year','date'],ascending=[False,True],inplace=True)
    # Draw box plots (using Seaborn)
    fig, (axy, axm) = plt.subplots(1,2)
    fig.set_figwidth(15)
    fig.set_figheight(7)
    
    axy = sns.boxplot(x=df_box.year, y=df_box.value, ax=axy)
    axy.set_title('Year-wise Box Plot (Trend)')
    axy.set_xlabel('Year')
    axy.set_ylabel('Page Views')
    
    axm = sns.boxplot(x='month', y='value',data=df_box, ax=axm)
    axm.set_title('Month-wise Box Plot (Seasonality)')
    axm.set_xlabel('Month')
    axm.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
