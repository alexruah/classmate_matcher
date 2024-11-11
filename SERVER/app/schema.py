from pydantic import EmailStr, BaseModel, Field
from sqlmodel import Relationship

class UserBase(BaseModel):
    email: EmailStr

class UserLog(UserBase):
    password: str

class UserCreate(UserLog):
    first_name: str
    last_name: str

class ClassBase(BaseModel):
    name: str
    description: str = None
    teacher_id: int

class ClassCreate(ClassBase):
    pass

class ClassRead(ClassBase):
    id: int

    class Config:
        orm_mode: True

class UserRead(UserBase):
    id: int
    first_name: str
    last_name: str
    is_teacher: bool

    class Config:
        orm_mode: True

class UserReadWithClasses(UserRead):
    classes: list[ClassRead] = []
    teaching_classes: list[ClassRead] = []

class ClassReadWithStudents(ClassRead):
    students: list[UserRead] = []
    teacher: UserRead = None

class StudentInfoUpdate(BaseModel):
    info: str
