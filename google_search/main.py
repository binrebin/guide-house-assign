from tkinter import *
from tkinter import filedialog

from db_func import *



def search_and_save():
    global page
    page = 1
    insert(s_term.get(), page)
    listing.delete(0, END)
    listing.insert(END, (s_term.get()))
    label2['text'] = f"Page - {page}"

def prev_page():
    global page
    page = page -1 if page < 2 else 1
    insert(s_term.get(), page )
    listing.delete(0, END)
    listing.insert(END, (s_term.get()))
    label2['text'] = f"Page - {page}"

def next_page():
    global page
    page = page + 1 if page < 50 else 50
    insert(s_term.get(), page )
    listing.delete(0, END)
    listing.insert(END, (s_term.get()))
    label2['text'] = f"Page - {page}"

def download_db():
    download_csv()
    

def upload_csv(event=None):
    filename = filedialog.askopenfilename()
    insert_csv(filename)
    listing.delete(0, END)
    for row in view():
        listing.insert(END, row)

def get_selected_row(event):

    global selected_tuple
    index = listing.curselection()[0]
    selected_tuple = listing.get(index)

    entry1.delete(0, END)
    entry1.insert(END, selected_tuple[1])



window = Tk()

window.wm_title("Google Search for Guide House")

# Labels for entry fields.
label1 = Label(window, text = "Search Google")
label1.grid(row = 0, column = 0)

label2 = Label(window, text = "Page - ")
label2.grid(row = 0, column = 2)


# Entry Fields.
s_term = StringVar()
entry1 = Entry(window, textvariable = s_term)
entry1.grid(row = 0, column = 1)


# List all data.
listing = Listbox(window, height = 9, width = 35)
listing.grid(row = 6, column = 0, rowspan = 6, columnspan = 2)

# Scrollbar.
scroller = Scrollbar(window)
scroller.grid(row = 6, column = 2, rowspan = 6)

# Configure scrollbar for Listbox.
listing.configure(yscrollcommand = scroller.set)
scroller.configure(command = listing.yview)

listing.bind('<<ListboxSelect>>', get_selected_row)

# Buttons for various operations on data.
button1 = Button(window, 
                text = "Go", 
                width = 12, 
                command = search_and_save)
button1.grid(row = 6, column = 3)

button2 = Button(window, 
                text = "Previous Page", 
                width = 12, 
                command = prev_page)
button2.grid(row = 7, column = 3)

button3 = Button(window, 
                text = "Next Page", 
                width = 12, 
                command = next_page)
button3.grid(row = 8, column = 3)

button4 = Button(window, 
                text = "Close", 
                width = 12, 
                command = window.destroy)
button4.grid(row = 9, column = 3)

# Keep window open until closed.
window.mainloop()