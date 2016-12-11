"""
This is a modification of the scatter_matrix method;
it allows plotting sub-sections of the scatter plot
matrix. With the official method you can only plot
the entire matrix. This method allows selecting the
`cols` and `rows` you're interested in plotting.
Note that this wouldn't be possible even by calling
scatter_matrix on a subset of the dataframe, because
this wouldn't allow comparing different `cols`/`rows'.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas
import pandas.tools.plotting
from pandas.compat import range, lrange, lmap, map, zip, string_types

def scatter_matrix(frame, cols, rows, figsize=None, ax=None, grid=False,
                   diagonal='hist', marker='.', density_kwds=None,
                   hist_kwds=None, range_padding=0.05, **kwds):
    """
    Draw a matrix of scatter plots.
    Parameters
    ----------
    frame : DataFrame
    cols : [str]
      labels of the columns to be rendered
    rows:  [str]
      labels of the rows to be rendered
    alpha : float, optional
        amount of transparency applied
    figsize : (float,float), optional
        a tuple (width, height) in inches
    ax : Matplotlib axis object, optional
    grid : bool, optional
        setting this to True will show the grid
    diagonal : {'hist', 'kde'}
        pick between 'kde' and 'hist' for
        either Kernel Density Estimation or Histogram
        plot in the diagonal
    marker : str, optional
        Matplotlib marker type, default '.'
    hist_kwds : other plotting keyword arguments
        To be passed to hist function
    density_kwds : other plotting keyword arguments
        To be passed to kernel density estimate plot
    range_padding : float, optional
        relative extension of axis range in x and y
        with respect to (x_max - x_min) or (y_max - y_min),
        default 0.05
    kwds : other plotting keyword arguments
        To be passed to scatter function
    Examples
    --------
    >>> df = DataFrame(np.random.randn(1000, 4), columns=['A','B','C','D'])
    >>> scatter_matrix(df, alpha=0.2)
    """
    import matplotlib.pyplot as plt

    df = frame._get_numeric_data()
    w = len(cols)
    h = len(rows)
    naxes = w * h
    fig, axes = pandas.tools.plotting._subplots(naxes=naxes, figsize=figsize, ax=ax,
                          squeeze=False)

    # no gaps between subplots
    fig.subplots_adjust(wspace=0, hspace=0)

    #mask = pandas.tools.plotting.notnull(df)

    marker = pandas.tools.plotting._get_marker_compat(marker)

    hist_kwds = hist_kwds or {}
    density_kwds = density_kwds or {}

    # workaround because `c='b'` is hardcoded in matplotlibs scatter method
    #kwds.setdefault('c', plt.rcParams['patch.facecolor'])

    cols_boundaries_list = []
    for a in cols:
        values = df[a]#.values[mask[a].values]
        rmin_, rmax_ = np.min(values), np.max(values)
        rdelta_ext = (rmax_ - rmin_) * range_padding / 2.
        cols_boundaries_list.append((rmin_ - rdelta_ext, rmax_ + rdelta_ext))
    rows_boundaries_list = []
    for a in rows:
        values = df[a]#.values[mask[a].values]
        rmin_, rmax_ = np.min(values), np.max(values)
        rdelta_ext = (rmax_ - rmin_) * range_padding / 2.
        rows_boundaries_list.append((rmin_ - rdelta_ext, rmax_ + rdelta_ext))

    for i, a in zip(lrange(w), cols):
        for j, b in zip(lrange(h), rows):
            ax = axes[i, j]

            if cols[i] == rows[j]:
                values = df[a]#.values[mask[a].values]

                # Deal with the diagonal by drawing a histogram there.
                if diagonal == 'hist':
                    ax.hist(values, **hist_kwds)

                elif diagonal in ('kde', 'density'):
                    from scipy.stats import gaussian_kde
                    y = values
                    gkde = gaussian_kde(y)
                    ind = np.linspace(y.min(), y.max(), 1000)
                    ax.plot(ind, gkde.evaluate(ind), **density_kwds)

                ax.set_xlim(cols_boundaries_list[i])

            else:
                #common = (mask[a] & mask[b]).values
                ax.scatter(df[b], df[a], marker=marker, **kwds)

                ax.set_xlim(rows_boundaries_list[j])
                ax.set_ylim(cols_boundaries_list[i])

            ax.set_xlabel(b)
            ax.set_ylabel(a)

            if j != 0:
                ax.yaxis.set_visible(False)
            if i != w - 1:
                ax.xaxis.set_visible(False)

    #if len(df.columns) > 1:
        #lim1 = cols_boundaries_list[0]
        #locs = axes[0][1].yaxis.get_majorticklocs()
        #locs = locs[(lim1[0] <= locs) & (locs <= lim1[1])]
        #adj = (locs - lim1[0]) / (lim1[1] - lim1[0])

        #lim0 = axes[0][0].get_ylim()
        #adj = adj * (lim0[1] - lim0[0]) + lim0[0]
        #axes[0][0].yaxis.set_ticks(adj)

        #if np.all(locs == locs.astype(int)):
            ## if all ticks are int
            #locs = locs.astype(int)
        #axes[0][0].yaxis.set_ticklabels(locs)

    pandas.tools.plotting._set_ticks_props(axes, xlabelsize=8, xrot=90, ylabelsize=8, yrot=0)

    return axes
