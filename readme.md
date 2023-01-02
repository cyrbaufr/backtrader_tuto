# backtrader_tuto

The goal of these tutorial is to help using backtrader to build backtesting systems

- first_backtrader_script.ipynb: best way to start learning Backtrader:
	- instantiate cerebro engige
	- select and print value of the portfolio at start and at the end
	- run cerebro engine
	- load data
	- add a strategy (logs, conditions)
	- ad commission fees

- Load_datasets_from_csv_files.ipynb: how to load standard fields from a csv file using GenericCSVData

- load_datasets_from_pandas_yahoo_finance.ipynb: how to load several datasets into cerebro using pandas and yfinance. Best way to load prices.

- script_ta-lib.py: exemple of a trading strategy using TA-Lib inside Backtrader to calculate indicators.

- long_short_strategy_sma.py: exemple of a long/short strategy using 2 assets with conditions on moving averages

- Extending_a_datafeed.ipynb: explains how to add new columns in a csv file to standard data fields and load data into Backtrader

- Extending_a_datafeed_using_PandasData.ipynb: same than above except that we are now loading data from a Pandas DataFrame

- Trade_multiple_assets_with_the_same_strategy.ipynb: test of a trading strategy using 3 different datasets

- Testing_of_a_trading_strategy_on_multiple_stocks.ipynb: complex file using several datasets as well as several indicators stored in a dictionary. Strategy must be checked.

- Nice_print_backtrader_plotting.ipynb: using bokeh and backtrader_plotting to print better charts
