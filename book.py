"""
Book Module
Defines the Book class and related constants.
Demonstrates Course Outcomes:
- CO3: Tuples (ALLOWED_CATEGORIES), dictionaries, and string operations.
- CO5: Object-Oriented Programming (Class, Constructor, Methods, State).
"""

# CO3: Tuple - Fixed collection of standard library book categories
ALLOWED_CATEGORIES = (
    "Fiction",
    "Non-Fiction",
    "Science",
    "Technology",
    "History",
    "Literature",
    "General"
)


class Book:
    """
    Represents a book in the library system.
    Demonstrates CO5: Class, constructor (__init__), instance variables, and methods.
    """

    def __init__(self, book_id: str, title: str, author: str, category: str, is_available: bool = True):
        # Clean and format string inputs (CO3: String Operations)
        self.book_id = book_id.strip().upper()
        self.title = title.strip().title()
        self.author = author.strip().title()
        self.category = category.strip().title()
        self.is_available = is_available

    def mark_as_borrowed(self):
        """Marks the book as currently borrowed (unavailable)."""
        self.is_available = False

    def mark_as_returned(self):
        """Marks the book as returned (available)."""
        self.is_available = True

    def to_dict(self) -> dict:
        """
        CO3 & CO4: Converts the Book object into a dictionary for JSON serialization.
        """
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "is_available": self.is_available
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        CO4: Creates a Book instance from a dictionary loaded from JSON.
        """
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            category=data["category"],
            is_available=data.get("is_available", True)
        )

    def __str__(self) -> str:
        """User-friendly string representation of a Book."""
        status = "Available" if self.is_available else "Issued"
        return f"[{self.book_id}] {self.title} by {self.author} | Category: {self.category} | Status: {status}"
