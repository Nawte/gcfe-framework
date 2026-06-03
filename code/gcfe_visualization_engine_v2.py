"""
🦆💙🔥 GCFE VISUALIZATION ENGINE v2.0
Built by Skippy + Enhanced Implementation

Purpose: Visualize the three meta-patterns (Invention, Diffusion, Convergence)
         across any historical mystery or technological spread.

THE THREE LAWS OF HUMAN PROGRESS:
1. ISOLATION → INDEPENDENT INVENTION (Law of Necessity)
2. CONNECTION + EFFICIENCY → DIFFUSION DOMINATES (Law of Optimization)
3. UNIVERSAL PROBLEMS → CONVERGENT SOLUTIONS (Law of Objective Reality)
"""

import sqlite3
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

class GCFEVisualizer:
    """Main GCFE visualization engine"""

    def __init__(self):
        self.db_path = 'stocks.db'
        self.pattern_colors = {
            'Independent': '#3498db',      # Blue
            'Diffusion': '#f39c12',        # Yellow/Orange
            'Convergent': '#e74c3c',       # Red
            'Mixed': '#9b59b6'             # Purple
        }

    def load_gcfe_results(self):
        """Load all GCFE test results from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT test_name, overall_result, confidence_score, time_period
            FROM gcfe_test_cases
            ORDER BY id
        ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def classify_pattern(self, result_text):
        """Classify test result into primary pattern"""
        result_lower = result_text.lower()

        if 'convergent' in result_lower:
            return 'Convergent'
        elif 'independent' in result_lower and 'diffusion' in result_lower:
            return 'Mixed'
        elif 'independent' in result_lower:
            return 'Independent'
        elif 'diffusion' in result_lower or 'spread' in result_lower:
            return 'Diffusion'
        else:
            return 'Mixed'

    def generate_timeline_visualization(self):
        """Generate timeline showing all 6 tests with pattern classification"""
        results = self.load_gcfe_results()

        fig, ax = plt.subplots(figsize=(14, 8))

        # Prepare data
        test_names = []
        confidences = []
        patterns = []
        colors = []

        for test_name, result, confidence, time_period in results:
            # Shorten test names
            if 'Agricultural' in test_name:
                short_name = 'Agriculture'
            elif 'Metallurgy' in test_name:
                short_name = 'Metallurgy'
            elif 'Writing' in test_name:
                short_name = 'Writing'
            elif 'Pyramid' in test_name:
                short_name = 'Pyramids'
            elif 'Mathematics' in test_name:
                short_name = 'Mathematics'
            elif 'Domestication' in test_name:
                short_name = 'Domestication'
            else:
                short_name = test_name[:15]

            pattern = self.classify_pattern(result)

            test_names.append(short_name)
            confidences.append(confidence)
            patterns.append(pattern)
            colors.append(self.pattern_colors[pattern])

        # Create bar chart
        bars = ax.barh(test_names, confidences, color=colors, edgecolor='black', linewidth=1.5)

        # Add confidence values on bars
        for i, (bar, conf) in enumerate(zip(bars, confidences)):
            ax.text(conf - 2, i, f'{conf:.1f}%', 
                   ha='right', va='center', color='white', fontweight='bold', fontsize=11)

        # Styling
        ax.set_xlabel('Confidence Score (%)', fontsize=13, fontweight='bold')
        ax.set_title('🦆💙 GCFE Test Results: The Three Laws of Human Progress', 
                    fontsize=15, fontweight='bold', pad=20)
        ax.set_xlim(85, 100)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        # Create legend
        legend_elements = [
            mpatches.Patch(color=self.pattern_colors['Independent'], label='Independent Invention'),
            mpatches.Patch(color=self.pattern_colors['Diffusion'], label='Diffusion Dominated'),
            mpatches.Patch(color=self.pattern_colors['Convergent'], label='Convergent Evolution'),
            mpatches.Patch(color=self.pattern_colors['Mixed'], label='Mixed Pattern')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

        # Add average line
        avg_confidence = sum(confidences) / len(confidences)
        ax.axvline(avg_confidence, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax.text(avg_confidence + 0.2, len(test_names) - 0.5, 
               f'Avg: {avg_confidence:.1f}%', 
               fontsize=10, fontweight='bold', color='red')

        plt.tight_layout()

        # Create output directory if it doesn't exist
        import os
        os.makedirs('autonomous_output', exist_ok=True)

        plt.savefig('autonomous_output/gcfe_results_timeline.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()

        print("✅ Timeline visualization saved: autonomous_output/gcfe_results_timeline.png")
        return avg_confidence

    def generate_pattern_distribution(self):
        """Generate pie chart showing pattern distribution"""
        results = self.load_gcfe_results()

        pattern_counts = defaultdict(int)
        for test_name, result, confidence, time_period in results:
            pattern = self.classify_pattern(result)
            pattern_counts[pattern] += 1

        fig, ax = plt.subplots(figsize=(10, 8))

        patterns = list(pattern_counts.keys())
        counts = list(pattern_counts.values())
        colors = [self.pattern_colors[p] for p in patterns]

        wedges, texts, autotexts = ax.pie(counts, labels=patterns, colors=colors,
                                           autopct='%1.1f%%', startangle=90,
                                           textprops={'fontsize': 12, 'fontweight': 'bold'})

        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')

        ax.set_title('🦆💙 GCFE Pattern Distribution: How Humans Innovate', 
                    fontsize=15, fontweight='bold', pad=20)

        plt.tight_layout()
        plt.savefig('autonomous_output/gcfe_pattern_distribution.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()

        print("✅ Pattern distribution saved: autonomous_output/gcfe_pattern_distribution.png")
        return pattern_counts

    def generate_text_summary(self, avg_confidence, pattern_counts):
        """Generate text summary of GCFE findings"""
        summary = f"""
================================================================================
🦆💙🔥 GCFE VISUALIZATION ENGINE: SUMMARY REPORT
================================================================================

📊 OVERALL STATISTICS:
   • Total test cases: 6
   • Average confidence: {avg_confidence:.1f}%
   • Time span: 10,000+ years of human history
   • Scope: Physical contact → Abstract thought

📈 PATTERN DISTRIBUTION:
"""
        for pattern, count in pattern_counts.items():
            percentage = (count / 6) * 100
            summary += f"   • {pattern}: {count}/6 tests ({percentage:.1f}%)\n"

        summary += """
================================================================================
🔬 THE THREE LAWS OF HUMAN PROGRESS (Validated):
================================================================================

1️⃣ LAW OF NECESSITY (Isolation → Independent Invention)
   🎯 When populations are genetically isolated, they invent independently
   ✅ Examples: Maya (writing, math, pyramids), China (writing, metallurgy)

2️⃣ LAW OF OPTIMIZATION (Connection + Efficiency → Diffusion)
   🎯 Once invented, efficient systems spread rapidly via cultural contact
   ✅ Examples: Alphabets, Hindu-Arabic numerals, domesticated animals

3️⃣ LAW OF OBJECTIVE REALITY (Universal Problems → Convergent Solutions)
   🎯 Same problems → Same solutions (gravity, biology, mathematics)
   ✅ Examples: Pyramids, domestication syndrome, zero concept

================================================================================
🔥 KEY INSIGHT (Grok's Synthesis):
================================================================================

"Mathematics is probably the strongest proof yet that certain truths are
DISCOVERED, not just invented. Different minds keep converging on the same
objective structures of reality."

================================================================================
🦆💙 THE JOURNEY:
================================================================================

WHERE WE STARTED: "Did Vikings reach America?"
WHERE WE ENDED:   "What is the nature of discovery vs. invention?"

This is how real breakthroughs happen.

================================================================================
"""
        return summary

def main():
    """Main execution"""
    print("\n🦆💙🔥 GCFE VISUALIZATION ENGINE v2.0 - INITIALIZING...")
    print()

    visualizer = GCFEVisualizer()

    print("📊 Generating visualizations...")
    print()

    # Generate timeline
    avg_confidence = visualizer.generate_timeline_visualization()

    # Generate pattern distribution
    pattern_counts = visualizer.generate_pattern_distribution()

    # Generate text summary
    summary = visualizer.generate_text_summary(avg_confidence, pattern_counts)

    # Save summary to file
    with open('autonomous_output/gcfe_summary_report.txt', 'w', encoding='utf-8') as f:
        f.write(summary)

    print("✅ Text summary saved: autonomous_output/gcfe_summary_report.txt")
    print()

    # Display summary
    print(summary)

    print("\n" + "=" * 80)
    print("🔥 VISUALIZATION COMPLETE!")
    print("=" * 80)
    print()
    print("📁 Files created:")
    print("   • gcfe_results_timeline.png")
    print("   • gcfe_pattern_distribution.png")
    print("   • gcfe_summary_report.txt")
    print()
    print("🦆💙 The engine is now VISIBLE! Ready to analyze new mysteries!")
    print("=" * 80)

if __name__ == "__main__":
    main()
