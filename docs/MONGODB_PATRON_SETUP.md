# MongoDB Patron System Setup Guide

This guide explains how to set up and use the MongoDB-based patron management system for the gRPC Library project.

## Overview

The patron system provides comprehensive management of library patrons using MongoDB as the backend database. It includes:

- **Patron Model**: Complete patron information with membership tracking
- **Repository Pattern**: Clean separation of data access logic
- **MongoDB Integration**: Robust connection management and indexing
- **gRPC Services**: Full CRUD operations via gRPC

## Prerequisites

1. **MongoDB Installation**
   - Install MongoDB Community Server
   - Ensure MongoDB is running on `localhost:27017` (default)
   - Or set up MongoDB Atlas for cloud deployment

2. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

Set the following environment variable for MongoDB connection:

```bash
# For local MongoDB
export MONGODB_URI="mongodb://localhost:27017/"

# For MongoDB Atlas (cloud)
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
```

### Database Configuration

The system uses the following default settings:
- **Database Name**: `library_db`
- **Collection Name**: `patrons`
- **Connection Timeout**: 5 seconds
- **Socket Timeout**: 20 seconds

## Patron Model Structure

```python
@dataclass
class Patron:
    id: Optional[str]                    # MongoDB ObjectId
    first_name: str                      # Patron's first name
    last_name: str                      # Patron's last name
    email: str                          # Unique email address
    phone: Optional[str]                # Phone number
    address: Optional[str]              # Physical address
    membership_type: str                # student, faculty, community, premium
    membership_start_date: datetime     # When membership began
    membership_end_date: Optional[datetime]  # When membership expires
    books_checked_out: List[str]       # List of checked out book IDs
    total_books_borrowed: int           # Lifetime book count
    active: bool                       # Membership status
    created_at: datetime              # Record creation timestamp
    updated_at: datetime              # Last update timestamp
```

## Membership Types

- **student**: University students with limited borrowing privileges
- **faculty**: University faculty with extended privileges
- **community**: Local community members
- **premium**: Premium members with enhanced benefits

## Usage Examples

### Basic Operations

```python
from models.patron import Patron
from repository.patron_repository import PatronRepository
from repository.mongodb_database import connect_mongodb

# Connect to MongoDB
connect_mongodb()

# Initialize repository
patron_repo = PatronRepository()

# Create a new patron
patron = Patron(
    id=None,
    first_name="John",
    last_name="Doe",
    email="john.doe@university.edu",
    membership_type="student",
    membership_start_date=datetime.now(),
    books_checked_out=[],
    total_books_borrowed=0,
    active=True,
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Create patron
patron_id = patron_repo.create_patron(patron)

# Retrieve patron
retrieved_patron = patron_repo.get_patron_by_id(patron_id)

# Search patrons
search_results = patron_repo.search_patrons_by_name("John")

# List patrons with pagination
all_patrons = patron_repo.list_patrons(limit=50, offset=0, active_only=True)
```

### Book Checkout Operations

```python
# Checkout a book
success = patron_repo.checkout_book(patron_id, "book-123")

# Return a book
success = patron_repo.return_book(patron_id, "book-123")
```

## Database Indexes

The system automatically creates the following indexes for optimal performance:

- **Email**: Unique index for fast email lookups
- **Membership Type**: Index for filtering by membership type
- **Active Status**: Index for filtering active/inactive patrons
- **Name**: Compound index on first_name and last_name for name searches

## gRPC Services

The following gRPC services are available for patron management:

### Patron CRUD Operations
- `CreatePatron`: Create a new patron
- `UpdatePatron`: Update existing patron information
- `GetPatron`: Retrieve patron by ID or email
- `DeletePatron`: Remove a patron
- `ListPatrons`: List patrons with pagination
- `SearchPatrons`: Search patrons by name

### Membership Management
- `UpdatePatronMembership`: Update membership type and expiration

## Error Handling

The system includes comprehensive error handling:

- **Duplicate Email**: Prevents creation of patrons with existing emails
- **Connection Issues**: Graceful handling of MongoDB connection problems
- **Validation Errors**: Input validation for required fields
- **Not Found**: Proper handling when patrons don't exist

## Running the Example

Execute the example script to see the system in action:

```bash
python examples/patron_example.py
```

This will:
1. Connect to MongoDB
2. Create sample patrons (student, faculty, community)
3. Demonstrate various operations (search, list, checkout/return)
4. Clean up connections

## Testing

Run the connection test:

```bash
python repository/mongodb_database.py
```

This will verify MongoDB connectivity and create necessary indexes.

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Ensure MongoDB is running
   - Check connection string format
   - Verify network connectivity

2. **Duplicate Key Error**
   - Email addresses must be unique
   - Check for existing patrons with same email

3. **Index Creation Failed**
   - Ensure proper MongoDB permissions
   - Check for existing conflicting indexes

### Logs

The system provides detailed logging for:
- Connection status
- Database operations
- Error conditions
- Index creation

## Security Considerations

- Use environment variables for sensitive connection strings
- Implement proper authentication for production MongoDB instances
- Consider using MongoDB's built-in security features
- Regularly update dependencies for security patches

## Performance Optimization

- Indexes are automatically created for common query patterns
- Connection pooling is handled by PyMongo
- Pagination is supported for large result sets
- Consider MongoDB sharding for very large datasets


