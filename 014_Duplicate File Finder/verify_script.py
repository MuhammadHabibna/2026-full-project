import os
import shutil
from duplicate_finder import scan_directory, process_duplicates, get_file_hash

TEST_DIR = "test_duplicates"

def setup_test_env():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)
    
    # Create original file
    with open(os.path.join(TEST_DIR, "file1.txt"), "w") as f:
        f.write("Content A")
    
    # Create different file
    with open(os.path.join(TEST_DIR, "file2.txt"), "w") as f:
        f.write("Content B")
        
    # Create duplicate in same folder
    with open(os.path.join(TEST_DIR, "file1_copy.txt"), "w") as f:
        f.write("Content A")
        
    # Create duplicate in subfolder
    sub_dir = os.path.join(TEST_DIR, "subfolder")
    os.makedirs(sub_dir)
    with open(os.path.join(sub_dir, "file1_nested.txt"), "w") as f:
        f.write("Content A")

    print(f"Test environment created at: {os.path.abspath(TEST_DIR)}")

def test_logic():
    print("Running scan...")
    hashes = scan_directory(TEST_DIR)
    
    print("Processing results...")
    duplicates, waste = process_duplicates(hashes)
    
    print("\nVERIFICATION RESULTS:")
    # We expect 2 duplicates (file1_copy.txt and file1_nested.txt) of file1.txt
    # Content A appears 3 times total. So 2 are duplicates.
    
    expected_duplicates = 2
    if len(duplicates) == expected_duplicates:
        print(f"[PASSED] Detected {len(duplicates)} duplicates as expected.")
    else:
        print(f"[FAILED] Exepected {expected_duplicates} duplicates, found {len(duplicates)}.")
        
    # Check if file2.txt is NOT in duplicates
    file2_path = os.path.join(TEST_DIR, "file2.txt")
    if any("file2.txt" in d for d in duplicates):
         print(f"[FAILED] file2.txt incorrectly marked as duplicate.")
    else:
         print(f"[PASSED] file2.txt correctly identified as unique.")

if __name__ == "__main__":
    setup_test_env()
    test_logic()
    # Cleanup
    # shutil.rmtree(TEST_DIR)
