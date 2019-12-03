from io import BytesIO
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import HTML
# reset to matplotlib defaults rather than seaborn ones
plt.rcdefaults()
# Turn off the max column width so the images won't be truncated
pd.set_option('display.max_colwidth', -1)
#Monkey patch the dataframe so the sparklines are displayed
pd.DataFrame._repr_html_ = lambda self: self.to_html(escape=False)

# Display pandas linebreaks properly
# Save the original `to_html` function to call it later
pd.DataFrame.base_to_html = pd.DataFrame.to_html
# Call it here in a controlled way
pd.DataFrame.to_html = (
    lambda df, *args, **kwargs: 
        (df.base_to_html(*args, **kwargs)
           .replace(r"\n", "<br/>"))
)


def dist_plot(org_value,
              distribution,
              figsize=(3.5, 1),
              **kwags): 

    fig, ax = plt.subplots(1,1,figsize=figsize,**kwags)
    sns.kdeplot(distribution,ax=ax,linewidth=0.9)
    ax.axvline(org_value,color='r',linewidth=1)
    ax = remove_clutter(ax)
    return plt

def sparkline_plot(series,
                   figsize=(3.5, 1),
                   **kwags): 

    fig, ax = plt.subplots(1,1,figsize=figsize,**kwags)
    series.reset_index().plot(ax=ax,linewidth=0.9)
    ax = remove_clutter(ax)
    return plt

def remove_clutter(ax):
    ax.legend()#_.remove()
    ax.legend_.remove()
    for k,v in ax.spines.items():
        v.set_visible(False)
    ax.tick_params(labelsize=5)
    ax.set_yticks([])
    #ax.set_xticks([])
    ax.xaxis.set_label_text('')
    plt.tight_layout()
    return ax

def html_plt(plt):
    # return in HTML format
    img = BytesIO()
    plt.savefig(img, transparent=True)
    plt.close()
    html = '<img src=\"data:image/png;base64,{}"/>'.format(
            base64.b64encode(img.getvalue()).decode())
    return html

def get_stats(df,
              measure='measure',
              aggregators=['code']):
    #1 calculate stats
    agg = df.groupby(aggregators).agg(['mean','std','skew'])[measure]
    kurtosis = df.groupby(aggregators).apply(pd.DataFrame.kurt)
    agg['kurtosis'] = kurtosis[measure]
    df = df.join(agg)
    #2 calculate the # of std deviations an entity is away from the mean
    df['z_score'] = (df[measure]-agg['mean'])/agg['std']
    #self['z_score'] = self['z_score'].abs() # change to absolute values
    df = df.dropna()
    return df

def dist_table(df, column, subset=None):
    if subset is not None:
        index = subset
    else:
        index = df.index
    series = pd.Series(index=index,name='plots')
    for idx in index:
        plot = dist_plot(df.loc[idx,column],
                         df.loc[idx[0],column])
        series.loc[idx] = html_plt(plot)
    df = df.join(series, how='right')
    df = df.round(decimals=2)
    return HTML(df.to_html(escape=False))

def sparkline_table(df, column, subset=None):
    if subset is not None:
        index = subset
    else:
        index = df.index
    series = pd.Series(index=index,name='plots')
    for idx in index:
        plot = sparkline_plot(df.loc[idx,column])
        series.loc[idx] = html_plt(plot)
    df = df.join(series, how='right')
    df = df.round(decimals=2)
    series['one'] = 1
    return series
