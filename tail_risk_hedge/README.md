TODO

* fix calculate_option_payoff - currently does not use strike_price but accepts it as input
* cache options data info
* fix getting options expiration date
* use calculated risk-free rate - 30 year treasury
* refactor _estimate_implied_volatility to reflect real world
* increase options duration (what should the ideal duration be?)
* number of contracts to buy at what strike price with what expiration date
* expiration date of contracts
* how can we test this is in the real world?
* how to roll the options?
* remove cap of 0.1-0.5, the test can include extremes


DONE
* simulate options pricing
* calculate hedge
* display metrics
* add validation
* explicitly state option strategy