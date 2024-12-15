import sqlite3
from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Either id or name must be provided.")

        if id:
            if not isinstance(id, int):
                raise ValueError("ID must be an integer.")
            self._id = id
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM authors WHERE id = ?", (self._id,))
            result = cursor.fetchone()
            connection.close()
            if not result:
                raise ValueError("No author found with the provided ID.")
            self._name = result[0]
        else:
            if not isinstance(name, str) or len(name) == 0:
                raise ValueError("Name must be a non-empty string.")
            self._name = name
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            connection.commit()
            self._id = cursor.lastrowid
            connection.close()

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    def articles(self):
        from models.article import Article
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM articles WHERE author_id = ?", (self.id,))
        article_ids = cursor.fetchall()
        connection.close()
        return [Article(id=row[0]) for row in article_ids]

    def magazines(self):
        from models.magazine import Magazine
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazine_ids = cursor.fetchall()
        connection.close()
        return [Magazine(id=row[0]) for row in magazine_ids]
