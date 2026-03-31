from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str

class CreateUser(SQLModel):
    name: str
    email: str
    password: str   # ✅ important

class LoginUser(SQLModel):
    email: str
    password: str