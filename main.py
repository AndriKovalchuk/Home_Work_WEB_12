from fastapi import FastAPI, Depends, HTTPException
from middlewares import CustomHeaderMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

app.add_middleware(CustomHeaderMiddleware)


@app.get("/")
def read_root():
    return {"Message": "Welcome to FastAPI!"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Database is configured correctly"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
