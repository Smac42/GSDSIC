# FAQ Database Template

A powerful, searchable FAQ database template built with Python that can be used as a foundation for an FAQ page. This solution provides full-text search, tag filtering, CRUD operations, and multiple export formats.

## Features

✅ **SQLite-based storage** - Portable, serverless database  
✅ **Full-text search** - Search across questions and answers  
✅ **Tag/keyword filtering** - Organize and filter by tags  
✅ **Category support** - Group FAQs by categories  
✅ **CRUD operations** - Complete Create, Read, Update, Delete functionality  
✅ **Case-insensitive search** - Find entries regardless of case  
✅ **Relevance scoring** - Search results ranked by relevance  
✅ **Export/Import** - JSON and CSV export formats  
✅ **CLI interface** - Command-line tool for easy management  
✅ **Well-documented API** - Clean, easy-to-use Python API  

## Quick Start

### 1. Installation

No external dependencies required! This project uses Python's standard library.

```bash
# Clone the repository
git clone https://github.com/Smac42/GSDSIC.git
cd GSDSIC

# Make scripts executable (optional)
chmod +x faq_cli.py example_usage.py
```

Requirements:
- Python 3.6 or higher
- No external packages needed (uses only standard library)

### 2. Run Example Script

The easiest way to get started is to run the example usage script:

```bash
python3 example_usage.py
```

This will create example databases and demonstrate all key features.

### 3. Import Sample Data

Load the sample FAQ data into a new database:

```bash
python3 faq_cli.py import sample_faq_data.json
```

### 4. Try Searching

Search the FAQ database:

```bash
# Text search
python3 faq_cli.py search "password"

# Tag search
python3 faq_cli.py search-tags "security,account"

# List all entries
python3 faq_cli.py list
```

## Usage Guide

### Python API

#### Basic Usage

```python
from faq_database import FAQDatabase

# Create or open a database
db = FAQDatabase("my_faq.db")

# Create an entry
entry_id = db.create_entry(
    question="How do I reset my password?",
    answer="Click 'Forgot Password' on the login page...",
    tags=["password", "account", "login"],
    category="Account Management"
)

# Search by text
results = db.search_text("password")
for entry in results:
    print(f"Q: {entry['question']}")
    print(f"A: {entry['answer']}")

# Close the database
db.close()
```

#### Using Context Manager (Recommended)

```python
from faq_database import FAQDatabase

with FAQDatabase("my_faq.db") as db:
    # Your database operations here
    results = db.search_text("payment")
    # Database automatically closes when exiting the context
```

### API Reference

#### Creating Entries

```python
# Create a new FAQ entry
entry_id = db.create_entry(
    question="Your question here",
    answer="Your answer here",
    tags=["tag1", "tag2"],  # Optional
    category="Category Name"  # Optional
)
```

#### Reading Entries

```python
# Get a single entry by ID
entry = db.read_entry(entry_id)
# Returns: {
#     'id': 1,
#     'question': '...',
#     'answer': '...',
#     'category': '...',
#     'tags': ['tag1', 'tag2'],
#     'date_added': '...',
#     'date_modified': '...'
# }

# Get all entries
all_entries = db.get_all_entries()
```

#### Updating Entries

```python
# Update specific fields (others remain unchanged)
db.update_entry(
    entry_id=1,
    answer="Updated answer text",  # Optional
    tags=["new", "tags"],  # Optional, replaces all tags
    category="New Category"  # Optional
)
```

#### Deleting Entries

```python
# Delete an entry by ID
success = db.delete_entry(entry_id)
```

#### Searching

##### Text Search

```python
# Case-insensitive search (default)
results = db.search_text("payment")

# Case-sensitive search
results = db.search_text("Python", case_sensitive=True)

# Results include relevance scores
for entry in results:
    print(f"Relevance: {entry['relevance']}")  # 2 = question match, 1 = answer match
```

##### Tag Search

```python
# Search for entries with ANY of the specified tags
results = db.search_by_tags(["billing", "payment"], match_all=False)

# Search for entries with ALL of the specified tags
results = db.search_by_tags(["security", "account"], match_all=True)
```

##### Category Search

```python
# Search by category
results = db.search_by_category("Technical Support")
```

##### Combined Search

```python
# Search with multiple criteria
results = db.search_combined(
    text_query="password",
    tags=["security"],
    category="Account Management"
)
```

#### Listing Tags and Categories

```python
# Get all unique tags
tags = db.get_all_tags()

# Get all unique categories
categories = db.get_all_categories()
```

#### Import/Export

```python
# Export to JSON
db.export_to_json("backup.json")

# Export to CSV
db.export_to_csv("backup.csv")

# Import from JSON
db.import_from_json("data.json")
```

### Command-Line Interface

The CLI provides easy access to all database functions.

#### Basic Commands

```bash
# Create a new entry
python3 faq_cli.py create \
    "How do I contact support?" \
    "Email us at support@example.com" \
    --tags "support,contact,help" \
    --category "Support"

# Read an entry
python3 faq_cli.py read 1

# Update an entry
python3 faq_cli.py update 1 \
    --answer "New answer text" \
    --tags "updated,tags"

# Delete an entry
python3 faq_cli.py delete 1
python3 faq_cli.py delete 1 --force  # Skip confirmation
```

#### Search Commands

```bash
# Text search
python3 faq_cli.py search "password"
python3 faq_cli.py search "password" --verbose  # Show full details
python3 faq_cli.py search "Python" --case-sensitive

# Tag search
python3 faq_cli.py search-tags "security,account"
python3 faq_cli.py search-tags "security,account" --match-all

# Category search
python3 faq_cli.py search-category "Billing"
```

#### List Commands

```bash
# List all entries
python3 faq_cli.py list
python3 faq_cli.py list --verbose

# List all tags
python3 faq_cli.py list-tags

# List all categories
python3 faq_cli.py list-categories
```

#### Import/Export Commands

```bash
# Export to JSON (default)
python3 faq_cli.py export backup.json

# Export to CSV
python3 faq_cli.py export backup.csv --format csv

# Import from JSON
python3 faq_cli.py import sample_faq_data.json
```

#### Using Different Database Files

```bash
# Specify a custom database file
python3 faq_cli.py --db custom.db list
python3 faq_cli.py --db custom.db search "query"
```

## File Structure

```
GSDSIC/
├── faq_database.py          # Core FAQ database module
├── faq_cli.py               # Command-line interface
├── example_usage.py         # Example usage demonstrations
├── sample_faq_data.json     # Sample FAQ entries
└── README.md                # This file
```

## Database Schema

The database uses two tables:

### faq_entries Table
- `id` - Primary key (auto-increment)
- `question` - Question text (TEXT, NOT NULL)
- `answer` - Answer text (TEXT, NOT NULL)
- `category` - Optional category (TEXT)
- `date_added` - Creation timestamp (TIMESTAMP)
- `date_modified` - Last modification timestamp (TIMESTAMP)

### tags Table
- `id` - Primary key (auto-increment)
- `faq_id` - Foreign key to faq_entries (INTEGER, NOT NULL)
- `tag` - Tag text (TEXT, NOT NULL, lowercase)

Indexes are created on `faq_id`, `tag`, and `category` for optimal search performance.

## Integration Examples

### Web Application Integration

```python
from flask import Flask, request, jsonify
from faq_database import FAQDatabase

app = Flask(__name__)

@app.route('/api/faq/search')
def search_faq():
    query = request.args.get('q', '')
    tags = request.args.getlist('tag')
    
    with FAQDatabase() as db:
        if tags:
            results = db.search_combined(text_query=query, tags=tags)
        else:
            results = db.search_text(query)
    
    return jsonify(results)

@app.route('/api/faq/<int:faq_id>')
def get_faq(faq_id):
    with FAQDatabase() as db:
        entry = db.read_entry(faq_id)
    
    if entry:
        return jsonify(entry)
    else:
        return jsonify({'error': 'Not found'}), 404
```

### Static Site Generation

```python
from faq_database import FAQDatabase
import json

# Export FAQ data for static site
with FAQDatabase() as db:
    categories = db.get_all_categories()
    
    faq_data = {}
    for category in categories:
        faq_data[category] = db.search_by_category(category)
    
    # Save for static site
    with open('faq_data.json', 'w') as f:
        json.dump(faq_data, f, indent=2)
```

## Advanced Features

### Custom Relevance Scoring

The `search_text()` method returns results with relevance scores:
- **2** - Match found in question (higher priority)
- **1** - Match found in answer
- **0** - No match (shouldn't appear in results)

Results are automatically sorted by relevance and then by modification date.

### Partial Matching

All text searches support partial matching:
```python
db.search_text("pass")  # Matches "password", "passphrase", "bypass", etc.
```

### Tag Case Normalization

Tags are automatically converted to lowercase for consistent searching:
```python
db.create_entry(..., tags=["Security", "ACCOUNT"])
# Stored as: ["security", "account"]

db.search_by_tags(["SECURITY"])  # Will find the entry
```

## Performance Considerations

- **Indexes** - Indexes on tags, categories, and foreign keys ensure fast searches
- **Connection Pooling** - For web applications, consider using connection pooling
- **Batch Operations** - For bulk imports, use transactions for better performance
- **Database Size** - SQLite handles databases up to 281 TB, suitable for most FAQ use cases

## Extending the Database

### Adding Custom Fields

```python
# Modify _create_tables() in faq_database.py
cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT,
        author TEXT,  -- New field
        view_count INTEGER DEFAULT 0,  -- New field
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
```

### Adding Full-Text Search (FTS5)

For more advanced full-text search capabilities, you can integrate SQLite's FTS5:

```python
# Add to _create_tables()
cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS faq_fts 
    USING fts5(question, answer, content='faq_entries', content_rowid='id')
""")
```

## Troubleshooting

### Database Locked Error
If you get "database is locked" errors in a multi-threaded environment:
```python
# Use connection with timeout
db = FAQDatabase("faq.db")
db.conn.execute("PRAGMA busy_timeout = 5000")  # 5 second timeout
```

### Import Errors
Ensure the JSON file is properly formatted:
```bash
python3 -m json.tool sample_faq_data.json
```

## License

This is a template project. Feel free to use and modify for your needs.

## Contributing

Contributions are welcome! Areas for improvement:
- Additional export formats
- Full-text search with FTS5
- RESTful API wrapper
- Web UI interface
- Multilingual support
- Fuzzy search capabilities

## Support

For issues or questions:
1. Check the example usage: `python3 example_usage.py`
2. Review this README
3. Open an issue on GitHub
