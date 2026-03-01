import sqlite3
import os


# took me a while to figure this out but this gets the correct path to the database
def get_database_path():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_directory, "data", "rugby.db")


# simple connection function so i dont repeat this everywhere
def create_connection():
    connection = sqlite3.connect(get_database_path())
    return connection


# teams table stores (basic info about each rugby team)
def create_teams_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            short_name TEXT,
            country TEXT,
            league TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Teams table created successfully")


# competitions table (different rugby competitions)
def create_competitions_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_name TEXT NOT NULL,
            competition_type TEXT,
            season TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Competitions table created successfully")


# standings table (league standings for each competition)
def create_standings_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS standings (
            standing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            competition_id INTEGER NOT NULL,
            position INTEGER,
            played INTEGER,
            won INTEGER,
            drawn INTEGER,
            lost INTEGER,
            points INTEGER,
            scraped_date TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (team_id),
            FOREIGN KEY (competition_id) REFERENCES competitions (competition_id)
        )
    """)

    connection.commit()
    connection.close()
    print("Standings table created successfully")


# matches table (stores all match results)
def create_matches_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            home_score INTEGER,
            away_score INTEGER,
            match_date TEXT,
            FOREIGN KEY (competition_id) REFERENCES competitions (competition_id)
        )
    """)

    connection.commit()
    connection.close()
    print("Matches table created successfully")


# run to make sure it works
create_teams_table()
create_competitions_table()
create_standings_table()
create_matches_table()
