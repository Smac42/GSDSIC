"""
FAQ Database Module

A searchable FAQ database implementation using SQLite with full-text search,
tag filtering, and CRUD operations.
"""

import sqlite3
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import re


class FAQDatabase:
    """
    A searchable FAQ database with support for full-text search,
    tag filtering, and various export formats.
    """
    
    def __init__(self, db_path: str = "faq_database.db"):
        """
        Initialize the FAQ database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create the necessary database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Create FAQ entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faq_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                faq_id INTEGER NOT NULL,
                tag TEXT NOT NULL,
                FOREIGN KEY (faq_id) REFERENCES faq_entries(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better search performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tags_faq_id ON tags(faq_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category ON faq_entries(category)
        """)
        
        self.conn.commit()
    
    def create_entry(self, question: str, answer: str, tags: List[str] = None,
                    category: str = None) -> int:
        """
        Create a new FAQ entry.
        
        Args:
            question: The FAQ question text
            answer: The FAQ answer text
            tags: List of tags/keywords for the entry
            category: Optional category for the entry
        
        Returns:
            The ID of the newly created entry
        """
        cursor = self.conn.cursor()
        
        # Insert the FAQ entry
        cursor.execute("""
            INSERT INTO faq_entries (question, answer, category)
            VALUES (?, ?, ?)
        """, (question, answer, category))
        
        faq_id = cursor.lastrowid
        
        # Insert tags if provided
        if tags:
            for tag in tags:
                cursor.execute("""
                    INSERT INTO tags (faq_id, tag)
                    VALUES (?, ?)
                """, (faq_id, tag.lower()))
        
        self.conn.commit()
        return faq_id
    
    def read_entry(self, entry_id: int) -> Optional[Dict]:
        """
        Read a single FAQ entry by ID.
        
        Args:
            entry_id: The ID of the entry to read
        
        Returns:
            Dictionary containing the entry data, or None if not found
        """
        cursor = self.conn.cursor()
        
        # Get the FAQ entry
        cursor.execute("""
            SELECT * FROM faq_entries WHERE id = ?
        """, (entry_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Get tags for this entry
        cursor.execute("""
            SELECT tag FROM tags WHERE faq_id = ?
        """, (entry_id,))
        
        tags = [tag_row['tag'] for tag_row in cursor.fetchall()]
        
        return {
            'id': row['id'],
            'question': row['question'],
            'answer': row['answer'],
            'category': row['category'],
            'tags': tags,
            'date_added': row['date_added'],
            'date_modified': row['date_modified']
        }
    
    def update_entry(self, entry_id: int, question: str = None, answer: str = None,
                    tags: List[str] = None, category: str = None) -> bool:
        """
        Update an existing FAQ entry.
        
        Args:
            entry_id: The ID of the entry to update
            question: New question text (optional)
            answer: New answer text (optional)
            tags: New list of tags (optional, replaces existing tags)
            category: New category (optional)
        
        Returns:
            True if successful, False if entry not found
        """
        cursor = self.conn.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM faq_entries WHERE id = ?", (entry_id,))
        if not cursor.fetchone():
            return False
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        if question is not None:
            update_fields.append("question = ?")
            params.append(question)
        
        if answer is not None:
            update_fields.append("answer = ?")
            params.append(answer)
        
        if category is not None:
            update_fields.append("category = ?")
            params.append(category)
        
        if update_fields:
            update_fields.append("date_modified = CURRENT_TIMESTAMP")
            params.append(entry_id)
            
            query = f"UPDATE faq_entries SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
        
        # Update tags if provided
        if tags is not None:
            # Delete existing tags
            cursor.execute("DELETE FROM tags WHERE faq_id = ?", (entry_id,))
            
            # Insert new tags
            for tag in tags:
                cursor.execute("""
                    INSERT INTO tags (faq_id, tag)
                    VALUES (?, ?)
                """, (entry_id, tag.lower()))
        
        self.conn.commit()
        return True
    
    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete an FAQ entry.
        
        Args:
            entry_id: The ID of the entry to delete
        
        Returns:
            True if successful, False if entry not found
        """
        cursor = self.conn.cursor()
        
        # Check if entry exists
        cursor.execute("SELECT id FROM faq_entries WHERE id = ?", (entry_id,))
        if not cursor.fetchone():
            return False
        
        # Delete tags (cascades in schema, but explicit for clarity)
        cursor.execute("DELETE FROM tags WHERE faq_id = ?", (entry_id,))
        
        # Delete the entry
        cursor.execute("DELETE FROM faq_entries WHERE id = ?", (entry_id,))
        
        self.conn.commit()
        return True
    
    def search_text(self, query: str, case_sensitive: bool = False) -> List[Dict]:
        """
        Search for FAQ entries by text in questions and answers.
        
        Args:
            query: The search query
            case_sensitive: Whether to perform case-sensitive search
        
        Returns:
            List of matching FAQ entries with relevance scores
        """
        cursor = self.conn.cursor()
        
        # Prepare search pattern
        if case_sensitive:
            pattern = f"%{query}%"
            like_op = "LIKE"
        else:
            pattern = f"%{query.lower()}%"
            like_op = "LIKE"
            query_lower = query.lower()
        
        # Search in questions and answers
        if case_sensitive:
            cursor.execute(f"""
                SELECT DISTINCT e.*, 
                       CASE 
                           WHEN e.question {like_op} ? THEN 2
                           WHEN e.answer {like_op} ? THEN 1
                           ELSE 0
                       END as relevance
                FROM faq_entries e
                WHERE e.question {like_op} ? OR e.answer {like_op} ?
                ORDER BY relevance DESC, e.date_modified DESC
            """, (pattern, pattern, pattern, pattern))
        else:
            cursor.execute(f"""
                SELECT DISTINCT e.*, 
                       CASE 
                           WHEN LOWER(e.question) {like_op} ? THEN 2
                           WHEN LOWER(e.answer) {like_op} ? THEN 1
                           ELSE 0
                       END as relevance
                FROM faq_entries e
                WHERE LOWER(e.question) {like_op} ? OR LOWER(e.answer) {like_op} ?
                ORDER BY relevance DESC, e.date_modified DESC
            """, (pattern, pattern, pattern, pattern))
        
        results = []
        for row in cursor.fetchall():
            entry = self.read_entry(row['id'])
            entry['relevance'] = row['relevance']
            results.append(entry)
        
        return results
    
    def search_by_tags(self, tags: List[str], match_all: bool = False) -> List[Dict]:
        """
        Search for FAQ entries by tags.
        
        Args:
            tags: List of tags to search for
            match_all: If True, entry must have all tags. If False, any tag matches.
        
        Returns:
            List of matching FAQ entries
        """
        if not tags:
            return []
        
        cursor = self.conn.cursor()
        
        # Convert tags to lowercase for case-insensitive matching
        tags_lower = [tag.lower() for tag in tags]
        
        if match_all:
            # Entry must have all tags
            placeholders = ','.join(['?' for _ in tags_lower])
            cursor.execute(f"""
                SELECT e.*, COUNT(DISTINCT t.tag) as tag_count
                FROM faq_entries e
                JOIN tags t ON e.id = t.faq_id
                WHERE t.tag IN ({placeholders})
                GROUP BY e.id
                HAVING tag_count = ?
                ORDER BY e.date_modified DESC
            """, tags_lower + [len(tags_lower)])
        else:
            # Entry must have at least one tag
            placeholders = ','.join(['?' for _ in tags_lower])
            cursor.execute(f"""
                SELECT DISTINCT e.*
                FROM faq_entries e
                JOIN tags t ON e.id = t.faq_id
                WHERE t.tag IN ({placeholders})
                ORDER BY e.date_modified DESC
            """, tags_lower)
        
        results = []
        for row in cursor.fetchall():
            entry = self.read_entry(row['id'])
            results.append(entry)
        
        return results
    
    def search_by_category(self, category: str) -> List[Dict]:
        """
        Search for FAQ entries by category.
        
        Args:
            category: The category to search for
        
        Returns:
            List of matching FAQ entries
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM faq_entries
            WHERE category = ?
            ORDER BY date_modified DESC
        """, (category,))
        
        results = []
        for row in cursor.fetchall():
            entry = self.read_entry(row['id'])
            results.append(entry)
        
        return results
    
    def search_combined(self, text_query: str = None, tags: List[str] = None,
                       category: str = None, case_sensitive: bool = False) -> List[Dict]:
        """
        Perform a combined search with multiple criteria.
        
        Args:
            text_query: Text to search in questions and answers
            tags: Tags to filter by
            category: Category to filter by
            case_sensitive: Whether text search is case-sensitive
        
        Returns:
            List of matching FAQ entries
        """
        cursor = self.conn.cursor()
        
        # Build query dynamically based on provided criteria
        conditions = []
        params = []
        
        # Text search condition
        if text_query:
            if case_sensitive:
                conditions.append("(e.question LIKE ? OR e.answer LIKE ?)")
                pattern = f"%{text_query}%"
            else:
                conditions.append("(LOWER(e.question) LIKE ? OR LOWER(e.answer) LIKE ?)")
                pattern = f"%{text_query.lower()}%"
            params.extend([pattern, pattern])
        
        # Category condition
        if category:
            conditions.append("e.category = ?")
            params.append(category)
        
        # Build base query
        if tags:
            tags_lower = [tag.lower() for tag in tags]
            placeholders = ','.join(['?' for _ in tags_lower])
            
            base_query = f"""
                SELECT DISTINCT e.*
                FROM faq_entries e
                JOIN tags t ON e.id = t.faq_id
                WHERE t.tag IN ({placeholders})
            """
            params = tags_lower + params
            
            if conditions:
                base_query += " AND " + " AND ".join(conditions)
        else:
            if conditions:
                base_query = f"""
                    SELECT DISTINCT e.*
                    FROM faq_entries e
                    WHERE {" AND ".join(conditions)}
                """
            else:
                # No criteria, return all
                base_query = "SELECT * FROM faq_entries e"
        
        base_query += " ORDER BY e.date_modified DESC"
        
        cursor.execute(base_query, params)
        
        results = []
        for row in cursor.fetchall():
            entry = self.read_entry(row['id'])
            results.append(entry)
        
        return results
    
    def get_all_entries(self) -> List[Dict]:
        """
        Get all FAQ entries.
        
        Returns:
            List of all FAQ entries
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM faq_entries ORDER BY date_modified DESC")
        
        results = []
        for row in cursor.fetchall():
            entry = self.read_entry(row['id'])
            results.append(entry)
        
        return results
    
    def get_all_tags(self) -> List[str]:
        """
        Get all unique tags in the database.
        
        Returns:
            List of unique tags
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT tag FROM tags ORDER BY tag")
        return [row['tag'] for row in cursor.fetchall()]
    
    def get_all_categories(self) -> List[str]:
        """
        Get all unique categories in the database.
        
        Returns:
            List of unique categories
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category FROM faq_entries 
            WHERE category IS NOT NULL 
            ORDER BY category
        """)
        return [row['category'] for row in cursor.fetchall()]
    
    def export_to_json(self, filepath: str):
        """
        Export all FAQ entries to a JSON file.
        
        Args:
            filepath: Path to the output JSON file
        """
        entries = self.get_all_entries()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, filepath: str):
        """
        Export all FAQ entries to a CSV file.
        
        Args:
            filepath: Path to the output CSV file
        """
        entries = self.get_all_entries()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if entries:
                fieldnames = ['id', 'question', 'answer', 'category', 'tags', 
                            'date_added', 'date_modified']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for entry in entries:
                    # Convert tags list to comma-separated string
                    entry_copy = entry.copy()
                    entry_copy['tags'] = ', '.join(entry['tags']) if entry['tags'] else ''
                    writer.writerow(entry_copy)
    
    def import_from_json(self, filepath: str):
        """
        Import FAQ entries from a JSON file.
        
        Args:
            filepath: Path to the input JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        for entry in entries:
            # Skip if entry has an ID (from export), create new entry instead
            self.create_entry(
                question=entry['question'],
                answer=entry['answer'],
                tags=entry.get('tags', []),
                category=entry.get('category')
            )
        
        self.conn.commit()
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
