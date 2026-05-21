import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.indexer import index_all

if __name__ == "__main__":
    index_all()