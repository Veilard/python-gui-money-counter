import sqlite3
import tkinter as tk
from tkinter import END, messagebox

def create_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                   id INTEGER PRIMARY KEY,
                   name TEXT,
                   amount REAL, 
                   category TEXT,
                   date DATE)
                   ''')
    conn.commit()
    conn.close()

def add_expense():
    name = name_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()

    if name and amount and category and date:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)", (name, amount, category, date))
        conn.commit()
        conn.close()
        
        name_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        
        result_text.delete(1.0, END)
        result_text.insert(END, 'Запись внесена.')
    else: 
        result_text.delete(1.0, END)
        result_text.insert(END, 'Ошибка при создании записи. Проверьте правильность введенных данных.')

def view_expenses_by_date():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date", (start_date, end_date))
    expenses = cursor.fetchall()

    conn.close()

    result_text.delete(1.0, END)

    if expenses:
        result_text.insert(END, 'Расходы по датам:')
        for expense in expenses:
            result_text.insert(END, f"ID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Категория: {expense[3]}, Дата: {expense[4]}")
    else:
        result_text.insert(END, "Нет расходов в указанный период")

def view_expenses_by_category():
    category = category_view_entry.get()

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE category=? ORDER BY date", (category,))
    expenses = cursor.fetchall()

    conn.close()

    result_text.delete(1.0, END)

    if expenses:
        result_text.insert(END, f"Расходы в категории '{category}':")
        for expense in expenses:
            result_text.insert(END, f"\nID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Дата: {expense[4]}" )
    else:
        result_text.insert(END, f"Нет расходов в категории '{category}'.")

def view_all_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    conn.close()

    result_text.delete(1.0, END)

    if expenses:
        for expense in expenses: 
            result_text.insert(END, f"ID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Категория: {expense[3]}, Дата: {expense[4]}\n")
    else:
        result_text.insert(END, 'Данные не найдены.')

def delete_all_expenses():
    result_text.delete(1.0, END)
    confirmation = messagebox.askokcancel('Подтверждение', 'Вы уверены что хотите удалить все данные?')
    if confirmation:
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()

        result_text.insert(END, 'Данные удалены.')
    else:
        result_text.insert(END, 'Операция отменена.')

root = tk.Tk()
root.title("ExpenseTracker")

name_label = tk.Label(root, text='Название расхода')
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

amount_label = tk.Label(root, text='Сумма расхода')
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

category_label = tk.Label(root, text='Категория расхода')
category_label.pack()
category_entry = tk.Entry(root)
category_entry.pack()

date_label = tk.Label(root, text='Дата расхода')
date_label.pack()
date_entry = tk.Entry(root)
date_entry.pack()

add_button = tk.Button(root, text='Добавить расход', command=add_expense)
add_button.pack()

empty_label = tk.Label(root, text="\n")
empty_label.pack()

dates_frame = tk.Frame()
dates_frame.pack()

dates_label = tk.Label(dates_frame, text='РАБОТА С ДАТАМИ')
dates_label.grid(row=0, column=0, columnspan=2)

start_date_label = tk.Label(dates_frame, text='С')
start_date_label.grid(row=1, column=0)
end_date_label = tk.Label(dates_frame, text='ПО')
end_date_label.grid(row=1, column=1)

start_date_entry = tk.Entry(dates_frame)
start_date_entry.grid(row=2, column=0, padx=10)
end_date_entry = tk.Entry(dates_frame)
end_date_entry.grid(row=2, column=1, padx=10)

date_expenses_button = tk.Button(dates_frame, text='Показать расходы в период', command=view_expenses_by_date)
date_expenses_button.grid(row=3, column=0, columnspan=2, pady=10)

empty_label = tk.Label(root, text="\n")
empty_label.pack()

frame = tk.Frame()
frame.pack()

view_category_label = tk.Label(frame, text='Категория')
view_category_label.pack()
category_view_entry = tk.Entry(frame)
category_view_entry.pack()
add_button = tk.Button(frame, text='Просмотр расходов по категории', command=view_expenses_by_category)
add_button.pack()
result_text = tk.Text(frame, height=10, width=50)
result_text.pack()
empty_label = tk.Label(frame, text="") 
empty_label.pack()

add_button = tk.Button(frame, text='Посмотреть все расходы', command=view_all_expenses)
add_button.pack()

empty_label = tk.Label(frame, text="")
empty_label.pack()
add_button = tk.Button(frame, text='УДАЛИТЬ ДАННЫЕ', bg='#ff4122',fg='white', pady=5, command=delete_all_expenses)
add_button.pack()
empty_label = tk.Label(frame, text="")
empty_label.pack()

root.mainloop()
