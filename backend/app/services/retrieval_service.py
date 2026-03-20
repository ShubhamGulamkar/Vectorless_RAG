from sqlalchemy import text

def search_documents(db, query: str):
    sql = text("""
        SELECT id, title, content
        FROM documents
        WHERE to_tsvector('english', content)
        @@ plainto_tsquery('english', :query)
        LIMIT 5
    """)

    results = db.execute(sql, {"query": query}).fetchall()
    return results