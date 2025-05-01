import tail_risk_hedge

def print_metrics(metrics):
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ')}: {value}")

# Stable scenario (original example)
stable_metrics = tail_risk_hedge.calculate_portfolio_metrics(
    portfolio_value=100000,
    hedge_ratio=0.01,
    spy_start=500,
    spy_end=525,
    strike_price=400,
    option_value_end=0,
    option_price=1,
    expiry_date="2025-07-18"
)
print("Stable Scenario:")
print_metrics(stable_metrics)

# Crash scenario
crash_metrics = tail_risk_hedge.calculate_portfolio_metrics(
    portfolio_value=100000,
    hedge_ratio=0.01,
    spy_start=500,
    spy_end=350,
    strike_price=400,
    option_value_end=50,
    option_price=1,
    expiry_date="2025-07-18"
)
print("\nCrash Scenario:")
print_metrics(crash_metrics)

data_provider = tail_risk_hedge.YahooFinanceDataProvider(seed=42, cache_file="spy_cache.pkl")
stable_data = data_provider.generate_scenario("stable")
crash_data = data_provider.generate_scenario("crash")

stable_metrics = tail_risk_hedge.calculate_portfolio_metrics(
    portfolio_value=100000,
    hedge_ratio=0.01,
    **stable_data
)
print("Dynamic Stable Scenario:")
print_metrics(stable_metrics)

crash_metrics = tail_risk_hedge.calculate_portfolio_metrics(
    portfolio_value=100000,
    hedge_ratio=0.01,
    **crash_data
)
print("\nDynamic Crash Scenario:")
print_metrics(crash_metrics)