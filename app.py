from fastapi import FastAPI, Request, Depends, BackgroundTasks, File, UploadFile
from fastapi.templating import Jinja2Templates
import uvicorn

from database import SessionLocal, engine
import models
from models import Data_Table # import table class we created
from sqlalchemy.orm import Session

# import python-multipart
from pydantic import BaseModel 

import yfinance
import pandas as pd

app = FastAPI()

# Create the table from table structure in database.py
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class DataRequest(BaseModel):
	name: str


# Create db session
def get_db():
	try:
		db = SessionLocal()
		yield db

	finally:
		db.close()



# Route to homepage
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
	"""
	Displays the homepage
	"""

	# Get all contents of database
	table1 = db.query(Data_Table).all()

	print(table1)

	# return the home.html template
	return templates.TemplateResponse("home.html", {
		"request" : request,
		"table1" : table1
		})

# Route to page1
@app.get("/page1")
def create_page1(request: Request):
	"""
	Creates data and stores in database
	"""
	return templates.TemplateResponse("page1.html",{
		"request" : request
		})


# Content that will do operations on our data
def fetch_data(id: int):
	db = SessionLocal()
	data = db.query(Data_Table).filter(Data_Table.id == id).first()

	data.col1 = 10
	data.col2 = 20
	data.col3 = 90

	# # or using data from local folder
	# if data.name == "LGD":
	# 	# file = pd.read_csv('./Data/input_combined.csv')

	# 	# do whatever is neede to the data here
	# 	data.col1 = 10
	# 	data.col2 = 20
	# 	data.col3 = 90

	# else:
	# 	data.col1 = 99
	# 	data.col2 = 55
	# 	data.col3 = 77

	db.add(data)
	db.commit()



# Post route for data entered in field
@app.post("/data")
def create_data(data_request : DataRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	"""
	Created data and stores it in the database
	""" 
	table = Data_Table()
	table.name = data_request.name

	# Add data to databse record
	db.add(table)
	db.commit()

	# Create background tasks
	background_tasks.add_task(fetch_data, table.id)

	return {
	"code" : "success", 
	"message" : "data created"
	}


# Post routes for file uploads 
# SEE SCRIPT IN FASTAPI MAC v2!! It works
@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/uploadcsv")
def upload_csv(csv_file: UploadFile = File(...)):
    dataframe = pd.read_csv(csv_file.file)
    # do something with dataframe here (?)
    return {"filename": csv_file.filename}

