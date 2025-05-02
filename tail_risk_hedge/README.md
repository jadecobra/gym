TODO

* abstract test_calculate_option_payoff_stable and test_calculate_option_payoff_crash
* abstract _load_data and _load_put_options_cache
* fix getting options expiration date
* use calculated risk-free rate - 30 year treasury
* refactor _estimate_implied_volatility to reflect real world
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


DONE
* fix calculate_option_payoff
* cache options data info
* simulate options pricing
* calculate hedge
* display metrics
* add validation
* explicitly state option strategy