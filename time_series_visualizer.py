import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)
# print(df)

# Clean data
top_p = df.value.quantile(0.975)
lower_p = df.value.quantile(0.025)
# print(df<lower_p)
df = df.mask((df< lower_p) | (df > top_p))
df = df.dropna(subset='value')
# print(df.columns)


def draw_line_plot():
    # Draw line plot
    fig=plt.figure()
    plt.plot(df.index, df['value'],color='red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    # plt.show()
   
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    df_bar['month'] = df_bar['month'].apply(lambda data: months[data-1])
    df_bar["month"] = pd.Categorical(df_bar["month"], categories=months)
    df_bar = df_bar.groupby(['year','month']).mean().reset_index()   
    df_bar=df_bar.pivot(columns='month',index='year',values='value')
    
    # print(df_bar)

    # Draw bar plot
    ax = df_bar.plot(kind="bar")
    fig=ax.get_figure()    
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # print(df_box)

    # Draw box plots (using Seaborn)
    fig,axes = plt.subplots(1,2)

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")


    sns.boxplot(x="month", y="value", data=df_box, order=months, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    # plt.show()





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
