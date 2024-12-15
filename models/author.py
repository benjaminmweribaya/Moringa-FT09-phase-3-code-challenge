import sqlite3
from models.article import Article
from models.magazine import Magazine
from database.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Either id or name must be provided.")

        if name:
            if not isinstance(name, str) or len(name) == 0:
                raise ValueError("Name must be a non-empty string.")

            if not hasattr(self, '_name'):
                self._name = name

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            connection.commit()

            self._id = cursor.lastrowid
            connection.close()
        else:
            if not isinstance(id, int):
                raise ValueError("ID must be an integer.")
            
            self._id = id
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM authors WHERE id = ?", (self._id,))
            result = cursor.fetchone()
            if result is None:
                raise ValueError("No author found with the provided ID.")
            self._name = result[0]
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
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id FROM articles
            WHERE author_id = ?
        ''', (self.id,))
        article_ids = cursor.fetchall()
        connection.close()
        return [Article(id=article_id[0]) for article_id in article_ids]

    def magazines(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazine_ids = cursor.fetchall()
        connection.close()
        return [Magazine(id=magazine_id[0]) for magazine_id in magazine_ids]
