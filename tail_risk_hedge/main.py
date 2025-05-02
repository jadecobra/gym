import tail_risk_hedge

def print_header(scenario, delimiter_length=60):
    print('\n')
    print('-'*delimiter_length)
    print(f'\t{scenario} scenario')
    print('-'*delimiter_length)

def print_metrics(metrics):
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ')}: {value}")

data_provider = tail_risk_hedge.YahooFinanceDataProvider(
    seed=42, cache_file="price_cache.pkl", put_options_cache_file="put_options_cache.pkl"
)

print_header("dynamic stable")
print_metrics(
    tail_risk_hedge.calculate_portfolio_metrics(
        portfolio_value=100000,
        insurance_ratio=0.01,
        **data_provider.generate_scenario("stable")
    )
)

print_header("dynamic crash")
print_metrics(
    tail_risk_hedge.calculate_portfolio_metrics(
        portfolio_value=100000,
        insurance_ratio=0.01,
        **data_provider.generate_scenario("crash")
    )
)