# Group 2 — Library Management System (Python)

A console-based Library Management System developed for the Python Integrated Course Outcomes Evaluation (**CO3, CO4, CO5**).

---

## 👥 Group Details (Group 2)
- **Problem Statement**: Library Management System (manage books, members, borrowing, and returning)
- **Course Outcomes Covered**:
  - **CO3**: Data Structures (`list`, `dict`, `set`, `tuple`) & String Operations (`.strip()`, `.lower()`, `.upper()`, `.title()`, substring `in`)
  - **CO4**: File Handling (`JSON` read/write with `with open`) & Exception Handling (`try...except` for `FileNotFoundError`, `json.JSONDecodeError`, input validation)
  - **CO5**: Object-Oriented Programming (Classes, Constructors `__init__`, Inheritance `super()`, and Polymorphism via method overriding)

---

## 📁 Project Structure

```text
mini Proj/
│
├── main.py          # Interactive console menu & user input handling
├── library.py       # Core business logic, file persistence, search, borrow & return
├── book.py          # Book class and category tuple
├── member.py        # Member base class, StudentMember and FacultyMember subclasses
├── test_system.py   # Automated verification script
│
└── data/
    ├── books.json        # Saved book records
    ├── members.json      # Saved member records
    └── transactions.json # Borrow & return transaction history
```

---

## 🚀 How to Run the Program

In the project root folder, open your terminal (PowerShell / Command Prompt) and run:

```bash
python main.py
```

To run the automated verification test suite:

```bash
python test_system.py
```

---

## 🎓 Mapping to Evaluation Rubric (50 Marks)

### 1. CO3: Data Structures & String Operations (10 Marks)
- **`list`**: Stores all books (`self.books`), transaction history (`self.transactions`), and search results.
- **`dict`**: Maps member IDs to Member objects (`self.members[member_id] = member`) for $O(1)$ fast lookups; used for JSON serialization (`to_dict()`).
- **`set`**: `self.issued_book_ids` tracks IDs of books currently borrowed to prevent double-borrowing with $O(1)$ checks.
- **`tuple`**: `ALLOWED_CATEGORIES` in `book.py` defines immutable category options; return values `(bool, str)` return status and message.
- **String Operations**:
  - `.strip()`: Cleans leading/trailing spaces from user inputs.
  - `.lower()`: Case-insensitive searching (`query in book.title.lower()`).
  - `.upper()`: Standardizes Book IDs and Member IDs (`B101`, `S101`).
  - `.title()`: Formats book titles and author names cleanly.
  - `f-strings`: Tabular alignment with column widths for clean console display.

### 2. CO4: File Handling & Exception Handling (10 Marks)
- **File Handling**:
  - Reads data using `json.load()` inside `with open(..., "r")`.
  - Writes data using `json.dump(..., indent=4)` inside `with open(..., "w")`.
  - Data remains preserved across application restarts.
- **Exception Handling**:
  - `FileNotFoundError`: Gracefully starts with an empty list on the first run; automatically creates the directory and file on save.
  - `json.JSONDecodeError`: Catches corrupted JSON files safely without crashing the program.
  - `ValueError` / Input Validation: Rejects invalid menu numbers, empty book fields, duplicate IDs, and unauthorized book returns.

### 3. CO5: OOP, Inheritance & Polymorphism (10 Marks)
- **Classes & Objects**:
  - `Book`: Manages book properties (`book_id`, `title`, `author`, `category`, `is_available`).
  - `Member`: Base class with common attributes (`member_id`, `name`, `email`).
- **Inheritance**:
  - `StudentMember(Member)` inherits from `Member` using `super().__init__(...)`.
  - `FacultyMember(Member)` inherits from `Member` using `super().__init__(...)`.
- **Polymorphism & Method Overriding**:
  - Both subclasses override `get_borrow_limit()`:
    - `StudentMember.get_borrow_limit()` returns **2** books.
    - `FacultyMember.get_borrow_limit()` returns **5** books.
  - Both subclasses override `get_member_type()`.
  - When borrowing, `library.py` executes:
    ```python
    limit = member.get_borrow_limit() # Dynamically invokes Student (2) or Faculty (5)
    if current_borrowed >= limit:
        # Borrow rejected
    ```

---

## 📋 Step-by-Step Teacher Walkthrough Order

Follow this exact sequence during the live demonstration:

1. **Run Application**:
   - Run `python main.py`.
   - Point out that it loads existing JSON files or starts cleanly.
2. **Add Books (Option 1)**:
   - Add Book `B101`, Title: `Python Crash Course`, Author: `Eric Matthes`, Category: `Technology`.
   - Add Book `B102`, Title: `Clean Code`, Author: `Robert C. Martin`, Category: `Technology`.
   - Try adding `B101` again — show the duplicate ID rejection error.
3. **View All Books (Option 2)**:
   - Show the neatly formatted table with status `Available`.
4. **Search Books (Option 3)**:
   - Search for `python` (lowercase), then `PYTHON` (uppercase).
   - Point out that both return the book because of `.lower()` and `in` operator.
5. **Register Members (Option 4)**:
   - Register Student: ID `S101`, Name `Anshul Kumar`, Email `anshul@college.edu`, Type `1` (Student).
   - Register Faculty: ID `F101`, Name `Dr. Sharma`, Email `sharma@univ.edu`, Type `2` (Faculty).
6. **View Members (Option 5)**:
   - Show the members table displaying the polymorphic borrow limits (**2** for student, **5** for faculty).
7. **Borrow Books & Show Polymorphic Rule (Option 6)**:
   - Member `S101` borrows `B101` -> Success.
   - Member `F101` tries to borrow `B101` -> Error: Book is already issued.
   - Member `S101` borrows `B102` -> Success (now holding 2/2).
   - Member `S101` tries to borrow a 3rd book -> Error: Student borrowing limit of 2 reached!
8. **View Issued Books (Option 8)**:
   - Show the active loans with transaction ID, borrower name, and date.
9. **Return Book (Option 7)**:
   - Faculty `F101` tries to return `B101` -> Error: Cannot return; book was borrowed by `S101`.
   - Student `S101` returns `B101` -> Success.
10. **Data Persistence Verification (Exit & Restart)**:
    - Select Option `9` (Exit).
    - Open `data/books.json`, `data/members.json`, `data/transactions.json` to show the JSON records.
    - Run `python main.py` again and select Option `2` — show that all records persist!
