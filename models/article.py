import sqlite3
from models.author import Author
from models.magazine import Magazine
from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if id is None and (author_id is None or magazine_id is None or title is None):
            raise ValueError("Either id or (author_id, magazine, and title) must be provided.")

        if id:
            self._id = id
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT title, author_id, magazine_id FROM articles WHERE id = ?", (self._id,))
            row = cursor.fetchone()
            connection.close()
            if not row:
                raise ValueError("No article found with the provided ID.")
            self._title = row[0]
            self._author_id = row[1]
            self._magazine_id = row[2]
        else:
            if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
                raise ValueError("Title must be a string between 5 and 50 characters.")
            self._title = title
            self._author_id = author_id
            self._magazine_id = magazine_id
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self._title, self._author_id, self._magazine_id),
            )
            connection.commit()
            self._id = cursor.lastrowid
            connection.close()

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        from models.author import Author
        return Author(id=self._author_id)

    @property
    def magazine(self):
        from models.magazine import Magazine
        return Magazine(id=self._magazine_id)
    

    

