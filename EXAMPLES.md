# FAQ Database - Usage Examples

This document shows real examples of using the FAQ Database Template.

## Example 1: Quick Start with CLI

```bash
# Import sample data
$ python3 faq_cli.py import sample_faq_data.json
✓ Imported data from sample_faq_data.json
Total entries in database: 15

# Search for entries about passwords
$ python3 faq_cli.py search "password"
Found 1 result(s) for 'password':
============================================================

[1] ID: 1 (Relevance: 2)
Question: How do I reset my password?
Answer: To reset your password, click on the 'Forgot Password' link...

# Search by tags
$ python3 faq_cli.py search-tags "security,account"
Found 4 result(s) matching any of tags: security, account
============================================================

[1] ID: 1
Question: How do I reset my password?
Tags: password, account, login, security

[2] ID: 3
Question: How can I cancel my subscription?
Tags: subscription, cancel, billing, account

[3] ID: 13
Question: How do I enable two-factor authentication?
Tags: 2fa, security, authentication, login, account

[4] ID: 4
Question: Is my data secure?
Tags: security, privacy, encryption, data protection
```

## Example 2: Python API Usage

```python
from faq_database import FAQDatabase

# Create or open database
with FAQDatabase("my_faq.db") as db:
    # Create a new entry
    entry_id = db.create_entry(
        question="How do I get started?",
        answer="Simply sign up and follow the tutorial!",
        tags=["getting started", "tutorial"],
        category="Getting Started"
    )
    print(f"Created entry {entry_id}")
    
    # Search by text
    results = db.search_text("tutorial")
    for entry in results:
        print(f"Q: {entry['question']}")
        print(f"A: {entry['answer']}")
    
    # Search by tags
    results = db.search_by_tags(["getting started"])
    print(f"Found {len(results)} entries")
    
    # Export data
    db.export_to_json("backup.json")
```

## Example 3: Advanced Search

```python
from faq_database import FAQDatabase

with FAQDatabase("faq.db") as db:
    # Combined search: text + tags + category
    results = db.search_combined(
        text_query="password",
        tags=["security"],
        category="Account Management"
    )
    
    # Results are automatically sorted by relevance
    for entry in results:
        print(f"ID: {entry['id']}")
        print(f"Question: {entry['question']}")
        print(f"Relevance: {entry.get('relevance', 'N/A')}")
```

## Example 4: CRUD Operations

```python
from faq_database import FAQDatabase

with FAQDatabase("faq.db") as db:
    # CREATE
    new_id = db.create_entry(
        question="What is Python?",
        answer="Python is a programming language.",
        tags=["python", "programming"],
        category="Technical"
    )
    
    # READ
    entry = db.read_entry(new_id)
    print(entry['question'])
    
    # UPDATE
    db.update_entry(
        new_id,
        answer="Python is a high-level programming language.",
        tags=["python", "programming", "language"]
    )
    
    # DELETE
    db.delete_entry(new_id)
```

## Example 5: List Operations

```python
from faq_database import FAQDatabase

with FAQDatabase("faq.db") as db:
    # Get all entries
    all_entries = db.get_all_entries()
    print(f"Total: {len(all_entries)} entries")
    
    # Get all tags
    tags = db.get_all_tags()
    print(f"Available tags: {', '.join(tags)}")
    
    # Get all categories
    categories = db.get_all_categories()
    print(f"Categories: {', '.join(categories)}")
```

## Example 6: Case-Insensitive Search

```python
from faq_database import FAQDatabase

with FAQDatabase("faq.db") as db:
    # Case-insensitive (default)
    results = db.search_text("PYTHON")  # Finds "python", "Python", etc.
    
    # Case-sensitive
    results = db.search_text("Python", case_sensitive=True)
```

## Example 7: Tag Matching Options

```python
from faq_database import FAQDatabase

with FAQDatabase("faq.db") as db:
    # Match ANY tag (OR logic)
    results = db.search_by_tags(
        ["security", "billing"],
        match_all=False
    )
    # Returns entries with "security" OR "billing"
    
    # Match ALL tags (AND logic)
    results = db.search_by_tags(
        ["security", "account"],
        match_all=True
    )
    # Returns only entries with BOTH "security" AND "account"
```

## Example 8: Export and Import

```python
from faq_database import FAQDatabase

# Export to JSON
with FAQDatabase("source.db") as db:
    db.export_to_json("faq_backup.json")
    db.export_to_csv("faq_backup.csv")

# Import from JSON (to a different database)
with FAQDatabase("destination.db") as db:
    db.import_from_json("faq_backup.json")
    print(f"Imported {len(db.get_all_entries())} entries")
```

## Example 9: Context Manager Usage

```python
from faq_database import FAQDatabase

# Recommended: Use context manager
with FAQDatabase("faq.db") as db:
    # Database operations here
    results = db.search_text("query")
    # Database automatically closes when exiting

# Alternative: Manual management
db = FAQDatabase("faq.db")
try:
    results = db.search_text("query")
finally:
    db.close()
```

## Example 10: Web Integration (Flask)

```python
from flask import Flask, request, jsonify
from faq_database import FAQDatabase

app = Flask(__name__)

@app.route('/api/faq/search')
def search():
    query = request.args.get('q', '')
    with FAQDatabase("faq.db") as db:
        results = db.search_text(query)
    return jsonify(results)

@app.route('/api/faq/<int:id>')
def get_faq(id):
    with FAQDatabase("faq.db") as db:
        entry = db.read_entry(id)
    return jsonify(entry) if entry else ('Not found', 404)

if __name__ == '__main__':
    app.run()
```
