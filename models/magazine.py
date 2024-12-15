import sqlite3
from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None and (name is None or category is None):
            raise ValueError("Either id or (name and category) must be provided.")

        if id:
            self._id = id
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT name, category FROM magazines WHERE id = ?", (self._id,))
            row = cursor.fetchone()
            connection.close()
            if not row:
                raise ValueError("No magazine found with the provided ID.")
            self._name = row[0]
            self._category = row[1]
        else:
            if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
                raise ValueError("Name must be a string between 2 and 16 characters.")
            if not isinstance(category, str) or len(category) == 0:
                raise ValueError("Category must be a non-empty string.")
            self._name = name
            self._category = category
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
            connection.commit()
            self._id = cursor.lastrowid
            connection.close()

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def category(self):
        return self._category

    def articles(self):
        from models.article import Article
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        article_ids = cursor.fetchall()
        connection.close()
        return [Article(id=row[0]) for row in article_ids]

    def contributors(self):
        from models.author import Author
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.id FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        author_ids = cursor.fetchall()
        connection.close()
        return [Author(id=row[0]) for row in author_ids]

    def article_titles(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT title FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        connection.close()
        return titles if titles else None

    def contributing_authors(self):
        from models.author import Author
        connection = get_db_connection()
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
        return [Author(id=row[0]) for row in author_ids]
