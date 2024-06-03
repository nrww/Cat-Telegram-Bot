
from fastapi import FastAPI, File, UploadFile, Response
from fastapi import APIRouter, Header

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)



