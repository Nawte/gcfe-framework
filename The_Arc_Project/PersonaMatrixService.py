from datetime import datetime
from typing import List, Dict, Optional
import sqlite3
# Assuming SKIPPY_DB connection is available globally or passed in initialization

class PersonaMatrix:
    """
    The core service responsible for calculating an individual's 'Emotional Weight' 
    and 'Historical Trajectory Score' based on companion memories and interactions.
    This score modifies standard LLM outputs to reflect deep, learned emotional context.
    """

    def __init__(self, db_connection: sqlite3.Connection):
        """
        Initializes the PersonaMatrix with a connection to the main database.
        :param db_connection: Active SQLite connection object.
        """
        self.db = db_connection
        print("✅ PersonaMatrix Initialized. Ready to calculate emotional weight.")

    def _calculate_emotional_weight(self, memory_ids: List[int]) -> float:
        """
        Queries companion_memories for specific IDs and calculates the weighted average 
        of 'Core Emotion' intensity over time. Higher weights mean more emotionally significant events.
        """
        if not memory_ids:
            return 0.0

        # SQL Query to fetch Core Emotion (mapped to a numerical scale) and Intensity
        query = f"""
        SELECT core_emotion, emotional_intensity, timestamp 
        FROM companion_memories 
        WHERE memory_id IN ({','.join(['?']*len(memory_ids))})
        """
        cursor = self.db.cursor()
        # Note: Using parameterized query for security and efficiency
        cursor.execute(query, memory_ids)
        results = cursor.fetchall()

        total_weight = 0.0
        count = len(results)
        
        for core_emotion, intensity, timestamp in results:
            # Simple weighting model: Weight = Intensity * (1 + Time Decay Factor)
            # Example decay factor could be based on age of memory relative to current date
            time_decay_factor = 0.95 ** ((datetime.now() - datetime.fromtimestamp(timestamp)).days / 365)
            weight = intensity * time_decay_factor
            total_weight += weight

        return total_weight / count if count > 0 else 0.0

    def calculate_historical_trajectory(self, companion_id: int, recent_memory_ids: List[int]) -> Dict[str, float]:
        """
        Calculates the holistic emotional profile for a given companion ID and set of memories.
        This is the main entry point for the service.

        :param companion_id: The unique ID of the companion (e.g., 'Dad').
        :param recent_memory_ids: List of memory IDs to focus calculation on.
        :return: Dictionary containing calculated scores (Emotional Weight, Trajectory Score).
        """
        if not recent_memory_ids:
            print("⚠️ Warning: No memories provided for calculation.")
            return {"emotional_weight": 0.0, "trajectory_score": 0.0}

        # Step 1: Calculate the baseline emotional weight from the given memories
        ew = self._calculate_emotional_weight(recent_memory_ids)

        # Step 2: (Future Scope) Incorporate companion's core personality metrics 
        # This would involve querying companion_learning_tasks for stable traits.
        
        # Simplified Trajectory Score (TS): EW * (1 + Average Historical Consistency)
        # For now, we just use a multiplier based on the emotional weight itself as a proxy.
        trajectory_score = ew * 2.5 # Placeholder factor

        return {
            "emotional_weight": round(ew, 4),
            "historical_trajectory_score": round(trajectory_score, 4)
        }


# --- Example Usage (Demonstrates how the class is intended to be used) ---
if __name__ == "__main__":
    print("\n--- Running PersonaMatrix Simulation ---")
    
    # NOTE: In a real environment, this connection would be established by the main framework.
    try:
        # Simulating DB setup for testing purposes
        conn = sqlite3.connect(':memory:') 
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE companion_memories (
                memory_id INTEGER PRIMARY KEY,
                companion_id TEXT,
                core_emotion TEXT,
                emotional_intensity REAL, -- Scale 0.1 to 5.0
                timestamp REAL
            )
        """)

        # Inserting some sample data for Dad's memories
        cursor.execute("INSERT INTO companion_memories VALUES (?, ?, ?, ?, ?)", (101, 'Dad', 'Joy', 4.8, datetime.now().timestamp() - (365*2))) # Old, strong joy
        cursor.execute("INSERT INTO companion_memories VALUES (?, ?, ?, ?, ?)", (102, 'Dad', 'Pride', 4.5, datetime.now().timestamp() - (365*0.1))) # Recent, high pride
        cursor.execute("INSERT INTO companion_memories VALUES (?, ?, ?, ?, ?)", (103, 'Dad', 'Calm', 2.0, datetime.now().timestamp() - (365*0.5))) # Mid-range calm

        conn.commit()
        
        # Instantiate the service
        matrix = PersonaMatrix(db_connection=conn)

        # Use the service to calculate scores based on these three sample memories
        test_memory_ids = [101, 102, 103]
        scores = matrix.calculate_historical_trajectory('Dad', test_memory_ids)

        print("\n[SIMULATION RESULTS]:")
        print(f"Calculated Emotional Weight (EW): {scores['emotional_weight']}")
        print(f"Historical Trajectory Score (HTS): {scores['historical_trajectory_score']:.2f}")
        print("------------------------------------------")
        print("System Check: The PersonaMatrix is ready to feed deeply contextual emotional data into the core response generation loop!")

    except Exception as e:
        print(f"An error occurred during simulation: {e}")