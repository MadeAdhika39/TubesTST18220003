from pymongo import MongoClient
from schemas.motorSchemas import *
from models.motorModel import Motor

client = MongoClient("mongodb+srv://madeadhika:tubestst@madeadhika.i8uwgf8.mongodb.net/?retryWrites=true&w=majority")
db = client.madetst
collection_name = db["motor"]
collection_user = db["user"]
collection_bbm = db["bbm"]