#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Analysis.py

Summary:
    Test the `ModernPortfolio` module.

    For further documentation please refer to
    <https://www.field-theory.org/posts/mathematics-of-investing.html>

Copyright:
    (c) since 2008 by Dr. Wolfram Schroers <wolfram.schroers -at- field-theory.org>
    All rights reserved.

"""

# region Imports

import pytest
import os, sys

from ModernPortfolio import Analysis, Datasource


# endregion

# region Test cases

def test_timeseries():
    """Test the TimeSeries analysis (using Gaussian errors)."""
    asset_close = [22.9, 24.8, 40.3]
    ts = Datasource.TimeSeries(asset_close)

    assert ts is not None
    assert ts.volatility() == pytest.approx(0.27, 0.01)
    assert ts.expected_return() == pytest.approx(0.35, 0.03)
    assert len(ts.relative_returns()) == 2
    assert ts.relative_returns()[0] == pytest.approx(0.083, 0.01)
    assert ts.relative_returns()[1] == pytest.approx(0.62, 0.01)
    assert ts.covariance_with(Datasource.TimeSeries(asset_close)) == pytest.approx(0.0734493)


def test_datasource():
    """Test the additional capability of `Datasource` to associate a name with a `TimeSeries`."""
    asset_close = [22.9, 24.8, 40.3]
    ds = Datasource.DataSource(asset_close, 'My asset')

    assert ds is not None
    assert ds.volatility() == pytest.approx(0.27, 0.01)
    assert ds.expected_return() == pytest.approx(0.35, 0.03)
    assert ds.get_name() == 'My asset'


def test_analysis():
    """Test the full analysis of a portfolio."""
    asset1_close = [22.9, 24.8, 40.3]
    asset2_close = [101.3, 129.9, 104.5]

    analysis = Analysis.PortfolioAnalysis(Analysis.Portfolio([Datasource.DataSource(asset1_close, "Asset 1"),
                                                              Datasource.DataSource(asset2_close, "Asset 2")]))

    assert analysis is not None
    assert analysis.get_portfolio() is not None
    assert analysis.get_portfolio().num_assets() == 2

    biscan = analysis.scan_asset_pairs()
    assert type(biscan) is list
    assert len(biscan) == 100

    minvar = analysis.minimum_variance_montecarlo()
    assert type(minvar) is tuple
    assert len(minvar) == 2

# endregion
