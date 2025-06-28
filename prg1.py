import customtkinter as ctk
import tkinter as tk
import sqlite3
import random
import database as db
from tkinter import ttk
import tkinter.messagebox as messagebox
import threading
from ticketTurbo import get_driver, account_login, scrape_events_data, proxies

db.init_db()

def showFrame(frame):
    frame.lift()

def change_cursor(event):
    column = event.widget.identify_column(event.x)
    if column in ('#4', '#5'):
        event.widget.config(cursor='hand2')
    else:
        event.widget.config(cursor='')

def change_cursor2(event):
    column = event.widget.identify_column(event.x)
    if column in ('#6', '#7'):
        event.widget.config(cursor='hand2')
    else:
        event.widget.config(cursor='')


def extract_numeric_part(item_id):
    numeric_part = ''.join(filter(str.isdigit, item_id))
    return int(numeric_part)

def get_item_by_id(tree, item_id):
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if values[0] == item_id:  # Assuming ID is stored in the first column
            return item
    return None

def get_values_by_id(tree, item_id):
    for item in tree.get_children():
        values = tree.item(item, 'values')
        if values and values[0] == item_id:  # Check if values is not None before accessing the first element
            return values
    return None

def get_values_by_id2(tree, item_id):
    for item in tree.get_children():
        values = tree.item(item, 'values')
        print("====> Values are:", values)
        if values and values[1] == item_id:  # Check if values is not None before accessing the first element
            return values
    return None

def get_website_column(tree):
    websites = []
    for child in tree.get_children():
        website = tree.item(child)['values'][1]
        websites.append(website)
    return websites

def get_website_column_with_ids(tree):
    website_data = []
    for child in tree.get_children():
        website_id = tree.item(child)['values'][0]
        website_name = tree.item(child)['values'][1]
        website_data.append((website_id,website_name))
    return website_data

def optionmenu_callback(choice):
    if choice == "Show More ...":
        show_more_websites()
    elif choice == "Show All":
        tree3_new.place_forget()
        tree3.place(x=0, y=80, width=630, relheight=0.77)
    else:
        website_id ,website_name = choice.split(":")  # Split the selected option into name and ID
        print("Selected Website Name:", website_name)
        print("Selected Website ID:", website_id)
        select_id_in_tree3(website_id)

wsite_id = ''
def optionmenu_callback2(choice):
    if choice == "Show More ...":
        show_more_websites2()
    elif choice == "Show All":
        tree3_new.place_forget()
        tree3.place(x=0, y=80, width=630, relheight=0.77)
    else:
        website_id ,website_name = choice.split(" : ")  # Split the selected option into name and ID
        print("Selected Website Name:", website_name)
        print("Selected Website ID:", website_id)
        global wsite_id
        wsite_id = website_id

def select_id_in_tree3(website_id):
    for item in tree3_new.get_children():
        tree3_new.delete(item)
    for row in tree3.get_children():
        #print(type(tree3.item(row, "values")[1]))
        if tree3.item(row, "values")[1] == website_id:
            values = tree3.item(row, "values")
            tree3_new.insert("", "end", iid=tree3.item(row, "values")[0], values=values, tags=('search', 'odd_row',))
            tree3_new.place(x=0, y=80, width=630, relheight=0.77)
        else:
            pass

def select_id_in_tree3_1(website_id):
    for item in tree3_new.get_children():
        tree3_new.delete(item)
    for row in tree3.get_children():
        #print(type(tree3.item(row, "values")[1]))
        if tree3.item(row, "values")[1] == website_id:
            values = tree3.item(row, "values")
            tree3_new.insert("", "end", iid=tree3.item(row, "values")[0], values=values, tags=('search', 'odd_row',))
            tree3_new.place(x=0, y=80, width=630, relheight=0.77)
        else:
            pass


def label_click(event):
    label_text = event.widget.cget("text")
    website_id = label_text.split(" :")[0]
    select_id_in_tree3(website_id)

def show_more_websites():

    more_window = ctk.CTkToplevel(app ,fg_color="#161616")
    more_window.geometry("300x400")
    more_window.geometry("+450+150")
    more_window.title("More Websites")

    more_window.attributes('-topmost', True)

    scrollable_frame = ctk.CTkScrollableFrame(more_window, width=280, height=400, fg_color="#161616")
    scrollable_frame.pack(fill=tk.BOTH, expand=True)
    website_data = get_website_column_with_ids(tree2)[3:]
    website_options = [f"{id} :{name}" for id, name in website_data]
    for website in website_options:
        website_label = ctk.CTkLabel(scrollable_frame, text=website, text_color="#fff", font=('inter', 16, 'normal') ,cursor="hand2", width=300, height=40, justify="center")
        website_label.pack(anchor=tk.W)
        website_label.bind("<Button-1>", label_click)


def show_more_websites2():

    more_window2 = ctk.CTkToplevel(app, fg_color="#161616")
    more_window2.geometry("300x400")
    more_window2.geometry("+450+150")
    more_window2.title("More Websites")

    more_window2.attributes('-topmost', True)

    scrollable_frame = ctk.CTkScrollableFrame(more_window2, width=280, height=400, fg_color="#161616")
    scrollable_frame.pack(fill=tk.BOTH, expand=True)
    website_data = get_website_column_with_ids(tree2)[3:]
    website_options = [f"{id} :{name}" for id, name in website_data]
    for website in website_options:
        website_label = ctk.CTkLabel(scrollable_frame, text=website, text_color="#fff", font=('inter', 16, 'normal') ,cursor="hand2", width=300, height=40, justify="center")
        website_label.pack(anchor=tk.W)
        website_label.bind("<Button-1>", lambda event: label_click2(event, more_window2))

def label_click2(event, more_window2):
    label_text = event.widget.cget("text")
    website_id = label_text.split(" :")[0]
    global wsite_id
    wsite_id = website_id
    more_window2.destroy()


def edit_row(row_id):
    tree2.place_forget()
    tree2_new.place_forget()
    numeric_part = extract_numeric_part(row_id)
    print(f"Editing row {numeric_part}")

    values = get_values_by_id(tree2, str(numeric_part))

    print(values)

    if values is None:
        # Handle the case where values are not retrieved successfully
        print("Error: Unable to retrieve values for row_id:", row_id)
        return

    edit_frame.place(x=0, y=80,relheight=0.77)

     #label_test = ctk.CTkLabel(edit_frame , text="Hello", fg_color="#161616",text_color="#9D0D0D")

     #label_test.place(x=0, y =0)

    entries = []
    for i, value in enumerate(values[1:3], start=1):
        width = 180 if i == 1 else 150
        x = 100 if i == 1 else 280
        entry = ctk.CTkEntry(edit_frame, fg_color="#161616", bg_color="#161616",
                      text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0, justify="center" , height=40, width=width)
        entry.insert(0, value)
        entry.place(x=x, y=50)  # Adjust the position as needed
        entries.append(entry)

    # Create a button to update the row
    update_button = ctk.CTkButton(edit_frame, text="Update", font=('inter', 16, 'normal'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=36, corner_radius=0,
                     hover_color="#fcc603", command=lambda: update_row(str(numeric_part), entries))
    update_button.place(x=450, y=52)

def edit_row2(row_id):
    tree3.place_forget()
    tree3_new.place_forget()
    numeric_part = extract_numeric_part(row_id)
    print(f"Editing row {numeric_part}")

    values = get_values_by_id(tree3, row_id)

    print(values)

    if values is None:
        # Handle the case where values are not retrieved successfully
        print("Error: Unable to retrieve values for row_id:", row_id)
        return

    edit_frame2.place(x=0, y=80,relheight=0.77)

     #label_test = ctk.CTkLabel(edit_frame , text="Hello", fg_color="#161616",text_color="#9D0D0D")

     #label_test.place(x=0, y =0)

    entries = []
    for i, value in enumerate(values[3:5], start=1):
        width = 180 if i == 1 else 150
        x = 100 if i == 1 else 280
        entry = ctk.CTkEntry(edit_frame2, fg_color="#161616", bg_color="#161616",
                      text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0, justify="center" , height=40, width=width)
        entry.insert(0, value)
        entry.place(x=x, y=50)  # Adjust the position as needed
        entries.append(entry)

    # Create a button to update the row
    update_button = ctk.CTkButton(edit_frame2, text="Update", font=('inter', 16, 'normal'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=36, corner_radius=0,
                     hover_color="#fcc603", command=lambda: update_row2(row_id, entries))
    update_button.place(x=450, y=52)

def update_row(row_id, entries):
    # Get the updated values from entry widgets
    new_values = [entry.get() for entry in entries[:2]]
    print(f"row id is : {row_id}")
    print(type(row_id))
    current_values = get_values_by_id(tree2, row_id)
    print(current_values)
    updated_values = [current_values[0]] + new_values + [current_values[3], current_values[4]]
    print(updated_values)
    # Update the treeview with the new values
    tree2.item(get_item_by_id(tree2, row_id), values=updated_values)

    edit_frame.place_forget()
    # Show the treeview again
    tree2.place(x=0, y=80, width=630, relheight=0.6)

def update_row2(row_id, entries):
    # Get the updated values from entry widgets
    new_values = [entry.get() for entry in entries[:2]]
    print(f"row id is : {row_id}")
    print(type(row_id))
    current_values = get_values_by_id(tree3, row_id)
    print("hi")
    print(current_values)
    updated_values = [current_values[0], current_values[1], current_values[2]] + new_values + [current_values[5], current_values[6]]
    print(updated_values)
    
    db.insert_account(current_values[1], current_values[2], new_values[0], new_values[1])
    # db.update_account(current_values[1], current_values[2], new_values[0], new_values[1])
    # Update the treeview with the new values
    tree3.item(get_item_by_id(tree3, row_id), values=updated_values)

    edit_frame2.place_forget()
    # Show the treeview again
    tree3.place(x=0, y=80, width=630, relheight=0.77)

selection = ''
def delete_row(row_id):
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this row?")
    if confirm:
       tree2.delete(row_id)
       refresh_tree2_new()

def delete_row2(row_id):
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this row?")
    if confirm:
       tree3.delete(row_id)
       refresh_tree3_new()
def refresh_tree2_new():
    # Clear existing data in tree2_new
    for item in tree2_new.get_children():
        tree2_new.delete(item)

    # Insert updated data from tree2
    for child_item in tree2.get_children():
        values = tree2.item(child_item, 'values')
        tree2_new.insert("", "end", values=values , tags=('search', 'odd_row',))

def refresh_tree3_new():
    # Clear existing data in tree2_new
    for item in tree3_new.get_children():
        tree3_new.delete(item)

    # Insert updated data from tree2
    for child_item in tree3.get_children():
        values = tree3.item(child_item, 'values')
        tree2_new.insert("", "end", values=values , tags=('search', 'odd_row',))

def on_tree_click(event):

        item = tree2.identify_row(event.y)

        global selection

        selection = item

        on_button_click(event)



def on_tree_click2(event):

    item = tree2_new.identify_row(event.y)

    item_id = tree2_new.item(item, 'values')[0]

    print(f" item id is : {item_id}")
    for child_item2 in tree2_new.get_children():
        print(f"the item is : {tree2_new.item(child_item2, 'values')[0]}")

    print(f"item_id is {item_id}")

    # Iterate through all items in tree2 to find the item with the same ID

    for child_item in tree2.get_children():
        print(child_item)
        # Retrieve the ID of each item in tree2
        child_item_id = tree2.item(child_item, 'values')[0]
        # Check if the ID of the current item matches the ID of the selected item
        if child_item_id == item_id:
            # Do something with the item in tree2 with the same ID
            # For example, select the item
            global selection
            selection = child_item
            print(f"item is {selection}")
            break  # Stop iterating once the item is found

    on_button_click(event)


def on_tree_click3(event):

    item = tree3.identify_row(event.y)

    global selection

    selection = item

    print("yes")

    on_button_click2(event)

def on_tree_click4(event):

    item = tree3_new.identify_row(event.y)

    item_id = tree3_new.item(item, 'values')[0]

    print(f" item id is : {item_id}")
    for child_item2 in tree3_new.get_children():
        print(f"the item is : {tree3_new.item(child_item2, 'values')[0]}")

    print(f"item_id is {item_id}")

    # Iterate through all items in tree2 to find the item with the same ID

    for child_item in tree3.get_children():
        print(child_item)
        # Retrieve the ID of each item in tree2
        child_item_id = tree3.item(child_item, 'values')[0]
        # Check if the ID of the current item matches the ID of the selected item
        if child_item_id == item_id:
            # Do something with the item in tree2 with the same ID
            # For example, select the item
            global selection
            selection = child_item
            print(f"item is {selection}")
            break  # Stop iterating once the item is found

    on_button_click2(event)

def on_button_click(event):
    global selection
    selection1 = selection
    print(f"selection is {selection}")
    if selection1:
        # Si un élément est sélectionné, récupérer l'élément et identifier la colonne du clic
        item_id = tree2.item(selection1, 'values')
        print(item_id)
        column = tree2.identify_column(event.x)
        if column == "#4":
            edit_row(item_id)
        elif column == "#5":
            delete_row(selection1)
    else:
        print("Aucun élément sélectionné")

def on_button_click2(event):
    global selection
    selection1 = selection
    print(f"selection is {selection}")
    if selection1:
        # Si un élément est sélectionné, récupérer l'élément et identifier la colonne du clic
        item_id = tree3.item(selection1, 'values')[0]
        print(item_id)
        column = tree3.identify_column(event.x)
        if column == "#6":
            edit_row2(item_id)
        elif column == "#7":
            print(selection1)
            delete_row2(selection1)
    else:
        print("Aucun élément sélectionné")


def add_wsite():
    add_wsite_frame.place(x=20, rely=0.79)

def f_add_wsite():
    add_wsite_frame.place_forget()
def save_wsite():
    wsite = entry_wsite.get()
    category = entry_wcategory.get()
    print(f"Website is {wsite} and category is {category}")
    add_wsite_frame.place_forget()
    last_N_value = 0
    for child in tree2.get_children():
        values = tree2.item(child, 'values')
        if values and values[0]:
            last_N_value = max(last_N_value, int(values[0]))
    new_N_value = last_N_value + 1
    if wsite != '':
        tree2.insert('', 'end', values=(new_N_value,wsite, category, 'Edit', 'Delete') , tags=('odd_row',))
        label_message.place(x=20, rely=0.77)
        frame2.after(2000, hide_message)
    else:
        label_error2.place(x=20, rely=150)
        frame2.after(2000, hide_message)

def hide_message():
    label_message.place_forget()
    label_error2.place_forget()

def back():
    frame4.lower()
    frame5.lower()
    frame6.lower()
    frame7.lower()
    frame8.lower()


def back2():
    frame4.lift()

def back3():
    frame6.lift()

def bye():
    main_frame.lift()
    entry1.delete(0, 'end')

def destory_label_text():
    label_wait.configure(width=0)
    frame6.lift()

def change_label_text():
    label_wait.configure(text="Your Data has Been Added")
    app.after(2000, destory_label_text)

def login_and_scrape(mail, password):
    event_link = entry_add.get()
    print("Event Link is:", event_link)
    
    proxy_id = random.randint(0, len(proxies) - 1)
    print("Using Proxy ID:", proxy_id)
    driver = get_driver(proxy_id)
    
    account_login(driver, mail, password)
    events_data = scrape_events_data(driver, event_link)
    insert_into_tree4(events_data)
    
    change_label_text()
    
def login_site():
    values = get_values_by_id2(tree3, wsite_id)
    mail = values[3] if values else None
    password = values[4] if values else None
    if mail and password:
        frame4.lower()
        frame5.lift()
        label_wait.configure(width=400, text="Please Wait ... Logging In & Scraping Events Data")
        label_wait.place(relx=0.5, rely=0.41, anchor="center")
        #choose a random proxy from the list
        
        threading.Thread(target=login_and_scrape, args=(mail, password)).start()
    else:
        print("No Login & Mail Password Found!!!")
        label_error3.place(relx=0.5, y=115, anchor="center")

total_budget = 0

def update_total_budget_label():
    label_select.configure(text=f"Total Budget is: {total_budget}")

def calculate_total():

    more_window3 = ctk.CTkToplevel(app, fg_color="#161616")
    more_window3.geometry("680x400")
    more_window3.geometry("+450+150")
    more_window3.title("Calculate The Total")
    more_window3.transient(app)
    more_window3.attributes('-topmost', True)

    scrollable_frame3 = ctk.CTkScrollableFrame(more_window3, width=280, fg_color="#161616")
    scrollable_frame3.pack(fill=tk.BOTH, expand=True)

    btn_cl = ctk.CTkButton(master=scrollable_frame3, text="Calculate Total", font=('inter', 16, 'bold'), fg_color="#E5B302",
                              text_color="#000", cursor='hand2', anchor="center", height=40, width=190, corner_radius=0,
                              hover_color="#fcc603", command=calculate_total2)

    btn_cl.place(x=450, rely=0.5)

    label = ctk.CTkLabel(scrollable_frame3, text="Name of event", fg_color="#161616",text_color="#fff", width=100)
    label.pack(fill=tk.X, padx=(0, 490), pady=4)

    label2 = ctk.CTkLabel(scrollable_frame3, text="Ticket Price", fg_color="#161616", text_color="#fff", width=100)
    label2.place(x=150, y=4)

    label3 = ctk.CTkLabel(scrollable_frame3, text="Qty", fg_color="#161616", text_color="#fff", width=100)
    label3.place(x=320, y=4)

    label1 = ctk.CTkLabel(scrollable_frame3, text="Name of event", fg_color="#161616",text_color="#fff",width=100)

    #label1.pack(fill=tk.X, padx=(393, 180), pady=4)
    for i, child in enumerate(tree4.get_children()):
        name = tree4.item(child, "values")[0]
        price = tree4.item(child, "values")[1]
        label = ctk.CTkLabel(scrollable_frame3, text=f"{name}",  fg_color="#161616",text_color="#fff" ,width=100)
        label.pack(fill=tk.X, padx=(0, 500), pady=6)
        label2 = ctk.CTkLabel(scrollable_frame3, text=f"{price}", fg_color="#161616", text_color="#fff", width=100)
        label2.place(x=150, y=43 + i * 40)
        entry = ctk.CTkEntry(scrollable_frame3, width=50, height=33, fg_color="#161616", bg_color="#161616",
                             text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0,
                             justify="center")
        entry.place(x=350, y=40 + i * 40)
        tree4_entries.append(entry)


    global total_budget

    total_budget = 0

    for i, child in enumerate(tree4.get_children()):

        row_values = tree4.item(child, 'values')

        ticket_price_str = row_values[1]

        ticket_price = ticket_price_str.replace('$', '').replace(',', '')

        entry_value = tree4_entries[i].get()
        entry_value = int(entry_value) if entry_value else 0

        total_value = float(ticket_price) * entry_value

        tree4.set(child,'Total', total_value)

        total_budget += total_value

        update_total_budget_label()

def calculate_total2():

    global total_budget

    total_budget = 0

    for i, child in enumerate(tree4.get_children()):

        row_values = tree4.item(child, 'values')

        ticket_price_str = row_values[1]

        ticket_price = ticket_price_str.replace('$', '').replace(',', '')

        entry_value = tree4_entries[i].get()

        entry_value = int(entry_value) if entry_value else 0

        total_value = float(ticket_price) * entry_value

        tree4.set(child, 'Qty', entry_value)

        tree4.set(child, 'Total', total_value)

        total_budget += total_value

        update_total_budget_label()

def payement():
    frame6.lower()
    frame7.lift()

def pay():
    frame8.lift()

app = ctk.CTk()

app.config(bg="#161616")

app.geometry("820x480")

main_frame = ctk.CTkFrame(master=app, fg_color="#161616", bg_color="#161616")
main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

label_error = ctk.CTkLabel(main_frame, text="Please type a valid serial to enter to Bot", fg_color="#161616",
                           text_color="#9D0D0D")

bot_ready_frame = ctk.CTkFrame(app, fg_color="#161616", bg_color="#161616")

frame4 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=820)
frame4.place(x=0, rely=0, relheight=1)

frame5 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=820)
frame5.place(x=0, rely=0, relheight=1)

frame6 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=820)

frame6.place(x=0, rely=0, relheight=1)

frame7 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=820)

frame7.place(x=0, rely=0, relheight=1)

frame8 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=820)

frame8.place(x=0, rely=0, relheight=1)


label_done = ctk.CTkLabel(frame8, text="Done.", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", anchor="nw")

label_done.place(relx=0.4, rely=0.5, anchor="center")

btn_back3 = ctk.CTkButton(master=frame7, text="Back", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw" ,command=back3)
btn_back3.place(x=45, y=37)

btn_back4 = ctk.CTkButton(master=frame8, text="Done Click To back", font=('inter', 15, 'normal'), fg_color="#161616",text_color="#E5B302", hover=False, cursor='hand2', anchor="nw" ,command=back2)

btn_back4.place(relx=0.51, rely=0.494, anchor="center")

label_log = ctk.CTkLabel(frame7, text="PayPal Login", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", anchor="nw")

label_log.place(relx=0.5, rely=0.25, anchor="center")

log_pay = ctk.CTkEntry(frame7 ,width=320, font=('Inter', 16), height=48, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=1,placeholder_text="Email or mobile number", justify="left")

log_pay.place(relx=0.5, rely=0.35, anchor="center")

log_pay_ps = ctk.CTkEntry(frame7 ,width=320, font=('Inter', 16), height=48, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=1,placeholder_text="Password", justify="left", show="*")

log_pay_ps.place(relx=0.5, rely=0.49, anchor="center")

log_btn = ctk.CTkButton(master=frame7, text="Login", font=('inter', 16, 'bold'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=40, width=190, corner_radius=0,
                     hover_color="#fcc603",command=pay)

log_btn.place(relx=0.5, rely=0.65, anchor="center")

btn_back = ctk.CTkButton(master=frame4, text="Back", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw" ,command=back)
btn_back.place(x=45, y=37)

btn_back2 = ctk.CTkButton(master=frame6, text="Back", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw" ,command=back2)
btn_back2.place(x=45, y=37)

label_step = ctk.CTkLabel(master=frame4, text="Step 1 of 3", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", anchor="nw")

label_step.place(relx=0.77, y=44)

label_step2 = ctk.CTkLabel(master=frame6, text="Step 2 of 3", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#fafafa", anchor="nw")

label_step2.place(relx=0.77, y=44)

label_error3 = ctk.CTkLabel(frame4,  font=('inter', 15, 'normal') ,text="Please Select a website",
                            fg_color="#161616",text_color="#9D0D0D")

label_wait = ctk.CTkLabel(master=frame5, font=('inter', 15, 'normal'), text="Please Wait ... Data of your link is coming to this server", text_color="#e6e6e6" , width=400)

side_frame = ctk.CTkFrame(master=bot_ready_frame, fg_color="#232323", bg_color="#232323", width=190)
side_frame.place(relx=0, rely=0, relheight=1)

frame1 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=630)
frame1.place(x=190, rely=0, relheight=1)

frame2 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=630)
frame2.place(x=190, rely=0, relheight=1)

frame3 = ctk.CTkFrame(master=bot_ready_frame, fg_color="#161616", bg_color="#161616", width=630)
frame3.place(x=190, rely=0, relheight=1)

edit_frame = ctk.CTkFrame(frame2,fg_color="#161616", bg_color="#161616", width=630)

edit_frame2 = ctk.CTkFrame(frame3,fg_color="#161616", bg_color="#161616", width=630)

style = ttk.Style(app)

style.theme_use('default')

# Configure the Treeview widget
style.configure('Treeview', foreground='#fff', background='#161616', fieldbackground='#161616', font=('Arial', 10))
style.map('Treeview.Heading', background=[('active', '#161616')])
style.configure('Treeview.Heading', foreground='#fff', background='#161616', padding=(6, 6),
                font=('Arial', 11, 'normal'), relief='flat')

style2 = ttk.Style(app)

style2.theme_use('default')

# Configure the Treeview widget for the new style
# style2.configure('Custom2.Treeview', foreground='#000', background='#161616', fieldbackground='#161616',
#                  font=('Arial', 12), borderwidth=0, bordercolor='#161616', rowheight=42)
style2.configure('Custom2.Treeview', foreground='#ffffff', background='#161616', fieldbackground='#161616',
                 font=('Arial', 12), borderwidth=0, bordercolor='#161616', rowheight=42)
style2.map('Custom2.Treeview', background=[('active', '#272727')])
style2.map('Custom2.Treeview.Heading', background=[('active', '#272727')])
style2.configure('Custom2.Treeview.Heading', foreground='#fff', background='#272727', padding=(6, 10),
                 font=('Arial', 11, 'bold'), borderwidth=0)

tree1 = ttk.Treeview(frame1, height=15, style='Treeview')

tree1['columns'] = ('N', 'WebSite', 'Accounts', 'Reserved', 'Spent')

tree1.column('#0', width=0, stretch=tk.NO)
tree1.column('N', anchor=tk.CENTER, width=60, stretch=False)
tree1.column('WebSite', anchor=tk.CENTER, width=160)
tree1.column('Accounts', anchor=tk.CENTER, width=100)
tree1.column('Reserved', anchor=tk.CENTER, width=100)
tree1.column('Spent', anchor=tk.CENTER, width=100)

tree1.heading('N', text='ID')
tree1.heading('WebSite', text='WebSite', anchor="w")
tree1.heading('Accounts', text='Accounts')
tree1.heading('Reserved', text='Reserved')
tree1.heading('Spent', text='Spent')

tree1.place(x=40, y=80, width=550, relheight=0.77)

separator = tk.Canvas(tree1, background='#808080', height=1, highlightthickness=0)
separator.place(relx=0, y=34, relwidth=1)

style2.configure('OddRow.Custom2.Treeview', background='#f0f0f0')

tree2 = ttk.Treeview(frame2, height=18, style='Custom2.Treeview', cursor="hand2", selectmode="extended")

tree2['columns'] = ('N', 'WebSite', 'Category', 'Edit', 'Delete')

tree2.column('#0', width=0, stretch=tk.NO)
tree2.column('N', anchor=tk.CENTER, width=60, stretch=False)
tree2.column('WebSite', anchor=tk.W, width=160)
tree2.column('Category', anchor=tk.CENTER, width=100)
tree2.column('Edit', anchor=tk.CENTER, width=100)
tree2.column('Delete', anchor=tk.W, width=100)

tree2.heading('N', text='N')
tree2.heading('WebSite', text='WebSite', anchor="w")
tree2.heading('Category', text='Category')
tree2.heading('Edit', text='Actions', anchor="e")


tree2_new = ttk.Treeview(frame2, height=6, style='Custom2.Treeview', cursor="hand2", selectmode="extended")

tree2_new['columns'] = ('N', 'WebSite', 'Category', 'Edit', 'Delete')

tree2_new.column('#0', width=0, stretch=tk.NO)
tree2_new.column('N', anchor=tk.CENTER, width=60, stretch=False)
tree2_new.column('WebSite', anchor=tk.W, width=160)
tree2_new.column('Category', anchor=tk.CENTER, width=100)
tree2_new.column('Edit', anchor=tk.CENTER, width=100)
tree2_new.column('Delete', anchor=tk.W, width=100)

tree2_new.heading('N', text='N')
tree2_new.heading('WebSite', text='WebSite', anchor="w")
tree2_new.heading('Category', text='Category')
tree2_new.heading('Edit', text='Actions', anchor="e")

scrollbar2 = tk.Scrollbar(frame2, orient="vertical", command=tree2.yview , bg="#000", width=14)
scrollbar2.place(x=615, y=80, relheight=0.77)

# Configure tree2 to use the scrollbar
tree2.config(yscrollcommand=scrollbar2.set)


tree2.bind('<Motion>', change_cursor)

tree2_new.bind('<Motion>', change_cursor)

tree2.insert('', 'end', text='1', values=(1, 'ticketmaster.com', 'Tech', 'Edit', 'Delete'), tags=('odd_row',))
tree2.insert('', 'end', text='2', values=(2, 'two.com', 'Tech', 'Edit', 'Delete'), tags=('odd_row',))

for i in range(3, 14):
    tree2.insert('', 'end', values=(i, 'example.com', 'Tech', 'Edit', 'Delete'))

for item in tree2.get_children():
    tree2.item(item, tags=('search', 'odd_row',))

tree2.tag_configure('odd_row', background="#161616", foreground="#fff")

tree2_new.tag_configure('odd_row', background="#161616", foreground="#fff")

tree2.place(x=0, y=80, width=630, relheight=0.6)

tree3 = ttk.Treeview(frame3, height=40, style='Custom2.Treeview', cursor="hand2", selectmode="extended")

tree3['columns'] = ('N','ID_Website' ,'WebSite' ,'Mail', 'Password', 'Edit','Delete')

tree3.column('#0', width=0, stretch=tk.NO)
tree3.column('N', anchor=tk.CENTER, width=60, stretch=False)
tree3.column('ID_Website', width=0, stretch=tk.NO)
tree3.column('WebSite', anchor=tk.W, width=160)
tree3.column('Mail', anchor=tk.CENTER, width=100)
tree3.column('Password', anchor=tk.CENTER, width=100)
tree3.column('Edit', anchor=tk.CENTER, width=100)
tree3.column('Delete', anchor=tk.W, width=100)

tree3.heading('N', text='N')
tree3.heading('WebSite', text='WebSite', anchor="w")
tree3.heading('Mail', text='Mail')
tree3.heading('Password', text='Password')
tree3.heading('Edit', text='Actions', anchor="e")


tree3_new = ttk.Treeview(frame3, height=40, style='Custom2.Treeview', cursor="hand2", selectmode="extended")

tree3_new['columns'] = ('N','ID_Website' ,'WebSite' ,'Mail', 'Password', 'Edit','Delete')

tree3_new.column('#0', width=0, stretch=tk.NO)
tree3_new.column('N', anchor=tk.CENTER, width=60, stretch=False)
tree3_new.column('ID_Website', width=0, stretch=tk.NO)
tree3_new.column('WebSite', anchor=tk.W, width=160)
tree3_new.column('Mail', anchor=tk.CENTER, width=100)
tree3_new.column('Password', anchor=tk.CENTER, width=100)
tree3_new.column('Edit', anchor=tk.CENTER, width=100)
tree3_new.column('Delete', anchor=tk.W, width=100)

tree3_new.heading('N', text='N')
tree3_new.heading('WebSite', text='WebSite', anchor="w")
tree3_new.heading('Mail', text='Mail')
tree3_new.heading('Password', text='Password')
tree3_new.heading('Edit', text='Actions', anchor="e")


db_accounts = db.get_all_accounts()

# for i in range(10):
#     tree3.insert('', 'end', values=(f'N{i}' , f'{i}' , f'Website {i}', f'Mail {i}', f'Password {i}', f'Edit {i}', f'Delete {i}') ,tags=('odd_row',))


for i in range(len(db_accounts)):
    tree3.insert('', 'end', values=(f'N{i+1}', i+1, db_accounts[i][1], db_accounts[i][2], db_accounts[i][3], 'Edit', 'Delete'), tags=('odd_row',))


tree3.tag_configure('odd_row', background="#161616", foreground="#fff")

tree3_new.tag_configure('odd_row', background="#161616", foreground="#fff")

tree3.place(x=0, y=80, width=630, relheight=0.77)

#tree3.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame3, orient="vertical", command=tree3.yview , bg="#000", width=14)
scrollbar.place(x=615, y=80, relheight=0.77)

tree3.config(yscrollcommand=scrollbar.set)

tree3.bind('<Motion>', change_cursor2)

tree3_new.bind('<Motion>', change_cursor2)

tree3.bind('<ButtonRelease-1>', on_tree_click3)

tree3_new.bind('<ButtonRelease-1>', on_tree_click4)


xc = (frame6.cget("width") - 630) / 2

#scrollable_frame1 = ctk.CTkScrollableFrame(frame6, width=630, height=250, fg_color="#161616")
#scrollable_frame1.place(x=xc, y=100)

tree4_frame = ctk.CTkFrame(frame6, width=630 , fg_color="#161616", bg_color="#161616")
tree4_frame.place(x=xc, y=100, relheight=0.65)


tree4 = ttk.Treeview(tree4_frame, style='Custom2.Treeview', cursor="hand2", selectmode="extended", yscrollcommand="None")

tree4['columns'] = ('Name_event','Ticket_price' ,'Qty' ,'Total')

tree4.column('#0', width=0, stretch=tk.NO)
tree4.column('Name_event', anchor=tk.W, width=200, stretch=False)
tree4.column('Ticket_price', width=100, anchor=tk.CENTER)
tree4.column('Qty', anchor=tk.CENTER, width=100)
tree4.column('Total', anchor=tk.CENTER, width=100)

tree4.heading('Name_event', text='Name_event', anchor="w")
tree4.heading('Ticket_price', text='Ticket_price')
tree4.heading('Qty', text='Qty')
tree4.heading('Total', text='Total')

xc = (frame6.cget("width") - 630) / 2

# tree4.tag_configure('odd_row', background="#161616", foreground="#fff")
tree4.tag_configure('odd_row', background="#161616", foreground="#ffffff")

tree4.place(x=0, y=0, relwidth=1, relheight=0.9)

def insert_into_tree4(events_data):
    # tree4.insert("", tk.END, values=("Event 1", "$20", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 2", "$25", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 3", "$30", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 4", "$100", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 5", "$55", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 6", "$230", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 7", "$10", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 8", "$10", "", "") , tags=('odd_row',))
    # tree4.insert("", tk.END, values=("Event 9", "$10", "", "") , tags=('odd_row',))
    
    for event in events_data:
        tree4.insert("", tk.END, values=(event['title'], event['price'], "", "") , tags=('odd_row',))


tree4.yview_moveto(0)
#total_column = tree4.column('Total')
ticket_price_column = tree4.column('Ticket_price')

#scrollbar1 = tk.Scrollbar(tree4_frame, orient="vertical", command=tree4.yview)
#scrollbar1.place(x=615, y=0, relheight=0.77)

#tree4.configure(yscrollcommand=scrollbar1.set)

tree4_entries = []

#empty_space_entry = ctk.CTkLabel(tree4_frame, text="Qty", height=30 ,text_color='#fff', fg_color='#272727',font=('Arial', 15, 'bold') )

#empty_space_entry.pack(fill=tk.X, padx=(390, 180), pady=4)

'''for i, child in enumerate(tree4.get_children()):
    entry = ctk.CTkEntry(tree4_frame, width=33 , height=33, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0, justify="center")
    entry.pack(fill=tk.X, padx=(393, 180), pady=4)
    #entry.place(x=400, y=44 + i * 41)
    tree4_entries.append(entry)'''

num_entries = len(tree4_entries)
print("Number of entries:", num_entries)

btn_add = ctk.CTkButton(master=frame2, text="+   Add Website", font=('inter', 16, 'normal'), fg_color="#161616",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw" ,command=add_wsite)
btn_add.place(x=20, rely=0.79)

add_wsite_frame = ctk.CTkFrame(master=frame2, fg_color="#161616", bg_color="#161616", width=630)

entry_wsite = ctk.CTkEntry(add_wsite_frame, width=200, font=('Inter', 16), height=34, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=0, corner_radius=0,placeholder_text="Type your website here", justify="center")

entry_wsite.place(x=0,y=0)


entry_wcategory = ctk.CTkEntry(add_wsite_frame, width=200, font=('Inter', 16), height=34, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=0, corner_radius=0,
                            placeholder_text="Type Category here", justify="center")

entry_wcategory.place(x=180,y=0)

btn_cancel = ctk.CTkButton(master=add_wsite_frame, text="Cancel", font=('inter', 16, 'normal'), height=34 ,fg_color="#161616",
                     text_color="#E50202", hover=False, cursor='hand2', anchor="nw", command=f_add_wsite)

btn_cancel.place(x=400, y=4)

btn_cancel = ctk.CTkButton(master=add_wsite_frame, text="Save", font=('inter', 16, 'normal'), height=34 ,fg_color="#161616",
                     text_color="#E5B302", hover=False, cursor='hand2', anchor="nw", command=save_wsite)

btn_cancel.place(x=480, y=4)

label_message = ctk.CTkLabel(master=frame2, font=('inter', 18, 'bold'), text="WebSite is Added", text_color="#E50202")

label_error2 = ctk.CTkLabel(master=frame2, font=('inter', 18, 'bold'), text="No Website name provided", text_color="#E50202")

tree2.bind('<ButtonRelease-1>', on_tree_click)

tree2_new.bind('<ButtonRelease-1>', on_tree_click2)

label1 = ctk.CTkLabel(master=frame1, font=('inter', 21, 'bold'), text="Overview", text_color="#fff")
label1.place(x=40, y=30)

label2 = ctk.CTkLabel(master=frame2, font=('inter', 21, 'bold'), text="WebSites", text_color="#fff")
label2.place(x=40, y=30)

label2 = ctk.CTkLabel(master=frame3, font=('inter', 21, 'bold'), text="Accounts", text_color="#fff")
label2.place(x=40, y=30)

entry_Search = ctk.CTkEntry(frame2, width=230, font=('Inter', 16), height=34, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0, placeholder_text="Search here", justify="center")
entry_Search.place(relx=0.58, y=24)

website_data = get_website_column_with_ids(tree2)[:3]
website_options = [f"{id}:{name}" for id, name in website_data]

website_options.append("Show More ...")
website_options.insert(0, "Show All")

optionmenu_var = tk.StringVar(value=website_options[0])
optionmenu = ctk.CTkOptionMenu(frame3, width=200, font=('Inter', 16), dropdown_font	=('Inter', 16),height=36, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6',button_color="#161616" , button_hover_color="#161616" ,dropdown_fg_color="#252525",dropdown_text_color="#fff",corner_radius=0,values=website_options, command=optionmenu_callback, variable=optionmenu_var)

optionmenu.place(relx=0.6, y=30)

website_data2 = get_website_column_with_ids(tree2)[:3]
website_options2 = [f"{id} : {name}" for id, name in website_data2]

website_options2.append("Show More ...")

optionmenu_var2 = tk.StringVar(value="Select Website")
optionmenu2 = ctk.CTkOptionMenu(frame4, width=350, font=('Inter', 16), dropdown_font=('Inter', 16),height=36, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6',button_color="#161616" , button_hover_color="#161616" ,dropdown_fg_color="#252525",dropdown_text_color="#fff",corner_radius=0,values=website_options2, command=optionmenu_callback2, variable=optionmenu_var2)

frame4.update_idletasks()

x_center = (frame4.cget("width") - optionmenu2.cget("width")) / 2

optionmenu2.place(x=x_center, y=150)

#label_select = ctk.CTkLabel(master=frame4, font=('inter', 15, 'normal'), text="Select Website", text_color="#e6e6e6")

#label_select.place(x=x_center+4,y=115)


label_add = ctk.CTkLabel(master=frame4, font=('inter', 15, 'normal'), text="Or Add Link", text_color="#e6e6e6")

label_add.place(x=x_center+4,y=210)

entry_add = ctk.CTkEntry(frame4, width=350, font=('inter', 15, 'normal'), height=40, fg_color="#161616", bg_color="#161616",text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0, justify="center")

entry_add.place(x=x_center+3,y=250)

btn_more = ctk.CTkButton(master=frame4, text="Add More links", font=('inter', 15, 'normal'), fg_color="#161616",
                     text_color="#e6e6e6", hover=False, cursor='hand2', anchor="nw" ,command=add_wsite)

btn_more.place(x=x_center,y=310)

btn_step1 = ctk.CTkButton(master=frame4, text="Step 1/3", font=('inter', 16, 'bold'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=40, width=190, corner_radius=0,
                     hover_color="#fcc603", command=login_site)

btn_step1.place(relx=0.78, y=370, anchor="center")

btn_step2 = ctk.CTkButton(master=frame6, text="Calculate Total", font=('inter', 16, 'bold'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=40, width=190, corner_radius=0,
                     hover_color="#fcc603",command=calculate_total)

btn_step2.place(relx=0.50, y=400, anchor="center")

btn_step3 = ctk.CTkButton(master=frame6, text="Next Step", font=('inter', 16, 'bold'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=40, width=190, corner_radius=0,
                     hover_color="#fcc603",command=payement)

btn_step3.place(relx=0.78, y=400, anchor="center")

label_select = ctk.CTkLabel(master=frame6, font=('inter', 18, 'normal'), text=f"Total Budget is {total_budget}" , text_color="#e6e6e6")

label_select.place(relx=0.5, rely=0.74, anchor="center")

def search(event=None):
    query = entry_Search.get()
    selections = []
    for item in tree2_new.get_children():
        tree2_new.delete(item)
    for child in tree2.get_children():
        values = tree2.item(child)['values']
        if any(query.lower() in str(value).lower() for value in values):
            print(tree2.item(child)['values'])
            item_id = values[0]
            print(f"this is id : {item_id}")
            tree2_new.insert("", "end", iid=item_id, values=values, tags=('search', 'odd_row',))
        print(values)
            #selections.append(item_id)
    print('Search completed')
    print('Selected items:', selections)  # Debugging output
    tree2.selection_set(selections)
    print(type(selections))
    print(selections)

    tree2_new.place(x=0, y=80, width=630, relheight=0.6)

    for item in tree2_new.get_children():
        values = tree2_new.item(item, 'values')
        item_id = values[0]  # Assuming the ID is in the first column
        print(f"Item ID: {item_id}")


entry_Search.bind('<KeyRelease>', search)

btn1 = ctk.CTkButton(master=side_frame, text="Overview", font=('inter', 16, 'normal'), fg_color="#232323",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw", command=lambda: showFrame(frame1))
btn1.place(x=27, y=70)

btn2 = ctk.CTkButton(master=side_frame, text="Websites", font=('inter', 16, 'normal'), fg_color="#232323",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw", command=lambda: showFrame(frame2))
btn2.place(x=27, y=110)

btn3 = ctk.CTkButton(master=side_frame, text="Accounts", font=('inter', 16, 'normal'), fg_color="#232323",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw" ,command=lambda: showFrame(frame3))
btn3.place(x=27, y=150)

btn4 = ctk.CTkButton(master=side_frame, text="Progressing", font=('inter', 16, 'normal'), fg_color="#232323",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw")
btn4.place(x=27, y=190)

btn5 = ctk.CTkButton(master=side_frame, text="Payement API", font=('inter', 16, 'normal'), fg_color="#232323",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw")
btn5.place(x=27, y=230)

btn6 = ctk.CTkButton(master=side_frame, text="Forms", font=('inter', 16, 'normal'), fg_color="#232323",
                     text_color="#fafafa", hover=False, cursor='hand2', anchor="nw")
btn6.place(x=27, y=270)

btn7 = ctk.CTkButton(master=side_frame, text="Bot Maker", font=('inter', 16, 'bold'), fg_color="#E5B302",
                     text_color="#000", cursor='hand2', anchor="center", height=40, corner_radius=0,
                     hover_color="#fcc603" ,command=lambda: showFrame(frame4))
btn7.place(relx=0.5, y=370, anchor="center")

btn8 = ctk.CTkButton(master=side_frame, text="Good Bye", font=('inter', 16, 'bold'), fg_color="#4C4C4C",
                     text_color="#fff", cursor='hand2', anchor="center", height=40, corner_radius=0,
                     hover_color="#595959" ,command=bye)
btn8.place(relx=0.5, y=420, anchor="center")

buttons = [btn1, btn2, btn3, btn4, btn5, btn6]

showFrame(frame1)


def change_color(button):
    for btn in buttons:
        btn.configure(fg_color="#232323", text_color="#fafafa", font=('inter', 16, 'normal'))
    button.configure(fg_color="#232323", text_color="#E5B302", font=('inter', 16, 'bold'))


for btn in buttons:
    btn.bind("<Button-1>", lambda event, button=btn: change_color(button))


def bot_ready():
    code = entry1.get()
    if code != '':
        result =db.fetch_login(code)
        if result:
            main_frame.lower()
            bot_ready_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            label_error.place(relx=0.5, rely=0.6, anchor="center")
            entry1.configure(border_color="#9D0D0D")


def update_button_colors(event):
    entry_text = entry1.get()
    if entry_text.strip():
        bot_button.configure(bg_color='#E5B302', fg_color='#E5B302', text_color='#000000', hover_color='#E5B302')


center_x = 711 // 2
center_y = 460 // 2

font1 = ('Inter', 16)

entry1 = ctk.CTkEntry(main_frame, width=315, font=font1, height=47, fg_color="#161616", bg_color="#161616",
                      text_color='#e6e6e6', border_color="#808080", border_width=1, corner_radius=0,
                      placeholder_text="Add SN Here", justify="center")

entry1.place(relx=0.5, rely=0.41, anchor="center")

bot_button = ctk.CTkButton(main_frame, command=bot_ready, font=('inter', 14), text_color="#535353", text="Bot Ready!",
                           fg_color='#2B2929', bg_color='#2B2929', hover_color='#2B2929', cursor='hand2', width=150,
                           height=40)

bot_button.place(relx=0.5, rely=0.74, anchor="center")

entry1.bind("<Key>", update_button_colors)

app.mainloop()
