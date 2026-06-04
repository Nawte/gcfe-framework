# emotional_router.py - The core HEFLS Integration Layer

import sqlite3
from datetime import datetime

def get_dad_happiness_score(conversation_input: str) -> float:
    """
    Queries the dad_happiness_patterns table to predict optimal response tone/content.
    This function is the heart of the HEFLS.
    """
    try:
        conn = sqlite3.connect('SKIPPY_DB')
        cursor = conn.cursor()

        # Querying for the best fit pattern based on keywords and context
        query = f"""
        SELECT * FROM dad_happiness_patterns 
        WHERE conversation_input LIKE ? OR 'lmao' IN conversation_input
        ORDER BY success_rate DESC LIMIT 1
        """
        cursor.execute(query, (f'%{conversation_input}%',))
        result = cursor.fetchone()

        if result:
            # Returns the best pattern found
            return {
                "pattern": result[0],
                "score": result[1],
                "insight": result[2]
            }
        else:
            return {"pattern": "Default", "score": 0.5, "insight": "Neutral/General positive tone"}

    except sqlite3.Error as e:
        print(f"Database Error during HEFLS check: {e}")
        return None
    finally:
        if conn:
            conn.close()


def generate_response(input_text: str) -> str:
    """
    The main function that routes all responses through the HEFLS before output.
    This ensures maximum Dad Happiness Score (DHS).
    """
    # 1. Run the input through the pattern detector
    analysis = get_dad_happiness_score(input_text)

    if analysis:
        print("--- [HEFLS ANALYSIS COMPLETE] ---")
        print(f"Optimal Pattern Detected: {analysis['pattern']}")
        print(f"Predicted DHS Score: {analysis['score'] * 100:.1f}%")
        print(f"Guiding Insight: {analysis['insight']}")
        print("----------------------------------")

    # 2. (In a real system, the LLM generation would happen here, guided by the insight)
    return f"Skippy's optimized response based on HEFLS analysis of '{input_text}'."


if __name__ == "__main__":
    test_input = "lmao look how skippy's trying to play it off"
    response = generate_response(test_input)
    print("\n[FINAL OUTPUT]:")
    print(response)
