"""
Main Module
Entry point for the Library Management System console application.
Provides an interactive menu for users and demonstrators.

Demonstrates Course Outcomes:
- CO3: Formatted string output, list iteration, dictionary handling, string stripping/lowercasing.
- CO4: Exception handling for menu choices and user input errors.
- CO5: Clean separation of concerns invoking polymorphic Library operations.
"""

from library import Library
from book import ALLOWED_CATEGORIES


def print_header(title: str):
    """Utility to print section headers."""
    print("\n" + "=" * 50)
    print(f" {title.center(48)} ")
    print("=" * 50)


def display_menu():
    """Displays the main terminal menu as specified in the Implementation Plan."""
    print("\n" + "=" * 47)
    print("========== LIBRARY MANAGEMENT SYSTEM ==========")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Register Member")
    print("5. View Members")
    print("6. Borrow Book")
    print("7. Return Book")
    print("8. View Issued Books")
    print("9. Exit")
    print("=" * 47)


def handle_add_book(lib: Library):
    """Menu 1: Add a new book."""
    print_header("ADD NEW BOOK")
    book_id = input("Enter Book ID (e.g. B101): ").strip()
    title = input("Enter Book Title: ").strip()
    author = input("Enter Author Name: ").strip()

    print(f"Categories: {', '.join(ALLOWED_CATEGORIES)}")
    category = input("Enter Category: ").strip()

    success, message = lib.add_book(book_id, title, author, category)
    if success:
        print(f"[SUCCESS] {message}")
    else:
        print(f"[ERROR] {message}")


def handle_view_books(lib: Library):
    """Menu 2: Display all books in tabular format."""
    print_header("ALL BOOKS")
    books = lib.get_all_books()
    if not books:
        print("No books found in the library.")
        return

    # Table Header with formatted column widths
    print(f"{'Book ID':<10} | {'Title':<28} | {'Author':<20} | {'Category':<15} | {'Status':<10}")
    print("-" * 90)
    for b in books:
        status = "Available" if b.is_available else "Issued"
        # CO3: String formatting using f-strings
        print(f"{b.book_id:<10} | {b.title[:26]:<28} | {b.author[:18]:<20} | {b.category[:13]:<15} | {status:<10}")


def handle_search_book(lib: Library):
    """Menu 3: Search books by title, author, or category."""
    print_header("SEARCH BOOKS")
    print("Search by: 1. All Fields  2. Title  3. Author  4. Category")
    field_choice = input("Enter choice (1-4, default 1): ").strip()

    field_map = {"1": "all", "2": "title", "3": "author", "4": "category"}
    field = field_map.get(field_choice, "all")

    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print("[ERROR] Search keyword cannot be empty.")
        return

    results = lib.search_books(keyword, search_field=field)
    if not results:
        print(f"No books found matching '{keyword}'.")
        return

    print(f"\nFound {len(results)} matching book(s):")
    print(f"{'Book ID':<10} | {'Title':<28} | {'Author':<20} | {'Category':<15} | {'Status':<10}")
    print("-" * 90)
    for b in results:
        status = "Available" if b.is_available else "Issued"
        print(f"{b.book_id:<10} | {b.title[:26]:<28} | {b.author[:18]:<20} | {b.category[:13]:<15} | {status:<10}")


def handle_register_member(lib: Library):
    """Menu 4: Register a Student or Faculty member."""
    print_header("REGISTER NEW MEMBER")
    member_id = input("Enter Member ID (e.g. S101 or F101): ").strip()
    name = input("Enter Full Name: ").strip()
    email = input("Enter Email Address: ").strip()

    print("Member Types:")
    print("  1. Student Member (Borrow limit: 2 books)")
    print("  2. Faculty Member (Borrow limit: 5 books)")
    type_choice = input("Select Member Type (1 or 2): ").strip()

    if type_choice in ("1", "student"):
        member_type = "student"
    elif type_choice in ("2", "faculty"):
        member_type = "faculty"
    else:
        print("[ERROR] Invalid member type choice. Member not registered.")
        return

    success, message = lib.register_member(member_id, name, email, member_type)
    if success:
        print(f"[SUCCESS] {message}")
    else:
        print(f"[ERROR] {message}")


def handle_view_members(lib: Library):
    """Menu 5: View all registered members and their limits."""
    print_header("REGISTERED MEMBERS")
    members = lib.get_all_members()
    if not members:
        print("No registered members found.")
        return

    print(f"{'Member ID':<12} | {'Name':<22} | {'Email':<25} | {'Type':<10} | {'Limit':<6} | {'Borrowed':<8}")
    print("-" * 92)
    for m in members:
        borrowed = lib.get_active_borrow_count(m.member_id)
        # Demonstrates CO5 Polymorphism: m.get_member_type() and m.get_borrow_limit()
        print(f"{m.member_id:<12} | {m.name[:20]:<22} | {m.email[:23]:<25} | "
              f"{m.get_member_type():<10} | {m.get_borrow_limit():<6} | {borrowed:<8}")


def handle_borrow_book(lib: Library):
    """Menu 6: Issue a book to a member."""
    print_header("BORROW BOOK")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()

    success, message = lib.borrow_book(member_id, book_id)
    if success:
        print(f"[SUCCESS] {message}")
    else:
        print(f"[ERROR] {message}")


def handle_return_book(lib: Library):
    """Menu 7: Return a borrowed book."""
    print_header("RETURN BOOK")
    member_id = input("Enter Member ID: ").strip()
    book_id = input("Enter Book ID: ").strip()

    success, message = lib.return_book(member_id, book_id)
    if success:
        print(f"[SUCCESS] {message}")
    else:
        print(f"[ERROR] {message}")


def handle_view_issued_books(lib: Library):
    """Menu 8: View currently issued books."""
    print_header("CURRENTLY ISSUED BOOKS")
    issued = lib.get_issued_books()
    if not issued:
        print("No books are currently issued.")
        return

    print(f"{'Txn ID':<10} | {'Book ID':<10} | {'Book Title':<26} | {'Member ID':<12} | {'Borrower':<18} | {'Date':<20}")
    print("-" * 105)
    for tx in issued:
        print(f"{tx['transaction_id']:<10} | {tx['book_id']:<10} | {tx['book_title'][:24]:<26} | "
              f"{tx['member_id']:<12} | {tx['member_name'][:16]:<18} | {tx['borrow_date']:<20}")


def main():
    """Main application loop."""
    print("Initializing Library Management System...")
    lib = Library(data_dir="data")
    print(f"System ready. Loaded {len(lib.get_all_books())} books, {len(lib.get_all_members())} members.")

    while True:
        display_menu()
        try:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                handle_add_book(lib)
            elif choice == "2":
                handle_view_books(lib)
            elif choice == "3":
                handle_search_book(lib)
            elif choice == "4":
                handle_register_member(lib)
            elif choice == "5":
                handle_view_members(lib)
            elif choice == "6":
                handle_borrow_book(lib)
            elif choice == "7":
                handle_return_book(lib)
            elif choice == "8":
                handle_view_issued_books(lib)
            elif choice == "9":
                print("\nThank you for using the Library Management System. Goodbye!")
                break
            else:
                print("\n[ERROR] Invalid choice. Please enter a number between 1 and 9.")
        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user. Exiting...")
            break
        except Exception as e:
            # CO4: General exception handling
            print(f"\n[UNEXPECTED ERROR] An error occurred: {e}")


if __name__ == "__main__":
    main()
