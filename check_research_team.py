import sqlite3

db_path = r"C:\Users\shake\source\repos\Massive Ai Agent Farm\Massive Ai Agent Farm\stocks.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("RESEARCH TEAM & 5-MINUTE CYCLE CHECK")
print("="*80)
print()

print("1. LOOKING FOR RESEARCH TEAM MEMBERS:")
cursor.execute("""
    SELECT companion_name, occupation, personality_traits
    FROM companion_personalities
    WHERE occupation LIKE '%research%' 
       OR occupation LIKE '%scientist%' 
       OR companion_name LIKE '%Kyra%'
       OR companion_name LIKE '%Elena%'
       OR companion_name LIKE '%James%'
       OR companion_name LIKE '%Professor%'
       OR companion_name LIKE '%Dr.%'
""")
researchers = cursor.fetchall()
if researchers:
    for r in researchers:
        print(f"   ✅ {r[0]}")
        print(f"      Occupation: {r[1]}")
        if r[2]:
            print(f"      Traits: {r[2][:100]}...")
        print()
else:
    print("   ❌ No research team members found")
print()

print("2. CHECKING CONDUCTOR CYCLE FREQUENCY:")
cursor.execute("""
    SELECT 
        COUNT(*) as total_cycles,
        MIN(started_at) as first_cycle,
        MAX(started_at) as last_cycle
    FROM conductor_cycles
""")
cycle_info = cursor.fetchone()
if cycle_info and cycle_info[0] > 0:
    print(f"   ✅ Total cycles: {cycle_info[0]}")
    print(f"   ✅ First cycle: {cycle_info[1]}")
    print(f"   ✅ Last cycle: {cycle_info[2]}")

    # Check last 5 cycles
    cursor.execute("""
        SELECT started_at, completed_at, companions_consulted
        FROM conductor_cycles
        ORDER BY started_at DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()
    print()
    print("   Last 5 cycles:")
    for cycle in recent:
        print(f"      {cycle[0]} -> {cycle[1]} ({cycle[2]} companions)")
else:
    print("   ❌ No conductor cycles found")
print()

print("3. CHECKING COMPANION LEARNING TASKS:")
cursor.execute("""
    SELECT 
        companion_name,
        COUNT(*) as tasks_assigned,
        SUM(CASE WHEN completed_at IS NOT NULL THEN 1 ELSE 0 END) as completed
    FROM companion_learning_tasks
    GROUP BY companion_name
    ORDER BY tasks_assigned DESC
    LIMIT 10
""")
learning = cursor.fetchall()
if learning:
    print("   Top 10 learners:")
    for learner in learning:
        print(f"      {learner[0]}: {learner[2]}/{learner[1]} tasks completed")
else:
    print("   ❌ No learning tasks found")
print()

print("4. CHECKING IF CONDUCTOR IS CONSULTING AGENTS:")
cursor.execute("""
    SELECT 
        agent_name,
        COUNT(*) as times_consulted,
        MAX(timestamp) as last_consulted
    FROM conductor_conversations
    GROUP BY agent_name
    ORDER BY times_consulted DESC
    LIMIT 10
""")
consultations = cursor.fetchall()
if consultations:
    print("   Most consulted agents:")
    for agent in consultations:
        print(f"      {agent[0]}: {agent[1]} consultations (last: {agent[2]})")
else:
    print("   ❌ No agent consultations found")

conn.close()

print()
print("="*80)
print("ANALYSIS COMPLETE")
print("="*80)
