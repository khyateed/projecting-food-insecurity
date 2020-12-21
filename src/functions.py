# CAPSTONE PROJECT FUNCTIONS
# Projecting Food Insecurity Rates in the US
# By Khyatee Desai


# This .py file contains functions used in EDA.ipynb to generate lineplots, barcharts,
# and choropleth maps.

# import necessary packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd

def lineplot(df, features, title=None):
    '''input 1: dataframe
       input 2: one or more features to be plotted (list)
       input 3: (optional) title for chart
       output: One or more overlayed lineplots'''
    
    plt.figure(figsize=(20, 8));
    for feat in features:
        x = df.groupby("Year")[feat].mean().reset_index().dropna()
        y = (x[feat] - min(x[feat])) / (max(x[feat]) - min(x[feat]))
        ax= sns.lineplot(x=x['Year'].astype(int), y= y, label=feat, linewidth = 4)
    ax.set_title(title, fontsize=24);
    ax.set_ylabel('Scaled Value', fontsize=20);
    ax.set_xlabel('Year', fontsize=20);
    ax.legend(prop=dict(size=18));
    plt.xticks(fontsize=16);
    plt.yticks(fontsize=16);
#     plt.savefig('../images/line_'+title+'.png',format = 'png',bbox_inches='tight', transparent=True)


def barchart(df, features, title=None):
    '''input 1: dataframe
       input 2: one or more features to be plotted (list)
       input 3: (optional) title for chart
       output: One or more side-by-side barcharts'''
    
    plot_df = df.groupby("Year")[features].mean().fillna(0)
    for feat in features:
        plot_df[feat] =(plot_df[feat] - min(plot_df[feat])) / (max(plot_df[feat]) - min(plot_df[feat]))
    plot_df.plot(by='Year',kind='bar',fontsize=16,rot='horizontal',figsize=(25,10));
    plt.xlabel('Year', fontdict={'fontsize':24});
    plt.ylabel('Scaled Count', fontdict={'fontsize':24});
    plt.xticks(fontsize=22);
    plt.yticks(fontsize=22);
    plt.legend(prop=dict(size=22));
    plt.title(title, fontdict={'fontsize':30});
#     plt.savefig('../images/bar_'+title+'.png',format = 'png',bbox_inches='tight', transparent=True)

def choropleth(df, feature, year, cmap, title=None):
    '''input 1: dataframe
       input 2: features to be plotted (string)
       input 3: year for map (string)
       input 4: color map palette (string) - look at seaborn documentation for options
       input 5: (optional) title for chart
       output: Choropleth map'''
    
    map_df = df[df.Year == year]
    # Read shapefile using Geopandas
    shape_df = gpd.read_file('../datasets/shapefile/cb_2018_us_county_500k.shp')
    geo_df = shape_df.merge(map_df, left_on='GEOID', right_on='FIPS')
    fig, ax = plt.subplots(figsize = (40,40))
    ax.patch.set_alpha(0.0)
    vmin = geo_df[feature].min()
    vmax = geo_df[feature].max()
    geo_df.plot(ax=ax, column =feature, cmap=cmap, legend = False,antialiased=False)
    if title:
        ax.set_title(title+", "+year, fontdict={'fontsize': 60}, loc='center')
    else:
        ax.set_title(feature+", "+year, fontdict={'fontsize': 60}, loc='center')
    ax.set(xlim=(-126, -66), ylim=(24, 50));
    plt.xticks([], [])
    plt.yticks([], [])
    cax = fig.add_axes([.95, 0.28, 0.02, 0.5])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=30))
    sm._A = []
    cbr = fig.colorbar(sm, cax=cax)
    cbr.set_label(feature, size=45)
    cbr.ax.tick_params(labelsize=35) 
    ax.set_axis_off()
    # ax.annotate("__Optional Annotation__", xy=(0.25, .1), size=20, xycoords='figure fraction')
#     plt.savefig('../images/'+year+title+'.png',format = 'png',bbox_inches='tight', transparent=True)





