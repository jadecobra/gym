import tail_risk_hedge

def print_header(scenario, delimiter_length=60):
    print("\n" + "-" * delimiter_length)
    print(f"\t{scenario} scenario")
    print("-" * delimiter_length)

def print_metrics(metrics):
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ')}: {value}")

data_provider = tail_risk_hedge.YahooFinanceDataProvider(
    cache_file="price_cache.pkl",
    put_options_cache_file="put_options_cache.pkl",
    vix_cache_file="vix_cache.pkl",
    seed=42
)
portfolio_value = 100000
insurance_ratio = 0.01

print_header("stable")
print_metrics(
    tail_risk_hedge.calculate_portfolio_metrics(
        portfolio_value=portfolio_value,
        insurance_ratio=insurance_ratio,
        **data_provider.generate_scenario("stable")
    )
)

print_header("crash")
print_metrics(
    tail_risk_hedge.calculate_portfolio_metrics(
        portfolio_value=portfolio_value,
        insurance_ratio=insurance_ratio,
        **data_provider.generate_scenario("crash")
    )
)