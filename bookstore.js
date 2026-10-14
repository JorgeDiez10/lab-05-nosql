// Lab 05 - Case Study 1: The Bookstore's New Inventory System
// Run this file from the repository's top-level folder so that
// authors.json and books.json are found.

// Step 2:
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
// printjson() is needed so the results show up when this file runs as a script
print("--- All authors ---")
printjson(db.authors.find().toArray())
print("--- All books ---")
printjson(db.books.find().toArray())

// Step 6: insert two new books
// Both books use author_004, a new author who is added in Step 7
db.books.insertMany([
  {
    title: "One Hundred Years of Solitude",
    published_year: 1967,
    author_ids: ["author_004"]
  },
  {
    title: "Love in the Time of Cholera",
    published_year: 1985,
    author_ids: ["author_004"]
  }
])

// Step 7: add missing authors
// author_004 is not in authors.json, so it has to be inserted by hand
db.authors.insertOne({
  _id: "author_004",
  name: "Gabriel García Márquez",
  nationality: "Colombian",
  bio: {
    short: "Colombian novelist and Nobel Prize winner, known for magical realism.",
    long: "Gabriel García Márquez was a Colombian novelist, short-story writer, and journalist. He is best known for One Hundred Years of Solitude and Love in the Time of Cholera, and he won the Nobel Prize in Literature in 1982."
  }
})

// Step 8: filter books by a list of authors
// author_001 (Jane Austen) comes from the loaded files, author_004 was added in Step 7
print("--- Books by author_001 or author_004 ---")
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray())
