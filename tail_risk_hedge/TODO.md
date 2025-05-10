TODO

* Implement cache migration logic to handle version changes gracefully (e.g., convert old cache formats to new ones)
* Add checks for cache file integrity (e.g., validate DataFrame structure before loading).
* migrate old cahce, fix cache versioning limitations
* fix synthetic data to simulate realism - clustering, fat tails
* use config file for out of money parameters
* improve exception handling for yfinance to be more robust
* test coverage - include cache corruption, extreme market conditions, concurrent API calls
* performance
* add documentation
* Reuse a single scenario for all ratios per iteration could improve consistency
* Integration tests for end-to-end execution (e.g., running main.main()) are missing, which could catch issues in argument parsing or scenario execution
* The _fetch_option_chain method assumes ticker_data.options is non-empty, which could fail if no options data is available.
* add visualization using matplotlib to create charts showing risk-return tradeoff between insurance ratios with pareto frontier to visualize efficient fronter of protection vs cost
* add comparison mode to run multiple ratios 0.1-0.3, displaying side-by-side compaison
* implement cache manager for unified cache handling across data sources - VIX, options, historical data
* replace option_price=1.0 with more robust default to improve realism
* fix getting options expiration date
* use calculated risk-free rate - 30 year treasury
* increase options duration (what should the ideal duration be?)
* number of contracts to buy at what strike price with what expiration date
* expiration date of contracts
* how can we test this is in the real world?
* how to roll the options?
* remove cap of 0.1-0.5, the test can include extremes
* round final display
* use Decimals instead of floats
* get VIX data from internet add to metrics
* Add support for multiple expiration dates or strike price ranges.
* optimize tests
* optimize code
* Support caching multiple expiration dates
* calculate the insurance strategy cost that would be profitable between 1-3%


Improve Synthetic Data:
Use a more sophisticated model for synthetic data, such as a geometric Brownian motion or GARCH model, to better simulate market dynamics.
Allow configuration of synthetic data parameters (e.g., volatility, drift) via arguments.
Make Hardcoded Parameters Configurable:
Add command-line arguments or config file options for:
Price range for out-of-the-money puts (currently 70%–90%).
Default volatility values (e.g., 0.2 for stable, 0.3 for crash).
Synthetic data generation parameters.
Expand Scenario Types:
Add support for additional scenarios (e.g., "bullish" with upward price trends, "volatile" with high fluctuations).
Allow users to define custom scenarios via the config file (e.g., specify price change ranges).
Strengthen Error Handling:
Extend backoff_retries to handle additional yfinance errors (e.g., ConnectionError, HTTPError).
Add fallback logic for invalid ticker data or missing option chains.
Improve Test Coverage:
Add tests for:
ResultPrinter methods to ensure correct formatting and output.
Cache corruption scenarios (e.g., truncated or malformed pickle files).
Edge cases in financial calculations (e.g., zero option prices, extreme price changes).
Use a coverage tool (e.g., pytest-cov) to identify untested code paths.
Optimize Performance:
Use parallel processing (e.g., multiprocessing or concurrent.futures) for comparison mode iterations.
Batch API calls to yfinance when fetching multiple data types (e.g., prices and options simultaneously).
Optimize DataFrame operations in run_comparison (e.g., preallocate DataFrame, use vectorized operations).
Add Documentation:
Create a README with:
Program overview and purpose.
Installation instructions (e.g., required packages: yfinance, pandas, numpy).
Usage examples for single-scenario and comparison modes.
Explanation of financial assumptions (e.g., why 2/12 years for time to expiry).
Add docstrings to key functions (e.g., calculate_portfolio_metrics, generate_scenario) describing parameters, return values, and assumptions.
Enhance Logging:
Add more detailed logging for key operations (e.g., scenario generation, API call successes/failures).
Allow configuration of log levels (e.g., via command-line argument --verbose).
Add Input Validation for Ratios:
Ensure --min-ratio, --max-ratio, and --ratio are within reasonable bounds (e.g., 0 to 1).
Validate that --min-ratio ≤ --max-ratio and --ratio-steps produces valid steps.
Support Additional Data Sources:
Add support for alternative data providers (e.g., Alpha Vantage, IEX Cloud) to reduce reliance on yfinance.
Implement an abstract data provider interface to make it easy to swap providers.


DONE
* cache VIX data
* refactor _estimate_implied_volatility to reflect real world
* fix calculate_option_payoff
* cache options data info
* simulate options pricing
* calculate hedge
* display metrics
* add validation
* explicitly state option strategy