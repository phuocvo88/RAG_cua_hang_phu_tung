"""
Database migration script to create knowledge_feedbacks table
"""
import sqlite3
import os

def create_feedback_table():
    """Create knowledge_feedbacks table in SQLite database"""
    db_path = './database/store.db'

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create knowledge_feedbacks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            corrected_knowledge TEXT NOT NULL,
            submitted_by TEXT DEFAULT 'Staff',
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
            reviewed_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reviewed_at TIMESTAMP,
            notes TEXT
        )
    ''')

    # Create indexes for better query performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_feedback_status
        ON knowledge_feedbacks(status)
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_feedback_created_at
        ON knowledge_feedbacks(created_at)
    ''')

    conn.commit()
    print("[OK] knowledge_feedbacks table created successfully")

    # Verify table creation
    cursor.execute('''
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='knowledge_feedbacks'
    ''')
    result = cursor.fetchone()

    if result:
        print("[OK] Table verification successful")

        # Show table schema
        cursor.execute('PRAGMA table_info(knowledge_feedbacks)')
        columns = cursor.fetchall()
        print("\nTable schema:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    else:
        print("[ERROR] Table verification failed")

    conn.close()

if __name__ == "__main__":
    create_feedback_table()
