import time

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ComicsLibrary.controllers:app", host="0.0.0.0", port=8000, reload=True)