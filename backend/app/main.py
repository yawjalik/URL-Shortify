from fastapi import Body, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
import os
from loguru import logger

from db import Database
from schema import Tags, Schema
from url_shortener import URLShortener
from utils.HashIds import HashIds

# Load env variables
load_dotenv()
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_DATABASE")
hostname = os.getenv("BACKEND_HOST")
salt = "69420lmao"
allowed_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

# Tags and Schema
tags = Tags()
schema = Schema()

# Create app
app = FastAPI(
    title="URL Shortify",
    description="Accepts a longer URL and returns a shorter URL",
    version="1.0.0",
    openapi_tags=tags.tags_metadata
)

 # CORS setup
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# copypasted security settings (credits to chkhong)
# https://geekflare.com/http-header-implementation/https://geekflare.com/http-header-implementation/
HEADERS = {
  # CORS setting
  "Access-Control-Allow-Credentials": "true",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "*",
  "Access-Control-Allow-Headers": "*",
  # security setting
  "X-Frame-Options": "SAMEORIGIN",
  "X-Content-Type-Options": "nosniff",
  "X-XSS-Protection": "1; mode=block",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "Expect-CT": "max-age=86400, enforce", # enforcement of Certificate Transparency for 24 hours
  "Content-Security-Policy": "default-src https:"
}

db = Database(HOST, USER, PASSWORD, DATABASE)
url_shortener = URLShortener(db, hostname)
hashids = HashIds(salt=salt, min_length=7, alphabet=allowed_alphabet)

# Routes (credits to chkhong)
@app.get("/_healthcheck", status_code=status.HTTP_200_OK)
def healthcheck():
    content = {"status": "OK"}
    return JSONResponse(content=content, headers=HEADERS)

@app.post("/shorten", tags=["URL"], response_model=schema.ShortenResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(request:schema.ShortenRequest = Body(..., examples=schema.ShortenRequest.Example.examples)):
    args = request.dict()
    status_code, content = url_shortener.shorten(args, hashids)
    return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.get("/stats", tags=["Getting stats"], response_model=schema.StatsResponse, status_code=status.HTTP_200_OK)
def get_all_stats():
    status_code, content = url_shortener.get_all_stats()
    return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.get("/stats/{hash}", tags=["Getting stats"], response_model=schema.StatsByHashResponse, status_code=status.HTTP_200_OK)
def get_stat_by_hash(hash: str):
    status_code, content = url_shortener.get_stats_by_hash(hash)
    return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.post("/stats/find", tags=["Getting stats"], response_model=schema.StatsByOriginalURLResponse, status_code=status.HTTP_200_OK)
def get_stat_by_original_url(request:schema.StatsByOriginalURLRequest = Body(..., examples=schema.StatsByOriginalURLRequest.Example.examples)):
    args = request.dict()
    status_code, content = url_shortener.get_stat_by_original_url(args)
    return JSONResponse(content=content, headers=HEADERS, status_code=status_code)

@app.get("/{hash}", tags=["Redirect"], response_class=RedirectResponse, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
def redirect(hash: str) -> RedirectResponse:
    return RedirectResponse(url_shortener.redirect(hash))
