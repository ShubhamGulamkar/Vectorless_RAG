from sqlalchemy import text
from app.core.database import engine
from app.models.document import Base


def create_tables():
    """
    Create database tables if they do not exist.
    """
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def create_index():
    """
    Create Full Text Search index for vectorless retrieval.
    """
    print("Creating search index...")

    query = """
    CREATE INDEX IF NOT EXISTS idx_documents_fts
    ON documents
    USING GIN (to_tsvector('english', content));
    """

    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()

    print("Index created successfully.")


def main():
    create_tables()
    create_index()
    print("Database initialized successfully.")


if __name__ == "__main__":
    main()