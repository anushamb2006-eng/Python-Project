"""
Seed Data Script
Pre-populates the library with 10 standard books and all 6 group members (Group 2).
Run this script anytime you want to reset or initialize sample data for a demo!
Usage:
    python seed_data.py
"""

from library import Library


def populate_seed_data():
    lib = Library(data_dir="data")

    print("=== SEEDING 10 SAMPLE BOOKS & GROUP 2 MEMBERS ===")

    # 1. Standard Collection of 10 Books
    sample_books = [
        ("B101", "Python Crash Course", "Eric Matthes", "Technology"),
        ("B102", "Clean Code", "Robert C. Martin", "Technology"),
        ("B103", "Introduction To Algorithms", "Thomas H. Cormen", "Science"),
        ("B104", "The Pragmatic Programmer", "Andy Hunt", "Technology"),
        ("B105", "To Kill A Mockingbird", "Harper Lee", "Literature"),
        ("B106", "A Brief History Of Time", "Stephen Hawking", "Science"),
        ("B107", "Sapiens: A Brief History Of Humankind", "Yuval Noah Harari", "History"),
        ("B108", "1984", "George Orwell", "Fiction"),
        ("B109", "Design Patterns", "Erich Gamma", "Technology"),
        ("B110", "The Great Gatsby", "F. Scott Fitzgerald", "Literature")
    ]

    for bid, title, author, cat in sample_books:
        existing = next((b for b in lib.get_all_books() if b.book_id == bid), None)
        if not existing:
            ok, msg = lib.add_book(bid, title, author, cat)
            print(f"Book: {bid} - {msg}")
        else:
            print(f"Book: {bid} already present ({existing.title})")

    # 2. Add Group 2 Members (Roll Nos from evaluation sheet)
    group_members = [
        ("25BTRCF007", "Asin", "asin@college.edu", "student"),
        ("25BTRCF008", "Anne Reeja A", "anne@college.edu", "student"),
        ("25BTRCF009", "Anshul Kumar", "anshul@college.edu", "student"),
        ("25BTRCF010", "Anusha M B", "anusha@college.edu", "student"),
        ("25BTRCF011", "Archit Raj", "archit@college.edu", "student"),
        ("25BTRCF012", "Aryan Raj", "aryan@college.edu", "student"),
        ("FAC001", "Dr. Ramesh Sharma", "ramesh@college.edu", "faculty"),
        ("FAC002", "Prof. Sunita Rao", "sunita@college.edu", "faculty"),
    ]

    for mid, name, email, mtype in group_members:
        if mid not in lib.members:
            ok, msg = lib.register_member(mid, name, email, mtype)
            print(f"Member: {mid} - {msg}")
        else:
            print(f"Member: {mid} already registered ({lib.members[mid].name})")

    lib.save_data()
    print("\n[SUCCESS] Sample data initialized successfully!")
    print(f"Total Books: {len(lib.get_all_books())}")
    print(f"Total Members: {len(lib.get_all_members())}")


if __name__ == "__main__":
    populate_seed_data()
