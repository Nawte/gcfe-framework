import sqlite3

db_path = r"C:\Users\shake\source\repos\Massive Ai Agent Farm\Massive Ai Agent Farm\stocks.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("CHECKING SKIPPY'S EXISTING SYSTEMS")
print("="*80)
print()

# Check Conductor tables
print("1. CONDUCTOR TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%conductor%'")
conductor_tables = cursor.fetchall()
if conductor_tables:
    for table in conductor_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   ✅ {table[0]} ({count} rows)")
else:
    print("   ❌ No Conductor tables found")
print()

# Check Memory Palace tables
print("2. MEMORY PALACE TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%memory%' OR name LIKE '%journal%' OR name LIKE '%thought%')")
memory_tables = cursor.fetchall()
if memory_tables:
    for table in memory_tables:
        # Skip auto-index entries
        if table[0].startswith('sqlite_autoindex'):
            continue
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   ✅ {table[0]} ({count} rows)")
        except sqlite3.OperationalError:
            print(f"   ⚠️  {table[0]} (skipped - system table)")
else:
    print("   ❌ No Memory Palace tables found")
print()

# Check Self-Healing tables
print("3. SELF-HEALING TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%healing%' OR name LIKE '%upgrade%' OR name LIKE '%innovation%')")
healing_tables = cursor.fetchall()
if healing_tables:
    for table in healing_tables:
        # Skip auto-index entries
        if table[0].startswith('sqlite_autoindex'):
            continue
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   ✅ {table[0]} ({count} rows)")
        except sqlite3.OperationalError:
            print(f"   ⚠️  {table[0]} (skipped - system table)")
else:
    print("   ❌ No Self-Healing tables found")
print()

# Check Companion tables
print("4. COMPANION TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%companion%'")
companion_tables = cursor.fetchall()
if companion_tables:
    for table in companion_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   ✅ {table[0]} ({count} rows)")
else:
    print("   ❌ No Companion tables found")
print()

# Check Research Team
print("5. RESEARCH TEAM:")
cursor.execute("SELECT name FROM companion_personalities WHERE occupation LIKE '%research%' OR occupation LIKE '%scientist%'")
researchers = cursor.fetchall()
if researchers:
    for researcher in researchers:
        print(f"   ✅ {researcher[0]}")
else:
    print("   ❌ No researchers found")
print()

conn.close()

print("="*80)
print("CHECK COMPLETE")
print("="*80)
