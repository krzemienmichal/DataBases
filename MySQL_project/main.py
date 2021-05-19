from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import dbOperations as db


def lis_plantowatch_movies(master):
    for widget in master.winfo_children():
        widget.destroy()
    # cnx, cursor = db.db_connect()
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map("Treeview", background=[("selected", "magenta")])
    tree_frame = Frame(master)
    tree_frame.pack(fill=X)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    ptw_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    ptw_tree.pack(pady=20, padx=20, fill="both")

    tree_scroll.config(command=ptw_tree.yview)
    ptw_tree['columns'] = ("Username", "Titles")

    ptw_tree.column("#0", width=0, stretch=NO)
    ptw_tree.column("Username", anchor=W, width=120, minwidth=50)
    ptw_tree.column("Titles", anchor=W, width=120, minwidth=50)

    # headings
    ptw_tree.heading("#0", text="", anchor=CENTER)
    ptw_tree.heading("Username", text="Username", anchor=CENTER)
    ptw_tree.heading("Titles", text="Titles", anchor=CENTER)

    ptw_tree.tag_configure('oddrow', background="white")
    ptw_tree.tag_configure("evenrow", background="lightblue")

    def load_data():
        for record in ptw_tree.get_children():
            ptw_tree.delete(record)
        err, data = db.show_ptw_for_all_users(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    ptw_tree.insert("", END, values=row, tags='evenrow')
                else:
                    ptw_tree.insert("", END, values=row, tags='oddrow')
                count += 1
    load_data()

    entry_frame = Frame(tree_frame)
    entry_frame.pack(fill=X, padx=20)
    user_label = Label(entry_frame, text="Username")
    user_label.grid(row=0, column=0, padx=10, pady=10)
    user_entry = Entry(entry_frame, disabledbackground="white", disabledforeground="black")
    user_entry.grid(row=0, column=1, padx=10, pady=10)

    ptw_label = Label(entry_frame, text="Title")
    ptw_label.grid(row=1, column=0, padx=10, pady=10)
    ptw_entry = Entry(entry_frame)
    ptw_entry.grid(row=1, column=1, padx=10, pady=10)

    button_frame = Frame(tree_frame)
    button_frame.pack(fill=X, padx=20)

    # Creating scroll
    movie_scroll = Scrollbar(tree_frame)
    movie_scroll.pack(side=RIGHT, fill=Y)

    # Creating movie Treeview
    movie_tree = ttk.Treeview(tree_frame, yscrollcommand=movie_scroll.set, selectmode="extended")
    movie_tree.pack(pady=20, padx=20, fill="both")

    movie_scroll.config(command=movie_tree.yview)  # Scroll configuration
    movie_tree['columns'] = ("Movie_ID", "Title", "RunningTime", "Director", "ProductionCompany", "Genre")

    # Columns settings
    movie_tree.column("#0", width=0, stretch=NO)
    movie_tree.column("Movie_ID", anchor=CENTER, width=40, minwidth=40)
    movie_tree.column("Title", anchor=W, width=120, minwidth=100)
    movie_tree.column("RunningTime", anchor=CENTER, width=120, minwidth=100)
    movie_tree.column("Director", anchor=W, width=120, minwidth=100)
    movie_tree.column("ProductionCompany", anchor=W, width=120, minwidth=100)
    movie_tree.column("Genre", anchor=W, width=120, minwidth=100)

    # Headings settings
    movie_tree.heading("#0", text="")
    movie_tree.heading("Movie_ID", text="ID", anchor=CENTER)
    movie_tree.heading("Title", text="Title", anchor=CENTER)
    movie_tree.heading("RunningTime", text="Running Time", anchor=CENTER)
    movie_tree.heading("Director", text="Director", anchor=CENTER)
    movie_tree.heading("ProductionCompany", text="Production Company", anchor=CENTER)
    movie_tree.heading("Genre", text="Genre", anchor=CENTER)

    # Striped treeview
    movie_tree.tag_configure('oddrow', background="white")
    movie_tree.tag_configure("evenrow", background="lightblue")

    def load_movies_data():
        for record in movie_tree.get_children():
            movie_tree.delete(record)
        err, data = db.list_movies(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    movie_tree.insert("", END, values=row, tags='evenrow')
                else:
                    movie_tree.insert("", END, values=row, tags='oddrow')
                count += 1

    load_movies_data()

    def clean_records():
        user_entry.delete(0, END)
        ptw_entry.delete(0, END)

    def select_records(x):
        clean_records()
        selected = ptw_tree.focus()
        values = ptw_tree.item(selected, 'values')
        if values:
            user_entry.insert(0, values[0])
            ptw_entry.insert(0, values[1])

    def add_ptw_to_user():
        ptw_data = [user_entry.get()]
        selected = movie_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Movie",
                                   message="You have to chose at least one movie to add")
        else:
            title = []
            for i in selected:
                value = (movie_tree.item(i, 'values'))
                title.append(value[1])
            for record in title:
                ptw_data.append(record)
            print(ptw_data)
            err = db.add_ptw(data=ptw_data, cursor=cursor, cnx=cnx)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            else:
                if confirm():
                    cnx.commit()
                    load_data()
                else:
                    cnx.rollback()

    def remove_ptw_from_user():
        ptw_data = [user_entry.get()]
        selected = movie_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Movie",
                                   message="You have to chose at least one movie to add")
        else:
            title = []
            for i in selected:
                value = (movie_tree.item(i, 'values'))
                title.append(value[1])
            for record in title:
                ptw_data.append(record)
            print(ptw_data)
            err = db.remove_ptw(data=ptw_data, cursor=cursor, cnx=cnx)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            else:
                if confirm():
                    cnx.commit()
                    load_data()
                else:
                    cnx.rollback()

    # bind the treeview
    ptw_tree.bind("<ButtonRelease-1>", select_records)

    add_record_button = Button(button_frame, text="Add Title", command=add_ptw_to_user)
    add_record_button.grid(row=2, column=0, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove Title", command=remove_ptw_from_user)
    remove_one_button.grid(row=2, column=2, padx=10, pady=10)

    clean_fields_button = Button(button_frame, text="Clean Field", command=clean_records)
    clean_fields_button.grid(row=2, column=3, padx=10, pady=10)

    refresh_button = Button(button_frame, text="Refresh Data", command=load_data)
    refresh_button.grid(row=2, column=4, padx=10, pady=10)


def list_users_watched_movies(master):
    for widget in master.winfo_children():
        widget.destroy()
    # cnx, cursor = db.db_connect()
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map("Treeview", background=[("selected", "magenta")])
    tree_frame = Frame(master)
    tree_frame.pack(fill=X)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    watched_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    watched_tree.pack(pady=20, padx=20, fill="both")

    tree_scroll.config(command=watched_tree.yview)
    watched_tree['columns'] = ("Username", "Titles")

    watched_tree.column("#0", width=0, stretch=NO)
    watched_tree.column("Username", anchor=W, width=120, minwidth=50)
    watched_tree.column("Titles", anchor=W, width=120, minwidth=50)

    # headings
    watched_tree.heading("#0", text="", anchor=CENTER)
    watched_tree.heading("Username", text="Username", anchor=CENTER)
    watched_tree.heading("Titles", text="Titles", anchor=CENTER)

    watched_tree.tag_configure('oddrow', background="white")
    watched_tree.tag_configure("evenrow", background="lightblue")

    def load_data():
        for record in watched_tree.get_children():
            watched_tree.delete(record)
        err, data = db.show_watched_for_all_users(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    watched_tree.insert("", END, values=row, tags='evenrow')
                else:
                    watched_tree.insert("", END, values=row, tags='oddrow')
                count += 1

    load_data()

    entry_frame = Frame(tree_frame)
    entry_frame.pack(fill=X, padx=20)
    user_label = Label(entry_frame, text="Username")
    user_label.grid(row=0, column=0, padx=10, pady=10)
    user_entry = Entry(entry_frame, disabledbackground="white", disabledforeground="black")
    user_entry.grid(row=0, column=1, padx=10, pady=10)

    watched_label = Label(entry_frame, text="Title")
    watched_label.grid(row=1, column=0, padx=10, pady=10)
    watched_entry = Entry(entry_frame)
    watched_entry.grid(row=1, column=1, padx=10, pady=10)

    button_frame = Frame(tree_frame)
    button_frame.pack(fill=X, padx=20)

    # Creating scroll
    movie_scroll = Scrollbar(tree_frame)
    movie_scroll.pack(side=RIGHT, fill=Y)

    # Creating movie Treeview
    movie_tree = ttk.Treeview(tree_frame, yscrollcommand=movie_scroll.set, selectmode="extended")
    movie_tree.pack(pady=20, padx=20, fill="both")

    movie_scroll.config(command=movie_tree.yview)  # Scroll configuration
    movie_tree['columns'] = ("Movie_ID", "Title", "RunningTime", "Director", "ProductionCompany", "Genre")

    # Columns settings
    movie_tree.column("#0", width=0, stretch=NO)
    movie_tree.column("Movie_ID", anchor=CENTER, width=40, minwidth=40)
    movie_tree.column("Title", anchor=W, width=120, minwidth=100)
    movie_tree.column("RunningTime", anchor=CENTER, width=120, minwidth=100)
    movie_tree.column("Director", anchor=W, width=120, minwidth=100)
    movie_tree.column("ProductionCompany", anchor=W, width=120, minwidth=100)
    movie_tree.column("Genre", anchor=W, width=120, minwidth=100)

    # Headings settings
    movie_tree.heading("#0", text="")
    movie_tree.heading("Movie_ID", text="ID", anchor=CENTER)
    movie_tree.heading("Title", text="Title", anchor=CENTER)
    movie_tree.heading("RunningTime", text="Running Time", anchor=CENTER)
    movie_tree.heading("Director", text="Director", anchor=CENTER)
    movie_tree.heading("ProductionCompany", text="Production Company", anchor=CENTER)
    movie_tree.heading("Genre", text="Genre", anchor=CENTER)

    # Striped treeview
    movie_tree.tag_configure('oddrow', background="white")
    movie_tree.tag_configure("evenrow", background="lightblue")

    def load_movies_data():
        for record in movie_tree.get_children():
            movie_tree.delete(record)
        err, data = db.list_movies(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    movie_tree.insert("", END, values=row, tags='evenrow')
                else:
                    movie_tree.insert("", END, values=row, tags='oddrow')
                count += 1

    load_movies_data()

    def clean_records():
        user_entry.delete(0, END)
        watched_entry.delete(0, END)

    def select_records(x):
        clean_records()
        selected = watched_tree.focus()
        values = watched_tree.item(selected, 'values')
        if values:
            user_entry.insert(0, values[0])
            watched_entry.insert(0, values[1])

    def add_watched_to_user():
        ptw_data = [user_entry.get()]
        selected = movie_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Movie",
                                   message="You have to chose at least one movie to add")
        else:
            title = []
            for i in selected:
                value = (movie_tree.item(i, 'values'))
                title.append(value[1])
            for record in title:
                ptw_data.append(record)
            print(ptw_data)
            err = db.add_watched(data=ptw_data, cursor=cursor, cnx=cnx)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            else:
                if confirm():
                    cnx.commit()
                    load_data()
                else:
                    cnx.rollback()

    def remove_watched_from_user():
        ptw_data = [user_entry.get()]
        selected = movie_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Movie",
                                   message="You have to chose at least one movie to add")
        else:
            title = []
            for i in selected:
                value = (movie_tree.item(i, 'values'))
                title.append(value[1])
            for record in title:
                ptw_data.append(record)
            print(ptw_data)
            err = db.remove_watched(data=ptw_data, cursor=cursor, cnx=cnx)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            else:
                if confirm():
                    cnx.commit()
                    load_data()
                else:
                    cnx.rollback()

    # bind the treeview
    watched_tree.bind("<ButtonRelease-1>", select_records)

    add_record_button = Button(button_frame, text="Add Title", command=add_watched_to_user)
    add_record_button.grid(row=2, column=0, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove Title", command=remove_watched_from_user)
    remove_one_button.grid(row=2, column=2, padx=10, pady=10)

    clean_fields_button = Button(button_frame, text="Clean Field", command=clean_records)
    clean_fields_button.grid(row=2, column=3, padx=10, pady=10)

    refresh_button = Button(button_frame, text="Refresh Data", command=load_data)
    refresh_button.grid(row=2, column=4, padx=10, pady=10)


def list_movies(master):
    # Clearing views to avoid multiple instance of the same table
    for widget in master.winfo_children():
        widget.destroy()

        # Creating frame
    tree_frame = Frame(master)
    tree_frame.pack(fill=X)

    entry_frame = Frame(master)
    entry_frame.pack(fill=X)

    movies_button_frame = Frame(master)
    movies_button_frame.pack(fill=X)

    genre_frame = Frame(master)
    genre_frame.pack(side=LEFT)

    # Configuring treeview style
    tree_style = ttk.Style()
    tree_style.theme_use("default")
    tree_style.configure("Treeview",
                         background="#dddddd",
                         foreground="black",
                         rowheight=25,
                         fieldbackground="#dddddd")
    tree_style.map("Treeview", background=[("selected", "magenta")])

    # Creating scroll
    movie_scroll = Scrollbar(tree_frame)
    movie_scroll.pack(side=RIGHT, fill=Y)

    # Creating movie Treeview
    movie_tree = ttk.Treeview(tree_frame, yscrollcommand=movie_scroll.set, selectmode="extended")
    movie_tree.pack(pady=20, padx=20, fill="both")

    movie_scroll.config(command=movie_tree.yview)  # Scroll configuration
    movie_tree['columns'] = ("Movie_ID", "Title", "RunningTime", "Director", "ProductionCompany", "Genre")

    # Columns settings
    movie_tree.column("#0", width=0, stretch=NO)
    movie_tree.column("Movie_ID", anchor=CENTER, width=40, minwidth=40)
    movie_tree.column("Title", anchor=W, width=120, minwidth=100)
    movie_tree.column("RunningTime", anchor=CENTER, width=120, minwidth=100)
    movie_tree.column("Director", anchor=W, width=120, minwidth=100)
    movie_tree.column("ProductionCompany", anchor=W, width=120, minwidth=100)
    movie_tree.column("Genre", anchor=W, width=120, minwidth=100)

    # Headings settings
    movie_tree.heading("#0", text="")
    movie_tree.heading("Movie_ID", text="ID", anchor=CENTER)
    movie_tree.heading("Title", text="Title", anchor=CENTER)
    movie_tree.heading("RunningTime", text="Running Time", anchor=CENTER)
    movie_tree.heading("Director", text="Director", anchor=CENTER)
    movie_tree.heading("ProductionCompany", text="Production Company", anchor=CENTER)
    movie_tree.heading("Genre", text="Genre", anchor=CENTER)

    # Striped treeview
    movie_tree.tag_configure('oddrow', background="white")
    movie_tree.tag_configure("evenrow", background="lightblue")

    def load_movies_data():
        for record in movie_tree.get_children():
            movie_tree.delete(record)
        err, data = db.list_movies(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    movie_tree.insert("", END, values=row, tags='evenrow')
                else:
                    movie_tree.insert("", END, values=row, tags='oddrow')
                count += 1
    load_movies_data()

    id_label = Label(entry_frame, text="ID")
    id_label.grid(row=2, column=0, padx=10, pady=10)
    id_entry = Entry(entry_frame, disabledbackground="white", disabledforeground="black")
    id_entry.grid(row=2, column=1, padx=10, pady=10)

    title_label = Label(entry_frame, text="Title")
    title_label.grid(row=0, column=0, padx=10, pady=10)
    title_entry = Entry(entry_frame)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    rt_label = Label(entry_frame, text="Running Time")
    rt_label.grid(row=0, column=2, padx=10, pady=10)
    rt_entry = Entry(entry_frame)
    rt_entry.grid(row=0, column=3, padx=10, pady=10)

    director_label = Label(entry_frame, text="Director")
    director_label.grid(row=0, column=4, padx=10, pady=10)
    director_entry = Entry(entry_frame)
    director_entry.grid(row=0, column=5, padx=10, pady=10)

    pc_label = Label(entry_frame, text="Production Company")
    pc_label.grid(row=1, column=0, padx=10, pady=10)
    pc_entry = Entry(entry_frame)
    pc_entry.grid(row=1, column=1, padx=10, pady=10)

    genre_label = Label(entry_frame, text="Genre")
    genre_label.grid(row=1, column=2, padx=10, pady=10)
    genre_entry = Entry(entry_frame)
    genre_entry.grid(row=1, column=3, padx=10, pady=10)

    # Genre frame
    genre_scroll = Scrollbar(genre_frame)
    genre_scroll.pack(fill=Y, side=LEFT)

    genre_tree = ttk.Treeview(genre_frame, yscrollcommand=genre_scroll.set, selectmode="extended")
    genre_tree.pack(pady=20, padx=20, side=LEFT)

    genre_scroll.config(command=genre_tree.yview)  # Scroll configuration

    genre_tree['columns'] = ("Genre_ID", "MovieGenre")
    genre_tree.column("#0", width=0, stretch=NO)
    genre_tree.column("Genre_ID", width=30, minwidth=30)
    genre_tree.column("MovieGenre", width=100, minwidth=100)

    genre_tree.heading("#0", text="")
    genre_tree.heading("Genre_ID", text="ID")
    genre_tree.heading("MovieGenre", text="Genre")

    genre_tree.tag_configure('oddrow', background="white")
    genre_tree.tag_configure("evenrow", background="lightblue")

    def load_genre_data():
        for record in genre_tree.get_children():
            movie_tree.delete(record)
        err, data = db.list_genres(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    genre_tree.insert("", END, values=row, tags='evenrow')
                else:
                    genre_tree.insert("", END, values=row, tags='oddrow')
                count += 1

    load_genre_data()

    def clean_records():
        id_entry.config(state=NORMAL)
        id_entry.delete(0, END)
        title_entry.delete(0, END)
        rt_entry.delete(0, END)
        director_entry.delete(0, END)
        pc_entry.delete(0, END)
        genre_entry.delete(0, END)

    def select_records(x):
        clean_records()
        selected = movie_tree.focus()
        values = movie_tree.item(selected, 'values')
        if values:
            id_entry.config(state=NORMAL)
            id_entry.insert(0, values[0])
            id_entry.config(state=DISABLED)
            title_entry.insert(0, values[1])
            rt_entry.insert(0, values[2])
            director_entry.insert(0, values[3])
            pc_entry.insert(0, values[4])
            genre_entry.insert(0, values[5])

    def add_movie():
        data = [title_entry.get(),
                rt_entry.get(),
                director_entry.get(),
                pc_entry.get(), ]
        selected = genre_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Genre",
                                   message="You have to chose at least one movie genre")
        else:
            genre = []
            for i in selected:
                value = (genre_tree.item(i, 'values'))
                genre.append(value[1])
            genre_data = []
            for record in genre:
                genre_data.append(record)
            err = db.add_movies(cursor, cnx, title_entry.get(), tuple(data), genre_data)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            else:
                if confirm():
                    cnx.commit()
                else:
                    cnx.rollback()
                load_movies_data()

    def add_genre_to_movie():
        selected = genre_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Genre",
                                   message="You have to chose at least one movie genre")
        else:
            genre = []
            for i in selected:
                value = (genre_tree.item(i, 'values'))
                genre.append(value[1])
            genre_data = []
            for record in genre:
                genre_data.append(record)
            err = db.add_genre_to_movies(cursor, cnx, title_entry.get(), genre_data)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            if confirm():
                cnx.commit()
            else:
                cnx.rollback()
            load_movies_data()

    def remove_genre_from_movie():
        selected = genre_tree.selection()
        if selected == ():
            messagebox.showwarning(title="Chose Genre",
                                   message="You have to chose at least one movie genre")
        else:
            genre = []
            for i in selected:
                value = (genre_tree.item(i, 'values'))
                genre.append(value[1])
            genre_data = []
            for record in genre:
                genre_data.append(record)
            err = db.delete_genre_from_movies(cursor, cnx, title_entry.get(), genre_data)
            if err is not None:
                messagebox.showerror(title="SQL Error", message=err)
            if confirm():
                cnx.commit()
            else:
                cnx.rollback()
            load_movies_data()

    def remove_selected():
        x = movie_tree.focus()
        value = movie_tree.item(x, 'values')
        err = db.delete_movies(value[1], cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        load_movies_data()

    def update_movie():
        movie_data = (id_entry.get(),
                      title_entry.get(),
                      rt_entry.get(),
                      director_entry.get(),
                      pc_entry.get())
        err = db.update_movies(cursor, cnx, movie_data)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            if confirm():
                cnx.commit()
            else:
                cnx.rollback()
            load_movies_data()

    # bind the treeview
    movie_tree.bind("<ButtonRelease-1>", select_records)

    add_record_button = Button(movies_button_frame, text="Add Record",
                               command=add_movie, width=20)
    add_record_button.grid(row=2, column=0, padx=10, pady=10)

    add_genre_button = Button(movies_button_frame, text="Add Genre To Movie",
                              command=add_genre_to_movie, width=20)
    add_genre_button.grid(row=3, column=0, padx=10, pady=10)

    rmv_genre_button = Button(movies_button_frame, text="Remove Genre From Movie",
                              command=remove_genre_from_movie, width=20)
    rmv_genre_button.grid(row=3, column=1, padx=10, pady=10)

    update_button = Button(movies_button_frame, text="Update Data",
                           command=update_movie, width=20)
    update_button.grid(row=2, column=1, padx=10, pady=10)

    remove_one_button = Button(movies_button_frame, text="Remove Selected",
                               command=remove_selected, width=20)
    remove_one_button.grid(row=2, column=2, padx=10, pady=10)

    clean_fields_button = Button(movies_button_frame, text="Clean Field",
                                 command=clean_records, width=20)
    clean_fields_button.grid(row=2, column=3, padx=10, pady=10)

    refresh_button = Button(movies_button_frame, text="Refresh Data",
                            command=load_movies_data, width=20)
    refresh_button.grid(row=2, column=4, padx=10, pady=10)


def manage_clients_info(master):
    for widget in master.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#dddddd",
                    foreground="black",
                    rowheight=25,
                    fieldackground="#dddddd")
    style.map("Treeview", background=[("selected", "magenta")])
    tree_frame = Frame(master)
    tree_frame.pack(fill=BOTH)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    clients_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    clients_tree.pack(pady=20, padx=20, fill="both")

    tree_scroll.config(command=clients_tree.yview)
    clients_tree['columns'] = ("Client_ID", "FirstName", "LastName", "BirthDate", "Email", "Username")
    # columns
    clients_tree.column("#0", width=0, stretch=NO)
    clients_tree.column("Client_ID", anchor=CENTER, minwidth=40, width=40)
    clients_tree.column("FirstName", anchor=W, minwidth=30, width=140)
    clients_tree.column("LastName", anchor=W, minwidth=30, width=140)
    clients_tree.column("BirthDate", anchor=CENTER, minwidth=30, width=120)
    clients_tree.column("Email", anchor=W, minwidth=30, width=140)
    clients_tree.column("Username", anchor=W, minwidth=30, width=140)

    # headings
    clients_tree.heading("#0", text="")
    clients_tree.heading("Client_ID", text="ID", anchor=CENTER)
    clients_tree.heading("FirstName", text="First Name", anchor=CENTER)
    clients_tree.heading("LastName", text="Last Name", anchor=CENTER)
    clients_tree.heading("BirthDate", text="Birth Date", anchor=CENTER)
    clients_tree.heading("Email", text="Email", anchor=CENTER)
    clients_tree.heading("Username", text="Username", anchor=CENTER)

    clients_tree.tag_configure('oddrow', background="white")
    clients_tree.tag_configure("evenrow", background="lightblue")

    # Add Data
    def load_data():
        for record in clients_tree.get_children():
            clients_tree.delete(record)
        err, data = db.list_clients(cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            count = 0
            for row in data:
                if count % 2 == 0:
                    clients_tree.insert("", END, values=row, tags='evenrow')
                else:
                    clients_tree.insert("", END, values=row, tags='oddrow')
                count += 1

    load_data()

    entry_frame = Frame(master)
    entry_frame.pack(fill=X, padx=20)
    id_label = Label(entry_frame, text="ID")
    id_label.grid(row=2, column=0, padx=10, pady=10)
    id_entry = Entry(entry_frame, disabledbackground="white", disabledforeground="black", state=DISABLED)
    id_entry.grid(row=2, column=1, padx=10, pady=10)

    fn_label = Label(entry_frame, text="First Name")
    fn_label.grid(row=0, column=0, padx=10, pady=10)
    fn_entry = Entry(entry_frame)
    fn_entry.grid(row=0, column=1, padx=10, pady=10)

    ln_label = Label(entry_frame, text="Last Name")
    ln_label.grid(row=0, column=2, padx=10, pady=10)
    ln_entry = Entry(entry_frame)
    ln_entry.grid(row=0, column=3, padx=10, pady=10)

    bd_label = Label(entry_frame, text="Birth Date")
    bd_label.grid(row=0, column=4, padx=10, pady=10)
    bd_entry = Entry(entry_frame)
    bd_entry.grid(row=0, column=5, padx=10, pady=10)

    email_label = Label(entry_frame, text="Email")
    email_label.grid(row=1, column=0, padx=10, pady=10)
    email_entry = Entry(entry_frame)
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    username_label = Label(entry_frame, text="Username")
    username_label.grid(row=1, column=2, padx=10, pady=10)
    username_entry = Entry(entry_frame)
    username_entry.grid(row=1, column=3, padx=10, pady=10)

    password_label = Label(entry_frame, text="Password")
    password_label.grid(row=1, column=4, padx=10, pady=10)
    password_entry = Entry(entry_frame)
    password_entry.grid(row=1, column=5, padx=10, pady=10)
    password_entry.config(show="*")

    def clean_records():
        id_entry.config(state=NORMAL)
        id_entry.delete(0, END)
        id_entry.config(state=DISABLED)
        fn_entry.delete(0, END)
        ln_entry.delete(0, END)
        bd_entry.delete(0, END)
        email_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)

    def select_records(x):
        clean_records()
        selected = clients_tree.focus()
        values = clients_tree.item(selected, 'values')
        if values:
            id_entry.config(state=NORMAL)
            id_entry.insert(0, values[0])
            id_entry.config(state=DISABLED)
            fn_entry.insert(0, values[1])
            ln_entry.insert(0, values[2])
            bd_entry.insert(0, values[3])
            email_entry.insert(0, values[4])
            username_entry.insert(0, values[5])
            password_entry.insert(0, "")

    def add_client():
        client_data = (fn_entry.get(),
                       ln_entry.get(),
                       bd_entry.get(),
                       email_entry.get(),
                       username_entry.get(),
                       password_entry.get())
        msg = db.add_clients(data=client_data, cursor=cursor, cnx=cnx)
        if msg is not None:
            messagebox.showerror(title="SQL Error", message=msg)
        else:
            if confirm():
                cnx.commit()
                load_data()
            else:
                cnx.rollback()

    def remove_selected():
        x = clients_tree.focus()
        values = clients_tree.item(x, 'values')
        err = db.delete_clients(values[0], cursor, cnx)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            if confirm():
                cnx.commit()
                load_data()
            else:
                cnx.rollback()

    def update_record():
        client_data = (id_entry.get(),
                       fn_entry.get(),
                       ln_entry.get(),
                       bd_entry.get(),
                       email_entry.get(),
                       username_entry.get(),
                       password_entry.get())

        err = db.update_clients(cursor, cnx, client_data)
        if err is not None:
            messagebox.showerror(title="SQL ERROR", message=err)
        else:
            if confirm():
                cnx.commit()
                load_data()
            else:
                cnx.rollback()

    button_frame = Frame(master)
    button_frame.pack(fill=X, padx=20)

    # bind the treeview
    clients_tree.bind("<ButtonRelease-1>", select_records)

    add_record_button = Button(button_frame, text="Add Record", command=add_client)
    add_record_button.grid(row=2, column=0, padx=10, pady=10)

    update_button = Button(button_frame, text="Update Data", command=update_record)
    update_button.grid(row=2, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame, text="Remove Selected", command=remove_selected)
    remove_one_button.grid(row=2, column=2, padx=10, pady=10)

    clean_fields_button = Button(button_frame, text="Clean Field", command=clean_records)
    clean_fields_button.grid(row=2, column=3, padx=10, pady=10)

    refresh_button = Button(button_frame, text="Refresh Data", command=load_data)
    refresh_button.grid(row=2, column=4, padx=10, pady=10)


def confirm():
    conf = messagebox.askyesno(title="Confirmation", message="Do you want to make changes?")
    return conf


if __name__ == "__main__":
    error, cnx, cursor = db.db_connect(user="", password="",
                                       host="", database="")
    if error is not None:
        messagebox.showerror(title="SQL ERROR", message=error)
    else:
        # create root window
        root = Tk()
        root.geometry('1200x760')

        left_frame = Frame(root, bg="#002266")
        left_frame.pack(side="left", fill='both')
        central_frame = Frame(root, bg="#e6eeff")
        central_frame.pack(expand=True, fill='both')
        # frame inside root window

        # buttons
        manage_users_button = Button(left_frame, text='Manage Clients', bd=5, width=15,
                                     command=lambda: manage_clients_info(central_frame))
        manage_users_button.pack(padx=10, pady=10)

        manage_movies_button = Button(left_frame, text='Manage Movies', bd=5, width=15,
                                      command=lambda: list_movies(central_frame))
        manage_movies_button.pack(padx=10, pady=10)

        list_plantowatch_button = Button(left_frame, text='List Plan To Watch', bd=5, width=15,
                                         command=lambda: lis_plantowatch_movies(central_frame))
        list_plantowatch_button.pack(padx=10, pady=10)

        list_watched_button = Button(left_frame, text='List Watched', bd=5, width=15,
                                     command=lambda: list_users_watched_movies(central_frame))
        list_watched_button.pack(padx=10, pady=10)

        # Tkinter event loop
        root.mainloop()

        cnx.close()
