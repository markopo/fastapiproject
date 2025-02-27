from sqlalchemy import Column, String, Integer
from db import Base, Session, engine

import crud


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"



def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with Session() as session:
        user = User(
            name="Test Testson",
            email="test.testson@mail.com",
        )

        exist_user = crud.get_user_by_email(session, user.email)

        if not exist_user:
            session.add(user)
            session.commit()

        print(session.query(User).all())

