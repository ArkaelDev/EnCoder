Backend project in FastAPI.

CRUD That lets you upload files, encrypt them and send them to other users. Similar to a mail service.

Database with PostgreSQL, orm with sqlalchemy.

Encryption with _______

This project is a demo

## TODO list

- [x] Set up PostgreSQL database and orm.

- [x] POST endpoint to upload files.

- [x] GET endpoint to see specific file (by id).

- [x] Refactor architecture.

- [x] Apply tests.

- [x] Pydantic schemas.

- [x] User model.

- [x]JWT Token and authorization.

- [ ] User roles, owner, viewer and editor
    - [x] Change file database structure, allow ownership
    - [x] make uploadfile endpoint exclusive to registered users
    - [x] get user when uploading file
    - [ ] allow users to pass permision

- [ ] GET endpoint too see every file that a user has access.

- [ ] POST endpoint to share files.

- [ ] Set up encryption.

- [ ] Set up rate limit.
