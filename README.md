# API Webserver Project Planning

## (R1): Identification of the Problem

The problem I am trying to solve by building this particular app is to provide users with a platform to create, manage, and share personal diaries online. Users should be able to securely store their diary entries, organize them with tags, receive comments and likes, and search for entries easily.

## (R2): Why It's a Problem

It is very important to preserve personal memories, there is a need for a secure and private platform to keep diaries, digital diaries can enhance accessibility and organization compared to traditional methods.

## (R3): Database System Choice

### For this Online Diary API project I am choosing SQLite as the Database System

#### Advantages

1. **Simplicity and No Installation Required:** SQLite is a serverless, self-contained database engine that doesn't require a separate database server to be installed or configured. It's essentially a library that you can include in your application. This simplicity is ideal for small projects where you want to keep the development and deployment process straightforward.

2. **Portability:** SQLite databases are just files on disk, making them highly portable. You can easily move or share your project along with its database by copying the SQLite file. This is convenient for development and testing.

3. **Low Resource Usage:** SQLite is lightweight and designed to operate efficiently with minimal resource consumption. It's a good choice for projects with low to moderate data storage and access needs.

4. **Zero Configuration:** Since SQLite doesn't require a separate server, you don't need to worry about server setup, configuration files, or user access control. This can save you time and effort in project setup.

#### Drawbacks

1. **Concurrency Limitations:** SQLite has limitations when it comes to concurrent write access. In a multi-user or high-traffic application, where multiple processes or threads need to write to the database simultaneously, SQLite might not perform as well as other database systems like PostgreSQL or MySQL. It uses a file-level locking mechanism, which can lead to contention and performance bottlenecks.

2. **Limited Features:** SQLite is intentionally minimalist in terms of features compared to more robust database systems. It lacks some advanced features like stored procedures, user-defined functions, and complex access control mechanisms. Depending on your project's requirements, this might or might not be an issue.

3. **Scalability:** SQLite is not designed for large-scale, high-traffic applications. If your project grows significantly in terms of data volume and traffic, you may eventually need to migrate to a more scalable database solution.

4. **Limited Compatibility:** While SQLite follows SQL standards, it has some differences in SQL syntax and behavior compared to other database systems. This might lead to compatibility issues if you plan to switch to a different database system in the future.

In summary, SQLite is a great choice for small projects, prototyping, or applications with low to moderate data requirements due to its simplicity, ease of use, and portability. However, it's essential to consider its limitations in terms of concurrency, scalability, and advanced features if your project's requirements evolve over time.

## (R4): ORM Benefits

- Simplifies database interactions by using Python objects.
- Provides a higher-level abstraction for database operations.
- Supports database independence, allowing you to switch databases with minimal code changes.
- Offers automatic database schema generation and migration tools.
- Enhances code readability and maintainability by using Python classes to represent database tables.

## (R5): Endpoint Documentation

### Documenting Planned Endpoints (Planning Stage)

During the planning stage, I've outlined the planned endpoints for my API, which will be implemented during the development phase. Here's a preliminary list of these endpoints:

| Endpoint             | Method(s) | Description                        |
|----------------------|-----------|------------------------------------|
| `/api/register`      | POST      | User registration                  |
| `/api/login`         | POST      | User login                         |
| `/api/diaries`       | GET, POST | List all diaries, create a diary   |
| `/api/diaries/int:id`| GET, PUT, DELETE | Retrieve, update, delete a diary  |
| ...                  | ...       | ...                                |

While these endpoints are still in the planning stage, they serve as a blueprint for the API's functionality. During development, I will implement each endpoint, define the required data, and specify the expected response data. Additionally, I will ensure that the API adheres to REST conventions and includes appropriate HTTP request methods.

As the development phase progresses, I will update this documentation to reflect the actual implementation of the endpoints, providing more detailed information about their functionality and usage.

This preliminary documentation helps me visualize the API's structure and serves as a reference for development tasks. It will be expanded and refined as the project evolves.

### Endpoints

#### -Auth APIs

| Endpoint         | Method | Description          | Authorization |
|------------------|--------|----------------------|---------------|
| `/auth/register` | POST   | Register a new user  | NONE          |
| `/auth/login`    | POST   | Log In existing user | NONE          |

- Sample Request Body

```json
{
   "email": "newuser@example.com",
   "password": "password"
}
```

- Sample Response Body (2XX)

```json
{
   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ezJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjA3NjI4NCwianRpIjoiZDNhOGRhMTktNWVjYS00MTAwLWI0MDItYThjNmQzNzY1ZTFiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIxQHB5Y2FkZW15LmNvbSIsIm5iZiI6MTY5NjA3NjI4NCwiZXhwIjoxNjk2MDc3MTg0fQ.8xmiiBNeqzfr_U38b-99kBMD00nvViastgqVkf0tz2Y"
}
 ```

#### -User APIs

| Endpoint               | Method | Description          | Authorization |
|------------------------|--------|----------------------|---------------|
| `/users/`              | GET    | Get all users        | NONE          |
| `/users/`              | POST   | Create a new user    | NONE          |
| `/users/<int:user_id>` | GET    | Get user by ID       | NONE          |
| `/users/<int:user_id>` | PUT    | Update existing user | NONE          |
| `/users/<int:user_id>` | DELETE | Delete existing user | NONE          |

- Sample Request Body

```json
{
   "email": "newuser@example.com",
   "password": "password"
}
```

- Sample Response Body (2XX: GET, POST, PUT)

```json
{
   "comments": [
      {
         "content": "Comment by user1 on entry1",
         "date_created": "2023-09-30T15:01:57.005853",
         "entry_id": 1,
         "id": 1
      },
      {
         "content": "Comment by user 1 on entry 2",
         "date_created": "2023-09-30T15:01:57.005853",
         "entry_id": 2,
         "id": 2
      }
   ],
   "diaries": [
      {
         "date_created": "2023-09-30T15:01:56.974576",
         "id": 1,
         "privacy": "PrivacyOptions.PUBLIC",
         "title": "User1 Diary1"
      },
      {
         "date_created": "2023-09-30T15:01:56.974576",
         "id": 2,
         "privacy": "PrivacyOptions.PRIVATE",
         "title": "User1 Diary2"
      }
   ],
   "email": "user1@example.com",
   "id": 1,
   "likes": [
      {
         "date_created": "2023-09-30T15:01:56.990225",
         "entry_id": 1,
         "id": 1
      },
      {
         "date_created": "2023-09-30T15:01:57.005853",
         "entry_id": 3,
         "id": 3
      }
   ]
}
 ```

- Sample Response Body (2XX: DELETE)

```json
{
   "message": "User deleted successfully"
}
```

#### -Diary APIs

| Endpoint                  | Method | Description                                           | Authorization |
|---------------------------|--------|-------------------------------------------------------|---------------|
| `/diaries/`               | GET    | Get all diaries for the logged-in user                | JWT Token     |
| `/diaries/`               | POST   | Create a new diary for the logged-in user             | JWT Token     |
| `/diaries/<int:diary_id>` | GET    | Get diary by ID if it belongs to logged-in user       | JWT Token     |
| `/diaries/<int:diary_id>` | PUT    | Update existing diary if it belongs to logged-in user | JWT Token     |
| `/diaries/<int:diary_id>` | DELETE | Delete existing diary if it belongs to logged-in user | JWT Token     |

- Auth Header

```json
{
   "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ezJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjA3NjI4NCwianRpIjoiZDNhOGRhMTktNWVjYS00MTAwLWI0MDItYThjNmQzNzY1ZTFiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIxQHB5Y2FkZW15LmNvbSIsIm5iZiI6MTY5NjA3NjI4NCwiZXhwIjoxNjk2MDc3MTg0fQ.8xmiiBNeqzfr_U38b-99kBMD00nvViastgqVkf0tz2Y"
}
```

**NOTE**: Replace the token above with your freshly generated token

- Sample Request Body

```json
{
   "title": "Diary1",
   "privacy": "PUBLIC"
}
```

- Sample Response Body (2XX: GET, POST, PUT)

```json
{
   "date_created": "2023-09-30T15:01:56.974576",
   "entries": [
      {
         "content": "Diary1 Entry1",
         "date_created": "2023-09-30T15:01:56.974576",
         "id": 1
      },
      {
         "content": "Diary1 Entry2",
         "date_created": "2023-09-30T15:01:56.990225",
         "id": 2
      }
   ],
   "id": 1,
   "privacy": "PUBLIC",
   "title": "User1 Diary1",
   "user": {
      "email": "user1@example.com",
      "id": 1
   }
}
 ```

- Sample Response Body (2XX: DELETE)

```json
{
   "message": "Diary deleted successfully"
}
```

#### -Entry APIs

| Endpoint                                    | Method | Description                                                         | Authorization |
|---------------------------------------------|--------|---------------------------------------------------------------------|---------------|
| `/entries/diaries/<int:diary_id>`           | GET    | Get all entries in the diary if it belongs to the logged-in user    | JWT Token     |
| `/entries/`                                 | POST   | Create a new entry in the diary if it belongs to the logged-in user | JWT Token     |
| `/entries/<int:entry_id>`                   | GET    | Get entry by ID if it belongs to logged-in user                     | JWT Token     |
| `/entries/<int:entry_id>`                   | PUT    | Update existing entry if it belongs to logged-in user               | JWT Token     |
| `/entries/<int:entry_id>`                   | DELETE | Delete existing entry if it belongs to logged-in user               | JWT Token     |
| `/entries/<int:entry_id>/tags/<int:tag_id>` | PUT    | Add tag to an entry if entry belongs to logged-in user              | JWT Token     |
| `/entries/<int:entry_id>/tags/<int:tag_id>` | DELETE | Delete tag from an entry if entry belongs to logged-in user         | JWT Token     |
| `/entries/tags/<int:tag_id>`                | GET    | Get all entries having the given tag id                             | NONE          |

- Auth Header

```json
{
   "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ezJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjA3NjI4NCwianRpIjoiZDNhOGRhMTktNWVjYS00MTAwLWI0MDItYThjNmQzNzY1ZTFiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIxQHB5Y2FkZW15LmNvbSIsIm5iZiI6MTY5NjA3NjI4NCwiZXhwIjoxNjk2MDc3MTg0fQ.8xmiiBNeqzfr_U38b-99kBMD00nvViastgqVkf0tz2Y"
}
```

**NOTE**: Replace the token above with your freshly generated token

- Sample Request Body

```json
{
   "content": "My new entry",
   "diary_id": 1
}
```

- Sample Response Body (2XX: GET, POST, PUT)

```json
{
   "comments": [
      {
         "content": "Comment by user1 on entry1",
         "date_created": "2023-09-30T15:01:57.005853",
         "id": 1,
         "user": {
            "email": "user1@example.com",
            "id": 1
         }
      }
   ],
   "content": "Diary1 Entry1",
   "date_created": "2023-09-30T15:01:56.974576",
   "diary": {
      "date_created": "2023-09-30T15:01:56.974576",
      "id": 1,
      "privacy": "PUBLIC",
      "title": "User1 Diary1",
      "user": {
         "email": "user1@example.com",
         "id": 1
      }
   },
   "id": 1,
   "likes": [
      {
         "date_created": "2023-09-30T15:01:56.990225",
         "id": 1,
         "user": {
            "email": "user1@example.com",
            "id": 1
         }
      },
      {
         "date_created": "2023-09-30T15:01:56.990225",
         "id": 2,
         "user": {
            "email": "user2@example.com",
            "id": 2
         }
      }
   ],
   "tags": [
      {
         "id": 1,
         "name": "Tag1"
      },
      {
         "id": 2,
         "name": "Tag2"
      }
   ]
}
 ```

- Sample Response Body (2XX: DELETE)

```json
{
   "message": "Entry deleted successfully"
}
```

#### -Like APIs

| Endpoint                        | Method | Description                                                               | Authorization |
|---------------------------------|--------|---------------------------------------------------------------------------|---------------|
| `/likes/entries/<int:entry_id>` | GET    | Get all likes on the entry                                                | NONE          |
| `/likes/`                       | POST   | Create a new like on the entry by the logged-in user if not already liked | JWT Token     |
| `/likes/<int:like_id>`          | GET    | Get like by ID                                                            | NONE          |
| `/likes/<int:like_id>`          | DELETE | Delete existing like if it belongs to logged-in user                      | JWT Token     |

- Auth Header

```json
{
   "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ezJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjA3NjI4NCwianRpIjoiZDNhOGRhMTktNWVjYS00MTAwLWI0MDItYThjNmQzNzY1ZTFiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIxQHB5Y2FkZW15LmNvbSIsIm5iZiI6MTY5NjA3NjI4NCwiZXhwIjoxNjk2MDc3MTg0fQ.8xmiiBNeqzfr_U38b-99kBMD00nvViastgqVkf0tz2Y"
}
```

**NOTE**: Replace the token above with your freshly generated token

- Sample Request Body

```json
{
   "entry_id": 4
}
```

- Sample Response Body (2XX: GET, POST, PUT)

```json
{
   "date_created": "2023-09-30T15:01:56.990225",
   "entry": {
      "content": "Diary1 Entry1",
      "date_created": "2023-09-30T15:01:56.974576",
      "diary": {
         "date_created": "2023-09-30T15:01:56.974576",
         "id": 1,
         "privacy": "PUBLIC",
         "title": "User1 Diary1",
         "user": {
            "email": "user1@example.com",
            "id": 1
         }
      },
      "id": 1
   },
   "id": 1,
   "user": {
      "email": "user1@example.com",
      "id": 1
   }
}
 ```

- Sample Response Body (2XX: DELETE)

```json
{
   "message": "Like deleted successfully"
}
```

#### -Comment APIs

| Endpoint                           | Method | Description                                             | Authorization |
|------------------------------------|--------|---------------------------------------------------------|---------------|
| `/comments/entries/<int:entry_id>` | GET    | Get all comments on the entry                           | NONE          |
| `/comments/`                       | POST   | Create a new comment by the logged-in user              | JWT Token     |
| `/comments/<int:comment_id>`       | GET    | Get comment by ID                                       | NONE          |
| `/comments/<int:comment_id>`       | PUT    | Update existing comment if it belongs to logged-in user | JWT Token     |
| `/comments/<int:comment_id>`       | DELETE | Delete existing comment if it belongs to logged-in user | JWT Token     |

- Auth Header

```json
{
   "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ezJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjA3NjI4NCwianRpIjoiZDNhOGRhMTktNWVjYS00MTAwLWI0MDItYThjNmQzNzY1ZTFiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InVzZXIxQHB5Y2FkZW15LmNvbSIsIm5iZiI6MTY5NjA3NjI4NCwiZXhwIjoxNjk2MDc3MTg0fQ.8xmiiBNeqzfr_U38b-99kBMD00nvViastgqVkf0tz2Y"
}
```

**NOTE**: Replace the token above with your freshly generated token

- Sample Request Body

```json
{
   "entry_id": 4,
   "content": "Nice entry!"
}
```

- Sample Response Body (2XX: GET, POST, PUT)

```json
{
   "content": "Comment by user1 on entry1",
   "date_created": "2023-09-30T15:01:57.005853",
   "entry": {
      "content": "Diary1 Entry1",
      "date_created": "2023-09-30T15:01:56.974576",
      "diary": {
         "date_created": "2023-09-30T15:01:56.974576",
         "id": 1,
         "privacy": "PUBLIC",
         "title": "User1 Diary1",
         "user": {
            "email": "user1@example.com",
            "id": 1
         }
      },
      "id": 1
   },
   "id": 1,
   "user": {
      "email": "user1@example.com",
      "id": 1
   }
}
 ```

- Sample Response Body (2XX: DELETE)

```json
{
   "message": "Comment deleted successfully"
}
```

#### -Tag APIs

| Endpoint             | Method | Description         | Authorization |
|----------------------|--------|---------------------|---------------|
| `/tags/`             | GET    | Get all tags        | NONE          |
| `/tags/`             | POST   | Create a new tag    | NONE          |
| `/tags/<int:tag_id>` | GET    | Get tag by ID       | NONE          |
| `/tags/<int:tag_id>` | PUT    | Update existing tag | NONE          |
| `/tags/<int:tag_id>` | DELETE | Delete existing tag | NONE          |

- Sample Request Body

```json
{
   "name": "tag1"
}
```

- Sample Response Body (2XX: GET, POST, PUT)

```json
{
   "entries": [
      {
         "content": "Diary1 Entry1",
         "date_created": "2023-09-30T15:01:56.974576",
         "diary": {
            "date_created": "2023-09-30T15:01:56.974576",
            "id": 1,
            "privacy": "PUBLIC",
            "title": "User1 Diary1",
            "user": {
               "email": "user1@example.com",
               "id": 1
            }
         },
         "id": 1
      },
      {
         "content": "Diary1 Entry2",
         "date_created": "2023-09-30T15:01:56.990225",
         "diary": {
            "date_created": "2023-09-30T15:01:56.974576",
            "id": 1,
            "privacy": "PUBLIC",
            "title": "User1 Diary1",
            "user": {
               "email": "user1@example.com",
               "id": 1
            }
         },
         "id": 2
      }
   ],
   "id": 1,
   "name": "Tag1"
}
 ```

- Sample Response Body (2XX: DELETE)

```json
{
   "message": "Tag deleted successfully"
}
```

## (R6): Entity Relationship Diagram (ERD)

![ERD Diagram](ERD.png)

The Entity Relationship Diagram (ERD) represents the normalized relational database for my web server, which is designed to manage online diaries. The ERD consists of multiple entities (models) and illustrates how they are related to one another.

### Entities (Models)

1. **Users:**
   - The "Users" entity represents registered users of the web server.
   - It includes attributes such as user_id (Primary Key), email, password, and other user-related information.
   - Users have a one-to-many relationship with Diaries, indicating that one user can have multiple diaries.

2. **Diaries:**

   - The "Diaries" entity represents individual diaries created by users.
   - It includes attributes such as diary_id (Primary Key), user_id (Foreign Key), title, privacy settings, and more.
   - Diaries have a one-to-many relationship with Entries, meaning that one diary can contain multiple diary entries.

3. **Entries:**

   - The "Entries" entity represents individual diary entries within diaries.
   - It includes attributes such as entry_id (Primary Key), diary_id (Foreign Key), date_created, content, and more.
   - Entries have a many-to-one relationship with Diaries, signifying that each entry belongs to one diary.
   - Additionally, Entries have one-to-many relationships with Comments and Likes, allowing multiple comments and likes for each entry.

4. **Tags:**

   - The "Tags" entity represents labels or keywords associated with diary entries for categorization.
   - It includes attributes such as tag_id (Primary Key), user_id (Foreign Key), and name.
   - Users can create multiple tags, and Tags have a many-to-many relationship with Entries through the EntryTags junction table.

5. **Comments:**

   - The "Comments" entity represents comments left by users on individual diary entries.
   - It includes attributes such as comment_id (Primary Key), user_id (Foreign Key), entry_id (Foreign Key), content, and more.
   - Comments have a many-to-one relationship with Entries, indicating that each comment belongs to one entry.

6. **Likes:**

   - The "Likes" entity represents likes or reactions given by users to individual diary entries.
   - It includes attributes such as like_id (Primary Key), user_id (Foreign Key), entry_id (Foreign Key), and more.
   - Likes also have a many-to-one relationship with Entries, signifying that each like is associated with one entry.

#### Relationships

- Users have a one-to-many relationship with Diaries (one user can have multiple diaries).
- Users have a one-to-many relationship with Likes.
- Users have a one-to-many relationship with Comments.
- Diaries have a one-to-many relationship with Entries (one diary can have multiple entries).
- Diaries have a many-to-one relationship with Users.
- Entries have a many-to-one relationship with Diaries (each entry belongs to one diary).
- Entries have a one-to-many relationship with Comments (one entry can have multiple comments).
- Comments have a many-to-one relationship with Entries (each comment belongs to one entry).
- Comments have a many-to-one relationship with Users.
- Entries have a one-to-many relationship with Likes (one entry can have multiple likes).
- Likes have a many-to-one relationship with Entries (each like belongs to one entry).
- Likes have a many-to-one relationship with Users.
- Tags have a many-to-many relationship with Entries via the EntryTags junction table, allowing multiple tags for each entry.

This ERD serves as a visual representation of the database structure and the relationships between entities, guiding the development of the web server for managing online diaries.

## (R7): Third-Party Services

### My Flask application uses several third-party services to enhance its functionality

1. I use Flask as the foundation of my web application, which is a third-party web framework designed for building web applications.

2. To handle authentication and authorization, I employ Flask-JWT-Extended, an extension for Flask that provides support for JSON Web Tokens (JWT).

3. For simplified database interactions, I integrate Flask-SQLAlchemy into my application. It builds on SQLAlchemy, a widely-used Object-Relational Mapping (ORM) library.

4. To securely hash passwords, I utilize Flask-Bcrypt, another Flask extension that integrates the 'bcrypt' library with my Flask application.

5. For seamless object serialization and deserialization, especially when converting complex data types like SQLAlchemy models into JSON responses, I rely on Flask-Marshmallow.

6. Lastly, I manage environment variables within my application using the python-dotenv library, which simplifies configuration and settings management.

## (R8): Project Models and Relationships

### Project Models and Relationships

In my Online Diary API project, I have designed several models (entities) that collectively represent the core elements of the application. These models have relationships with each other, defining how data is organized and connected within the database:

#### Users

- **user_id (Primary Key):** A unique identifier for each user.
- **email:** The user's email address, used for registration and authentication.
- **password:** Securely hashed password for user authentication.

#### Diaries

- **diary_id (Primary Key):** A unique identifier for each diary.
- **user_id (Foreign Key):** Establishes a one-to-many relationship with Users, indicating that each user can have multiple diaries.
- **title:** The title of the diary.
- **privacy:** Specifies the privacy settings for the diary (e.g., private, friends only, public).

#### Entries

- **entry_id (Primary Key):** A unique identifier for each diary entry.
- **diary_id (Foreign Key):** Forms a many-to-one relationship with Diaries, indicating that each entry belongs to one diary.
- **date_created:** The date when the entry was created.
- **content:** The content of the diary entry.

#### Tags

- **tag_id (Primary Key):** A unique identifier for each tag.
- **user_id (Foreign Key):** Establishes a one-to-many relationship with Users, allowing each user to have multiple tags.
- **name:** The name or label of the tag.

#### Comments

- **comment_id (Primary Key):** A unique identifier for each comment.
- **user_id (Foreign Key):** Establishes a one-to-many relationship with Users, indicating that each user can post multiple comments.
- **entry_id (Foreign Key):** Forms a many-to-one relationship with Entries, signifying that each comment is associated with one entry.
- **content:** The content of the comment.

#### Likes

- **like_id (Primary Key):** A unique identifier for each like.
- **user_id (Foreign Key):** Establishes a one-to-many relationship with Users, allowing each user to like multiple entries.
- **entry_id (Foreign Key):** Forms a many-to-one relationship with Entries, indicating that each like is associated with one entry.

#### EntryTags

- **id (Primary Key):** A unique identifier for each entry-tag relationship.
- **entry_id (Foreign Key):** Forms a many-to-one relationship with Entries, indicating that each entry can have multiple tags.
- **tag_id (Foreign Key):** Establishes a many-to-many relationship between Tags and Entries via the EntryTags junction table.

These model relationships form the foundation of my database schema, ensuring that data is structured efficiently and that users can interact with their diaries, entries, tags, comments, and likes seamlessly.

## (R9): Database Relations

### Database Relations

In my Online Diary API application, I have implemented various database relations to efficiently organize and manage user data, diaries, entries, tags, comments, and likes. These relations are represented as follows:

1. **Users to Diaries (One-to-Many):** Each user can have multiple diaries. This one-to-many relationship is established using a foreign key. In the `Diaries` table, the `user_id` field links each diary to a specific user, allowing users to own and manage their diaries.

2. **Diaries to Entries (One-to-Many):** Each diary can contain multiple entries. This one-to-many relationship is defined by the `diary_id` foreign key in the `Entries` table. Each entry is associated with a specific diary, enabling users to organize their diary content.

3. **Entries to Comments (One-to-Many):** Each entry can receive multiple comments. This one-to-many relationship is established using the `entry_id` foreign key in the `Comments` table. Each comment is linked to a particular entry, allowing users to engage in discussions about diary entries.

4. **Entries to Likes (One-to-Many):** Each entry can receive multiple likes from users. This one-to-many relationship is defined by the `entry_id` foreign key in the `Likes` table. Users can express their appreciation for diary entries through likes.

5. **Users to Tags (One-to-Many):** Each user can create multiple tags. This one-to-many relationship is established with the `user_id` foreign key in the `Tags` table. Users can categorize and organize their diary entries using these tags.

6. **Tags to Entries (Many-to-Many):** Diary entries can have multiple tags, and each tag can be associated with multiple entries. To represent this many-to-many relationship, an intermediary table called `EntryTags` is introduced. This table contains foreign keys `entry_id` and `tag_id`, forming a bridge between tags and entries.

These database relations are crucial for maintaining data integrity and ensuring efficient data retrieval. They enable users to create, organize, and interact with their diaries and diary entries seamlessly.

## Requirement 10 (R10): Task Allocation and Tracking

### Task Allocation and Tracking

As a solo developer working on this project, I employ a systematic approach to allocate and track tasks efficiently. Given the project's complexity, I've broken it down into manageable phases, focusing on one model at a time, as suggested by my teacher. Here's how I allocate and track tasks:

1. **Dividing the Project into Phases:** To maintain a structured workflow, I've divided the project into distinct phases, each corresponding to a specific model in the system. For instance, I'll start with the `Users` model and progress to the `Diaries`, `Entries`, `Tags`, `Comments`, and `Likes` models sequentially.

2. **Task Identification:** Within each phase, I identify and list the tasks associated with that particular model. These tasks include designing the model schema, creating API endpoints, implementing database operations, and ensuring proper validation and error handling.

3. **Task Prioritization:** I prioritize tasks based on their significance and dependencies. Critical tasks are addressed first to establish a foundation for subsequent tasks. For instance, user registration and authentication are prioritized before allowing users to create diaries or entries.

4. **Utilizing Version Control (Git):** I leverage version control with Git to maintain a historical record of project changes. With Git, I can create branches for each task or model, allowing me to work on new features or fixes without disrupting the main codebase.

5. **Project Management Tools:** Although I'm working alone, I use project management tools like GitHub Projects or Trello to create task boards. Here, I create cards for each task, assign them to specific phases, and mark their progress as I complete them. This visual representation helps me stay organized.

6. **Testing and Debugging:** After implementing each model, I thoroughly test its functionality to identify and rectify any issues. This testing phase ensures that each model works as intended before moving on to the next one.

7. **Documentation:** For each completed model, I update the project documentation, including the README.md file. This documentation covers the model's endpoints, expected request and response data, and any specific details about its implementation.

8. **Continuous Learning and Refinement:** Throughout the project, I engage in continuous learning to address challenges and improve my skills. I remain adaptable and open to making refinements as needed to enhance the project's quality.

9. **Meeting Milestones:** I set milestones for completing each model and phase, allowing me to measure my progress. Meeting these milestones provides a sense of accomplishment and motivates me to move forward.

By following this structured approach to task allocation and tracking, I can efficiently develop each model, ensuring that the entire project progresses smoothly and meets the required standards.
