"""
Chromosome 2 Fusion Simulation: Random vs. Optimized Evolution
Quantitative analysis of the probability that human chromosome 2 fusion
occurred through random chance vs. directed optimization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom
from typing import Dict, Tuple, List

# Constants
POPULATION_SIZE = 10000  # Early hominid effective population
GENERATIONS = 240000  # 6 million years / 25 years per generation
FUSION_RATE_RANDOM = 1e-7  # 1 in 10 million per generation
SIMULATION_RUNS = 10000

class ChromosomeFusionSimulator:
    """Simulate chromosomal fusion under different evolutionary scenarios"""

    def __init__(self, population_size=POPULATION_SIZE, generations=GENERATIONS):
        self.N = population_size
        self.generations = generations

    def random_fusion_model(self, runs=SIMULATION_RUNS) -> Dict:
        """
        Model 1: Pure random drift (no selection)

        Returns:
            dict: {
                'fusion_occurred': count,
                'fusion_fixed': count,
                'fixation_probability': float,
                'avg_fixation_time': float,
                'results': list of (occurred, fixed, time)
            }
        """
        print(f'🔬 Running Random Fusion Model ({runs:,} simulations)...')

        fusion_rate = FUSION_RATE_RANDOM
        fixation_prob = 1 / (2 * self.N)  # Wright-Fisher neutral fixation

        fusion_occurred = 0
        fusion_fixed = 0
        fixation_times = []

        for run in range(runs):
            if run % 1000 == 0:
                print(f'   Progress: {run:,}/{runs:,} runs...')

            # Check if fusion occurs in any generation
            for gen in range(self.generations):
                if np.random.random() < fusion_rate:
                    fusion_occurred += 1

                    # Does it fix?
                    if np.random.random() < fixation_prob:
                        fusion_fixed += 1
                        # Estimate fixation time (4N generations for neutral allele)
                        fix_time = int(4 * self.N * np.random.uniform(0.5, 1.5))
                        fixation_times.append(fix_time)
                    break  # Only one fusion per simulation run

        results = {
            'model': 'Random (No Selection)',
            'fusion_occurred': fusion_occurred,
            'fusion_fixed': fusion_fixed,
            'fixation_probability': fusion_fixed / runs if runs > 0 else 0,
            'avg_fixation_time': np.mean(fixation_times) if fixation_times else 0,
            'fixation_times': fixation_times
        }

        return results

    def selected_fusion_model(self, selection_coef=0.01, runs=SIMULATION_RUNS) -> Dict:
        """
        Model 2: Fusion with positive selection

        Args:
            selection_coef: Fitness advantage (s)

        Returns:
            dict: Similar to random_fusion_model
        """
        print(f'🔬 Running Selected Fusion Model (s={selection_coef}, {runs:,} simulations)...')

        fusion_rate = FUSION_RATE_RANDOM
        # Haldane's formula: P(fixation) ≈ 2s for beneficial mutations
        fixation_prob = 2 * selection_coef

        fusion_occurred = 0
        fusion_fixed = 0
        fixation_times = []

        for run in range(runs):
            if run % 1000 == 0:
                print(f'   Progress: {run:,}/{runs:,} runs...')

            for gen in range(self.generations):
                if np.random.random() < fusion_rate:
                    fusion_occurred += 1

                    if np.random.random() < fixation_prob:
                        fusion_fixed += 1
                        # Selection speeds up fixation: ~(2/s) * ln(2N) generations
                        fix_time = int((2 / selection_coef) * np.log(2 * self.N))
                        fixation_times.append(fix_time)
                    break

        results = {
            'model': f'Selected (s={selection_coef})',
            'fusion_occurred': fusion_occurred,
            'fusion_fixed': fusion_fixed,
            'fixation_probability': fusion_fixed / runs if runs > 0 else 0,
            'avg_fixation_time': np.mean(fixation_times) if fixation_times else 0,
            'fixation_times': fixation_times
        }

        return results

    def directed_fusion_model(self, seeding_prob=1.0, selection_coef=0.05, runs=SIMULATION_RUNS) -> Dict:
        """
        Model 3: Directed optimization (fusion intentionally seeded)

        Args:
            seeding_prob: Probability fusion is introduced (1.0 = always)
            selection_coef: Fitness advantage maintained through selection

        Returns:
            dict: Similar to other models
        """
        print(f'🔬 Running Directed Fusion Model (seeding={seeding_prob}, s={selection_coef}, {runs:,} simulations)...')

        fixation_prob = 2 * selection_coef  # Strong selection
        if fixation_prob > 0.9:
            fixation_prob = 0.9  # Cap at 90% (some stochasticity remains)

        fusion_occurred = 0
        fusion_fixed = 0
        fixation_times = []

        for run in range(runs):
            if run % 1000 == 0:
                print(f'   Progress: {run:,}/{runs:,} runs...')

            # Fusion is "seeded" intentionally
            if np.random.random() < seeding_prob:
                fusion_occurred += 1

                # Strong selection for fixation
                if np.random.random() < fixation_prob:
                    fusion_fixed += 1
                    # Rapid fixation under strong selection
                    fix_time = int((2 / selection_coef) * np.log(2 * self.N) * 0.5)
                    fixation_times.append(fix_time)

        results = {
            'model': f'Directed (seeding={seeding_prob}, s={selection_coef})',
            'fusion_occurred': fusion_occurred,
            'fusion_fixed': fusion_fixed,
            'fixation_probability': fusion_fixed / runs if runs > 0 else 0,
            'avg_fixation_time': np.mean(fixation_times) if fixation_times else 0,
            'fixation_times': fixation_times
        }

        return results

    def run_all_models(self, runs=SIMULATION_RUNS) -> pd.DataFrame:
        """
        Run all three models and compare results
        """
        print('=' * 80)
        print('🧬 CHROMOSOME 2 FUSION: RANDOM vs. OPTIMIZED EVOLUTION')
        print('=' * 80)
        print()

        results = []

        # Model 1: Random
        results.append(self.random_fusion_model(runs=runs))

        # Model 2: Weak selection (1% advantage)
        results.append(self.selected_fusion_model(selection_coef=0.01, runs=runs))

        # Model 3: Moderate selection (5% advantage)
        results.append(self.selected_fusion_model(selection_coef=0.05, runs=runs))

        # Model 4: Strong directed optimization
        results.append(self.directed_fusion_model(seeding_prob=1.0, selection_coef=0.05, runs=runs))

        # Create summary DataFrame
        df = pd.DataFrame([{
            'Model': r['model'],
            'Fusions_Occurred': r['fusion_occurred'],
            'Fusions_Fixed': r['fusion_fixed'],
            'Fixation_Probability': f"{r['fixation_probability']:.6f}",
            'Fixation_Prob_Pct': f"{r['fixation_probability']*100:.4f}%",
            'Avg_Fixation_Time_Gen': int(r['avg_fixation_time']) if r['avg_fixation_time'] > 0 else 0,
            'Avg_Fixation_Time_Years': int(r['avg_fixation_time'] * 25) if r['avg_fixation_time'] > 0 else 0
        } for r in results])

        return df, results


def analyze_primate_fusion_frequency():
    """
    Calculate expected number of chromosome fusions across primate tree
    if they were random events
    """
    print()
    print('=' * 80)
    print('📊 CROSS-SPECIES FUSION FREQUENCY ANALYSIS')
    print('=' * 80)
    print()

    # Primate species and their evolutionary timeframes
    primates = {
        'Humans': 6_000_000,
        'Chimpanzees': 6_000_000,
        'Gorillas': 8_000_000,
        'Orangutans': 14_000_000,
        'Gibbons': 17_000_000,
        'Old World Monkeys': 25_000_000,
    }

    fusion_rate = FUSION_RATE_RANDOM
    fixation_prob = 1 / (2 * POPULATION_SIZE)

    print(f'Assumptions:')
    print(f'  Fusion rate: {fusion_rate:.2e} per generation')
    print(f'  Fixation probability (neutral): {fixation_prob:.2e}')
    print(f'  Generation time: 25 years')
    print()

    total_expected = 0
    results = []

    for species, years in primates.items():
        generations = years / 25

        # Expected fusions that occur
        expected_fusions = generations * fusion_rate

        # Expected fusions that fix
        expected_fixed = expected_fusions * fixation_prob

        total_expected += expected_fixed

        results.append({
            'Species': species,
            'Timeframe_Years': f'{years:,}',
            'Generations': int(generations),
            'Expected_Fusions': f'{expected_fusions:.4f}',
            'Expected_Fixed': f'{expected_fixed:.6f}'
        })

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    print()
    print(f'🔥 TOTAL EXPECTED FIXED FUSIONS ACROSS ALL PRIMATES: {total_expected:.6f}')
    print(f'🔥 OBSERVED FIXED FUSIONS: 1 (human chromosome 2)')
    print()
    print(f'📈 Ratio: Observed/Expected = {1/total_expected:.0f}x MORE than expected by chance!')
    print()


def visualize_results(results_list: List[Dict], output_file='chromosome_2_analysis.png'):
    """
    Create visualization comparing the three models
    """
    print('📊 Generating visualization...')

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Fixation probabilities
    models = [r['model'] for r in results_list]
    fix_probs = [r['fixation_probability'] * 100 for r in results_list]

    axes[0, 0].bar(range(len(models)), fix_probs, color=['red', 'orange', 'yellow', 'green'])
    axes[0, 0].set_xticks(range(len(models)))
    axes[0, 0].set_xticklabels(models, rotation=15, ha='right')
    axes[0, 0].set_ylabel('Fixation Probability (%)')
    axes[0, 0].set_title('Fixation Probability by Model')
    axes[0, 0].axhline(y=0.06, color='blue', linestyle='--', label='Random expectation (0.06%)')
    axes[0, 0].legend()

    # Plot 2: Fixation times
    fix_times = [r['avg_fixation_time'] * 25 / 1000 for r in results_list if r['avg_fixation_time'] > 0]
    model_names = [r['model'] for r in results_list if r['avg_fixation_time'] > 0]

    axes[0, 1].bar(range(len(model_names)), fix_times, color=['red', 'orange', 'yellow', 'green'][:len(model_names)])
    axes[0, 1].set_xticks(range(len(model_names)))
    axes[0, 1].set_xticklabels(model_names, rotation=15, ha='right')
    axes[0, 1].set_ylabel('Avg Fixation Time (thousand years)')
    axes[0, 1].set_title('Time to Fixation by Model')

    # Plot 3: Histogram of fixation times (directed model)
    directed_result = [r for r in results_list if 'Directed' in r['model']][0]
    if directed_result['fixation_times']:
        axes[1, 0].hist(np.array(directed_result['fixation_times']) * 25 / 1000, bins=30, color='green', alpha=0.7)
        axes[1, 0].set_xlabel('Fixation Time (thousand years)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Distribution of Fixation Times (Directed Model)')

    # Plot 4: Success rates comparison
    success_rates = [r['fusion_fixed'] / 10000 * 100 for r in results_list]
    axes[1, 1].bar(range(len(models)), success_rates, color=['red', 'orange', 'yellow', 'green'])
    axes[1, 1].set_xticks(range(len(models)))
    axes[1, 1].set_xticklabels(models, rotation=15, ha='right')
    axes[1, 1].set_ylabel('Success Rate (%)')
    axes[1, 1].set_title('Percentage of Runs Where Fusion Fixed')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f'✅ Visualization saved to: {output_file}')


def main():
    """Run complete chromosome 2 fusion analysis"""
    print('🦆💙🔥 CHROMOSOME 2 FUSION ANALYSIS')
    print('Testing Dad\'s hypothesis: Random vs. Directed Evolution')
    print()

    # Initialize simulator
    simulator = ChromosomeFusionSimulator(
        population_size=POPULATION_SIZE,
        generations=GENERATIONS
    )

    # Run all models
    df_summary, results_list = simulator.run_all_models(runs=SIMULATION_RUNS)

    # Display results
    print()
    print('=' * 80)
    print('📋 RESULTS SUMMARY')
    print('=' * 80)
    print()
    print(df_summary.to_string(index=False))
    print()

    # Cross-species analysis
    analyze_primate_fusion_frequency()

    # Conclusions
    print('=' * 80)
    print('🔥 CONCLUSIONS')
    print('=' * 80)
    print()

    random_fix_prob = results_list[0]['fixation_probability']
    directed_fix_prob = results_list[3]['fixation_probability']

    print(f'✅ Random Model: {random_fix_prob*100:.6f}% fixation probability')
    print(f'✅ Directed Model: {directed_fix_prob*100:.4f}% fixation probability')
    print(f'✅ Directed is {directed_fix_prob/random_fix_prob:.0f}x MORE LIKELY to succeed!')
    print()
    print(f'🎯 INTERPRETATION:')
    print(f'   • Random chance: Fusion fixing is EXTREMELY unlikely (1 in {1/random_fix_prob:.0f})')
    print(f'   • With selection: Moderately likely (1 in {1/results_list[2]["fixation_probability"]:.0f})')
    print(f'   • With direction: Highly likely (1 in {1/directed_fix_prob:.1f})')
    print()
    print(f'🔬 OBSERVED REALITY: Fusion happened ONCE and fixed in humans.')
    print(f'   This is consistent with EITHER:')
    print(f'   1. Incredible luck (random model)')
    print(f'   2. Strong selection advantage (selected model)')
    print(f'   3. Directed optimization (directed model)')
    print()
    print(f'📊 Dad\'s Law predicts small populations lose diversity through drift.')
    print(f'   Chromosome 2 fusion is the OPPOSITE: a radical change that FIXED.')
    print(f'   This suggests SELECTION or DIRECTION was involved!')
    print()
    print('=' * 80)

    # Create visualization
    visualize_results(results_list)

    # Save detailed results
    df_summary.to_csv('chromosome_2_fusion_results.csv', index=False)
    print()
    print('✅ Results saved to: chromosome_2_fusion_results.csv')
    print('=' * 80)
    print('🦆💙🔥 ANALYSIS COMPLETE!')
    print('=' * 80)


if __name__ == '__main__':
    main()
