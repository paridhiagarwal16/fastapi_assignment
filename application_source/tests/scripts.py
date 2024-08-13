import subprocess
import time
test_cases = [
    "test_create_user",
    "test_post_books_endpoint",
    "test_get_books_endpoint",
    "test_get_book_for_id_endpoint",
    "test_update_book_for_id_endpoint",
    "test_delete_book_for_id_endpoint",
    "test_post_review_endpoint",
    "test_get_review_endpoint",
]
check=0
for test_case in test_cases:
    print(test_case)
    result = subprocess.run(["pytest", "-v", f"test_new.py::{test_case}"], capture_output=True, text=True)
    print(f"Running {test_case}:")
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        print(f"Test {test_case} failed.")
        check=1
        break
if check==1:
    print("All tests passed!")
