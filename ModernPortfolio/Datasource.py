#!/usr/bin/env python2.6 -ttt
# -*- coding: utf-8 -*-


""" Datasource.py

Summary:
    Classes related to provisioning time series data for the
    portfolio analysis. Time series data can be downloaded from the
    internet and analyzed using statistical methods to compute the
    expected return, volatility and correlations. This class can also
    be replaced by more sophisticated financial models (based on
    system dynamics, neural networks or other methods) or interfaces
    to such models.

    Classes implemented:
    - HistoricalQuotes
    - TimeSeries
    - DataSource

Note:
    The code to download historical quotes may no longer be functional.

    For further documentation please refer to
    <https://www.field-theory.org/posts/mathematics-of-investing.html>

Copyright:
    (c) since 2008 by Dr. Wolfram Schroers <wolfram.schroers -at- field-theory.org>
    All rights reserved.

"""

# region Imports

import datetime, math, warnings


# endregion

# region Classes

class HistoricalQuotes:
    """Download historical quotes from Yahoo Finance.

    This class downloads historical quotes from the Yahoo Finance web
    service. When using their service, please make sure that you
    always respect their usage conditions!

    """

    # Constants.
    DJ = '^DJI'
    Nasdaq = '^IXIC'
    DAX = '^GDAXI'
    ShanghaiComposite = '^SSEC'
    HangSeng = '^HSI'
    Nikkei = '^N225'
    TaiwanWeighted = '^TWII'
    SwissMarket = '^SSMI'
    TreasuryBill13w = '^IRX'
    TreasuryYield30y = '^TYX'
    TreasuryYield5y = '^FVX'
    GMCommodity = 'GIH11.CME'
    PHLXGoldSilver = '^XAU'

    quote_data = []

    def __init__(self, start_date, end_date, stock=DJ, spacing='d'):
        """Download and set up the requested history.

        This method downloads the requested history and sets it up
        properly.

        @param start_date Start of history, instance of datetime.date.
        @param end_date End of history, instance of datetime.date.
        @param stock Requested stock symbol, defaults to '^DJI'.
        @param spacing Time between subsequent history points.
        """

        import urllib.request, urllib.error, urllib.parse

        query = ('http://ichart.finance.yahoo.com/table.csv?' +
                 ('s=%s&d=%d&e=%d&f=%d&g=%s&a=%d&b=%d&c=%d&ignore=.csv' %
                  (stock,
                   end_date.month, end_date.day, end_date.year,
                   spacing,
                   start_date.month, start_date.day, start_date.year)))
        query_handle = urllib.request.urlopen(query)
        cont = query_handle.readlines()
        query_handle.close()
        del (cont[0])
        cont.sort(key=lambda x: x[:10])

        self.quote_data = []
        for datum in cont:
            entry = datum.strip().split(',')
            self.quote_data += [entry]

    def quote_data(self):
        """Return the raw quote data as a nested array."""
        return self.quote_data

    def time_series(self):
        """Return the chart values as an array with desired spacing."""
        result = []
        for datum in self.quote_data:
            result = result + [float(datum[-1])]
        return result


class TimeSeries:
    """Analyze a time series of data points.

    This class performs an analysis based on a simple, linear fit.

    """
    history = []

    def __init__(self, history):
        """Setup a time series with an array of individual data points."""
        self.history = history

    def length(self):
        """Return the length of the time series history."""
        return len(self.history)

    def relative_returns(self):
        """Return the relative (normalized) returns of time series."""
        rel_returns = []
        if len(self.history) < 2:
            return []
        for i in range(len(self.history) - 1):
            rel_returns.append((self.history[i + 1] - self.history[i]) /
                               self.history[i])
        return rel_returns

    def volatility(self):
        """Return the volatility (standard deviation) of the data set."""
        avg_vol = 0.0
        rel_returns = self.relative_returns()
        if len(rel_returns) > 1:
            exp_return = self.expected_return()
            for curr_val in rel_returns:
                avg_vol += math.pow((curr_val - exp_return), 2)
            return math.sqrt(avg_vol / len(rel_returns))
        else:
            return float('nan')

    def expected_return(self):
        """Return the expected return of the current data set."""
        avg_ret = 0.0
        rel_returns = self.relative_returns()
        if len(rel_returns) > 0:
            for curr_val in rel_returns:
                avg_ret += curr_val
            return (avg_ret / len(rel_returns))
        else:
            return float('nan')

    def correlation_with(self, other_series):
        """Return the correlation of the current and another time series."""
        if ((self.length() != other_series.length()) or
                (self.length() < 2)):
            return 0.0
        avg_corr = 0.0
        my_relret = self.relative_returns()
        other_relret = other_series.relative_returns()
        series_len = len(my_relret)
        for i in range(series_len):
            avg_corr += my_relret[i] * other_relret[i]
        avg_corr = avg_corr / series_len - (self.expected_return() *
                                            other_series.expected_return())
        return avg_corr


class DataSource(TimeSeries):
    """Provides input for the Portfolio class.

    A Portfolio class data source must provide the following methods:
    - __init__
    - get_name
    - volatility
    - expected_return
    - correlation_with

    """

    name = ""

    def __init__(self, history, name):
        """Setup the asset represented by this object."""
        self.name = name
        self.history = history

    def get_name(self):
        """Return the identifying tag of this object."""
        return self.name


# endregion

# region Main program

if __name__ == "__main__":
    print("Datasource - data provisioning module.")

# endregion
