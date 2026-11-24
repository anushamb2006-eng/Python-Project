"""
Member Module
Defines the Member hierarchy for library patrons.
Demonstrates Course Outcomes:
- CO5: Object-Oriented Programming:
  - Base class (Member)
  - Inheritance (StudentMember, FacultyMember subclass Member)
  - Constructors (__init__) & super() calls
  - Polymorphism & Method Overriding (get_borrow_limit, get_member_type)
- CO3: String operations & dictionary structures
- CO4: Data transformation for JSON persistence
"""


class Member:
    """
    Base class representing a generic library member.
    """

    def __init__(self, member_id: str, name: str, email: str):
        # Clean up and normalize member details (CO3: String Operations)
        self.member_id = member_id.strip().upper()
        self.name = name.strip().title()
        self.email = email.strip().lower()

    def get_borrow_limit(self) -> int:
        """
        Polymorphic method: Returns maximum books this member can borrow.
        Base implementation provides standard default limit.
        Subclasses override this behavior (CO5: Polymorphism).
        """
        return 1

    def get_member_type(self) -> str:
        """
        Polymorphic method: Returns member classification string.
        """
        return "General"

    def to_dict(self) -> dict:
        """
        Converts Member object to a dictionary for JSON file storage.
        """
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "member_type": self.get_member_type()
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Factory method to reconstruct the appropriate subclass from saved JSON data.
        """
        m_type = data.get("member_type", "").lower()
        if m_type == "student":
            return StudentMember(data["member_id"], data["name"], data["email"])
        elif m_type == "faculty":
            return FacultyMember(data["member_id"], data["name"], data["email"])
        else:
            return Member(data["member_id"], data["name"], data["email"])

    def __str__(self) -> str:
        return (f"[{self.member_id}] {self.name} ({self.get_member_type()}) | "
                f"Email: {self.email} | Borrow Limit: {self.get_borrow_limit()}")


class StudentMember(Member):
    """
    Child class representing a Student library member.
    Demonstrates Inheritance and Polymorphic Method Overriding (CO5).
    """

    def __init__(self, member_id: str, name: str, email: str):
        # Call parent constructor using super() (CO5)
        super().__init__(member_id, name, email)

    def get_borrow_limit(self) -> int:
        """
        Overrides parent method: Students are allowed to borrow up to 2 books.
        """
        return 2

    def get_member_type(self) -> str:
        """
        Overrides parent method: Identifies as Student.
        """
        return "Student"


class FacultyMember(Member):
    """
    Child class representing a Faculty library member.
    Demonstrates Inheritance and Polymorphic Method Overriding (CO5).
    """

    def __init__(self, member_id: str, name: str, email: str):
        # Call parent constructor using super() (CO5)
        super().__init__(member_id, name, email)

    def get_borrow_limit(self) -> int:
        """
        Overrides parent method: Faculty members are allowed to borrow up to 5 books.
        """
        return 5

    def get_member_type(self) -> str:
        """
        Overrides parent method: Identifies as Faculty.
        """
        return "Faculty"
