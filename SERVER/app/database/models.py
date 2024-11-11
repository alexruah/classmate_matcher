from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey('users.id'))
    teacher = relationship("User", back_populates="teaching_classes")
    students = relationship("User", secondary="student_classes", back_populates="classes")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_teacher = Column(Boolean, default=False)
    classes = relationship("Class", secondary="student_classes", back_populates="students")
    teaching_classes = relationship("Class", back_populates="teacher")
    student_info = relationship("StudentInfo", back_populates="student")
    feedback = relationship("Feedback", back_populates="student")

class StudentClass(Base):
    __tablename__ = 'student_classes'
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), primary_key=True)

class StudentInfo(Base):
    __tablename__ = 'student_info'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    info = Column(Text, nullable=False)
    student = relationship("User", back_populates="student_info")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    students = relationship("User", secondary="group_students", back_populates="groups")

class GroupStudent(Base):
    __tablename__ = 'group_students'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    feedback_text = Column(Text, nullable=False)
    student = relationship("User", back_populates="feedback")
    group = relationship("Group", back_populates="feedback")

