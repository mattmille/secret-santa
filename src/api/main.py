from fastapi import FastAPI, Depends, HTTPException

from database import engine,SessionLocal
from sqlalchemy.orm import Session

import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


# API endpoints
@app.post("/groups", response_model=modes.)
def create_group(group: models.GroupIn):
    # Generate a unique group code
    code = generate_code(6)
    
    # Insert group into the database
    # c.execute("INSERT INTO groups (name, code, is_public) VALUES (?, ?, ?)", (group.name, code, group.is_public))
    # conn.commit()
    
    # Retrieve the new group and return it
    group_id = c.lastrowid
    return models.GroupOut(id=group_id, name=group.name, code=code, is_public=group.is_public)

@app.get("/groups/{group_code}", response_model=models.GroupOut)
def get_group(group_code: str):
    c.execute("SELECT * FROM groups WHERE code = ?", (group_code,))
    group = c.fetchone()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return models.GroupOut(id=group[0], name=group[1], code=group[2], is_public=group[3])

@app.post("/groups/{group_id}/members", response_model=models.GroupOut)
def add_member(group_id: int, member: MemberIn):
    # Insert member into the database
    c.execute("INSERT INTO members (group_id, name, can_receive) VALUES (?, ?, ?)", 
              (member.group_id, member.name, member.can_receive))
    conn.commit()
    
    # Retrieve the new member and return it
    member_id = c.lastrowid
    return MemberOut(id=member_id, group_id=member.group_id, name=member.name, can_receive=member.can_receive)

@app.get("/groups/{group_id}/members", response_model=List[MemberOut])
def get_group_members(group_id: int):
    c.execute("SELECT * FROM members WHERE group_id = ?", (group_id,))
    members = c.fetchall()
    return [MemberOut(id=m[0], group_id=m[1], name=m[2], can_receive=m[3]) for m in members]

@app.post("/wishlists", response_model=WishlistItem)
def add_wishlist_item(item: WishlistItem, member_id: int):
    # Insert wishlist item into the database
    c.execute("INSERT INTO wishlists (member_id, item) VALUES (?, ?)", (member_id, item.item))
    conn.commit()
    
    # Retrieve the new wishlist item and return it
    item_id = c.lastrowid
    return WishlistItem(item=item.item)

@app.get("/wishlists/{member_id}", response_model=List[WishlistItem])
def get_member_wishlist(member_id: int):
    c.execute("SELECT * FROM wishlists WHERE member_id = ?", (member_id,))
    items = c.fetchall()
    return [WishlistItem(item=i[2]) for i in items]

@app.post("/messages", response_model=MessageIn)
def send_message(message: MessageIn):
    # Insert message into the database
    c.execute("INSERT INTO messages (group_id, sender_id, recipient_id, message) VALUES (?, ?, ?, ?)", 
              (message.group_id, message.sender_id, message.recipient_id, message.message))
    conn.commit()
    
    # Return the new message
    return message

@app.get("/messages/{group_id}", response_model=List[MessageIn])
def get_group_messages(group_id: int):
    c.execute("SELECT * FROM messages WHERE group_id = ?", (group_id,))
    messages = c.fetchall()
    return [MessageIn(group_id=m[1], sender_id=m[2], recipient_id=m[3], message=m[4]) for m in messages]

def generate_code(length):
    import string
    import random
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))