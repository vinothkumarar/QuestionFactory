"""
Question Factory OS v2.0
Knowledge Database Schema
"""

import sqlite3
from pathlib import Path


class KnowledgeSchema:

    def __init__(self):

        self.database = Path(__file__).parent / "knowledge.db"

    def create(self):

        connection = sqlite3.connect(self.database)

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code TEXT UNIQUE,

            name TEXT,

            enabled INTEGER DEFAULT 1

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS units(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            subject_id INTEGER,

            code TEXT,

            name TEXT,

            enabled INTEGER DEFAULT 1
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chapters(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            unit_id INTEGER,

            code TEXT,

            name TEXT,

            enabled INTEGER DEFAULT 1
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subtopics(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            chapter_id INTEGER,

            code TEXT,

            name TEXT,

            enabled INTEGER DEFAULT 1
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sets(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code TEXT,

            difficulty TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            subject_code TEXT,

            unit_code TEXT,

            chapter_code TEXT,

            subtopic_code TEXT,

            set_code TEXT,

            batch_no INTEGER,

            next_question INTEGER,

            status TEXT
        )
        """)

        connection.commit()

        connection.close()

        print()

        print("=" * 80)
        print("KNOWLEDGE DATABASE CREATED")
        print("=" * 80)
