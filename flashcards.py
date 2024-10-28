from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import atexit
from flashcardsDB import addSetName, getSetName, addWords, closeConnection, getAllSetNames, getWordsBySetID, deleteSet

# ---- Creating the Main Window ----
window = Tk()
window.title("Main Menu")
window.geometry("900x600")

# -------

# ---- Creating the Tabs on the Window ---
tabs = ttk.Notebook(window)

tab1 = Frame(tabs)
tab2 = Frame(tabs)
tab3 = Frame(tabs)
tab4 = Frame(tabs)

tabs.add(tab1, text = "Create Set")
tabs.add(tab2, text = "Add to Set")
tabs.add(tab3, text = "Select Set")
tabs.add(tab4, text = "Learn Mode")

# -------

# ---- CreateSet Window ---
currentSetID = None
selectedSetID = None

setNameEntry = Entry(tab1)

def handleAddSet():
    global currentSetID
    setName = setNameEntry.get()
    if setName:
        existingSetID = getSetName(setName)
        if existingSetID is not None:
            currentSetID = existingSetID
            messagebox.showinfo("Info", f"Set '{setName}' already exists.")
        else:
            currentSetID = addSetName(setName)
            messagebox.showinfo("Info", f"Added new Set: '{setName}' !")
        setNameEntry.delete(0, END)  # Clear the set name entry
        updateSetDropdown()  # Refresh the dropdown in Tab 2
        updateAddWordsDropdown()  # Refresh the dropdown for adding words in Tab 1
    else:
        messagebox.showwarning("Warning", "Please enter a set name.")

Label(tab1, text = "Set Name: ").pack()
setNameEntry.pack()

Button(tab1, text = "Save Set", command = handleAddSet).pack()
# -------

# ---- Edit Set Window ---
wordBox = Entry(tab2)
definitionBox = Entry(tab2)

Label(tab2, text = "Select a Set to Edit: ").pack()
addWordsSetVar = StringVar(tab2)  # Tracks the selected set name for adding words
addWordsSetDropdown = ttk.Combobox(tab2, textvariable=addWordsSetVar)
addWordsSetDropdown.pack(pady=10)

def updateAddWordsDropdown():
    # Fetch all available sets and update the dropdown in Tab 1
    setNames = getAllSetNames()
    addWordsSetDropdown['values'] = setNames

def handleAddWord():
    selectedSetName = addWordsSetVar.get()  # Get the selected set name from dropdown
    if selectedSetName:
        setID = getSetName(selectedSetName)  # Retrieve the set ID based on selection
        word = wordBox.get()
        definition = definitionBox.get()
        
        if setID is not None and word and definition:
            addWords(word, definition, setID)
            messagebox.showinfo("Info", f"Added word '{word}' with definition '{definition}' to set '{selectedSetName}'")
            wordBox.delete(0, END)
            definitionBox.delete(0, END)
        else:
            messagebox.showwarning("Warning", "Please enter both a word and definition.")
    else:
        messagebox.showwarning("Warning", "No set selected to add words.")

Label(tab2, text = "Word:").pack()
wordBox.pack()

Label(tab2, text = "Definition:").pack()
definitionBox.pack()

Button(tab2, text = "Add Word", command = handleAddWord).pack()
# -------

# ---- SelectSet Window ---
# Dropdown Menu for selecting a set
setNamesVar = StringVar(tab3)
setNamesDropdown = ttk.Combobox(tab3, textvariable=setNamesVar)
setNamesDropdown.pack(pady=10)

# Function to update the dropdown menu with available set names
def updateSetDropdown():
    # Fetch all available sets using the new function
    setNames = getAllSetNames()
    setNamesDropdown['values'] = setNames


# Function to show words for the selected set
def showSelectedSet():
    selectedSet = setNamesVar.get()
    if selectedSet:
        setID = getSetName(selectedSet)
        if setID:
            words = getWordsBySetID(setID)  # assuming you add this function in flashcardsDB.py
            # Display words in the selected set
            if words:
                wordsDisplay = "\n".join(f"{word}: {definition}" for word, definition in words)
                wordsLabel = Label(tab3, text=wordsDisplay, justify=LEFT)
                wordsLabel.pack(pady=10)
            else:
                messagebox.showinfo("Info", f"There were no words found in '{selectedSet}'!")
    else:
        messagebox.showwarning("Warning", "No set selected to display.")

def handleDeleteSet():
    selectedSetName = setNamesVar.get()  # Get the selected set name from the dropdown
    if selectedSetName:
        deleteSet(selectedSetName)  # Call the deleteSet function to remove the set
        messagebox.showinfo("Info", f"Deleted Set '{selectedSetName}'")
        updateSetDropdown()  # Refresh the dropdown to reflect changes
    else:
        messagebox.showwarning("Warning", "No set selected for deletion.")

def loadFlashcardsForLearnMode():
    global selectedSetID, currentFlashcards, currentIndex, showingWord
    
    selectedSet = setNamesVar.get()  # Get the selected set name from dropdown
    if selectedSet:
        selectedSetID = getSetName(selectedSet)  # Retrieve set ID for Learn Mode
        if selectedSetID:
            currentFlashcards = getWordsBySetID(selectedSetID)
            currentIndex = 0
            showingWord = True
            displayFlashcard()  # Display the first flashcard
        else:
            messagebox.showerror("Error", f"No set found with name '{selectedSet}'")
    else:
        messagebox.showwarning("Warning", "No set selected.")

Button(tab3, text = "Show Set", command = showSelectedSet).pack()
Button(tab3, text="Load in Learn Mode", command=loadFlashcardsForLearnMode).pack(pady=10)
Button(tab3, text = "Delete Set", command = handleDeleteSet).pack()
# -------

# ---- LearnMode Window ---
currentFlashcards = []  # Stores the (word, definition) pairs for the selected set
currentIndex = 0        # Tracks the current flashcard index
showingWord = True      # Tracks whether we're showing the word or the definition
flashcardLabel = None


def displayFlashcard():
    if currentFlashcards:
        word, definition = currentFlashcards[currentIndex]
        text = word if showingWord else definition
        flashcardLabel.config(text=text)
    else:
        flashcardLabel.config(text="No flashcards available.")


def flipFlashcard():
    global showingWord
    showingWord = not showingWord  # Toggle between word and definition
    displayFlashcard()

def nextFlashcard():
    global currentIndex, showingWord
    if currentFlashcards and currentIndex < len(currentFlashcards) - 1:
        currentIndex += 1
        showingWord = True  # Reset to show the word first
        displayFlashcard()

def previousFlashcard():
    global currentIndex, showingWord
    if currentFlashcards and currentIndex > 0:
        currentIndex -= 1
        showingWord = True  # Reset to show the word first
        displayFlashcard()

flashcardLabel = Label(tab4, text="", font=("Helvetica", 18), wraplength=400, justify=CENTER)
flashcardLabel.pack(pady=20)

Button(tab4, text="Flip", command=flipFlashcard).pack(side=LEFT, padx=10)
Button(tab4, text="Previous", command=previousFlashcard).pack(side=LEFT, padx=10)
Button(tab4, text="Next", command=nextFlashcard).pack(side=LEFT, padx=10)
# -------

tabs.pack()
atexit.register(closeConnection)
window.mainloop()