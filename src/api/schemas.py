from pydantic import BaseModel

class GroupSchema(BaseModel):
    id: int
    name: str
    code: str
    is_public: bool
    
class MemberSchema(BaseModel):
    id: int
    group_id: int
    name: str
    can_receive: bool

class WishlistItem(BaseModel):
    item: str

class MessageIn(BaseModel):
    group_id: int
    sender_id: int
    recipient_id: int
    message: str
