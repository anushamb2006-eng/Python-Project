# Library Management System - Record Book Visualizations

## 1. Project Block Diagram

```text
┌──────────────────────────────────────────────────────────────┐
│                       LIBRARY USER                           │
│              (Student / Faculty / Librarian)                 │
└────────────────────────────┬─────────────────────────────────┘
                             │ Menu Selection and Input
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                  Console Interface (UI)                      │
│  Add | View | Search | Register | Borrow | Return | Report   │
└────────────────────────────┬─────────────────────────────────┘
                             │ Calls Library Methods
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                        library.py                            │
│                     Core Business Logic                      │
│     Validation | Search | Borrow | Return | Persistence      │
└───────────────┬────────────────────────────┬─────────────────┘
                │                            │
                ▼                            ▼
┌──────────────────────────┐  ┌───────────────────────────────┐
│        book.py           │  │          member.py            │
│  Book Class              │  │  Member Base Class            │
│  ALLOWED_CATEGORIES      │  │  StudentMember                │
│                          │  │  FacultyMember                │
└──────────────────────────┘  └───────────────────────────────┘
                │                            │
                └──────────────┬─────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      data/ Directory                         │
│  books.json | members.json | transactions.json | books.csv   │
└──────────────────────────────────────────────────────────────┘
```

## 2. Data Flow Diagram - Level 0

```text
                           ┌──────────────┐
                           │    User      │
                           └──────┬───────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │ Book/member/borrow/return information          │
          ▼                                               ▼
┌────────────────────────────────────────────────────────────────┐
│             0. Library Management System                        │
│                                                                │
│  Processes catalogue, member, issue, return and report tasks.  │
└────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Success/error messages
                                  │ and tabular reports
                                  ▼
                           ┌──────────────┐
                           │    User      │
                           └──────────────┘
```

## 3. Data Flow Diagram - Level 1

```text
       ┌────────────┐
       │    User    │
       └─────┬──────┘
             │
 ┌───────────┼────────────┬────────────┬────────────┐
 │           │            │            │            │
 ▼           ▼            ▼            ▼            ▼
┌─────┐  ┌────────┐  ┌─────────┐  ┌────────┐  ┌────────┐
│ 1.0 │  │  2.0   │  │  3.0    │  │  4.0   │  │  5.0   │
│Add  │  │Search  │  │Register │  │ Borrow │  │Return  │
│Book │  │  Books │  │ Member  │  │  Book  │  │  Book  │
└──┬──┘  └───┬────┘  └────┬────┘  └───┬────┘  └───┬────┘
   │         │            │           │           │
   ▼         ▼            ▼           ▼           ▼
┌───────────────────────────────────────────────────────────┐
│                  Central Library Operations                │
│                       library.py                          │
└──────┬───────────────┬───────────────┬───────────────────┘
       │               │               │
       ▼               ▼               ▼
┌────────────┐  ┌────────────┐  ┌───────────────────┐
│  D1: Books │  │ D2: Members│  │ D3: Transactions  │
└────────────┘  └────────────┘  └───────────────────┘
       │               │               │
       └───────────────┴───────────────┘
                       │
                       ▼
              JSON and CSV Files
```

## 4. Class Diagram

```text
┌──────────────────────────┐
│          Member          │
├──────────────────────────┤
│ - member_id: str         │
│ - name: str              │
│ - email: str             │
├──────────────────────────┤
│ + get_borrow_limit(): int│
│ + get_member_type(): str │
│ + to_dict(): dict        │
│ + from_dict(): Member    │
└────────────┬─────────────┘
             │ Inheritance
             ├───────────────────────────────┐
             ▼                               ▼
┌────────────────────────┐     ┌────────────────────────┐
│     StudentMember      │     │     FacultyMember      │
├────────────────────────┤     ├────────────────────────┤
│ Borrow limit = 2       │     │ Borrow limit = 5       │
│ Member type = Student  │     │ Member type = Faculty  │
└────────────────────────┘     └────────────────────────┘


┌──────────────────────────┐
│           Book           │
├──────────────────────────┤
│ - book_id: str           │
│ - title: str             │
│ - author: str            │
│ - category: str          │
│ - is_available: bool     │
├──────────────────────────┤
│ + mark_as_borrowed()     │
│ + mark_as_returned()     │
│ + to_dict(): dict        │
└──────────────────────────┘
```

## 5. Main Program Control Flow

```text
START
  │
  ▼
Initialize Library and load JSON files
  │
  ▼
Display menu
  │
  ▼
Read user's menu choice
  │
  ├── 1 ──> Add Book
  ├── 2 ──> View All Books
  ├── 3 ──> Search Books
  ├── 4 ──> Register Member
  ├── 5 ──> View Members
  ├── 6 ──> Borrow Book
  ├── 7 ──> Return Book
  ├── 8 ──> View Issued Books
  └── 9 ──> Exit Program
  │
  ▼
Validate input and execute Library operation
  │
  ├── Success ──> Display success message and save data
  │
  └── Error ────> Display error message
  │
  ▼
Return to menu
```

## 6. Book Borrowing Flowchart

```text
START
  │
  ▼
Enter Member ID and Book ID
  │
  ▼
Is Member registered?
  │
  ├── No ──> Error: Member not found
  │
  └── Yes
       │
       ▼
  Is Book present?
       │
       ├── No ──> Error: Book not found
       │
       └── Yes
            │
            ▼
       Is Book available?
            │
            ├── No ──> Error: Book already issued
            │
            └── Yes
                 │
                 ▼
            Is active borrow count
            less than member limit?
                 │
                 ├── No ──> Error: Borrowing limit reached
                 │
                 └── Yes
                      │
                      ▼
                 Mark book unavailable
                      │
                      ▼
                 Add Book ID to issued set
                      │
                      ▼
                 Create transaction record
                      │
                      ▼
                 Save JSON and CSV files
                      │
                      ▼
                 Display success message
                      │
                      ▼
                    END
```

## 7. Book Return Flowchart

```text
START
  │
  ▼
Enter Member ID and Book ID
  │
  ▼
Does active issued transaction exist?
  │
  ├── No ──> Error: Book is not issued
  │
  └── Yes
       │
       ▼
  Does Member ID match original borrower?
       │
       ├── No ──> Error: Another member borrowed this book
       │
       └── Yes
            │
            ▼
       Mark book available
            │
            ▼
       Remove Book ID from issued set
            │
            ▼
       Update transaction status to RETURNED
            │
            ▼
       Add return date and time
            │
            ▼
       Save data
            │
            ▼
       Display success message
            │
            ▼
          END
```

## 8. File and Data Visualization

```text
Library Operations
        │
        ├──> books.json
        │    [book_id, title, author, category, is_available]
        │
        ├──> members.json
        │    [member_id, name, email, member_type]
        │
        ├──> transactions.json
        │    [transaction_id, member_id, book_id,
        │     borrow_date, return_date, status]
        │
        └──> books.csv
             Tabular book catalogue for spreadsheet view
```

## 9. Data Structures and Their Uses

| Data Structure | Variable | Purpose |
|---|---|---|
| List | `self.books` | Stores all Book objects |
| Dictionary | `self.members` | Maps member ID to Member object for fast lookup |
| Set | `self.issued_book_ids` | Stores IDs of currently issued books |
| List of Dictionaries | `self.transactions` | Stores complete issue and return history |
| Tuple | `ALLOWED_CATEGORIES` | Stores fixed allowed book categories |
| Tuple | Method return value | Returns `(success, message)` |

## 10. OOP Visualization

```text
Member
  │
  ├── StudentMember
  │     └── get_borrow_limit() -> 2
  │
  └── FacultyMember
        └── get_borrow_limit() -> 5

Library borrowing logic:

member.get_borrow_limit()
       │
       ├── Student object ──> returns 2
       │
       └── Faculty object ──> returns 5
```
