## Challenge
Mr Czesław from the STX BookStore company asked you for help with writing an application
that will allow him to browse the list of books and help him understand what needs to be
ordered for his bookstores.

The application must be a REST API. It needs to allow for some basic operations, such as:
- getting the list of books from the database
- adding a new book
- editing an existing book
- removing the book from the database

When it comes to getting the list of books, Mr Czesław wants to be able to filter the results by
title, author, publication year (where the range of years is given) and by the acquired state (if
the book is already acquired or not).

Mr Czesław would like to have the option to import books into his database using the publicly
available Google API:
- https://developers.google.com/books/docs/v1/using#WorkingVolumes (usage
example: https://www.googleapis.com/books/v1/volumes?q=Hobbit )

Mr Czesław wants to be able to import books by a given author via API. In response, he
wants to see the number of imported books.

## API
● list books
> GET /books

> GET /books?author="Tolkien"&from=2003&to=2022&acquired=false

Expected response format:
```JSON
[
 {
  "id": 123,
  "title": "Hobbit czyli Tam i z powrotem",
  "authors": [
   "J. R. R. Tolkien"
  ],
  "acquired": false,
  "published_year": "2004"
 },
 {
  "id": 340,
  "title": "A Middle English Reader",
  "authors": [
   "Kenneth Sisam",
   "J. R. R. Tolkien"
  ],
  "acquired": false,
  "published_year": "2005"
 }
]
```
● get details of single book
> GET /books/123

Response:
```JSON
{
 "id": 123,
 "external_id": "rToaogEACAAJ",
 "title": "Hobbit czyli Tam i z powrotem",
 "authors": [
  "J. R. R. Tolkien"
 ],
 "published_year": "2005",
 "acquired": false,
 "thumbnail":
 "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
}
```

● update details of single book
> PATCH /books/123

Example request body:
```JSON
{
"acquired": true
}
```

Example response:
```JSON
{
 "id": 123,
 "external_id": "rToaogEACAAJ",
 "title": "Hobbit czyli Tam i z powrotem",
 "authors": [
  "J. R. R. Tolkien"
 ],
 "published_year": "2005",
 "acquired": true,
 "thumbnail":
 "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
}
```

● delete a book
> DELETE /books/123

● import books

Download data about books from https://www.googleapis.com/books/v1/volumes for
requested author. Add new entries into the application database. Update already
existing ones.
> POST /import

Example request body:
```JSON
{"author": "nazwisko"}
```

Example response:
```JSON
{
"imported": 200
}
```

## Technical requirements
● Implement the application using one of the Python web frameworks (your choice)

● Deploy the application using a publicly available server, for example, Heroku

● Take care of good coding practices (PEP8, code organization, etc.)

When submitting the task, please provide us with:
- URL for the deployed application
- link to the public repository, so that our technical recruiters can look at the code.