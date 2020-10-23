#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Markowitz modern portfolio theory - example1.py

Summary:
    Example 1 that applies the Modern Portfolio Theory as
    introduced by Harry Markowitz. This example shows the space of
    portfolios possible with two (fictional) example assets.

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

# Example with two assets (Example 1).
# The data is provided as two time-series.
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

# Scan possible asset distributions, determine minimum variance portfolio.
analysis = PortfolioAnalysis(Portfolio([DataSource(NuAS_AdjClose, "NuAS"),
                                        DataSource(Pear_AdjClose, "Pear")]))
biscan = analysis.scan_asset_pairs()
minvar = analysis.minimum_variance_montecarlo()
print("\nMinimum variance portfolio:")
analysis.get_portfolio().report()

# Volatilities and returns for single assets.
analysis.get_portfolio().set_asset_distribution([1.0, 0.0])
nuas_single = (analysis.get_portfolio().get_volatility(),
               analysis.get_portfolio().get_expected_return())
analysis.get_portfolio().set_asset_distribution([0.0, 1.0])
pear_single = (analysis.get_portfolio().get_volatility(),
               analysis.get_portfolio().get_expected_return())
print("\nVolatility, expected return of NuAS shares: ",
      nuas_single,
      "\nVolatility, expected return of Pear shares: ",
      pear_single, "\n")

# Display results graphically (uses matplotlib, skips this step if
# that library is unavailable).
try:
    import matplotlib.pyplot as plt

    # Plot the two time-series.
    years = [y for y in range(1990, 2010)]
    year_labels = [y for y in range(1990, 2011, 5)]
    no_labels = ('', '', '', '', '')
    time_series = plt.figure()
    nuasplt = time_series.add_subplot(211)
    plt.axis([1990, 2010, 0, 100])
    plt.xticks(year_labels, no_labels)
    plt.grid(True)
    plt.text(1991, 83.3, 'NuAS shares', size=20)
    nuasplt.plot(years, NuAS_AdjClose, 'k')
    pearplt = time_series.add_subplot(212)
    plt.xlabel('Year', fontsize=20)
    plt.axis([1990, 2010, 50, 200])
    plt.xticks(year_labels, year_labels)
    plt.grid(True)
    plt.text(1991, 175., 'Pear shares', size=20)
    pearplt.plot(years, Pear_AdjClose, 'b')
    time_series.savefig('ex1-timeseries.png')

    # Plot corresponding risk-return diagram.
    fig = plt.figure()
    plt.plot([x[0] for x in biscan], [x[1] for x in biscan],
             "b-", linewidth=3.0)
    plt.plot(minvar[0], minvar[1], "r+", markersize=20.0)
    plt.axis([0.08, 0.26, 0.03, 0.11])
    plt.xlabel('Volatility $\sigma$', fontsize=20)
    plt.ylabel('Expected return $R$', fontsize=20)
    plt.annotate('Minimum variance\n(77% Pear, 23% NuAS)',
                 xy=minvar, xycoords='data', xytext=(-20, 150),
                 textcoords='offset points', size=20,
                 arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                 connectionstyle="angle3,angleA=0,angleB=-90"), )
    plt.annotate('100% Pear', xy=pear_single, xycoords='data',
                 xytext=(50, 20), textcoords='offset points', size=20,
                 arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                 connectionstyle="arc3,rad=0.2"), )
    plt.annotate('100% NuAS', xy=nuas_single, xycoords='data',
                 xytext=(-90, -75), textcoords='offset points', size=20,
                 arrowprops=dict(arrowstyle="fancy", fc="0.6", ec="none",
                                 connectionstyle="arc3,rad=-0.1"), )
    fig.savefig('ex1-risk-return.png')

except ModuleNotFoundError:
    import logging

    logging.error('Could not import matplotlib, skipped graphics')

# endregion
