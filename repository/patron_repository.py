from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from models.patron import Patron
from repository.mongodb_database import get_mongodb_connection


class IPatronRepository(ABC):
    """Patron repository interface"""

    @abstractmethod
    def create_patron(self, patron: Patron) -> str:
        """Create a new patron"""
        pass

    @abstractmethod
    def update_patron(self, patron: Patron) -> str:
        """Update an existing patron"""
        pass

    @abstractmethod
    def get_patron_by_id(self, patron_id: str) -> Optional[Patron]:
        """Get patron by ID"""
        pass

    @abstractmethod
    def get_patron_by_email(self, email: str) -> Optional[Patron]:
        """Get patron by email"""
        pass

    @abstractmethod
    def delete_patron_by_id(self, patron_id: str) -> bool:
        """Delete patron by ID"""
        pass

    @abstractmethod
    def list_patrons(self, limit: int = 100, offset: int = 0, active_only: bool = True) -> List[Patron]:
        """List patrons with pagination"""
        pass

    @abstractmethod
    def search_patrons_by_name(self, name: str, limit: int = 50) -> List[Patron]:
        """Search patrons by name (first or last)"""
        pass

    @abstractmethod
    def get_patrons_by_membership_type(self, membership_type: str) -> List[Patron]:
        """Get patrons by membership type"""
        pass

    @abstractmethod
    def checkout_book(self, patron_id: str, book_id: str) -> bool:
        """Add book to patron's checked out list"""
        pass

    @abstractmethod
    def return_book(self, patron_id: str, book_id: str) -> bool:
        """Remove book from patron's checked out list"""
        pass

    @abstractmethod
    def get_patrons_with_overdue_books(self) -> List[Patron]:
        """Get patrons who have overdue books (placeholder for future implementation)"""
        pass


class PatronRepository(IPatronRepository):
    """MongoDB implementation of IPatronRepository"""

    def __init__(self):
        self._connection = get_mongodb_connection()
        self._collection = None

    def _get_collection(self):
        """Get the patrons collection"""
        if not self._collection:
            self._collection = self._connection.get_collection("patrons")
        return self._collection

    def create_patron(self, patron: Patron) -> str:
        """Create a new patron"""
        try:
            collection = self._get_collection()
            patron_dict = patron.to_dict()
            
            # Remove id from dict for creation (MongoDB will generate it)
            if "_id" in patron_dict:
                del patron_dict["_id"]
            
            result = collection.insert_one(patron_dict)
            return str(result.inserted_id)
            
        except DuplicateKeyError:
            raise ValueError(f"Patron with email {patron.email} already exists")
        except Exception as e:
            raise Exception(f"Failed to create patron: {str(e)}")

    def update_patron(self, patron: Patron) -> str:
        """Update an existing patron"""
        try:
            collection = self._get_collection()
            patron_dict = patron.to_dict()
            
            # Update the updated_at timestamp
            patron_dict["updated_at"] = datetime.now()
            
            # Remove _id from update data
            patron_id = patron_dict.pop("_id")
            
            result = collection.update_one(
                {"_id": ObjectId(patron_id)},
                {"$set": patron_dict}
            )
            
            if result.matched_count == 0:
                raise ValueError(f"Patron with ID {patron_id} not found")
            
            return patron_id
            
        except Exception as e:
            raise Exception(f"Failed to update patron: {str(e)}")

    def get_patron_by_id(self, patron_id: str) -> Optional[Patron]:
        """Get patron by ID"""
        try:
            collection = self._get_collection()
            patron_data = collection.find_one({"_id": ObjectId(patron_id)})
            
            if patron_data:
                return Patron.from_dict(patron_data)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to get patron by ID: {str(e)}")

    def get_patron_by_email(self, email: str) -> Optional[Patron]:
        """Get patron by email"""
        try:
            collection = self._get_collection()
            patron_data = collection.find_one({"email": email})
            
            if patron_data:
                return Patron.from_dict(patron_data)
            return None
            
        except Exception as e:
            raise Exception(f"Failed to get patron by email: {str(e)}")

    def delete_patron_by_id(self, patron_id: str) -> bool:
        """Delete patron by ID"""
        try:
            collection = self._get_collection()
            result = collection.delete_one({"_id": ObjectId(patron_id)})
            
            return result.deleted_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to delete patron: {str(e)}")

    def list_patrons(self, limit: int = 100, offset: int = 0, active_only: bool = True) -> List[Patron]:
        """List patrons with pagination"""
        try:
            collection = self._get_collection()
            
            query = {}
            if active_only:
                query["active"] = True
            
            cursor = collection.find(query).skip(offset).limit(limit).sort("created_at", -1)
            
            patrons = []
            for patron_data in cursor:
                patrons.append(Patron.from_dict(patron_data))
            
            return patrons
            
        except Exception as e:
            raise Exception(f"Failed to list patrons: {str(e)}")

    def search_patrons_by_name(self, name: str, limit: int = 50) -> List[Patron]:
        """Search patrons by name (first or last)"""
        try:
            collection = self._get_collection()
            
            # Case-insensitive search in first_name or last_name
            query = {
                "$or": [
                    {"first_name": {"$regex": name, "$options": "i"}},
                    {"last_name": {"$regex": name, "$options": "i"}}
                ]
            }
            
            cursor = collection.find(query).limit(limit).sort("last_name", 1)
            
            patrons = []
            for patron_data in cursor:
                patrons.append(Patron.from_dict(patron_data))
            
            return patrons
            
        except Exception as e:
            raise Exception(f"Failed to search patrons by name: {str(e)}")

    def get_patrons_by_membership_type(self, membership_type: str) -> List[Patron]:
        """Get patrons by membership type"""
        try:
            collection = self._get_collection()
            
            cursor = collection.find({"membership_type": membership_type}).sort("last_name", 1)
            
            patrons = []
            for patron_data in cursor:
                patrons.append(Patron.from_dict(patron_data))
            
            return patrons
            
        except Exception as e:
            raise Exception(f"Failed to get patrons by membership type: {str(e)}")

    def checkout_book(self, patron_id: str, book_id: str) -> bool:
        """Add book to patron's checked out list"""
        try:
            collection = self._get_collection()
            
            result = collection.update_one(
                {"_id": ObjectId(patron_id)},
                {
                    "$addToSet": {"books_checked_out": book_id},
                    "$inc": {"total_books_borrowed": 1},
                    "$set": {"updated_at": datetime.now()}
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to checkout book: {str(e)}")

    def return_book(self, patron_id: str, book_id: str) -> bool:
        """Remove book from patron's checked out list"""
        try:
            collection = self._get_collection()
            
            result = collection.update_one(
                {"_id": ObjectId(patron_id)},
                {
                    "$pull": {"books_checked_out": book_id},
                    "$set": {"updated_at": datetime.now()}
                }
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            raise Exception(f"Failed to return book: {str(e)}")

    def get_patrons_with_overdue_books(self) -> List[Patron]:
        """Get patrons who have overdue books (placeholder for future implementation)"""
        # This would require integration with a checkout/loan system
        # For now, return empty list
        return []


