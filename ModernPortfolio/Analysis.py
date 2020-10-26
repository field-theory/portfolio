#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Analysis.py

Summary:
    Functions and classes that implement the analysis of a
    portfolio of assets whose properties are provided by an
    appropriate data source (typically, an instance of Datasource
    class). The core parts of the analysis are based on Monte-Carlo
    scans of the parameter space and work for a wide variety of
    underlying models.

    For further documentation please refer to
    <https://www.field-theory.org/posts/mathematics-of-investing.html>

Copyright:
    (c) since 2008 by Dr. Wolfram Schroers <wolfram.schroers -at- field-theory.org>
    All rights reserved.

"""

# region Imports

import math, warnings
from functools import reduce

# endregion

# region Constants

rel_tol = 1e-04
abs_tol = 1e-07


# endregion

# region Functions

def float_eq(a, b, rtol=rel_tol, atol=abs_tol):
    """Floating point (approximate) equality comparison."""
    return (abs(b - a) < (atol + rtol * (a + b)))


def vec_sum(vec):
    """Return the sum of the elements of a vector."""
    return reduce(lambda x, y: x + y, vec)


def vec_norm(vec, n=1.0):
    """Return a normalized vector (array)."""
    sum = vec_sum(vec)
    return [(vec[i] / sum * n) for i in range(len(vec))]


def frange(a, b, c):
    """Return a list of floats in range [a,b] with step c."""
    res = []
    if float_eq(c, 0.0):
        warnings.warn("Step size zero.")
        return res
    while True:
        res += [a];
        a += c
        if ((c > 0) and (a > b)):
            break
        if ((c < 0) and (a < b)):
            break
    return res


# endregion

# region Classes

class Asset:
    """A single asset in a portfolio.

    The asset is characterized by three properties: The current price,
    the expected return and the volatility.

    """

    # Instance variables.
    price = 0.0
    name = ""
    volatility = 0.0
    expected_return = 0.0

    def __init__(self, price=0.0, name="",
                 volatility=0.0, expected_return=0.0):
        """Setup the asset.

        Parameters are the current price, its name, volatility and
        expected return.
        """
        self.price = price
        self.name = name
        self.volatility = volatility
        self.expected_return = expected_return

    def get_price(self):
        """Return the asset price."""
        return self.price

    def get_name(self):
        """Return the asset's name."""
        return self.name

    def get_volatility(self):
        """Return the asset's volatility."""
        return self.volatility

    def get_expected_return(self):
        """Return the asset's expected return."""
        return self.expected_return


class Portfolio:
    """A collection of assets and their correlations.

    This class computes properties of the current portfolio based on
    the assets and their correlations.

    """

    assets = []
    correlations = {}

    def __init__(self, data_source: list = None):
        """Initialize a new (default: empty) portfolio.

        Args:
            data_source: An array of DataSource objects.
        """
        self.assets = []
        self.correlations = {}
        if data_source != None:

            # First, we add the assets.
            for investment in data_source:
                self.add_asset(Asset(1.0,
                                     investment.get_name(),
                                     investment.volatility(),
                                     investment.expected_return()),
                               1.0)

            # Next, we setup their correlations.
            num = self.num_assets()
            if num > 1:
                for i in range(num):
                    for j in range(num):
                        if i != j:
                            self.set_asset_correlation(self.get_asset(i),
                                                       self.get_asset(j),
                                                       data_source[i].covariance_with(data_source[j]))

        # Finally, we normalize the current distribution.
        norm = vec_sum([x[1] for x in self.assets])
        for i in range(self.num_assets()):
            self.set_asset_number(1.0 / norm, i)

    def num_assets(self):
        """Return the number of assets in current portfolio."""
        return len(self.assets)

    def add_asset(self, new_asset, asset_number):
        """Add an asset to the current portfolio."""
        self.assets.append([new_asset, asset_number])

    def del_asset(self, asset):
        """Remove an asset from the current portfolio."""
        for i in range(len(self.assets)):
            if asset == self.assets[i][0]:
                del (self.assets[i])
                break

    def get_asset(self, i):
        """Return asset at index i in portfolio."""
        if i < len(self.assets): return self.assets[i][0]

    def get_asset_number(self, i):
        """Return the number of assets at index i in portfolio."""
        if i < len(self.assets): return self.assets[i][1]

    def set_asset_number(self, asset_number, i):
        """Set the number of assets at index i in portfolio."""
        if i < len(self.assets): self.assets[i][1] = asset_number

    def get_asset_value(self, i):
        """Return the value of asset at index i in portfolio."""
        return self.get_asset(i).get_price() * self.get_asset_number(i)

    def get_asset_fractional_value(self, i):
        """Return the fractional value the asset has in the portfolio."""
        try:
            return self.get_asset_value(i) / self.get_value()
        except ZeroDivisionError:
            warnings.warn("Portfolio value problem.")
            return 0.0

    def set_asset_number_with_value(self, new_value, i):
        """Set the number of assets at index i such that it has a given value."""
        try:
            if i < len(self.assets):
                self.assets[i][1] = new_value / self.get_asset(i).get_price()
        except ZeroDivisionError:
            warnings.warn("Asset price value problem.")
            pass

    def replace_asset(self, new_asset, new_number, i):
        """Replace asset at index i in portfolio."""
        self.assets[i] = [new_asset, new_number]

    def set_asset_correlation(self, asset1, asset2, corr):
        """Set a correlation of two assets in portfolio."""
        if asset1 != asset2:
            self.correlations[(asset1, asset2)] = corr
            self.correlations[(asset2, asset1)] = corr

    def get_asset_correlation(self, asset1, asset2):
        """Return the correlation of two assets in portfolio."""
        if (asset1, asset2) in self.correlations:
            return self.correlations[(asset1, asset2)]
        elif (asset2, asset1) in self.correlations:
            return self.correlations[(asset2, asset1)]
        else:
            return 0.0

    def get_asset_distribution(self):
        """Return the current asset distribution in portfolio."""
        distrib = []
        for i in range(self.num_assets()):
            distrib.append(self.get_asset_fractional_value(i))
        return distrib

    def set_asset_distribution(self, new_distrib: list):
        """Set a new asset distribution in portfolio.

        The length of the array must correspond to the number of
        assets and the numbers have to be normalized, i.e., add up to
        1.0. On return, the total portfolio value is unchanged.

        Args:
            new_distrib: Array with float in range [0,1].
        """

        # Check input vector.
        num = len(new_distrib)
        if num != self.num_assets():
            warnings.warn("Problem with number of assets in portfolio.")
            return
        if not (float_eq(vec_sum(new_distrib), 1.0)):
            warnings.warn("Problem with input vector normalization.")
            return

        # Adjust asset distribution in portfolio.
        total = self.get_value()
        for i in range(num):
            self.set_asset_number_with_value(total * new_distrib[i], i)

    def get_value(self):
        """Return the total value of portfolio."""
        total = 0.0
        for asset in self.assets:
            total += asset[0].get_price() * asset[1]
        return total

    def get_volatility(self):
        """Return the volatility of the current portfolio."""
        total = 0.0
        num = self.num_assets()
        if num == 0:
            return 0.0

        # First, process the diagonal values.
        for i in range(num):
            total += math.pow(self.get_asset(i).get_volatility() *
                              self.get_asset_fractional_value(i), 2)

        # Then, add correlations (off-diagonal), if present.
        for i in range(num):
            for j in range(i, num):
                total += (2.0 *
                          self.get_asset_correlation(self.get_asset(i),
                                                     self.get_asset(j)) *
                          self.get_asset_fractional_value(i) *
                          self.get_asset_fractional_value(j))

        # Return result.
        return math.sqrt(total)

    def get_expected_return(self):
        """Return the expected return of the current portfolio."""
        avg_ret = 0.0
        for i in range(self.num_assets()):
            avg_ret += (self.get_asset(i).get_expected_return() *
                        self.get_asset_fractional_value(i))
        return avg_ret

    def report(self):
        """Print portfolio with major characteristics."""
        print(("Portfolio with %d assets: " % self.num_assets()))
        for i in range(self.num_assets()):
            print(("'%s': %f units at %f = %f; vol = %f, exp. return = %f" %
                   (self.get_asset(i).get_name(),
                    self.get_asset_number(i),
                    self.get_asset(i).get_price(),
                    self.get_asset(i).get_price() * self.get_asset_number(i),
                    self.get_asset(i).get_volatility(),
                    self.get_asset(i).get_expected_return())))
        print(("Portfolio value:  %f" % self.get_value()))
        print(("Total volatility: %f" % self.get_volatility()))
        print(("Expected return:  %f" % self.get_expected_return()))


class PortfolioAnalysis:
    """A collection of functions to analyze a portfolio.

    This class provides methods to analyze a portfolio and find
    interesting properties like minimum variance lines and optimal
    portfolios.

    """

    # Instance variables.
    portfolio = None
    log_flag = False

    # Instance methods.
    def __init__(self, portfolio=None, log_flag=False):
        """Setup an instance of this class."""
        self.portfolio = portfolio
        self.log_flag = log_flag
        return

    def get_portfolio(self):
        """Return the current portfolio."""
        return self.portfolio

    def set_portfolio(self, new_portfolio):
        """Set the portfolio to be analyzed."""
        self.portfolio = new_portfolio

    def scan_two_assets(self, i: int, j: int, res: float = 0.01) -> list:
        """Scan a sub-portfolio of the current portfolio with two assets.

        Return the resulting volatility and expected returns as a
        2d-array for a selection of all possible mixtures of two
        assets in the portfolio (only mixtures at discrete steps as
        specified by the res parameter are computed). The contribution
        of the other assets in the portfolio is thus set to zero.

        Args:
            i: Index of asset 1.
            j: Index of asset 2.
            res: Resolution step size for iteration.

        Returns:
             Array of set (volatility, expected return, asset distribution).
        """

        result = []
        cdist = [0.0 for k in range(self.portfolio.num_assets())]
        for x in frange(0.0, 1.0, res):
            cdist[i] = x;
            cdist[j] = 1.0 - x
            self.portfolio.set_asset_distribution(cdist)
            result.append((self.portfolio.get_volatility(),
                           self.portfolio.get_expected_return(),
                           cdist))
        return result

    def scan_asset_pairs(self, res=0.01) -> list:
        """Scan all sub-portfolios to which only two assets contribute.

        Returns:
             Similar to `self.scan_two_assets`, an array is returned.

        """

        result = []
        for i in range(self.portfolio.num_assets() - 1):
            for j in range(i + 1, self.portfolio.num_assets()):
                result += self.scan_two_assets(i, j, res)
        return result

    def scan_montecarlo(self, num: int = 10000) -> list:
        """Scan the entire space of asset distributions.

        Performs a Monte-Carlo scan of the entire space of asset
        distributions possible with the current portfolio. All
        distributions have equal statistical weight.

        If the log_flag is set to True, results will be logged to
        logging.info.

        Args:
            num: Number of Monte-Carlo samples.

        Returns:
             Similar to `self.scan_two_assets`, an array is returned.

        """

        import random
        rnd = random.SystemRandom()

        import logging
        threshold = 0.1
        stage = threshold

        result = []
        for i in range(num):
            cdist = vec_norm([rnd.random() for j in
                              range(self.portfolio.num_assets())])
            self.portfolio.set_asset_distribution(cdist)
            result.append((self.portfolio.get_volatility(),
                           self.portfolio.get_expected_return(),
                           cdist))
            if threshold < float(i) / num:
                if self.log_flag:
                    logging.info('%2.0f%% done.' % (threshold * 100.0))
                threshold += stage

        return result

    def minimum_variance_montecarlo(self, num: int = 10000) -> tuple:
        """Find the minimum variance portfolio using a Monte-Carlo scan.

        Performs a Monte-Carlo scan of the entire space of asset
        distributions and ends on the distribution with the smallest
        variance found. The volatility and expected returns for this
        distribution are returned, the minimum variance distribution
        is set as the final distribution.

        If the log_flag is set to True, results will be logged to
        logging.info.

        Note:
            This algorithm works not only in case of simple,
            statistical Markowitz-portfolios, but also in case of more
            complex economic simulations based on system dynamics!

        Args:
            num: Number of Monte-Carlo samples.

        Returns:
             The pair of minimum volatility and corresponding
             expected return.

        """

        import random
        rnd = random.SystemRandom()

        import logging
        threshold = 0.1
        stage = threshold

        min_vol_dist = vec_norm([rnd.random()
                                 for j in range(self.portfolio.num_assets())])
        self.portfolio.set_asset_distribution(min_vol_dist)
        min_vol = self.portfolio.get_volatility()
        for i in range(num):
            cdist = vec_norm([rnd.random()
                              for j in range(self.portfolio.num_assets())])
            self.portfolio.set_asset_distribution(cdist)
            cvol = self.portfolio.get_volatility()
            if cvol < min_vol:
                min_vol_dist = cdist[:]
                min_vol = cvol
            if threshold < float(i) / num:
                if self.log_flag:
                    logging.info('%2.0f%% done.' % (threshold * 100.0))
                threshold += stage

        self.portfolio.set_asset_distribution(min_vol_dist)
        return (self.portfolio.get_volatility(),
                self.portfolio.get_expected_return())

    def asset_dist_hull(self, dist_set: list) -> list:
        """Find the convex hull of an array of points.

        This method finds the subset of points that form the convex
        hull of the input data. The format of the data points is as
        returned by scan_montecarlo. Thus, this method can be used as
        a follow-up to MC-scans of the space of asset distributions.

        The algorithm used is from
        <https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain>

        Note:
            Like `scan_montecarlo`, this method works for any model
            underlying a portfolio; even complex system-dynamics-based
            economic simulations are analyzed correctly by these
            functions.

        Args:
            dist_set: Input array of set (volatility, expected
                      return, asset distribution).

        Returns:
             Subset of input data points that form the convex hull
             of input data points.
        """

        # Work on duplicate set, remove degenerate points.
        if len(dist_set) < 2:
            warnings.warn("Too few total data points for contour.")
            return dist_set

        sort_p = dist_set[:]
        sort_p.sort(key=lambda x: x[1])
        sort_p.sort(key=lambda x: x[0])
        i = 1
        while i < len(sort_p):
            if (float_eq(sort_p[i - 1][0], sort_p[i][0]) and
                    float_eq(sort_p[i - 1][1], sort_p[i][1])):
                del (sort_p[i])
            else:
                i += 1

        if len(sort_p) < 2:
            warnings.warn("Too few unique data points for contour.")
            return sort_p

        # Auxiliary functions.
        def cross_z(o, a, b):
            """Z-component of 2d-cross product of \vec{o-a} and \vec{o-b}."""
            return ((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))

        # Compose lower hull.
        lower_hull = []
        for p in sort_p:
            while ((len(lower_hull) > 3) and
                   (cross_z(lower_hull[-2], lower_hull[-1], p) < 0.0)):
                lower_hull.pop()
            lower_hull.append(p)

        # Compose upper hull:
        upper_hull = []
        for p in reversed(sort_p):
            while ((len(upper_hull) > 3) and
                   (cross_z(upper_hull[-2], upper_hull[-1], p) < 0.0)):
                upper_hull.pop()
            upper_hull.append(p)

        # We are done - return result.
        return (lower_hull[:-1] + upper_hull[:-1])


# endregion

# region Main program
if __name__ == "__main__":
    print("Analysis - statistical analysis of portfolio models")

# endregion
