import psycopg2

conn = psycopg2.connect(
    dbname="ragdb",
    user="postgres",
    password="password",
    host="localhost"
)

cur = conn.cursor()

docs = [
    ("Monitoring SOP", "Monitoring visit process includes planning, execution and reporting."),
    ("Clinical Study Guide", "Clinical trial monitoring ensures compliance."),
]

for title, content in docs:
    cur.execute(
        "INSERT INTO documents (title, content) VALUES (%s, %s)",
        (title, content)
    )

conn.commit()
cur.close()
conn.close()