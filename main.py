import pymysql # type: ignore
import tkinter as tk
from tkinter import messagebox

def clear_table():
    table_name = table_name_entry.get()
    if not table_name:
        messagebox.showerror("Error", "Please enter a table name.")
        return

    try:
        connection = pymysql.connect(
            host=host_entry.get(),
            port= int(port_entry.get()),
            user=user_entry.get(),
            password=password_entry.get(),
            database=database_entry.get(),
            cursorclass=pymysql.cursors.DictCursor 
        )

        with connection.cursor() as cursor: 
            sql = f"DELETE FROM `{table_name}`" 
            cursor.execute(sql)
        connection.commit() 

        connection.close()
        messagebox.showinfo("Success", f"Tabela '{table_name}' limpa com sucesso.")

    except pymysql.Error as err:
        messagebox.showerror("MySQL Error", str(err))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

window = tk.Tk()
window.title("Limpador de tabela mysql")

host_label = tk.Label(window, text="Host:")
host_label.grid(row=0, column=0, padx=5, pady=5)
host_entry = tk.Entry(window)
host_entry.grid(row=0, column=1, padx=5, pady=5)
host_entry.insert(0, "localhost")

port_label = tk.Label(window, text="Port:")
port_label.grid(row=1, column=0, padx=5, pady=5)
port_entry = tk.Entry(window)
port_entry.grid(row=1, column=1, padx=5, pady=5)
port_entry.insert(0, "3306")

user_label = tk.Label(window, text="User:")
user_label.grid(row=2, column=0, padx=5, pady=5)
user_entry = tk.Entry(window)
user_entry.grid(row=2, column=1, padx=5, pady=5)

password_label = tk.Label(window, text="Password:")
password_label.grid(row=3, column=0, padx=5, pady=5)
password_entry = tk.Entry(window, show="*")
password_entry.grid(row=3, column=1, padx=5, pady=5)

database_label = tk.Label(window, text="Database:")
database_label.grid(row=4, column=0, padx=5, pady=5)
database_entry = tk.Entry(window)
database_entry.grid(row=4, column=1, padx=5, pady=5)

table_name_label = tk.Label(window, text="Nome da tabela:")
table_name_label.grid(row=5, column=0, padx=5, pady=5)
table_name_entry = tk.Entry(window)
table_name_entry.grid(row=5, column=1, padx=5, pady=5)

clear_button = tk.Button(window, text="Limpar tabela", command=clear_table)
clear_button.grid(row=6, column=0, columnspan=2, pady=10)

window.mainloop()