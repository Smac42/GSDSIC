#!/usr/bin/env python3
"""
FAQ Database CLI

A command-line interface for interacting with the FAQ database.
Provides commands for CRUD operations, searching, and data management.
"""

import argparse
import sys
from faq_database import FAQDatabase


def create_entry(db, args):
    """Create a new FAQ entry."""
    tags = args.tags.split(',') if args.tags else []
    tags = [tag.strip() for tag in tags]
    
    entry_id = db.create_entry(
        question=args.question,
        answer=args.answer,
        tags=tags,
        category=args.category
    )
    print(f"✓ Created entry with ID: {entry_id}")


def read_entry(db, args):
    """Read and display an FAQ entry."""
    entry = db.read_entry(args.id)
    if entry:
        print(f"\nID: {entry['id']}")
        print(f"Question: {entry['question']}")
        print(f"Answer: {entry['answer']}")
        print(f"Category: {entry['category']}")
        print(f"Tags: {', '.join(entry['tags'])}")
        print(f"Added: {entry['date_added']}")
        print(f"Modified: {entry['date_modified']}")
    else:
        print(f"❌ Entry with ID {args.id} not found")


def update_entry(db, args):
    """Update an existing FAQ entry."""
    tags = args.tags.split(',') if args.tags else None
    if tags:
        tags = [tag.strip() for tag in tags]
    
    success = db.update_entry(
        entry_id=args.id,
        question=args.question,
        answer=args.answer,
        tags=tags,
        category=args.category
    )
    
    if success:
        print(f"✓ Updated entry ID {args.id}")
    else:
        print(f"❌ Entry with ID {args.id} not found")


def delete_entry(db, args):
    """Delete an FAQ entry."""
    if not args.force:
        # Confirm deletion
        entry = db.read_entry(args.id)
        if not entry:
            print(f"❌ Entry with ID {args.id} not found")
            return
        
        print(f"\nAre you sure you want to delete this entry?")
        print(f"Question: {entry['question'][:60]}...")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Deletion cancelled")
            return
    
    success = db.delete_entry(args.id)
    if success:
        print(f"✓ Deleted entry ID {args.id}")
    else:
        print(f"❌ Entry with ID {args.id} not found")


def search_text(db, args):
    """Search FAQ entries by text."""
    results = db.search_text(args.query, case_sensitive=args.case_sensitive)
    
    print(f"\nFound {len(results)} result(s) for '{args.query}':")
    print("="*60)
    
    for i, entry in enumerate(results, 1):
        print(f"\n[{i}] ID: {entry['id']} (Relevance: {entry['relevance']})")
        print(f"Question: {entry['question']}")
        if args.verbose:
            print(f"Answer: {entry['answer']}")
            print(f"Category: {entry['category']}")
            print(f"Tags: {', '.join(entry['tags'])}")
        else:
            answer_preview = entry['answer'][:100] + "..." if len(entry['answer']) > 100 else entry['answer']
            print(f"Answer: {answer_preview}")


def search_tags(db, args):
    """Search FAQ entries by tags."""
    tags = args.tags.split(',')
    tags = [tag.strip() for tag in tags]
    
    results = db.search_by_tags(tags, match_all=args.match_all)
    
    match_type = "all" if args.match_all else "any"
    print(f"\nFound {len(results)} result(s) matching {match_type} of tags: {', '.join(tags)}")
    print("="*60)
    
    for i, entry in enumerate(results, 1):
        print(f"\n[{i}] ID: {entry['id']}")
        print(f"Question: {entry['question']}")
        print(f"Tags: {', '.join(entry['tags'])}")
        if args.verbose:
            print(f"Answer: {entry['answer']}")


def search_category(db, args):
    """Search FAQ entries by category."""
    results = db.search_by_category(args.category)
    
    print(f"\nFound {len(results)} result(s) in category '{args.category}':")
    print("="*60)
    
    for i, entry in enumerate(results, 1):
        print(f"\n[{i}] ID: {entry['id']}")
        print(f"Question: {entry['question']}")
        if args.verbose:
            print(f"Answer: {entry['answer']}")


def list_all(db, args):
    """List all FAQ entries."""
    entries = db.get_all_entries()
    
    print(f"\nTotal entries: {len(entries)}")
    print("="*60)
    
    for i, entry in enumerate(entries, 1):
        print(f"\n[{i}] ID: {entry['id']}")
        print(f"Question: {entry['question']}")
        print(f"Category: {entry['category']}")
        print(f"Tags: {', '.join(entry['tags'])}")
        if args.verbose:
            print(f"Answer: {entry['answer']}")


def list_tags(db, args):
    """List all tags."""
    tags = db.get_all_tags()
    print(f"\nTotal tags: {len(tags)}")
    print("="*60)
    for tag in tags:
        print(f"  • {tag}")


def list_categories(db, args):
    """List all categories."""
    categories = db.get_all_categories()
    print(f"\nTotal categories: {len(categories)}")
    print("="*60)
    for category in categories:
        print(f"  • {category}")


def export_data(db, args):
    """Export FAQ data to file."""
    if args.format == 'json':
        db.export_to_json(args.output)
    elif args.format == 'csv':
        db.export_to_csv(args.output)
    
    print(f"✓ Exported data to {args.output}")


def import_data(db, args):
    """Import FAQ data from JSON file."""
    db.import_from_json(args.input)
    entries = db.get_all_entries()
    print(f"✓ Imported data from {args.input}")
    print(f"Total entries in database: {len(entries)}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FAQ Database CLI - Manage and search FAQ entries",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--db',
        default='faq_database.db',
        help='Path to the SQLite database file (default: faq_database.db)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new FAQ entry')
    create_parser.add_argument('question', help='The question text')
    create_parser.add_argument('answer', help='The answer text')
    create_parser.add_argument('--tags', help='Comma-separated list of tags')
    create_parser.add_argument('--category', help='Category for the entry')
    
    # Read command
    read_parser = subparsers.add_parser('read', help='Read an FAQ entry by ID')
    read_parser.add_argument('id', type=int, help='Entry ID to read')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update an FAQ entry')
    update_parser.add_argument('id', type=int, help='Entry ID to update')
    update_parser.add_argument('--question', help='New question text')
    update_parser.add_argument('--answer', help='New answer text')
    update_parser.add_argument('--tags', help='New comma-separated list of tags')
    update_parser.add_argument('--category', help='New category')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an FAQ entry')
    delete_parser.add_argument('id', type=int, help='Entry ID to delete')
    delete_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    
    # Search text command
    search_parser = subparsers.add_parser('search', help='Search FAQ entries by text')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--case-sensitive', action='store_true', 
                              help='Perform case-sensitive search')
    search_parser.add_argument('--verbose', '-v', action='store_true',
                              help='Show full entry details')
    
    # Search tags command
    tags_parser = subparsers.add_parser('search-tags', help='Search FAQ entries by tags')
    tags_parser.add_argument('tags', help='Comma-separated list of tags')
    tags_parser.add_argument('--match-all', action='store_true',
                            help='Match all tags (AND) instead of any (OR)')
    tags_parser.add_argument('--verbose', '-v', action='store_true',
                            help='Show full entry details')
    
    # Search category command
    category_parser = subparsers.add_parser('search-category', 
                                           help='Search FAQ entries by category')
    category_parser.add_argument('category', help='Category to search')
    category_parser.add_argument('--verbose', '-v', action='store_true',
                                help='Show full entry details')
    
    # List all command
    list_parser = subparsers.add_parser('list', help='List all FAQ entries')
    list_parser.add_argument('--verbose', '-v', action='store_true',
                           help='Show full entry details')
    
    # List tags command
    subparsers.add_parser('list-tags', help='List all tags')
    
    # List categories command
    subparsers.add_parser('list-categories', help='List all categories')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export FAQ data')
    export_parser.add_argument('output', help='Output file path')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                              help='Export format (default: json)')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import FAQ data from JSON')
    import_parser.add_argument('input', help='Input JSON file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Command handlers
    commands = {
        'create': create_entry,
        'read': read_entry,
        'update': update_entry,
        'delete': delete_entry,
        'search': search_text,
        'search-tags': search_tags,
        'search-category': search_category,
        'list': list_all,
        'list-tags': list_tags,
        'list-categories': list_categories,
        'export': export_data,
        'import': import_data,
    }
    
    try:
        with FAQDatabase(args.db) as db:
            handler = commands.get(args.command)
            if handler:
                handler(db, args)
            else:
                print(f"Unknown command: {args.command}")
                parser.print_help()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
