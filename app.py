from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def populate_test_data():
    """Populate the database with initial test data."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insert an author
    cursor.execute("INSERT OR IGNORE INTO authors (id, name) VALUES (?, ?)", (1, "John Doe"))

    # Insert a magazine
    cursor.execute("INSERT OR IGNORE INTO magazines (id, name, category) VALUES (?, ?, ?)", (1, "Tech Weekly", "Technology"))

    # Insert an article
    cursor.execute(
        "INSERT OR IGNORE INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)",
        (1, "Test Title", "This is a sample article content that is over 100 characters long to meet the requirement.", 1, 1)
    )

    connection.commit()
    connection.close()
    print("Test data has been populated!")

def main():
    # Initialize the database and create tables
    create_tables()

    # Populate test data
    populate_test_data()

    # Continue with user interaction
    print("Database initialized. Proceed with the application.")

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content (min 100 chars): ")

    # Validate article content length
    if len(article_content) < 100:
        print("Article content must be at least 100 characters.")
        return

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implementation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid  # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid  # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine["id"], magazine["name"], magazine["category"]))

    print("\nAuthors:")
    for author in authors:
        print(Author(author["id"], author["name"]))

    print("\nArticles:")
    for article in articles:
        print(Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]))

if __name__ == "__main__":
    main()
