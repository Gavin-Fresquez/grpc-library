from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional
import os
from datetime import datetime

class MongoDBConnection:
    """MongoDB connection manager"""
    
    def __init__(self, connection_string: Optional[str] = None, database_name: str = "library_db"):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string. If None, uses environment variable or default
            database_name: Name of the database to use
        """
        self.connection_string = connection_string or os.getenv(
            'MONGODB_URI', 
            'mongodb://localhost:27017/'
        )
        self.database_name = database_name
        self._client: Optional[MongoClient] = None
        self._database = None
        
    def connect(self) -> bool:
        """
        Establish connection to MongoDB
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self._client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,        # 10 second connection timeout
                socketTimeoutMS=20000           # 20 second socket timeout
            )
            
            # Test the connection
            self._client.admin.command('ping')
            self._database = self._client[self.database_name]
            
            print(f"Successfully connected to MongoDB database: {self.database_name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            print("Disconnected from MongoDB")
    
    def get_database(self):
        """
        Get the database instance
        
        Returns:
            Database instance or None if not connected
        """
        if not self._database:
            if not self.connect():
                return None
        return self._database
    
    def get_collection(self, collection_name: str):
        """
        Get a collection from the database
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection instance or None if not connected
        """
        database = self.get_database()
        if database:
            return database[collection_name]
        return None
    
    def is_connected(self) -> bool:
        """
        Check if MongoDB connection is active
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            if self._client:
                self._client.admin.command('ping')
                return True
        except:
            pass
        return False
    
    def create_indexes(self):
        """Create necessary indexes for optimal performance"""
        try:
            # Patrons collection indexes
            patrons_collection = self.get_collection("patrons")
            if patrons_collection:
                # Unique index on email
                patrons_collection.create_index("email", unique=True)
                # Index on membership_type for filtering
                patrons_collection.create_index("membership_type")
                # Index on active status
                patrons_collection.create_index("active")
                # Compound index for name searches
                patrons_collection.create_index([("first_name", 1), ("last_name", 1)])
                
            # Books collection indexes (if using MongoDB for books too)
            books_collection = self.get_collection("books")
            if books_collection:
                # Unique index on ISBN
                books_collection.create_index("isbn_number", unique=True)
                # Index on checked_out status
                books_collection.create_index("checked_out")
                
            print("Database indexes created successfully")
            
        except Exception as e:
            print(f"Error creating indexes: {e}")


# Global connection instance
_mongodb_connection: Optional[MongoDBConnection] = None

def get_mongodb_connection() -> MongoDBConnection:
    """
    Get the global MongoDB connection instance
    
    Returns:
        MongoDBConnection: The global connection instance
    """
    global _mongodb_connection
    if _mongodb_connection is None:
        _mongodb_connection = MongoDBConnection()
    return _mongodb_connection

def connect_mongodb() -> bool:
    """
    Connect to MongoDB using the global connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    connection = get_mongodb_connection()
    return connection.connect()

def disconnect_mongodb():
    """Disconnect from MongoDB"""
    global _mongodb_connection
    if _mongodb_connection:
        _mongodb_connection.disconnect()
        _mongodb_connection = None

if __name__ == '__main__':
    # Test connection
    if connect_mongodb():
        print('MongoDB connection successful')
        connection = get_mongodb_connection()
        connection.create_indexes()
        disconnect_mongodb()
    else:
        print('MongoDB connection failed')


