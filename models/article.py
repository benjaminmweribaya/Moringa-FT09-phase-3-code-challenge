import sqlite3
from models.author import Author
from models.magazine import Magazine
from database.connection import get_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author=None, magazine=None):
        if id is None and (author is None or magazine is None or title is None):
            raise ValueError("Either id or (author, magazine, and title) must be provided.")

        if author and magazine and title:
            if not isinstance(author, Author):
                raise ValueError("Author must be an instance of the Author class.")
            if not isinstance(magazine, Magazine):
                raise ValueError("Magazine must be an instance of the Magazine class.")
            if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
                raise ValueError("Title must be a string between 5 and 50 characters.")

            if not hasattr(self, '_author'):
                self._author = author
            if not hasattr(self, '_magazine'):
                self._magazine = magazine
            if not hasattr(self, '_title'):
                self._title = title

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO articles (author_id, magazine_id, title) 
                VALUES (?, ?, ?)
            ''', (self._author.id, self._magazine.id, self._title))
            connection.commit()

            self._id = cursor.lastrowid
            connection.close()
        else:
            self._id = id
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT title, author_id, magazine_id FROM articles WHERE id = ?", (self._id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("No article found with the provided ID.")
            self._title = row[0]
            self._author = Author(id=row[1])
            self._magazine = Magazine(id=row[2])
            connection.close()

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT title FROM articles
            WHERE id = ?
        ''', (self._id,))
        self._title = cursor.fetchone()[0]
        connection.close()
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    def get_author(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM authors
            WHERE id = ?
        ''', (self._author.id,))
        author_data = cursor.fetchone()
        connection.close()
        return Author(id=author_data[0], name=author_data[1]) if author_data else None

    def get_magazine(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT * FROM magazines
            WHERE id = ?
        ''', (self._magazine.id,))
        magazine_data = cursor.fetchone()
        connection.close()
        return Magazine(id=magazine_data[0], name=magazine_data[1], category=magazine_data[2]) if magazine_data else None

