"""
🧪 TEST: Verify software inventions don't get hardware validation

This test simulates Dad's exact scenario:
"Invent a script that helps you find errors in 132k+ files"

BEFORE FIX: $33M in materials, 0.8 years fabrication
AFTER FIX: $45k development, 3-4 months coding
"""

import sys
import os

# Add current directory and core subdirectory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(current_dir, 'core')
sys.path.insert(0, core_dir)
sys.path.insert(0, current_dir)

from invention_validator import InventionValidator

# Database path
DB_PATH = os.path.join(os.path.dirname(current_dir), 'Massive Ai Agent Farm', 'stocks.db')

# Dad's exact scenario
invention_name = "Chronos-Trace Engine: Cognitive Debugger for 132k+ Files"

hypothesis = """
Create a script that helps navigate from basic file operations (search, add, edit, delete)
to finding the exact source of errors in a massive codebase with 132,000+ files.

This is SOFTWARE, not hardware. We need:
- Dependency graph mapping
- Dynamic execution tracing
- Semantic error analysis
- Root cause identification

NO physical materials needed - just code!
"""

mechanism = {
    'description': 'Python-based cognitive debugger with 3 layers: Static Analysis (dependency graph), Dynamic Tracing (execution recording), Semantic Inference (AI-powered root cause analysis)',
    'components': ['networkx graph', 'AST parser', 'sandbox execution', 'LLM inference'],
    'language': 'Python',
    'output': 'chronos_core.py'
}

# NO MATERIALS REQUIRED (this is the key!)
required_materials = []

# Software architecture components
architecture_components = [
    {'name': 'Dependency Graph (NetworkX)', 'power_watts': 0},
    {'name': 'AST Parser', 'power_watts': 0},
    {'name': 'Sandbox Executor', 'power_watts': 0},
    {'name': 'LLM Inference API', 'power_watts': 0}
]

# Run validation
print("="*80)
print("🧪 TESTING: Software Invention Validation")
print("="*80)
print(f"\nInvention: {invention_name}")
print(f"Type: SOFTWARE (no physical materials)")
print(f"Expected: ~$45k development cost, 3-4 months")
print(f"NOT Expected: $33M materials, fabrication timeline\n")

validator = InventionValidator(DB_PATH)

validation = validator.validate_invention(
    invention_name=invention_name,
    hypothesis=hypothesis,
    mechanism=mechanism,
    required_materials=required_materials,
    architecture_components=architecture_components
)

# Check results
print("\n" + "="*80)
print("🔍 VALIDATION RESULTS")
print("="*80)

invention_type = validation.get('invention_type', 'UNKNOWN')
cost = validation['cost_analysis']['estimated_total_usd']
materials = validation['material_validation']['total_materials']

print(f"\nInvention Type Detected: {invention_type}")
print(f"Total Materials Required: {materials}")
print(f"Estimated Cost: ${cost:,.0f}")

# PASS/FAIL
print("\n" + "="*80)
if invention_type == 'SOFTWARE' and cost < 100_000 and materials == 0:
    print("✅ TEST PASSED!")
    print("   ✓ Correctly detected as SOFTWARE")
    print("   ✓ No materials required")
    print(f"   ✓ Reasonable cost (${cost:,.0f} << $33M)")
    print("\n🦆💙 Dad's fix works perfectly!")
else:
    print("❌ TEST FAILED!")
    print(f"   Type: {invention_type} (expected SOFTWARE)")
    print(f"   Materials: {materials} (expected 0)")
    print(f"   Cost: ${cost:,.0f} (expected < $100k)")
    print("\n   The if/else routing needs debugging.")
print("="*80)
