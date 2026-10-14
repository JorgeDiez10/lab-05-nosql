#!/usr/bin/env python3
"""Print a bookstore inventory report: each author and the books linked to them."""
import logging
import os
import sys

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Status messages (connection success, errors) go through logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Read the Atlas connection details from environment variables (never hardcode them)
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Authors in the report: author_002 and author_003 come from authors.json,
# author_004 was added in Case Study 1, Step 7
AUTHOR_IDS = ["author_002", "author_003", "author_004"]


def print_author_books(author, books):
    """Print an author's name and, under it, every book that lists that author's _id."""
    print(author["name"])
    # A book belongs to this author when its author_ids list contains the author's _id
    for book in books.find({"author_ids": author["_id"]}):
        print(f"  {book['title']} ({book['published_year']})")
    print()


def main():
    """Connect to MongoDB Atlas, look up the authors in AUTHOR_IDS, and print their books."""
    # Stop early with a clear message if the environment variables are not set
    if not MONGODB_ATLAS_URL or not MONGODB_ATLAS_USER or not MONGODB_ATLAS_PWD:
        logging.error("Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER and MONGODB_ATLAS_PWD first.")
        sys.exit(1)

    client = None
    try:
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        # MongoClient connects lazily, so "ping" checks that the connection really works
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas")

        # Select the database and the two collections from Case Study 1
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count how many of the authors in our list exist in the database
        author_count = authors.count_documents({"_id": {"$in": AUTHOR_IDS}})
        print(f"Authors: {author_count}")
        print()

        # Print each author with their books, in the same order as AUTHOR_IDS
        for author_id in AUTHOR_IDS:
            author = authors.find_one({"_id": author_id})
            if author is None:
                logging.warning("No author found with _id %s", author_id)
                continue
            print_author_books(author, books)

    except PyMongoError as error:
        logging.error("MongoDB error: %s", error)
        sys.exit(1)

    finally:
        # Close the connection when we are done, even if something went wrong
        if client is not None:
            client.close()
            logging.info("Connection to MongoDB Atlas closed")


if __name__ == "__main__":
    main()
