import sqlite3

# Create an in-memory SQLite database and a cursor
conn = sqlite3.connect(':memory:')
c = conn.cursor()

# Create Sets and Words tables
c.execute("""
    CREATE TABLE IF NOT EXISTS Sets (
        setID INTEGER PRIMARY KEY AUTOINCREMENT,
        setName TEXT NOT NULL
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS Words (
        wordID INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        definition TEXT NOT NULL,
        setID INTEGER,
        FOREIGN KEY (setID) REFERENCES Sets(setID)
    )
""")

# Function to add a set name to the database
def addSetName(setNameInput):
    with conn:
        c.execute("INSERT INTO Sets (setName) VALUES (?)", (setNameInput,))
        print(f"Successfully added set: {setNameInput}")
        return c.lastrowid  # Return the ID of the newly added set

# Function to retrieve a set by name
def getSetName(setNameSearch):
    c.execute("SELECT setID FROM Sets WHERE setName = ?", (setNameSearch,))
    result = c.fetchone()
    return result[0] if result else None

# Function to add a word and its definition to a set
def addWords(word, definition, setID):
    with conn:
        c.execute("INSERT INTO Words (word, definition, setID) VALUES (?, ?, ?)", 
                  (word, definition, setID))
        print(f"Successfully added: {word} : {definition} to setID {setID}")

def deleteSet(setNameSearch):
    setID = getSetName(setNameSearch)
    
    if setID:
        with conn:
            c.execute("DELETE FROM Words WHERE setID =?", (setID,))
            c.execute("DELETE FROM Sets WHERE setID =?", (setID,))
            print(f"Set '{setNameSearch}' and all its words have been deleted.")
    else:
        print(f"Set '{setNameSearch}' not found.")

def getWordsBySetID(setID):
    with conn:
        c.execute("SELECT word, definition FROM Words WHERE setID = ?", (setID,))
        return c.fetchall()  # Returns a list of tuples (word, definition)

def getAllSetNames():
    with conn:
        c.execute("SELECT setName FROM Sets")
        sets = c.fetchall()
        return [set[0] for set in sets]


def showSetWithWords(setNameSearch):
    # Get the setID based on the set name provided by the user
    setID = getSetName(setNameSearch)
    
    if setID:
        # Query to fetch all words and their definitions for the specified set
        c.execute("SELECT word, definition FROM Words WHERE setID = ?", (setID,))
        words = c.fetchall()
        
        # Display the set name and its words/definitions
        print(f"\nSet: {setNameSearch}")
        if words:
            print("Words and Definitions:")
            for word, definition in words:
                print(f"- {word}: {definition}")
        else:
            print("No words found in this set.")
    else:
        print(f"Set '{setNameSearch}' not found.")

# Close the connection
def closeConnection():
    conn.close()