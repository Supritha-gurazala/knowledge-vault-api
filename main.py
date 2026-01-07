from fastapi import FastAPI
from datetime import datetime
from database import init_db, get_connection
from models import Item, ItemCreate
from fastapi import HTTPException

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO items (title, content, type, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            item.title,
            item.content,
            item.type,
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()

    new_id = cursor.lastrowid
    row = conn.execute(
        "SELECT * FROM items WHERE id = ?",
        (new_id,)
    ).fetchone()

    conn.close()
    return dict(row)

@app.get("/items", response_model=list[Item])
def list_items():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM items ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]




@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM items WHERE id = ?",
        (item_id,)
    ).fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return dict(row)

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    cursor = conn.execute(
        "DELETE FROM items WHERE id = ?",
        (item_id,)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"deleted": item_id}

