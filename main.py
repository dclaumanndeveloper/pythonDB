import pymysql # type: ignore
import tkinter as tk
from tkinter import messagebox

def delete_all_data(db_config):
    cursor = db_config.cursor()

    # Get all table names (excluding system tables)
    cursor.execute("SHOW TABLES")
    
    tables = cursor.fetchall()
    table_names = [list(table.values())[0] for table in tables if 'Tables_in_mysql_distribuicao' in table]
    try:
        if not tables:
            print("No tables found in the database.")
            return
    except pymysql.Error as e:
        print(f"Error fetching table names: {e}")
    # Disable foreign key checks temporarily to avoid constraint issues
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
   
    db_config.commit()
    
    for table in table_names:
   
        try:
            # Truncate table (faster than DELETE FROM)
            if(table != 'users' and table != 'musical_instruments' and table != 'music_genres' and table != 'music_subgenres' and table != 'knex_migrations' and table != 'knex_migrations_lock' and table != 'languages' and table != 'countries'):
                cursor.execute(f"DELETE FROM `{table}`") # Use backticks for table names
                print(f"Data deleted from table: {table}")
                db_config.commit()
        except pymysql.Error as e:
            print(f"Error deleting data from table {table}: {e}")
            db_config.rollback() # Rollback in case of error in one table
            return # Stop the process if there is an error
   
    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db_config.commit()

    print("All data deletion process completed.")


    if db_config.open:
        cursor.close()
        db_config.close()

def clear_table():
    table_name = table_name_entry.get()
   # if not table_name:
   #    messagebox.showerror("Error", "Please enter a table name.")
   #     return

    try:
        connection = pymysql.connect(
            host=host_entry.get(),
            port= int(port_entry.get()),
            user=user_entry.get(),
            password=password_entry.get(),
            database=database_entry.get(),
            cursorclass=pymysql.cursors.DictCursor 
        )
    except pymysql.Error as err:
        messagebox.showerror("MySQL Error", str(err))
        return
    if delete_var.get():  # Check if the checkbox is checked
            if messagebox.askyesno("Confirm Deletion", "Are you absolutely sure you want to delete ALL data from ALL tables? This action is irreversible!"):
                try:
                    delete_all_data(connection)
                    messagebox.showinfo("Success", "Data deletion process completed.")
                except Exception as e: # Catch any exception during the deletion process
                    messagebox.showerror("Error", f"An error occurred: {e}")
            else:
                messagebox.showinfo("Cancelled", "Data deletion cancelled.")
    else:
        
        try:
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
delete_var = tk.BooleanVar()  # Variable to store the checkbox state
delete_check = tk.Checkbutton(window, text="Eu quero deletar os dados de todas as tabelas.", variable=delete_var)
delete_check.grid(row=6, column=0, columnspan=2, pady=10)  # Use grid instead of pack

clear_button = tk.Button(window, text="Limpar tabela", command=clear_table)
clear_button.grid(row=7, column=0, columnspan=2, pady=10)  # Adjust row number


window.mainloop()