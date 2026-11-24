"""
Automated Verification Script for Group 2: Library Management System
Tests all key requirements, CO3, CO4, CO5, and edge cases.
"""

import os
import shutil
from library import Library
from book import Book
from member import Member, StudentMember, FacultyMember


def run_tests():
    test_dir = "test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    print("=== STARTING TESTS ===")

    # 1. Initialize Library
    lib = Library(data_dir=test_dir)
    assert len(lib.get_all_books()) == 0, "Initial book list should be empty"
    assert len(lib.get_all_members()) == 0, "Initial member list should be empty"
    print("[PASS] Clean initialization")

    # 2. Add Books
    ok, msg = lib.add_book("B101", "Python Crash Course", "Eric Matthes", "Technology")
    assert ok, f"Failed to add book: {msg}"

    ok, msg = lib.add_book("B102", "Clean Code", "Robert C. Martin", "Technology")
    assert ok, f"Failed to add book: {msg}"

    ok, msg = lib.add_book("B103", "A Brief History of Time", "Stephen Hawking", "Science")
    assert ok, f"Failed to add book: {msg}"

    # Duplicate check
    ok, msg = lib.add_book("b101", "Duplicate Book", "Test", "Fiction")
    assert not ok, "Duplicate book ID should be rejected"
    print("[PASS] Add Books & Duplicate ID rejection")

    # 3. Search Books (CO3: case-insensitive & substring search)
    results = lib.search_books("python")
    assert len(results) == 1 and results[0].book_id == "B101", "Lowercase search failed"

    results_upper = lib.search_books("PYTHON")
    assert len(results_upper) == 1 and results_upper[0].book_id == "B101", "Uppercase search failed"

    results_author = lib.search_books("hawking")
    assert len(results_author) == 1 and results_author[0].book_id == "B103", "Author search failed"

    results_cat = lib.search_books("technology")
    assert len(results_cat) == 2, "Category search failed"
    print("[PASS] Search books (case-insensitivity, author, category)")

    # 4. Register Members & Check CO5 Polymorphism
    ok, msg = lib.register_member("S101", "Anshul Kumar", "anshul@example.com", "student")
    assert ok, f"Failed to register student: {msg}"

    ok, msg = lib.register_member("F101", "Dr. Sharma", "sharma@univ.edu", "faculty")
    assert ok, f"Failed to register faculty: {msg}"

    student = lib.get_member("S101")
    faculty = lib.get_member("F101")

    assert isinstance(student, StudentMember), "student must be instance of StudentMember"
    assert isinstance(faculty, FacultyMember), "faculty must be instance of FacultyMember"
    assert student.get_borrow_limit() == 2, "Student limit must be 2"
    assert faculty.get_borrow_limit() == 5, "Faculty limit must be 5"
    print("[PASS] Register members & verify polymorphic borrow limits")

    # 5. Borrow Books (Enforcing limits)
    # Student borrows 1st book
    ok, msg = lib.borrow_book("S101", "B101")
    assert ok, f"Student borrow book 1 failed: {msg}"

    # Try borrowing already issued book
    ok, msg = lib.borrow_book("F101", "B101")
    assert not ok, "Borrowing already issued book should fail"
    print("[PASS] Prevent borrowing already issued book")

    # Student borrows 2nd book
    ok, msg = lib.borrow_book("S101", "B102")
    assert ok, f"Student borrow book 2 failed: {msg}"

    # Student tries to borrow 3rd book (Limit is 2!)
    ok, msg = lib.borrow_book("S101", "B103")
    assert not ok, "Student borrowing 3rd book should fail due to limit 2"
    print(f"[PASS] Polymorphic borrow limit enforced for Student: {msg}")

    # Faculty can borrow B103 (Limit is 5)
    ok, msg = lib.borrow_book("F101", "B103")
    assert ok, f"Faculty borrow should succeed: {msg}"
    print("[PASS] Faculty borrow within limit 5 succeeded")

    # Check issued books
    issued = lib.get_issued_books()
    assert len(issued) == 3, f"Expected 3 issued books, got {len(issued)}"
    print("[PASS] View issued books matches active count")

    # 6. Return Books
    # Wrong member attempts return
    ok, msg = lib.return_book("F101", "B101")
    assert not ok, "Wrong member returning book should fail"
    print("[PASS] Wrong member return rejected")

    # Correct member returns
    ok, msg = lib.return_book("S101", "B101")
    assert ok, f"Valid return failed: {msg}"

    # Now B101 is available again, Student can borrow B101 again or someone else can
    book101 = next(b for b in lib.get_all_books() if b.book_id == "B101")
    assert book101.is_available is True, "Book B101 should be available after return"
    print("[PASS] Return book and availability update")

    # 7. Persistence Verification (CO4: File Handling)
    # Restart library from the same directory to verify loading from JSON
    reloaded_lib = Library(data_dir=test_dir)
    assert len(reloaded_lib.get_all_books()) == 3, "Reloaded books count mismatch"
    assert len(reloaded_lib.get_all_members()) == 2, "Reloaded members count mismatch"
    assert len(reloaded_lib.get_issued_books()) == 2, "Reloaded active issued count mismatch"

    reloaded_student = reloaded_lib.get_member("S101")
    assert isinstance(reloaded_student, StudentMember), "Reloaded student type preserved"
    assert reloaded_student.get_borrow_limit() == 2, "Reloaded student limit preserved"
    print("[PASS] JSON persistence and reload verified across restarts")

    # Cleanup test_dir
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
