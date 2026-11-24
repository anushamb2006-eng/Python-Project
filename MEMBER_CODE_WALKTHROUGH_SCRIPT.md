# Group 2 — Code Walkthrough & Evaluation Defense Script
### Integrated Problem Statement: Library Management System
**Course Outcomes Covered:** CO3 (Data Structures & Strings) | CO4 (File & Exception Handling) | CO5 (OOP, Inheritance & Polymorphism)

---

## 📌 Overview: Division of Responsibilities for the 6 Members

Based on the team work division plan, each member has an assigned functional module. During the walkthrough, each member must present:
1. **Their assigned block of code** (file and function).
2. **The Python programming concepts used** (CO3, CO4, CO5).
3. **How that code block contributes to the working of the Library System**.
4. **Live execution demo** (what to type and show the teacher).
5. **On-the-spot live modification defense**.

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Member 1 (Asin):         Book Management (book.py & add_book)                   │
│ Member 2 (Anne Reeja A): Search and Display Books (search_books & tables)       │
│ Member 3 (Anshul Kumar): Member Registration (Member Hierarchy & Dict)          │
│ Member 4 (Anusha M B):   Issue & Return Books (borrow_book & return_book)       │
│ Member 5 (Aryan Raj):    File Handling & Persistence (JSON & CSV Storage)       │
│ Member 6 (Archit Raj):   OOP, Inheritance & Polymorphism Integration            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

# 👤 MEMBER 1: Book Management
- **Student Name:** Asin
- **Assigned Feature:** Book Data Model & Adding Books
- **Files Involved:** `book.py` and `library.py` (`add_book`)

### 1. Code Block to Explain

```python
# book.py
ALLOWED_CATEGORIES = ("Fiction", "Non-Fiction", "Science", "Technology", "History", "Literature", "General")

class Book:
    def __init__(self, book_id: str, title: str, author: str, category: str, is_available: bool = True):
        self.book_id = book_id.strip().upper()
        self.title = title.strip().title()
        self.author = author.strip().title()
        self.category = category.strip().title()
        self.is_available = is_available

    def mark_as_borrowed(self):
        self.is_available = False

    def mark_as_returned(self):
        self.is_available = True
```

```python
# library.py
def add_book(self, book_id: str, title: str, author: str, category: str) -> tuple[bool, str]:
    clean_id = book_id.strip().upper()
    clean_title = title.strip()
    clean_author = author.strip()
    clean_cat = category.strip()

    if not clean_id or not clean_title or not clean_author or not clean_cat:
        return False, "Error: All book fields (ID, Title, Author, Category) are required."

    for book in self.books:
        if book.book_id == clean_id:
            return False, f"Error: Book with ID '{clean_id}' already exists."

    new_book = Book(clean_id, clean_title, clean_author, clean_cat, is_available=True)
    self.books.append(new_book)
    self.save_data()
    return True, f"Success: Book '{new_book.title}' (ID: {clean_id}) added successfully."
```

### 2. Python Concepts Used
* **CO5 (Classes & Objects):** Defined the `Book` blueprint with constructor `__init__`, instance attributes (`self.book_id`, `self.title`, `self.is_available`), and state-mutating methods (`mark_as_borrowed`, `mark_as_returned`).
* **CO3 (Tuples):** `ALLOWED_CATEGORIES` is a **tuple** (immutable collection) to ensure category constants cannot be accidentally modified during runtime.
* **CO3 (String Operations):**
  * `.strip()`: Removes accidental leading/trailing spaces entered by the user.
  * `.upper()`: Standardizes Book ID format (e.g., `b101` becomes `B101`).
  * `.title()`: Capitalizes first letters of titles and author names properly.
* **CO3 (Lists):** `self.books.append(new_book)` stores books dynamically in a list.
* **CO3 (Tuples for Return Values):** Returns `tuple[bool, str]` containing status and message.

### 3. Contribution to the Working of the Project
* Serves as the **foundation entity** of the whole library.
* Enforces **data integrity**: Prevents empty records and blocks duplicate book IDs so the library catalog never gets corrupted.
* Manages book state: Through `is_available`, it tells all other modules (search, borrow, view) whether a book is on the shelf or issued.

### 4. What to Demonstrate Live to the Teacher
1. Run `python main.py` and choose **Option 1 (Add Book)**.
2. Enter: ID: `B112`, Title: `Design Patterns`, Author: `Erich Gamma`, Category: `Technology`.
3. Show `[SUCCESS] Book 'Design Patterns' added successfully.`
4. Try adding `B112` again with different details $\rightarrow$ Show the teacher that the duplicate error message appears.

### 5. Likely Viva / Modification Request
* **Teacher asks:** *"Add a publisher attribute to the Book class."*
* **Modification:**
  In `book.py`:
  ```python
  def __init__(self, book_id, title, author, category, publisher="Unknown", is_available=True):
      ...
      self.publisher = publisher.strip().title()
  ```

---

# 👤 MEMBER 2: Search and Display Books
- **Student Name:** Anne Reeja A
- **Assigned Feature:** Searching & Tabular Formatting
- **Files Involved:** `library.py` (`search_books`, `get_all_books`) and `main.py` (`handle_search_book`, `handle_view_books`)

### 1. Code Block to Explain

```python
# library.py
def search_books(self, keyword: str, search_field: str = "all") -> list[Book]:
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
```

```python
# main.py
def handle_view_books(lib: Library):
    books = lib.get_all_books()
    print(f"{'Book ID':<10} | {'Title':<28} | {'Author':<20} | {'Category':<15} | {'Status':<10}")
    print("-" * 90)
    for b in books:
        status = "Available" if b.is_available else "Issued"
        print(f"{b.book_id:<10} | {b.title[:26]:<28} | {b.author[:18]:<20} | {b.category[:13]:<15} | {status:<10}")
```

### 2. Python Concepts Used
* **CO3 (String Operations):**
  * `.lower()`: Case-folding applied to both the user query and the book fields to allow seamless case-insensitive searching.
  * Membership operator `in`: Checks for partial substring matches (e.g. searching `"algo"` matches `"Introduction To Algorithms"`).
* **CO3 (Lists & Traversal):** Iterates over `self.books` with a `for` loop and builds a filtered `results` list.
* **CO3 (Formatted String Output):** Uses Python f-strings with column alignment specifiers:
  * `{b.book_id:<10}`: Left-aligns text with a width of 10 characters.
  * `{b.title[:26]:<28}`: Slices long titles to 26 characters max to prevent table breakage.

### 3. Contribution to the Working of the Project
* Enables library users and librarians to locate books quickly without knowing the exact Book ID or full title.
* Provides a human-readable visual summary of the inventory in aligned tables instead of raw python lists.

### 4. What to Demonstrate Live to the Teacher
1. Run `python main.py` and choose **Option 3 (Search Book)**.
2. Select `1 (All Fields)` and search `python` (lowercase) $\rightarrow$ Displays `Python Crash Course`.
3. Search `PYTHON` (uppercase) $\rightarrow$ Displays the same book.
4. Select `4 (Category)` and search `Science` $\rightarrow$ Displays all science books.

### 5. Likely Viva / Modification Request
* **Teacher asks:** *"How would you search books by availability status only?"*
* **Modification:**
  ```python
  def get_available_books(self) -> list[Book]:
      return [b for b in self.books if b.is_available]
  ```

---

# 👤 MEMBER 3: Member Registration
- **Student Name:** Anshul Kumar
- **Assigned Feature:** Patron Registration & Member Data Structure
- **Files Involved:** `member.py` (`Member` base class) and `library.py` (`register_member`, `get_member`, `get_all_members`)

### 1. Code Block to Explain

```python
# member.py
class Member:
    def __init__(self, member_id: str, name: str, email: str):
        self.member_id = member_id.strip().upper()
        self.name = name.strip().title()
        self.email = email.strip().lower()

    def get_borrow_limit(self) -> int:
        return 1

    def get_member_type(self) -> str:
        return "General"
```

```python
# library.py
def register_member(self, member_id: str, name: str, email: str, member_type: str) -> tuple[bool, str]:
    clean_id = member_id.strip().upper()
    clean_name = name.strip()
    clean_email = email.strip().lower()
    clean_type = member_type.strip().lower()

    if not clean_id or not clean_name or not clean_email:
        return False, "Error: Member ID, Name, and Email cannot be empty."

    # CO3: Fast O(1) membership check using dictionary keys
    if clean_id in self.members:
        return False, f"Error: Member with ID '{clean_id}' is already registered."

    # CO5: Instantiating appropriate class based on patron classification
    if clean_type == "student":
        member = StudentMember(clean_id, clean_name, clean_email)
    elif clean_type == "faculty":
        member = FacultyMember(clean_id, clean_name, clean_email)
    else:
        return False, "Error: Invalid member type. Please specify 'Student' or 'Faculty'."

    self.members[clean_id] = member
    self.save_data()
    return True, f"Success: {member.get_member_type()} Member '{member.name}' (ID: {clean_id}) registered."
```

### 2. Python Concepts Used
* **CO5 (Classes & Encapsulation):** Encapsulates member details (`member_id`, `name`, `email`) into distinct objects.
* **CO3 (Dictionaries):**
  * `self.members: dict[str, Member]`: Maps member IDs directly to Member objects.
  * Allows **$O(1)$ constant time lookup** when verifying members during borrowing and returning, rather than iterating through a slow list.
* **CO3 (String Formatting & Sanitization):**
  * `.strip()`: Cleans whitespace.
  * `.upper()`: Normalizes IDs (`s105` $\rightarrow$ `S105`).
  * `.lower()`: Normalizes emails (`Anshul@College.Edu` $\rightarrow$ `anshul@college.edu`).

### 3. Contribution to the Working of the Project
* Manages the library's patron records.
* Ensures that before anyone borrows a book, they are an authenticated and registered member of the institution.
* Connects the patron identity to their borrowing quota.

### 4. What to Demonstrate Live to the Teacher
1. Run `python main.py` and choose **Option 4 (Register Member)**.
2. Enter: ID: `S105`, Name: `Rahul Verma`, Email: `rahul@college.edu`, Type: `1 (Student)`.
3. Choose **Option 5 (View Members)** $\rightarrow$ Show Rahul Verma listed with limit `2`.
4. Try registering `S105` again $\rightarrow$ Show the duplicate ID rejection error.

### 5. Likely Viva / Modification Request
* **Teacher asks:** *"Why use a dictionary for members instead of a list?"*
* **Answer:** *"A dictionary provides $O(1)$ direct key lookup by `member_id`. If we had 10,000 members, looking up a member by ID in a list would take $O(n)$ time by scanning every item, whereas `self.members.get(member_id)` is instantaneous."*

---

# 👤 MEMBER 4: Issue and Return Books
- **Student Name:** Anusha M B
- **Assigned Feature:** Borrowing & Returning Transaction Lifecycle
- **Files Involved:** `library.py` (`borrow_book`, `return_book`, `get_issued_books`)

### 1. Code Block to Explain

```python
# library.py
def borrow_book(self, member_id: str, book_id: str) -> tuple[bool, str]:
    clean_mid = member_id.strip().upper()
    clean_bid = book_id.strip().upper()

    if not clean_mid or not clean_bid:
        return False, "Error: Both Member ID and Book ID are required."

    member = self.get_member(clean_mid)
    if not member:
        return False, f"Error: Member ID '{clean_mid}' not found."

    book = next((b for b in self.books if b.book_id == clean_bid), None)
    if not book:
        return False, f"Error: Book ID '{clean_bid}' not found."

    # CO3: Set membership check for availability
    if not book.is_available or clean_bid in self.issued_book_ids:
        return False, f"Error: Book '{book.title}' (ID: {clean_bid}) is already issued."

    # CO5: Polymorphic borrow limit verification
    current_borrowed = self.get_active_borrow_count(clean_mid)
    limit = member.get_borrow_limit()
    if current_borrowed >= limit:
        return False, f"Error: Borrowing limit reached! {member.get_member_type()} limit is {limit}."

    # Update states & record transaction
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
    return True, f"Success: Book '{book.title}' issued to {member.name} ({member.get_member_type()})."
```

```python
def return_book(self, member_id: str, book_id: str) -> tuple[bool, str]:
    clean_mid = member_id.strip().upper()
    clean_bid = book_id.strip().upper()

    # Find the active borrowing transaction
    active_tx = next((tx for tx in self.transactions if tx.get("book_id") == clean_bid and tx.get("status") == "ISSUED"), None)
    if not active_tx:
        return False, "Error: This book is not currently marked as issued."

    # Verify that the returning member is the one who borrowed it
    if active_tx["member_id"] != clean_mid:
        return False, f"Error: Book was borrowed by {active_tx['member_name']} ({active_tx['member_id']}), not {clean_mid}."

    book = next((b for b in self.books if b.book_id == clean_bid), None)
    book.mark_as_returned()
    self.issued_book_ids.remove(clean_bid)

    active_tx["status"] = "RETURNED"
    active_tx["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.save_data()
    return True, f"Success: Book '{book.title}' returned successfully."
```

### 2. Python Concepts Used
* **CO3 (Sets):** `self.issued_book_ids = set()` tracks issued IDs. Adding (`.add()`) and removing (`.remove()`) in a set prevents duplicate issuance and provides $O(1)$ membership checks.
* **CO3 (Lists of Dictionaries):** Stores transactions as structured dictionaries inside a list.
* **CO5 (Dynamic Polymorphism):** Invokes `member.get_borrow_limit()` to dynamically enforce borrowing limits without hardcoded `if-else` type checking.
* **Data Verification & Security:** Checks that only the original borrower can return the book.

### 3. Contribution to the Working of the Project
* Implements the **core operational workflow** of the library.
* Accurately tracks which books are in possession of which students/professors.
* Maintains a permanent transaction audit log with timestamps.

### 4. What to Demonstrate Live to the Teacher
1. Choose **Option 6 (Borrow Book)**.
2. Enter Member ID (e.g. Asin), Book: `B101` $\rightarrow$ Success.
3. Try borrowing `B101` again with another Member ID $\rightarrow$ Error: already issued.
4. Choose **Option 8 (View Issued Books)** $\rightarrow$ Shows active loan with date.
5. Choose **Option 7 (Return Book)** $\rightarrow$ Try returning with wrong ID, then correct ID $\rightarrow$ Success!

### 5. Likely Viva / Modification Request
* **Teacher asks:** *"Why do you check `active_tx['member_id'] != clean_mid`?"*
* **Answer:** *"To prevent student A from returning or tampering with a book that was officially checked out under student B's account."*

---

# 👤 MEMBER 5: File Handling & Data Persistence (JSON & CSV)
- **Student Name:** Aryan Raj
- **Assigned Feature:** JSON & CSV File Storage & Robust Exception Handling
- **Files Involved:** `library.py` (`load_data`, `save_data`), `data/books.json`, and `data/books.csv`

### 1. Code Block to Explain

```python
# library.py
import json
import csv

def load_data(self):
    # 1. Load Books with Exception Handling (CO4: JSON)
    try:
        with open(self.books_file, "r", encoding="utf-8") as f:
            raw_books = json.load(f)
            self.books = [Book.from_dict(b) for b in raw_books]
    except FileNotFoundError:
        # First-time run: create safe in-memory list
        self.books = []
    except json.JSONDecodeError:
        print(f"[Warning] '{self.books_file}' is corrupted. Starting with empty book list.")
        self.books = []

    # 2. Load Members
    try:
        with open(self.members_file, "r", encoding="utf-8") as f:
            raw_members = json.load(f)
            self.members = {m["member_id"]: Member.from_dict(m) for m in raw_members}
    except (FileNotFoundError, json.JSONDecodeError):
        self.members = {}

    # 3. Synchronize Issued Book IDs (CO3: Set Comprehension)
    self.issued_book_ids = {
        tx["book_id"] for tx in self.transactions if tx.get("status") == "ISSUED"
    }

def save_data(self):
    self._ensure_data_directory()
    
    # 1. JSON Persistence
    with open(self.books_file, "w", encoding="utf-8") as f:
        json.dump([b.to_dict() for b in self.books], f, indent=4)

    with open(self.members_file, "w", encoding="utf-8") as f:
        json.dump([m.to_dict() for m in self.members.values()], f, indent=4)

    with open(self.transactions_file, "w", encoding="utf-8") as f:
        json.dump(self.transactions, f, indent=4)

    # 2. CO4: CSV File Handling - Writes tabular reports in CSV format
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
```

### 2. Python Concepts Used
* **CO4 (JSON File Handling):**
  * `with open(..., "r")` & `with open(..., "w")`: Python context managers that guarantee files are automatically closed.
  * `json.load()` and `json.dump(..., indent=4)`: Serializing and deserializing Python objects to formatted JSON.
* **CO4 (CSV File Handling):**
  * `import csv`, `csv.writer()`, `writer.writerow([...])`: Generates standard comma-separated tabular files readable in Excel or any spreadsheet tool.
* **CO4 (Exception Handling):**
  * `try...except FileNotFoundError`: Handles first-time setup when no files exist yet.
  * `try...except json.JSONDecodeError`: Catches syntax errors in JSON without crashing.
* **CO3 (Set Comprehension):**
  * `{tx["book_id"] for tx in self.transactions ...}` dynamically reconstructs active loans set upon loading.

### 3. Contribution to the Working of the Project
* Ensures **data persistence**: Library records are not lost when the program terminates.
* Provides **fault tolerance**: The program will not crash due to missing files or formatting issues in data storage.
* Delivers **dual export**: Saves in JSON for application state and CSV for spreadsheet/data analytics.

### 4. What to Demonstrate Live to the Teacher
1. Add a new book or member in `python main.py`.
2. Exit the program (Option 9).
3. Open `data/books.json` and `data/books.csv` in VS Code / Notepad and show both files to the teacher.
4. Re-run `python main.py` $\rightarrow$ Point out that all data was reloaded automatically!

### 5. Likely Viva / Modification Request
* **Teacher asks:** *"What is the benefit of `with open(...)` compared to `f = open()`?"*
* **Answer:** *"With `with open()`, Python automatically closes the file stream when the block exits, even if an unhandled exception is raised. With manual `open()`, if an error occurs before `f.close()`, the file descriptor leaks and the file remains locked."*

---

# 👤 MEMBER 6: Classes, Inheritance & Polymorphism Integration
- **Student Name:** Archit Raj
- **Assigned Feature:** Object-Oriented Architecture, Subclassing & Polymorphic Rules
- **Files Involved:** `member.py` (`StudentMember`, `FacultyMember`) and `main.py` (Interactive Runner)

### 1. Code Block to Explain

```python
# member.py
class Member:
    def __init__(self, member_id: str, name: str, email: str):
        self.member_id = member_id.strip().upper()
        self.name = name.strip().title()
        self.email = email.strip().lower()

    def get_borrow_limit(self) -> int:
        return 1

    def get_member_type(self) -> str:
        return "General"


class StudentMember(Member):
    def __init__(self, member_id: str, name: str, email: str):
        super().__init__(member_id, name, email)  # CO5: Invoking Parent Constructor

    def get_borrow_limit(self) -> int:           # CO5: Method Overriding (Polymorphism)
        return 2

    def get_member_type(self) -> str:
        return "Student"


class FacultyMember(Member):
    def __init__(self, member_id: str, name: str, email: str):
        super().__init__(member_id, name, email)  # CO5: Invoking Parent Constructor

    def get_borrow_limit(self) -> int:           # CO5: Method Overriding (Polymorphism)
        return 5

    def get_member_type(self) -> str:
        return "Faculty"
```

```python
# Where Polymorphism is executed in library.py:
limit = member.get_borrow_limit()  # No "if isinstance(member, StudentMember)" needed!
if current_borrowed >= limit:
    return False, f"Borrowing limit of {limit} reached for {member.get_member_type()}."
```

### 2. Python Concepts Used
* **CO5 (Inheritance):**
  * `class StudentMember(Member)` and `class FacultyMember(Member)` inherit common attributes (`member_id`, `name`, `email`) from `Member`.
  * `super().__init__(member_id, name, email)` calls the base class constructor, avoiding code duplication.
* **CO5 (Polymorphism & Method Overriding):**
  * Both child classes provide their own version of `get_borrow_limit()` and `get_member_type()`.
  * The borrowing logic in `library.py` does not need to know whether an object is a Student or a Faculty member; it simply calls `member.get_borrow_limit()`, and Python dynamically dispatches the correct subclass method at runtime.
* **CO5 (Extensibility):**
  * New member types (e.g. `GuestMember`, `ResearchScholar`) can be added without changing a single line of borrowing validation code.

### 3. Contribution to the Working of the Project
* Enforces **institutional policies**: Students are limited to 2 books at a time, while Faculty are permitted up to 5 books.
* Keeps the code clean, modular, and maintainable following the Open-Closed Principle (SOLID).

### 4. What to Demonstrate Live to the Teacher
1. Select a Student member (e.g. Anshul Kumar).
2. Borrow 2 books successfully (`B101`, `B102`).
3. Try borrowing a 3rd book (`B103`) $\rightarrow$ Show the error: *Student members can borrow at most 2 books*.
4. Now select a Faculty member (e.g. Dr. Ramesh Sharma) and borrow 3 or more books $\rightarrow$ Succeeds because the faculty limit is 5!

### 5. Likely Viva / Modification Request
* **Teacher asks:** *"Add a new member type: GuestMember with a limit of 1 book."*
* **Modification:**
  In `member.py`:
  ```python
  class GuestMember(Member):
      def __init__(self, member_id: str, name: str, email: str):
          super().__init__(member_id, name, email)

      def get_borrow_limit(self) -> int:
          return 1

      def get_member_type(self) -> str:
          return "Guest"
  ```
  *Point out to the teacher that `library.py` requires zero changes to support `GuestMember` because of polymorphism!*

---

## 🏆 Summary Table for Quick Reference During Evaluation

| Member | Name | Main File | Key Concept | One-Line Summary |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Asin | `book.py` | CO5 Class, CO3 Tuple & Strings | Defines the Book entity, validates attributes, and blocks duplicate IDs. |
| **2** | Anne Reeja A | `library.py` | CO3 Search, Lowercase, f-strings | Implements case-insensitive substring search and formatted tables. |
| **3** | Anshul Kumar | `member.py` | CO5 Encapsulation, CO3 Dictionary | Registers patrons and stores them in an $O(1)$ lookup dictionary. |
| **4** | Anusha M B | `library.py` | CO3 Sets & Lists, Loan Rules | Issues and returns books, updates availability, and verifies borrower identity. |
| **5** | Aryan Raj | `library.py` | CO4 JSON & CSV I/O, `try...except` | Persists records in both JSON and CSV formats with crash-safe file handling. |
| **6** | Archit Raj | `member.py` | CO5 Inheritance & Polymorphism | Implements Member inheritance and overrides borrowing limits (2 for Student, 5 for Faculty). |
