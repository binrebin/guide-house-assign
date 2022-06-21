from tkinter import *
from tkinter import filedialog

from db_func import *

def add_command():
    insert(f_name.get(),
                    m_name.get(),
                    l_name.get(), 
                    address_1.get(),
                    city.get(),
                    state.get(),
                    ph_num.get())
    listing.delete(0, END)
    listing.insert(END, 
                    (f_name.get(), 
                    m_name.get(), 
                    l_name.get(), 
                    address_1.get(),
                    city.get(),
                    state.get(),
                    ph_num.get()
                    ))

def view_command():
    listing.delete(0, END)
    for row in view():
        listing.insert(END, row)

def delete_command():
    listing.delete(0, END)
    delete(selected_tuple[0])

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

    entry2.delete(0, END)
    entry2.insert(END, selected_tuple[2])

    entry3.delete(0, END)
    entry3.insert(END, selected_tuple[3])

    entry4.delete(0, END)
    entry4.insert(END, selected_tuple[4])

    entry5.delete(0, END)
    entry5.insert(END, selected_tuple[5])

    entry6.delete(0, END)
    entry6.insert(END, selected_tuple[6])

    entry7.delete(0, END)
    entry7.insert(END, selected_tuple[7])



window = Tk()

window.wm_title("Address book for Guide House")

# Labels for entry fields.
label1 = Label(window, text = "Firstname")
label1.grid(row = 0, column = 0)

label2 = Label(window, text = "Middlename")
label2.grid(row = 0, column = 2)

label3 = Label(window, text = "Lastname")
label3.grid(row = 1, column = 0)

label4 = Label(window, text = "Address 1")
label4.grid(row = 1, column = 2)

label5 = Label(window, text = "City")
label5.grid(row = 2, column = 0)

label6 = Label(window, text = "State")
label6.grid(row = 2, column = 2)

label7 = Label(window, text = "Phone number")
label7.grid(row = 3, column = 0)

# Entry Fields.
f_name = StringVar()
entry1 = Entry(window, textvariable = f_name)
entry1.grid(row = 0, column = 1)

m_name = StringVar()
entry2 = Entry(window, textvariable = m_name)
entry2.grid(row = 0, column = 3)

l_name = StringVar()
entry3 = Entry(window, textvariable = l_name)
entry3.grid(row = 1, column = 1)

address_1 = StringVar()
entry4 = Entry(window, textvariable = address_1)
entry4.grid(row = 1, column = 3)

city = StringVar()
entry5 = Entry(window, textvariable = city)
entry5.grid(row = 2, column = 1)

state = StringVar()
entry6 = Entry(window, textvariable = state)
entry6.grid(row = 2, column = 3)

ph_num = StringVar()
entry7 = Entry(window, textvariable = ph_num)
entry7.grid(row = 3, column = 1)

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
                text = "View All", 
                width = 12, 
                command = view_command)
button1.grid(row = 6, column = 3)

button2 = Button(window, 
                text = "Add Entry", 
                width = 12, 
                command = add_command)
button2.grid(row = 7, column = 3)

button3 = Button(window, 
                text = "Delete Selected", 
                width = 12, 
                command = delete_command)
button3.grid(row = 8, column = 3)

button4 = Button(window, 
                text = "Download CSV", 
                width = 12, 
                command = download_db)
button4.grid(row = 9, column = 3)

button5 = Button(window, 
                text = "Upload via CSV", 
                width = 12, 
                command = upload_csv)
button5.grid(row = 10, column = 3)

button6 = Button(window, 
                text = "Close", 
                width = 12, 
                command = window.destroy)
button6.grid(row = 11, column = 3)

# Keep window open until closed.
window.mainloop()