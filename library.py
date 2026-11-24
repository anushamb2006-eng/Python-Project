"""
Library Operations Module
Handles core business logic: adding books, registering members,
searching, borrowing, returning, and JSON file persistence.

Demonstrates Course Outcomes:
- CO3:
  - Lists: list of Book objects, list of transactions
  - Dictionaries: mapping member_id -> Member object, JSON serialization dictionaries
  - Sets: set of currently issued book IDs for fast lookup and uniqueness
  - Tuples: fixed return statuses and categories
  - String Operations: .strip(), .lower(), .upper(), .title(), and substring search ('in')
- CO4:
  - File handling (reading/writing JSON files with 'with open(...)')
  - Exception handling (try/except for FileNotFoundError, json.JSONDecodeError, ValueError)
- CO5:
  - Polymorphic calls to member.get_borrow_limit() during borrow operations
"""

import json
import csv
import os
from datetime import datetime
from book import Book, ALLOWED_CATEGORIES
from member import Member, StudentMember, FacultyMember


class Library:
    """
    Manages collection of books, members, and borrowing transactions.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, "books.json")
        self.members_file = os.path.join(data_dir, "members.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")

        # CO3: Multiple appropriate data structures
        # 1. List: stores Book objects
        self.books: list[Book] = []

        # 2. Dictionary: maps member_id (str) -> Member object for fast lookup
        self.members: dict[str, Member] = {}

        # 3. Set: maintains unique IDs of currently issued books
        self.issued_book_ids: set[str] = set()

        # 4. List: stores borrowing/returning transaction records (dicts)
        self.transactions: list[dict] = []

        # Ensure storage directory exists and load existing records
        self._ensure_data_directory()
        self.load_data()

    def _ensure_data_directory(self):
        """Creates the data/ directory if it doesn't already exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)

    # =========================================================================
    # CO4: FILE HANDLING & EXCEPTION HANDLING (JSON Persistence)
    # =========================================================================

    def load_data(self):
        """
        Loads library data from JSON files.
        Demonstrates robust exception handling for missing or corrupted files.
        """
        # Load Books
        try:
            with open(self.books_file, "r", encoding="utf-8") as f:
                raw_books = json.load(f)
                self.books = [Book.from_dict(b) for b in raw_books]
        except FileNotFoundError:
            # File doesn't exist yet on first run; initialize with empty list safely
            self.books = []
        except json.JSONDecodeError:
            print(f"[Warning] '{self.books_file}' is corrupted. Starting with empty book list.")
            self.books = []

        # Load Members
        try:
            with open(self.members_file, "r", encoding="utf-8") as f:
                raw_members = json.load(f)
                self.members = {}
                for m_data in raw_members:
                    member_obj = Member.from_dict(m_data)
                    self.members[member_obj.member_id] = member_obj
        except FileNotFoundError:
            self.members = {}
        except json.JSONDecodeError:
            print(f"[Warning] '{self.members_file}' is corrupted. Starting with empty member directory.")
            self.members = {}

        # Load Transactions
        try:
            with open(self.transactions_file, "r", encoding="utf-8") as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []
        except json.JSONDecodeError:
            print(f"[Warning] '{self.transactions_file}' is corrupted. Starting with empty transactions.")
            self.transactions = []

        # CO3: Set comprehension to reconstruct set of currently issued book IDs
        self.issued_book_ids = {
            tx["book_id"] for tx in self.transactions if tx.get("status") == "ISSUED"
        }

        # Synchronize availability state of books
        for book in self.books:
            book.is_available = (book.book_id not in self.issued_book_ids)

    def save_data(self):
        """
        Saves current books, members, and transactions into JSON files.
        Demonstrates safe writing using with open() and json.dump().
        """
        self._ensure_data_directory()

        # Save books
        with open(self.books_file, "w", encoding="utf-8") as f:
            books_data = [book.to_dict() for book in self.books]
            json.dump(books_data, f, indent=4)

        # Save members
        with open(self.members_file, "w", encoding="utf-8") as f:
            members_data = [member.to_dict() for member in self.members.values()]
            json.dump(members_data, f, indent=4)

        # Save transactions
        with open(self.transactions_file, "w", encoding="utf-8") as f:
            json.dump(self.transactions, f, indent=4)

        # CO4: CSV File Handling - Also generate CSV export for books
        try:
            books_csv_file = os.path.join(self.data_dir, "books.csv")
            with open(books_csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Book ID", "Title", "Author", "Category", "Status"])
                for b in self.books:
                    status = "Available" if b.is_available else "Issued"
                    writer.writerow([b.book_id, b.title, b.author, b.category, status])
        except Exception as e:
            print(f"[Warning] Failed to write CSV file: {e}")

    # =========================================================================
    # BOOK OPERATIONS
    # =========================================================================

    def add_book(self, book_id: str, title: str, author: str, category: str) -> tuple[bool, str]:
        """
        Adds a new book after validation.
        CO3: Uses tuple for return status (success: bool, message: str).
        """
        # CO3: String operations: .strip() and .upper()
        clean_id = book_id.strip().upper()
        clean_title = title.strip()
        clean_author = author.strip()
        clean_cat = category.strip()

        # Input validation
        if not clean_id or not clean_title or not clean_author or not clean_cat:
            return False, "Error: All book fields (ID, Title, Author, Category) are required."

        # Check for duplicate book ID
        for book in self.books:
            if book.book_id == clean_id:
                return False, f"Error: Book with ID '{clean_id}' already exists."

        # Create new Book instance and save
        new_book = Book(clean_id, clean_title, clean_author, clean_cat, is_available=True)
        self.books.append(new_book)
        self.save_data()
        return True, f"Success: Book '{new_book.title}' (ID: {clean_id}) added successfully."

    def get_all_books(self) -> list[Book]:
        """Returns list of all registered books."""
        return self.books

    def search_books(self, keyword: str, search_field: str = "all") -> list[Book]:
        """
        CO3: String operations for flexible searching:
        - .strip() removes whitespace
        - .lower() ensures case-insensitivity
        - 'in' keyword checks for substring matching
        """
        query = keyword.strip().lower()
        if not query:
            return []

        results = []
        for book in self.books:
            title_match = query in book.title.lower()
            author_match = query in book.author.lower()
            cat_match = query in book.category.lower()

            if search_field == "title" and title_match:
                results.append(book)
            elif search_field == "author" and author_match:
                results.append(book)
            elif search_field == "category" and cat_match:
                results.append(book)
            elif search_field == "all" and (title_match or author_match or cat_match):
                results.append(book)

        return results

    # =========================================================================
    # MEMBER OPERATIONS (CO5: OOP, Inheritance, Polymorphism)
    # =========================================================================

    def register_member(self, member_id: str, name: str, email: str, member_type: str) -> tuple[bool, str]:
        """
        Registers a new library member as Student or Faculty.
        Demonstrates polymorphic class instantiation.
        """
        clean_id = member_id.strip().upper()
        clean_name = name.strip()
        clean_email = email.strip().lower()
        clean_type = member_type.strip().lower()

        if not clean_id or not clean_name or not clean_email:
            return False, "Error: Member ID, Name, and Email cannot be empty."

        if clean_id in self.members:
            return False, f"Error: Member with ID '{clean_id}' is already registered."

        # CO5: Instantiate appropriate subclass based on type
        if clean_type == "student":
            member = StudentMember(clean_id, clean_name, clean_email)
        elif clean_type == "faculty":
            member = FacultyMember(clean_id, clean_name, clean_email)
        else:
            return False, "Error: Invalid member type. Please specify 'Student' or 'Faculty'."

        self.members[clean_id] = member
        self.save_data()
        return True, (f"Success: {member.get_member_type()} Member '{member.name}' "
                      f"(ID: {clean_id}) registered with borrow limit of {member.get_borrow_limit()}.")

    def get_all_members(self) -> list[Member]:
        """Returns list of all registered members."""
        return list(self.members.values())

    def get_member(self, member_id: str) -> Member | None:
        """Looks up a member by ID."""
        return self.members.get(member_id.strip().upper())

    def get_active_borrow_count(self, member_id: str) -> int:
        """Counts how many active books a member currently has borrowed."""
        clean_id = member_id.strip().upper()
        count = 0
        for tx in self.transactions:
            if tx.get("member_id") == clean_id and tx.get("status") == "ISSUED":
                count += 1
        return count

    # =========================================================================
    # BORROW & RETURN OPERATIONS (CO5: Polymorphism in Action)
    # =========================================================================

    def borrow_book(self, member_id: str, book_id: str) -> tuple[bool, str]:
        """
        Issues a book to a member.
        Demonstrates CO5: Polymorphic borrow limit check (member.get_borrow_limit()).
        """
        clean_mid = member_id.strip().upper()
        clean_bid = book_id.strip().upper()

        if not clean_mid or not clean_bid:
            return False, "Error: Both Member ID and Book ID are required."

        # 1. Validate member existence
        member = self.get_member(clean_mid)
        if not member:
            return False, f"Error: Member ID '{clean_mid}' not found."

        # 2. Validate book existence
        book = next((b for b in self.books if b.book_id == clean_bid), None)
        if not book:
            return False, f"Error: Book ID '{clean_bid}' not found."

        # 3. Check book availability
        if not book.is_available or clean_bid in self.issued_book_ids:
            return False, f"Error: Book '{book.title}' (ID: {clean_bid}) is already issued."

        # 4. Check member's borrowing limit using CO5 Polymorphism!
        current_borrowed = self.get_active_borrow_count(clean_mid)
        limit = member.get_borrow_limit()  # Calls overridden method polymorphically
        if current_borrowed >= limit:
            return False, (f"Error: Borrowing limit reached! {member.get_member_type()} members "
                          f"can borrow at most {limit} books. (Currently holding: {current_borrowed})")

        # 5. Process borrowing
        book.mark_as_borrowed()
        self.issued_book_ids.add(clean_bid)

        transaction = {
            "transaction_id": f"TXN-{len(self.transactions) + 1:04d}",
            "member_id": clean_mid,
            "member_name": member.name,
            "book_id": clean_bid,
            "book_title": book.title,
            "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "return_date": None,
            "status": "ISSUED"
        }
        self.transactions.append(transaction)
        self.save_data()

        return True, (f"Success: Book '{book.title}' issued to {member.name} ({member.get_member_type()}). "
                      f"Active borrows: {current_borrowed + 1}/{limit}.")

    def return_book(self, member_id: str, book_id: str) -> tuple[bool, str]:
        """
        Returns a borrowed book.
        Ensures only the member who borrowed the book can return it.
        """
        clean_mid = member_id.strip().upper()
        clean_bid = book_id.strip().upper()

        if not clean_mid or not clean_bid:
            return False, "Error: Both Member ID and Book ID are required."

        # 1. Check member exists
        if clean_mid not in self.members:
            return False, f"Error: Member ID '{clean_mid}' not found."

        # 2. Check book exists
        book = next((b for b in self.books if b.book_id == clean_bid), None)
        if not book:
            return False, f"Error: Book ID '{clean_bid}' not found."

        # 3. Locate active transaction for this book
        active_tx = None
        for tx in self.transactions:
            if tx.get("book_id") == clean_bid and tx.get("status") == "ISSUED":
                active_tx = tx
                break

        if not active_tx:
            return False, f"Error: Book '{book.title}' (ID: {clean_bid}) is not currently marked as issued."

        # 4. Verify returning member is the borrower
        if active_tx["member_id"] != clean_mid:
            borrower = self.members.get(active_tx['member_id'])
            borrower_name = borrower.name if borrower else active_tx['member_id']
            return False, (f"Error: Cannot return. Book was borrowed by {borrower_name} "
                          f"({active_tx['member_id']}), not member {clean_mid}.")

        # 5. Process return
        book.mark_as_returned()
        if clean_bid in self.issued_book_ids:
            self.issued_book_ids.remove(clean_bid)

        active_tx["status"] = "RETURNED"
        active_tx["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data()

        return True, f"Success: Book '{book.title}' returned successfully by {self.members[clean_mid].name}."

    def get_issued_books(self) -> list[dict]:
        """
        Returns list of all books currently issued.
        """
        return [tx for tx in self.transactions if tx.get("status") == "ISSUED"]
