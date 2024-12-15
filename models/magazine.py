import sqlite3
from models.article import Article
from models.author import Author
from database.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None and (name is None or category is None):
            raise ValueError("Either id or (name and category) must be provided.")

        if name and category:
            if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
                raise ValueError("Name must be a string between 2 and 16 characters.")
            if not isinstance(category, str) or len(category) == 0:
                raise ValueError("Category must be a non-empty string.")

            if not hasattr(self, '_name'):
                self._name = name
            if not hasattr(self, '_category'):
                self._category = category

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
            connection.commit()

            self._id = cursor.lastrowid
            connection.close()
        else:
            if not isinstance(id, int):
                raise ValueError("ID must be an integer.")

            self._id = id
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name, category FROM magazines WHERE id = ?", (self._id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError("No magazine found with the provided ID.")
            self._name = row[0]
            self._category = row[1]
            connection.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM magazines WHERE id = ?", (self._id,))
        self._name = cursor.fetchone()[0]
        connection.close()
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE magazines SET name = ? WHERE id = ?", (self._name, self._id))
        connection.commit()
        connection.close()

    @property
    def category(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT category FROM magazines WHERE id = ?", (self._id,))
        self._category = cursor.fetchone()[0]
        connection.close()
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE magazines SET category = ? WHERE id = ?", (self._category, self._id))
        connection.commit()
        connection.close()

    def articles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        article_ids = cursor.fetchall()
        connection.close()
        return [Article(id=article_id[0]) for article_id in article_ids]

    def contributors(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        author_ids = cursor.fetchall()
        connection.close()
        return [Author(id=author_id[0]) for author_id in author_ids]

    def article_titles(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT title FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        connection.close()
        return titles if titles else None

    def contributing_authors(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT authors.id FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))
        author_ids = cursor.fetchall()
        connection.close()
        return [Author(id=author_id[0]) for author_id in author_ids]
