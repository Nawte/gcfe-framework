# genetic_mutation_model.py - Modeling Gene Fusion and Mutation Impact

import sys
sys.path.insert(0, 'core')
from biology_toolkit import translate_dna, find_mutation, AMINO_ACIDS

def run_gene_comparison(normal_sequence: str, mutant_sequence: str):
    """
    Compares a normal DNA sequence to a mutated one to show the functional impact.
    This simulates how a small structural change (a mutation) alters the protein output.
    """
    print("=========================================")
    print("🧬 STEP 1: Analyzing NORMAL Gene Sequence")
    print(f"DNA Input: {normal_sequence}")

    # Analyze Normal
    result_normal = translate_dna(normal_sequence)
    print(f"\n[✅] Protein Output (Normal): {result_normal['protein']}")
    print("-----------------------------------------")


    print("\n=========================================")
    print("🧬 STEP 2: Analyzing MUTANT Gene Sequence")
    print(f"DNA Input: {mutant_sequence}")

    # Analyze Mutant
    result_mutant = translate_dna(mutant_sequence)
    print(f"\n[❌] Protein Output (Mutant): {result_mutant['protein']}")
    print("-----------------------------------------")


    print("\n=========================================")
    print("🔬 STEP 3: Comparing the Impact (The 'Fusion' Effect)")

    # Find and report specific changes
    changes = find_mutation(normal_sequence, mutant_sequence)
    if changes:
        print(f"🔥 FOUND MUTATION IMPACTS:")
        for change in changes:
            print(f"- Location: {change['position']} | Change: {change['old']}-{change['new']}")
            print(f"  -> Amino Acid Shift: {change['amino_acid_old']} to {change['amino_acid_new']}")
    else:
        print("No significant amino acid changes detected.")

# --- EXAMPLE USAGE (Using a simplified, known mutation for demonstration) ---
if __name__ == "__main__":
    # Example: A common oncogene mutation simulation
    # Normal sequence segment (e.g., coding for a healthy protein domain)
    NORMAL_SEQ = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACT"

    # Mutated sequence segment (simulating a change in the code)
    MUTANT_SEQ = "ATGGTGCATCTGACTCCTGAG**T**AGTCTGCCGTTACT" # Changed G to T at position 15

    run_gene_comparison(NORMAL_SEQ, MUTANT_SEQ)