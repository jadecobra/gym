import tail_risk_hedge
import argparse
import pandas
import numpy

def run_scenario(data_provider, portfolio_value, insurance_ratio, scenario_type):
    """Run a single scenario and return metrics."""
    scenario_data = data_provider.generate_scenario(scenario_type)
    return tail_risk_hedge.calculate_portfolio_metrics(
        portfolio_value=portfolio_value,
        insurance_ratio=insurance_ratio,
        **scenario_data
    )

def print_scenario_results(scenario_type, metrics, delimiter_length=60):
    """Print formatted results for a scenario."""
    print("\n" + "-" * delimiter_length)
    print(f"\t{scenario_type.upper()} SCENARIO")
    print("-" * delimiter_length)

    # Group and order metrics for better readability
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

def run_comparison(data_provider, portfolio_value, insurance_ratios, scenario_type, iterations=1):
    """
    Run multiple scenarios with different insurance ratios and compare results.

    Args:
        data_provider: The data provider instance
        portfolio_value: Initial portfolio value
        insurance_ratios: List of insurance ratios to compare
        scenario_type: Type of scenario to run ('stable' or 'crash')
        iterations: Number of simulations to run per ratio

    Returns:
        DataFrame with comparison results
    """
    results = []

    for _ in range(iterations):
        # Use the same scenario data for all ratios in this iteration
        scenario_data = data_provider.generate_scenario(scenario_type)

        for ratio in insurance_ratios:
            metrics = tail_risk_hedge.calculate_portfolio_metrics(
                portfolio_value=portfolio_value,
                insurance_ratio=ratio,
                **scenario_data
            )

            # Add ratio to metrics for identification
            metrics['insurance_ratio'] = ratio
            results.append(metrics)

    return pandas.DataFrame(results)

def print_comparison_results(comparison_df, key_metrics, delimiter_length=100):
    """
    Print formatted comparison results.

    Args:
        comparison_df: DataFrame with comparison results
        key_metrics: List of metrics to display in comparison
        delimiter_length: Length of delimiter line
    """
    print("\n" + "=" * delimiter_length)
    print(f"\tCOMPARISON OF INSURANCE RATIOS")
    print("=" * delimiter_length)

    # Group by insurance ratio and calculate statistics
    grouped = comparison_df.groupby('insurance_ratio')
    summary = grouped[key_metrics].agg(['mean', 'min', 'max', 'std'])

    # Print summary statistics
    pandas.set_option('display.float_format', '{:.4f}'.format)
    pandas.set_option('display.width', delimiter_length)
    print("\nSummary Statistics (mean, min, max, std):")
    print(summary)

    # Find optimal ratio based on risk-adjusted return
    mean_returns = grouped['portfolio_value_percent_change_with_insurance'].mean()
    std_returns = grouped['portfolio_value_percent_change_with_insurance'].std().fillna(0)
    sharpe_ratios = mean_returns / std_returns.replace(0, numpy.inf)

    print("\nRisk-Adjusted Returns (higher is better):")
    for ratio, sharpe in sharpe_ratios.items():
        sharpe_val = sharpe if not numpy.isinf(sharpe) else mean_returns[ratio]
        print(f"  Insurance Ratio {ratio:.2%}: {sharpe_val:.4f}")

    # Print recommendation
    best_ratio = sharpe_ratios.idxmax() if not sharpe_ratios.empty else insurance_ratios[0]
    print(f"\nRecommended insurance ratio: {best_ratio:.2%}")

    # Show performance in crash scenarios
    if 'scenario' in comparison_df.columns:
        crash_data = comparison_df[comparison_df['scenario'] == 'crash']
        if not crash_data.empty:
            crash_grouped = crash_data.groupby('insurance_ratio')
            crash_protection = crash_grouped['difference_between_portfolio_profit_with_insurance_and_without_insurance'].mean()

            print("\nAverage Crash Protection (higher is better):")
            for ratio, protection in crash_protection.items():
                print(f"  Insurance Ratio {ratio:.2%}: {protection:.2f}")

def main():
    """Main function to run tail risk hedge scenarios and comparisons."""
    parser = argparse.ArgumentParser(description="Run tail risk hedging scenarios")
    parser.add_argument("--portfolio", type=float, default=100000,
                        help="Portfolio value (default: 100000)")
    parser.add_argument("--ratio", type=float, default=0.01,
                        help="Insurance ratio for single scenario (default: 0.01)")
    parser.add_argument("--scenarios", nargs="+", default=["stable", "crash"],
                        choices=["stable", "crash"],
                        help="Scenarios to run (default: stable crash)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    parser.add_argument("--comparison", action="store_true",
                        help="Run comparison mode with multiple insurance ratios")
    parser.add_argument("--min-ratio", type=float, default=0.01,
                        help="Minimum insurance ratio for comparison (default: 0.01)")
    parser.add_argument("--max-ratio", type=float, default=0.03,
                        help="Maximum insurance ratio for comparison (default: 0.03)")
    parser.add_argument("--ratio-steps", type=int, default=5,
                        help="Number of steps between min and max ratio (default: 5)")
    parser.add_argument("--iterations", type=int, default=10,
                        help="Number of iterations for comparison mode (default: 10)")
    args = parser.parse_args()

    data_provider = tail_risk_hedge.YahooFinanceDataProvider(
        cache_file="price_cache.pkl",
        put_options_cache_file="put_options_cache.pkl",
        vix_cache_file="vix_cache.pkl",
        seed=args.seed
    )

    if args.comparison:
        # Generate insurance ratios from min to max
        insurance_ratios = numpy.linspace(args.min_ratio, args.max_ratio, args.ratio_steps).tolist()

        key_metrics = [
            'portfolio_value_percent_change_with_insurance',
            'portfolio_value_percent_change_without_insurance',
            'difference_between_portfolio_profit_with_insurance_and_without_insurance'
        ]

        for scenario_type in args.scenarios:
            print(f"\n\nRunning {args.iterations} iterations of {scenario_type} scenario with ratios: {insurance_ratios}")
            comparison_results = run_comparison(
                data_provider,
                args.portfolio,
                insurance_ratios,
                scenario_type,
                args.iterations
            )
            print_comparison_results(comparison_results, key_metrics)
    else:
        # Run single scenarios
        for scenario_type in args.scenarios:
            metrics = run_scenario(data_provider, args.portfolio, args.ratio, scenario_type)
            print_scenario_results(scenario_type, metrics)

if __name__ == "__main__":
    main()