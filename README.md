# Portfolio

This is a collection of Python programs to illustrates the modern portfolio strategy by Harry Markowitz with fictional assets.

You can apply the programs to analyze real historical assets, but these are not included for legal reasons. Furthermore, real assets do not follow a Gaussian distribution at their edges, so any estimates for volatility, performance and correlation may not be sufficient to bet your money on them!

For further information see the accompanying blog post on <https://www.field-theory.org/posts/mathematics-of-investing.html>.

I had originally written the programs using Python 2.6, but have now migrated them to 3.8.

## Running the examples

Two programs can be invoked directly with:

`example1.py`
: Get the risk-return profile of asset allocations for the first dataset (two assets).

`example2.py`
: Get the risk-return profile of asset allocations for the second dataset (four assets).

If all dependencies listed in `requirements.txt` are installed plots in `.png` format will be generated. Otherwise, the report is only printed to `stdout`.

## Creating nice figures

For generating the figures the dependencies in `requirements.txt` are needed. The easiest way to handle that is a virtual environment:
```bash
python3 -m venv venv3
source venv3/bin/activate
pip install -r requirements.txt
```

Now running `example1.py` and `example2.py` will also generate the figures seen in the blog post.

## Running tests

This repository contains a small collection of test cases that are run on <https://travis-ci.org>.

They can be run manually via
```bash
pytest
```
