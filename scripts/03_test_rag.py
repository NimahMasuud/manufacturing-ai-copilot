import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import rag_query

if __name__ == "__main__":
    test_questions = [
        "Which machine has the most downtime?",
        "What are the main causes of quality defects?",
        "Are there any temperature anomalies?"
    ]
    for q in test_questions:
        print(f"\nQ: {q}")
        print(f"A: {rag_query(q)}")
        print("-" * 60)