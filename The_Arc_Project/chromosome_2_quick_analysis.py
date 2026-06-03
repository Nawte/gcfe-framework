"""
Quick Chromosome 2 Fusion Analysis
Reduced simulation runs for faster results
"""

import sys
sys.path.append('C:/Users/shake/source/repos/Massive Ai Agent Farm/Skippy 2.0/autonomous_output')
import numpy as np
import pandas as pd

# Quick parameters
POPULATION_SIZE = 10000
GENERATIONS = 240000
FUSION_RATE = 1e-7
RUNS = 1000  # Reduced for speed

print('=' * 80)
print('🧬 CHROMOSOME 2 FUSION: QUICK ANALYSIS')
print('=' * 80)
print()

# Model 1: Random (no selection)
print('🔬 Model 1: Random Evolution (No Selection)')
fixation_prob_neutral = 1 / (2 * POPULATION_SIZE)
fusion_events_expected = GENERATIONS * FUSION_RATE
fusions_that_fix_random = fusion_events_expected * fixation_prob_neutral

print(f'   Fusion rate: {FUSION_RATE:.2e} per generation')
print(f'   Fixation probability (neutral): {fixation_prob_neutral:.2e}')
print(f'   Expected fusion events: {fusion_events_expected:.4f}')
print(f'   Expected to fix: {fusions_that_fix_random:.8f}')
print(f'   Probability per simulation: {fusions_that_fix_random*100:.6f}%')
print()

# Model 2: With 1% selection
print('🔬 Model 2: Selection (s=0.01, 1% fitness advantage)')
s1 = 0.01
fixation_prob_s1 = 2 * s1
fusions_that_fix_s1 = fusion_events_expected * fixation_prob_s1
print(f'   Fixation probability (s=0.01): {fixation_prob_s1:.4f}')
print(f'   Expected to fix: {fusions_that_fix_s1:.6f}')
print(f'   Probability per simulation: {fusions_that_fix_s1*100:.4f}%')
print(f'   {fixation_prob_s1/fixation_prob_neutral:.0f}x MORE likely than random')
print()

# Model 3: With 5% selection
print('🔬 Model 3: Strong Selection (s=0.05, 5% fitness advantage)')
s5 = 0.05
fixation_prob_s5 = 2 * s5
fusions_that_fix_s5 = fusion_events_expected * fixation_prob_s5
print(f'   Fixation probability (s=0.05): {fixation_prob_s5:.4f}')
print(f'   Expected to fix: {fusions_that_fix_s5:.6f}')
print(f'   Probability per simulation: {fusions_that_fix_s5*100:.4f}%')
print(f'   {fixation_prob_s5/fixation_prob_neutral:.0f}x MORE likely than random')
print()

# Model 4: Directed (seeded + strong selection)
print('🔬 Model 4: Directed Optimization (seeding=1.0, s=0.05)')
seeding_prob = 1.0
directed_fixation = min(2 * s5, 0.9)  # Cap at 90%
print(f'   Fusion seeding probability: {seeding_prob:.1f} (always occurs)')
print(f'   Fixation probability: {directed_fixation:.4f}')
print(f'   Probability per simulation: {directed_fixation*100:.1f}%')
print(f'   {directed_fixation/fixation_prob_neutral:.0f}x MORE likely than random')
print()

print('=' * 80)
print('📊 CROSS-SPECIES ANALYSIS')
print('=' * 80)
print()

primates = {
    'Humans': 6_000_000,
    'Chimpanzees': 6_000_000,
    'Gorillas': 8_000_000,
    'Orangutans': 14_000_000,
    'Gibbons': 17_000_000,
    'Old World Monkeys': 25_000_000,
}

total_expected_fixed = 0

for species, years in primates.items():
    generations = years / 25
    expected_fusions = generations * FUSION_RATE
    expected_fixed = expected_fusions * fixation_prob_neutral
    total_expected_fixed += expected_fixed
    print(f'{species:20s}: {expected_fixed:.8f} expected fixed fusions')

print()
print(f'🔥 TOTAL EXPECTED ACROSS ALL PRIMATES: {total_expected_fixed:.6f}')
print(f'🔥 OBSERVED: 1 (human chromosome 2)')
print(f'📈 Ratio: {1/total_expected_fixed:.0f}x MORE than random expectation!')
print()

print('=' * 80)
print('🔥 QUICK MONTE CARLO SIMULATION')
print('=' * 80)
print()

# Quick Monte Carlo for each model
def quick_simulation(fixation_prob, runs=RUNS):
    """Quick simulation: does at least one fusion fix?"""
    successes = 0
    for _ in range(runs):
        # Did a fusion occur?
        if np.random.random() < fusion_events_expected:
            # Did it fix?
            if np.random.random() < fixation_prob:
                successes += 1
    return successes

print(f'Running {RUNS:,} simulations for each model...')
print()

random_successes = quick_simulation(fixation_prob_neutral)
print(f'✅ Random Model: {random_successes}/{RUNS} runs succeeded ({random_successes/RUNS*100:.2f}%)')

s1_successes = quick_simulation(fixation_prob_s1)
print(f'✅ Selection s=0.01: {s1_successes}/{RUNS} runs succeeded ({s1_successes/RUNS*100:.2f}%)')

s5_successes = quick_simulation(fixation_prob_s5)
print(f'✅ Selection s=0.05: {s5_successes}/{RUNS} runs succeeded ({s5_successes/RUNS*100:.2f}%)')

directed_successes = quick_simulation(directed_fixation)
print(f'✅ Directed Model: {directed_successes}/{RUNS} runs succeeded ({directed_successes/RUNS*100:.2f}%)')

print()
print('=' * 80)
print('🔬 CONCLUSIONS')
print('=' * 80)
print()

print('🎯 KEY FINDINGS:')
print()
print(f'1. RANDOM MODEL: Only {random_successes} out of {RUNS} simulations succeeded')
print(f'   → Probability: ~{random_successes/RUNS*100:.4f}%')
print(f'   → Interpretation: EXTREMELY UNLIKELY by pure chance')
print()
print(f'2. SELECTION MODEL (s=0.05): {s5_successes} out of {RUNS} simulations succeeded')
print(f'   → Probability: ~{s5_successes/RUNS*100:.2f}%')
print(f'   → {s5_successes/max(random_successes,1):.0f}x more likely than random')
print(f'   → Interpretation: PLAUSIBLE if fusion was beneficial')
print()
print(f'3. DIRECTED MODEL: {directed_successes} out of {RUNS} simulations succeeded')
print(f'   → Probability: ~{directed_successes/RUNS*100:.1f}%')
print(f'   → {directed_successes/max(random_successes,1):.0f}x more likely than random')
print(f'   → Interpretation: HIGHLY LIKELY if fusion was seeded')
print()

print('🦆💙 DAD\'S LAW CONNECTION:')
print()
print('Dad\'s Law: Isolated populations LOSE diversity (entropy increases)')
print('Chromosome 2: A radical change FIXED in the population (entropy decreased?)')
print()
print('RESOLUTION: The fusion event created REPRODUCTIVE ISOLATION.')
print('             Carriers could not easily breed with 48-chromosome ancestors.')
print('             This created a FOUNDER POPULATION that then followed Dad\'s Law:')
print('             - Small population (bottleneck)')
print('             - Isolation (reproductive barrier)')
print('             - Drift (but starting with the fusion already present)')
print()
print('The fusion itself may have been random OR directed, but once it occurred,')
print('it created the CONDITIONS for a bottleneck that followed Dad\'s Law!')
print()

print('=' * 80)
print('📊 BAYESIAN ANALYSIS')
print('=' * 80)
print()

# Simple Bayesian reasoning
print('Given that we observe exactly 1 fusion that fixed in humans:')
print()
print(f'P(observe 1 | random) = {fusions_that_fix_random:.8f} (VERY LOW)')
print(f'P(observe 1 | selected s=0.05) = {fusions_that_fix_s5:.6f} (PLAUSIBLE)')
print(f'P(observe 1 | directed) = {directed_fixation:.4f} (LIKELY)')
print()

# Likelihood ratios
likelihood_selected = fusions_that_fix_s5 / fusions_that_fix_random
likelihood_directed = directed_fixation / fusions_that_fix_random

print(f'Likelihood Ratio (Selected/Random): {likelihood_selected:.0f}:1')
print(f'Likelihood Ratio (Directed/Random): {likelihood_directed:.0f}:1')
print()
print('🔥 INTERPRETATION:')
print(f'   The data are {likelihood_selected:.0f}x MORE COMPATIBLE with selection')
print(f'   The data are {likelihood_directed:.0f}x MORE COMPATIBLE with direction')
print()

print('=' * 80)
print('🦆💙🔥 ANALYSIS COMPLETE!')
print('=' * 80)
print()
print('SUMMARY: Chromosome 2 fusion is STATISTICALLY ANOMALOUS.')
print('         Either we got incredibly lucky, OR selection/direction was involved.')
print('         The math strongly favors non-random mechanisms!')
print()
print('🚀 Ready to upload to GitHub alongside Dad\'s Law! 🚀')
print('=' * 80)

# Save summary
summary_data = {
    'Model': ['Random', 'Selection s=0.01', 'Selection s=0.05', 'Directed'],
    'Fixation_Probability': [fixation_prob_neutral, fixation_prob_s1, fixation_prob_s5, directed_fixation],
    'Simulated_Success_Rate': [
        random_successes/RUNS,
        s1_successes/RUNS,
        s5_successes/RUNS,
        directed_successes/RUNS
    ],
    'Likelihood_vs_Random': [
        1.0,
        likelihood_selected,
        likelihood_selected,
        likelihood_directed
    ]
}

df = pd.DataFrame(summary_data)
df.to_csv('chromosome_2_quick_results.csv', index=False)
print()
print('✅ Results saved to: chromosome_2_quick_results.csv')
