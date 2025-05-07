import argparse
import pandas
import numpy
import tail_risk_hedge
import json
import os

class ResultPrinter:
    @staticmethod
    def print_scenario_results(scenario_type, metrics, delimiter_length=60):
        print("\n" + "-" * delimiter_length)
        print(f"\t{scenario_type.upper()} SCENARIO")
        print("-" * delimiter_length)
        sections = {
            "Market Conditions": [
                "scenario", "price_value_at_start", "price_value_at_end",
                "price_value_percent_change"
            ],
            "Option Strategy": [
                "option_strategy", "put_option_price", "number_of_contracts",
                "insurance_strategy_cost", "insurance_strategy_cost_as_percentage_of_portfolio"
            ],
            "Portfolio Performance": [
                "portfolio_value_at_start", "portfolio_value_at_end_with_insurance",
                "portfolio_value_at_end_without_insurance",
                "portfolio_value_percent_change_with_insurance",
                "portfolio_value_percent_change_without_insurance",
                "portfolio_profit_loss_with_insurance",
                "portfolio_profit_loss_without_insurance",
                "difference_between_portfolio_profit_with_insurance_and_without_insurance"
            ]
        }
        for section, keys in sections.items():
            print(f"\n{section}:")
            for key in keys:
                if key in metrics:
                    print(f"  {key.replace('_', ' ')}: {metrics[key]}")

    @staticmethod
    def print_comparison_results(comparison_df, key_metrics, delimiter_length=100):
        print("\n" + "=" * delimiter_length)
        print(f"\tCOMPARISON OF INSURANCE RATIOS")
        print("=" * delimiter_length)
        grouped = comparison_df.groupby('insurance_ratio')
        summary = grouped[key_metrics].agg(['mean', 'min', 'max', 'std'])
        pandas.set_option('display.float_format', '{:.4f}'.format)
        pandas.set_option('display.width', delimiter_length)
        print("\nSummary Statistics (mean, min, max, std):")
        print(summary)
        mean_returns = grouped['portfolio_value_percent_change_with_insurance'].mean()
        std_returns = grouped['portfolio_value_percent_change_with_insurance'].std().fillna(0)
        sharpe_ratios = mean_returns / std_returns.replace(0, numpy.inf)
        print("\nRisk-Adjusted Returns (higher is better):")
        for ratio, sharpe in sharpe_ratios.items():
            sharpe_val = sharpe if not numpy.isinf(sharpe) else mean_returns[ratio]
            print(f"  Insurance Ratio {ratio:.2%}: {sharpe_val:.4f}")
        best_ratio = sharpe_ratios.idxmax() if not sharpe_ratios.empty else comparison_df['insurance_ratio'].iloc[0]
        print(f"\nRecommended insurance ratio: {best_ratio:.2%}")
        if 'scenario' in comparison_df.columns:
            crash_data = comparison_df[comparison_df['scenario'] == 'crash']
            if not crash_data.empty:
                crash_grouped = crash_data.groupby('insurance_ratio')
                crash_protection = crash_grouped['difference_between_portfolio_profit_with_insurance_and_without_insurance'].mean()
                print("\nAverage Crash Protection (higher is better):")
                for ratio, protection in crash_protection.items():
                    print(f"  Insurance Ratio {ratio:.2%}: {protection:.2f}")

def load_config(config_path="config.json"):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def parse_arguments():
    config = load_config()
    parser = argparse.ArgumentParser(description="Run tail risk hedging scenarios")
    parser.add_argument("--portfolio", type=float, default=config.get('portfolio', 100000), help="Portfolio value (default: 100000)")
    parser.add_argument("--ratio", type=float, default=config.get('ratio', 0.01), help="Insurance ratio for single scenario (default: 0.01)")
    parser.add_argument("--scenarios", nargs="+", default=config.get('scenarios', ["stable", "crash"]), choices=["stable", "crash"], help="Scenarios to run (default: stable crash)")
    parser.add_argument("--seed", type=int, default=config.get('seed', 42), help="Random seed (default: 42)")
    parser.add_argument("--comparison", action="store_true", help="Run comparison mode with multiple insurance ratios")
    parser.add_argument("--min-ratio", type=float, default=config.get('min_ratio', 0.01), help="Minimum insurance ratio for comparison (default: 0.01)")
    parser.add_argument("--max-ratio", type=float, default=config.get('max_ratio', 0.03), help="Maximum insurance ratio for comparison (default: 0.03)")
    parser.add_argument("--ratio-steps", type=int, default=config.get('ratio_steps', 5), help="Number of steps between min and max ratio (default: 5)")
    parser.add_argument("--iterations", type=int, default=config.get('iterations', 10), help="Number of iterations for comparison mode (default: 10)")
    parser.add_argument("--cache-duration", type=int, default=config.get('cache_duration', 86400), help="Cache duration in seconds (default: 86400)")
    parser.add_argument("--risk-free-rate", type=float, default=config.get('risk_free_rate', 0.04), help="Risk-free rate (default: 0.04)")
    parser.add_argument("--time-to-expiry", type=float, default=config.get('time_to_expiry', 2/12), help="Time to option expiry in years (default: 2/12)")
    return parser.parse_args()

def run_scenario(data_provider, portfolio_value, insurance_ratio, scenario_type):
    scenario_data = data_provider.generate_scenario(scenario_type)
    return tail_risk_hedge.calculate_portfolio_metrics(
        portfolio_value=portfolio_value,
        insurance_ratio=insurance_ratio,
        **scenario_data
    )

def run_comparison(data_provider, portfolio_value, insurance_ratios, scenario_type, iterations=1):
    results = []
    for _ in range(iterations):
        scenario_data = data_provider.generate_scenario(scenario_type)
        for ratio in insurance_ratios:
            metrics = tail_risk_hedge.calculate_portfolio_metrics(
                portfolio_value=portfolio_value,
                insurance_ratio=ratio,
                **scenario_data
            )
            metrics['insurance_ratio'] = ratio
            results.append(metrics)
    return pandas.DataFrame(results)

def main():
    args = parse_arguments()
    data_provider = tail_risk_hedge.YahooFinanceDataProvider(
        cache_file="price_cache.pkl",
        put_options_cache_file="put_options_cache.pkl",
        vix_cache_file="vix_cache.pkl",
        seed=args.seed,
        cache_duration=args.cache_duration,
        risk_free_rate=args.risk_free_rate,
        time_to_expiry=args.time_to_expiry
    )
    key_metrics = [
        'portfolio_value_percent_change_with_insurance',
        'portfolio_value_percent_change_without_insurance',
        'difference_between_portfolio_profit_with_insurance_and_without_insurance'
    ]
    if args.comparison:
        insurance_ratios = numpy.linspace(args.min_ratio, args.max_ratio, args.ratio_steps).tolist()
        for scenario_type in args.scenarios:
            print(f"\n\nRunning {args.iterations} iterations of {scenario_type} scenario with ratios: {insurance_ratios}")
            comparison_results = run_comparison(
                data_provider,
                args.portfolio,
                insurance_ratios,
                scenario_type,
                args.iterations
            )
            ResultPrinter.print_comparison_results(comparison_results, key_metrics)
    else:
        for scenario_type in args.scenarios:
            metrics = run_scenario(data_provider, args.portfolio, args.ratio, scenario_type)
            ResultPrinter.print_scenario_results(scenario_type, metrics)

if __name__ == "__main__":
    main()