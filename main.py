from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from models import User, UserIn
from auth import hash_password, verify_password

app = FastAPI()

engine = create_engine("sqlite:///users.db")


def create_db():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db()


@app.post("/register")
def register(user: UserIn):
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        new_user = User(
            username=user.username,
            hashed_password=hash_password(user.password)
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {"message": "Usuario registrado correctamente"}


@app.post("/login")
def login(user: UserIn):
    with Session(engine) as session:
        db_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if not db_user:
            return {"message": "Login fallido"}

        if verify_password(user.password, db_user.hashed_password):
            return {"message": "Login exitoso"}

        return {"message": "Login fallido"}


@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users