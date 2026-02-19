#!/usr/bin/env python3
"""
Example Usage Script for FAQ Database

This script demonstrates how to use the FAQ database module for common operations
including creating entries, searching, and exporting data.
"""

from faq_database import FAQDatabase


def print_separator(title=""):
    """Print a visual separator."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    else:
        print('-'*60)


def print_entry(entry):
    """Pretty print a single FAQ entry."""
    print(f"\nID: {entry['id']}")
    print(f"Question: {entry['question']}")
    print(f"Answer: {entry['answer'][:100]}..." if len(entry['answer']) > 100 else f"Answer: {entry['answer']}")
    print(f"Category: {entry['category']}")
    print(f"Tags: {', '.join(entry['tags'])}")
    print(f"Added: {entry['date_added']}")
    if 'relevance' in entry:
        print(f"Relevance: {entry['relevance']}")


def example_create_entries():
    """Example: Creating FAQ entries."""
    print_separator("Example 1: Creating FAQ Entries")
    
    with FAQDatabase("example_faq.db") as db:
        # Create a simple entry
        entry_id = db.create_entry(
            question="How do I get started?",
            answer="Getting started is easy! Simply sign up for an account and follow the onboarding tutorial.",
            tags=["getting started", "tutorial", "beginner"],
            category="Getting Started"
        )
        print(f"✓ Created entry with ID: {entry_id}")
        
        # Create another entry
        entry_id = db.create_entry(
            question="What programming languages are supported?",
            answer="We support Python, JavaScript, Java, C++, and many more languages.",
            tags=["programming", "languages", "development"],
            category="Technical"
        )
        print(f"✓ Created entry with ID: {entry_id}")


def example_read_and_update():
    """Example: Reading and updating entries."""
    print_separator("Example 2: Reading and Updating Entries")
    
    with FAQDatabase("example_faq.db") as db:
        # Read an entry
        entry = db.read_entry(1)
        if entry:
            print("\nOriginal entry:")
            print_entry(entry)
            
            # Update the entry
            db.update_entry(
                1,
                answer="Getting started is easy! Sign up, complete the tutorial, and explore the dashboard.",
                tags=["getting started", "tutorial", "beginner", "onboarding"]
            )
            
            # Read the updated entry
            updated_entry = db.read_entry(1)
            print("\n✓ Updated entry:")
            print_entry(updated_entry)


def example_text_search():
    """Example: Full-text search."""
    print_separator("Example 3: Text Search")
    
    with FAQDatabase("example_faq.db") as db:
        # Search for entries containing "programming"
        results = db.search_text("programming")
        
        print(f"\nFound {len(results)} entries matching 'programming':")
        for entry in results:
            print_entry(entry)
        
        # Case-insensitive search (default)
        results = db.search_text("PYTHON")
        print(f"\n\nCase-insensitive search for 'PYTHON': {len(results)} results")


def example_tag_search():
    """Example: Tag-based search."""
    print_separator("Example 4: Tag Search")
    
    with FAQDatabase("example_faq.db") as db:
        # Search by single tag
        results = db.search_by_tags(["tutorial"])
        print(f"\nEntries with 'tutorial' tag: {len(results)}")
        for entry in results:
            print_entry(entry)
        
        # Search by multiple tags (any match)
        results = db.search_by_tags(["programming", "beginner"], match_all=False)
        print(f"\n\nEntries with 'programming' OR 'beginner' tag: {len(results)}")
        
        # Search by multiple tags (all must match)
        results = db.search_by_tags(["getting started", "tutorial"], match_all=True)
        print(f"Entries with 'getting started' AND 'tutorial' tags: {len(results)}")


def example_category_search():
    """Example: Category-based search."""
    print_separator("Example 5: Category Search")
    
    with FAQDatabase("example_faq.db") as db:
        # Get all categories
        categories = db.get_all_categories()
        print(f"\nAvailable categories: {', '.join(categories)}")
        
        # Search by category
        if categories:
            results = db.search_by_category(categories[0])
            print(f"\nEntries in '{categories[0]}' category: {len(results)}")
            for entry in results:
                print_entry(entry)


def example_combined_search():
    """Example: Combined search with multiple criteria."""
    print_separator("Example 6: Combined Search")
    
    with FAQDatabase("example_faq.db") as db:
        # Search with text and tags
        results = db.search_combined(
            text_query="started",
            tags=["tutorial"]
        )
        print(f"\nEntries matching text 'started' AND tag 'tutorial': {len(results)}")
        for entry in results:
            print_entry(entry)
        
        # Search with all criteria
        results = db.search_combined(
            text_query="programming",
            tags=["development"],
            category="Technical"
        )
        print(f"\n\nComplex search results: {len(results)}")


def example_list_operations():
    """Example: Listing tags and categories."""
    print_separator("Example 7: Listing Tags and Categories")
    
    with FAQDatabase("example_faq.db") as db:
        # Get all tags
        tags = db.get_all_tags()
        print(f"\nAll tags ({len(tags)}):")
        print(", ".join(tags))
        
        # Get all categories
        categories = db.get_all_categories()
        print(f"\nAll categories ({len(categories)}):")
        print(", ".join(categories))
        
        # Get all entries
        all_entries = db.get_all_entries()
        print(f"\nTotal entries in database: {len(all_entries)}")


def example_export():
    """Example: Exporting data."""
    print_separator("Example 8: Exporting Data")
    
    with FAQDatabase("example_faq.db") as db:
        # Export to JSON
        db.export_to_json("faq_export.json")
        print("✓ Exported to faq_export.json")
        
        # Export to CSV
        db.export_to_csv("faq_export.csv")
        print("✓ Exported to faq_export.csv")


def example_import():
    """Example: Importing data from JSON."""
    print_separator("Example 9: Importing Data")
    
    # First, let's use the sample data
    with FAQDatabase("imported_faq.db") as db:
        # Import from sample data file
        db.import_from_json("sample_faq_data.json")
        
        entries = db.get_all_entries()
        print(f"✓ Imported {len(entries)} entries from sample_faq_data.json")
        
        # Show a few examples
        print("\nSample imported entries:")
        for entry in entries[:3]:
            print_entry(entry)


def example_delete():
    """Example: Deleting entries."""
    print_separator("Example 10: Deleting Entries")
    
    with FAQDatabase("example_faq.db") as db:
        # Get current count
        before_count = len(db.get_all_entries())
        print(f"Entries before deletion: {before_count}")
        
        # Delete an entry
        success = db.delete_entry(1)
        if success:
            print("✓ Deleted entry ID 1")
        
        # Get new count
        after_count = len(db.get_all_entries())
        print(f"Entries after deletion: {after_count}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "="*60)
    print("  FAQ Database - Example Usage Demonstrations")
    print("="*60)
    
    try:
        # Run examples in order
        example_create_entries()
        example_read_and_update()
        example_text_search()
        example_tag_search()
        example_category_search()
        example_combined_search()
        example_list_operations()
        example_export()
        example_import()
        example_delete()
        
        print("\n" + "="*60)
        print("  All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_examples()
