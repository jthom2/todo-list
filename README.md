# FastAPI Todo App

A simple Todo application built using FastAPI and SQLAlchemy. This API allows for basic CRUD operations on Todo items.

## Features

- **Create Todo**: Add a new Todo item.
- **Read Todos**: Retrieve a list of all Todo items or get a specific Todo by its ID.
- **Update Todo**: Modify the content of a specific Todo item.
- **Delete Todo**: Remove a specific Todo item from the database.

## Tech Stack

- **Web Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Database Engine**: SQLite3

## API Endpoints

1. **GET** `/`: Welcome message.
2. **GET** `/todos`: Get a list of all Todo items.
3. **GET** `/todos/{todo_id}`: Retrieve a specific Todo by its ID.
4. **POST** `/todos`: Create a new Todo item.
5. **PUT** `/todos/{todo_id}`: Update a specific Todo item.
6. **DELETE** `/todos/{todo_id}`: Delete a specific Todo item.


## License

MIT

## Author

Jackson Thomas
