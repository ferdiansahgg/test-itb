import secrets
import base64
import pyotp
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import create_engine, Session, SQLModel, select
from typing import Annotated
from app.model import MOTD, MOTDBase
from fastapi.responses import FileResponse
from pathlib import Path

# SQLite Database
sqlite_file_name = "motd.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"  # Hanya 3 slash (/) sudah cukup
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

create_db_and_tables()

# FastAPI
app = FastAPI(docs_url=None, redoc_url=None)
security = HTTPBasic()

# Users - lengkapi dengan userid dan shared_secret yang sesuai
users = {"sister": "ii2210_sister_"} 

@app.get("/")
async def root():
    # Memberikan index.html sebagai response
    return FileResponse(Path("static/index.html"))

@app.get("/motd")
async def get_motd(session: SessionDep):
    statement = select(MOTD).order_by(MOTD.id.desc()).limit(1)
    motd = session.exec(statement).first()
    if motd:
        return {"motd": motd.motd, "creator": motd.creator, "created_at": motd.created_at}
    else:
        return {"message": "No message yet"}

@app.post("/motd")
async def post_motd(message: MOTDBase, session: SessionDep, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_password_bytes = credentials.password.encode("utf8")

    valid_username, valid_password = False, False

    try:
        if credentials.username in users:
            valid_username = True
            s = base64.b32encode(users.get(credentials.username).encode("utf-8")).decode("utf-8")
            totp = pyotp.TOTP(s=s, digest="SHA256", digits=8)
            valid_password = secrets.compare_digest(current_password_bytes, totp.now().encode("utf8"))

            if valid_password and valid_username:
                # Menambahkan message of the day ke basis data
                motd = MOTD(motd=message.motd, creator=credentials.username)
                session.add(motd)
                session.commit()
                session.refresh(motd)
                return motd
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid userid or password.") 
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid userid or password.")
    
    except HTTPException as e:
        raise e

# Jalankan server
if __name__ == "__main__":
    import uvicorn
    create_db_and_tables()
    uvicorn.run("app.main:app", host="0.0.0.0", port=17787, reload=True)
