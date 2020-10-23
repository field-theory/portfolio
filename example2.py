#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Markowitz modern portfolio theory - example2.py

Summary:
    Example 2 that applies the Modern Portfolio Theory as
    introduced by Harry Markowitz. This example shows the space of
    portfolios possible with four (fictional) assets.

    For further documentation please refer to
    <https://www.field-theory.org/posts/mathematics-of-investing.html>

Copyright:
    (c) since 2008 by Dr. Wolfram Schroers <wolfram.schroers -at- field-theory.org>
    All rights reserved.

"""

# region Imports

from ModernPortfolio.Datasource import *
from ModernPortfolio.Analysis import *

# endregion

# region Main program

# Example with four assets (Example 2).
# The data is again provided as time-series.
NuAS_AdjClose = [22.892837777730136, 24.828830832143666, 40.286301894070455,
                 36.664475604448285, 48.623986498765625, 48.321874564460188,
                 41.772431411235729, 47.369932463489988, 44.575972194219581,
                 56.1830830886623, 44.421942134487168, 66.766280220874435,
                 51.799808462291374, 74.330313810946862, 54.985810072770555,
                 68.70935631475561, 68.265879750349256, 68.055848642120921,
                 75.532025345847302, 91.221513849621331]
Pear_AdjClose = [101.31149185576028, 129.89511978941198, 104.46392584365572,
                 115.96149128646566, 115.05518054012674, 123.54931944503218,
                 112.47650349602119, 125.24588515401605, 124.42564938781938,
                 123.346053822911, 130.13781815794664, 134.00958877414627,
                 167.64823259361515, 178.04817680319806, 162.85331241992128,
                 182.07945786811328, 167.77215773203818, 195.89855026037856,
                 191.72618648507384, 188.35597922772348]
GBnd_AdjClose = [5.215776828302868, 4.8014237610156183, 4.8764306501790333,
                 5.1903784815689811, 5.1057340811233711, 5.3201833360709987,
                 5.3486507919432471, 5.3119335245124102, 5.4916433204265394,
                 5.3375481015755737, 5.6697753293398643, 5.748530686312483,
                 5.5046695817309352, 5.6968193841333203, 5.7567581890053594,
                 5.856919314008131, 5.9505462740408639, 5.6558178054482919,
                 5.6067924826282631, 6.0829444663572749]
REst_AdjClose = [1.3222544298901444, 1.3193943150091398, 1.3014250254640813,
                 1.3449842152194971, 1.3216841583452141, 1.2878230677775087,
                 1.2646419601213941, 1.3495413982684334, 1.2985503169403074,
                 1.2936207061184015, 1.3277264736402679, 1.2767034458803947,
                 1.2974606368100006, 1.3426374836152108, 1.3432918526554027,
                 1.3058314755417362, 1.2619248890933972, 1.3316280798401308,
                 1.2787844774752761, 1.3183397683362019]

# Scan possible asset distributions, determine minimum variance portfolio.
analysis = PortfolioAnalysis(Portfolio([DataSource(NuAS_AdjClose, "NuAS"),
                                        DataSource(Pear_AdjClose, "Pear"),
                                        DataSource(GBnd_AdjClose, "G-Bonds"),
                                        DataSource(REst_AdjClose, "Real estate")]))
mcscan = analysis.scan_montecarlo()
minvar = analysis.minimum_variance_montecarlo()
print("\nMinimum variance portfolio:")
analysis.get_portfolio().report()

# Find portfolio with expected return > 6% and smallest variance.
mchull = analysis.asset_dist_hull(mcscan)
cool_return = [x for x in mchull if x[1] > 0.06]
cool_return.sort(key=lambda x: x[1])
cool_return.sort(key=lambda x: x[0])
cool_return = cool_return[0]
print("\nPortfolio with min. var. and return > 6%:")
analysis.get_portfolio().set_asset_distribution(cool_return[2])
analysis.get_portfolio().report()

# Display results graphically (uses matplotlib, skips this step if
# that library is unavailable).
try:
    import matplotlib.pyplot as plt

    # Plot the four time-series.
    years = [y for y in range(1990, 2010)]
    year_labels = [y for y in range(1990, 2011, 5)]
    no_labels = ('', '', '', '', '')
    time_series = plt.figure()

    nuasplt = time_series.add_subplot(221)
    plt.axis([1990, 2010, 0, 100])
    plt.xticks(year_labels, no_labels)
    plt.grid(True)
    plt.text(1991, 83.3, 'NuAS shares', size=20)
    nuasplt.plot(years, NuAS_AdjClose, 'k')

    pearplt = time_series.add_subplot(222)
    plt.xlabel('Year', fontsize=20)
    plt.axis([1990, 2010, 50, 200])
    plt.xticks(year_labels, no_labels)
    plt.grid(True)
    plt.text(1991, 175., 'Pear shares', size=20)
    pearplt.plot(years, Pear_AdjClose, 'b')

    gbndplt = time_series.add_subplot(223)
    plt.axis([1990, 2010, 4, 7])
    plt.xticks(year_labels, year_labels)
    plt.grid(True)
    plt.text(1991, 6.5, 'G-Bonds', size=20)
    gbndplt.plot(years, GBnd_AdjClose, 'r')

    restplt = time_series.add_subplot(224)
    plt.axis([1990, 2010, 1.2, 1.4])
    plt.xticks(year_labels, year_labels)
    plt.grid(True)
    plt.text(1991, 1.36667, 'Real estate', size=20)
    restplt.plot(years, REst_AdjClose, 'g')

    time_series.savefig('ex2-timeseries.png')

    # Plot risk-return diagram.
    fig = plt.figure()
    plt.plot([x[0] for x in mcscan], [x[1] for x in mcscan],
             "r.", markersize=2.0)
    plt.plot([x[0] for x in mchull], [x[1] for x in mchull],
             "k-", linewidth=3.0)
    plt.plot(minvar[0], minvar[1], "b+", markersize=20.0)
    plt.xlabel('Volatility $\sigma$', fontsize=20)
    plt.ylabel('Expected return $R$', fontsize=20)
    plt.annotate('Minimum\nvariance',
                 xy=minvar, xycoords='data', xytext=(-30, 170),
                 textcoords='offset points', size=20,
                 arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                 connectionstyle="angle3,angleA=0,angleB=-90"), )
    plt.annotate('Return >6%\nsmallest risk', xy=(cool_return[0], cool_return[1]),
                 xycoords='data', xytext=(-60, 60),
                 textcoords='offset points', size=20,
                 arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                 connectionstyle="arc3,rad=0.2"), )
    fig.savefig('ex2-risk-return.png')

except ModuleNotFoundError:
    import logging

    logging.error('Could not import matplotlib, skipped graphics.')

# endregion
