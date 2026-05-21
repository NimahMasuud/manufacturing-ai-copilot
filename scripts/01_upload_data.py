import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.blob_upload import upload_csvs

if __name__ == "__main__":
    upload_csvs()