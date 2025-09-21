from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

@dataclass
class Patron:
    id: Optional[str]  # MongoDB ObjectId as string
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    membership_type: str  # "student", "faculty", "community", "premium"
    membership_start_date: datetime
    membership_end_date: Optional[datetime]
    books_checked_out: List[str]  # List of book IDs
    total_books_borrowed: int
    active: bool
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        """Convert Patron to dictionary for MongoDB storage"""
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "membership_type": self.membership_type,
            "membership_start_date": self.membership_start_date,
            "membership_end_date": self.membership_end_date,
            "books_checked_out": self.books_checked_out,
            "total_books_borrowed": self.total_books_borrowed,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        # Only include id if it exists (for updates)
        if self.id:
            data["_id"] = ObjectId(self.id)
            
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Patron':
        """Create Patron from MongoDB document"""
        return cls(
            id=str(data["_id"]) if "_id" in data else None,
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data.get("phone"),
            address=data.get("address"),
            membership_type=data["membership_type"],
            membership_start_date=data["membership_start_date"],
            membership_end_date=data.get("membership_end_date"),
            books_checked_out=data.get("books_checked_out", []),
            total_books_borrowed=data.get("total_books_borrowed", 0),
            active=data.get("active", True),
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )

    def get_full_name(self) -> str:
        """Get patron's full name"""
        return f"{self.first_name} {self.last_name}"

    def is_membership_active(self) -> bool:
        """Check if membership is currently active"""
        if not self.active:
            return False
        
        if self.membership_end_date:
            return datetime.now() <= self.membership_end_date
        
        return True

    def can_checkout_book(self, max_books: int = 5) -> bool:
        """Check if patron can checkout more books"""
        return (
            self.is_membership_active() and 
            len(self.books_checked_out) < max_books
        )


