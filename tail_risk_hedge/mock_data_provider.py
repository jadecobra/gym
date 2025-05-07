import numpy
import pandas
import datetime
import random

class MockDataProvider:
    """
    Mock data provider to use when YahooFinance is unavailable due to rate limiting.
    Generates synthetic market data based on empirical distributions.
    """

    def __init__(self, *, ticker="SPY", seed=None):
        if seed is not None:
            random.seed(seed)
            numpy.random.seed(seed)

        self.ticker = ticker
        self.current_price = 460.0  # Approximate SPY price
        self.risk_free_rate = 0.04
        self.time_to_expiry = 2 / 12

        # Generate synthetic historical data
        self._generate_historical_data()

    def _generate_historical_data(self):
        """Generate synthetic price history with realistic statistical properties."""
        days = 252  # One year of trading days
        daily_returns = numpy.random.normal(0.0003, 0.01, days)  # ~8% annual return, ~16% annual volatility

        # Start with current price and work backwards
        prices = [self.current_price]
        for ret in daily_returns:
            prices.append(prices[-1] / (1 + ret))
        prices.reverse()  # Now in chronological order

        # Create realistic OHLC data
        dates = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(days, 0, -1)]

        data = []
        for i, base_price in enumerate(prices):
            daily_volatility = base_price * 0.005 * (1 + random.uniform(-0.5, 1))
            high_price = base_price + daily_volatility * random.uniform(0.2, 1.0)
            low_price = base_price - daily_volatility * random.uniform(0.2, 1.0)

            # Ensure open and close are between high and low
            open_price = random.uniform(low_price, high_price)
            close_price = prices[i]  # Use the generated price as close

            # Make sure close respects high/low bounds
            close_price = max(low_price, min(high_price, close_price))

            data.append({
                'Date': dates[i],
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price
            })

        self.historical_data = pandas.DataFrame(data)
        self.historical_data.set_index('Date', inplace=True)

    def _generate_option_chain(self, price):
        """Generate synthetic option chain with realistic pricing."""
        volatility = self._get_vix_volatility()
        expiry_days = 60
        expiry_date = (datetime.datetime.now() + datetime.timedelta(days=expiry_days)).strftime("%Y-%m-%d")

        # Generate strikes from 70% to 130% of current price
        strikes = numpy.linspace(price * 0.7, price * 1.3, 15)

        put_data = []
        for strike in strikes:
            # Simple Black-Scholes approximation
            moneyness = strike / price
            time_value = price * volatility * numpy.sqrt(expiry_days/365)
            intrinsic_value = max(0, strike - price)

            # OTM puts are cheaper as strike decreases
            if moneyness < 1:
                option_price = time_value * moneyness + intrinsic_value
            else:
                option_price = time_value + intrinsic_value

            # Add some noise
            option_price *= (1 + random.uniform(-0.1, 0.1))

            put_data.append({
                'strike': strike,
                'lastPrice': option_price,
                'bid': option_price * 0.95,
                'ask': option_price * 1.05,
                'impliedVolatility': volatility * (1.5 - moneyness),  # Higher IV for lower strikes (skew)
                'volume': int(random.uniform(10, 1000) * (2 - moneyness)),  # More volume near the money
                'openInt': int(random.uniform(100, 10000) * (2 - moneyness))
            })

        puts = pandas.DataFrame(put_data)
        return puts, expiry_date

    def _get_vix_volatility(self, scenario="stable"):
        """Get synthetic VIX volatility level."""
        base_volatility = 0.18  # ~18% in normal markets
        if scenario == "crash":
            return base_volatility * 2.0  # ~36% in crash scenario
        return base_volatility

    def generate_scenario(self, scenario="stable"):
        """Generate market scenario with price movements and option data."""
        if scenario == "stable":
            price_change = random.normalvariate(0.03, 0.08)  # Slight upward bias
        else:  # crash
            price_change = random.normalvariate(-0.15, 0.08)  # Strong downward bias

        price_at_start = self.current_price
        price_at_end = price_at_start * (1 + price_change)

        # Ensure crash scenarios actually crash
        if scenario == "crash" and price_at_end > price_at_start * 0.9:
            price_at_end = price_at_start * random.uniform(0.7, 0.9)

        puts, expiry_date = self._generate_option_chain(price_at_start)

        # Select an OTM put option
        otm_puts = puts[puts['strike'] <= price_at_start * 0.9]
        if len(otm_puts) > 0:
            put = otm_puts.sample(n=1).iloc[0]
        else:
            # Fallback if no suitable puts
            strike_price = price_at_start * 0.8
            option_price = price_at_start * 0.02  # ~2% of underlying price

        strike_price = put['strike']
        option_price = put['lastPrice']

        return {
            "price_at_start": price_at_start,
            "price_at_end": price_at_end,
            "strike_price": strike_price,
            "option_price": option_price,
            "expiry_date": expiry_date
        }