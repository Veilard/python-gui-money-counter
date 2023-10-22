# 1. Возможность ввода:
#  1.1 Названия расхода
#  1.2 Потраченной суммы денег
#  1.3 Причисление расхода к конкретной группе расходов (транспорт, еда, жилье и т.д.)
# 2. Отслеживание даты и времени введенного расхода
# 3. Хранение вышеперечисленной информации в базе данных и группировка по датам и группам

import sqlite3
import argparse
import tkinter as tk

from argparse import ArgumentParser
from tkinter import END
from tkinter import messagebox

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


#Внесение расходов 
def add_expense():
    result_text.delete(1.0, END)
    #Поля ввода
    name = name_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()
    date = date_entry.get()


    #Добавление расхода в базу данных
    if (name and amount and category and date):
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO expenses (name, amount, category, date) VALUES (?, ?, ?, ?)", (name, amount, category, date))
        conn.commit()
        conn.close()
        name_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        result_text.insert(END, 'Запись внесена.')
    else: 
        result_text.insert(END, 'Ошибка при создании записи. Проверьте правильность введенных данных.')
    #Очистка полей после успешного ввода
    

#Создание главного окна
root = tk.Tk()
root.title("ExpenseTracker")



#Расходы по датам(от и до)
def view_expenses_by_date():
    result_text.delete(1.0, END)
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date", (start_date, end_date))
    expenses = cursor.fetchall()

    conn.close()

    if expenses:
        result_text.insert(END, 'Расходы по датам:')
        for expense in expenses:
            result_text.insert(END, f"ID: {expense[0]}, Название: {expense[1]}, Сумма: {expense[2]}, Категория: {expense[3]}, Дата: {expense[4]}")
    else:
        result_text.insert(END, "Нет расходов в указанный период")




#Расходы по категориям
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


#Просмотр всех расходов в базе данных
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


def view_sum_by_date(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
    total = cursor.fetchone()[0]

    print(f"Сумма всех расходов за указанный период: {total}")

def ask_if_ok():
    confirmation = tk.messagebox.askokcancel('Подтверждение', 'Вы уверены что хотите продолжить?')
    if confirmation:
        delete_all_expenses()
        print('Данные удалены')
        result_text.insert(END, 'Данные удалены.')
    else:
        print('Canceled')

def delete_all_expenses():
    result_text.delete(1.0, END)
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()

#Элементы интерфейса
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
empty_label = tk.Label(root, text="\n") #Empty space for margin
empty_label.pack()

#######################################################PROBLEM#####################################################################
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

#######################################################PROBLEM#####################################################################

empty_label = tk.Label(root, text="\n") #Empty space for margin
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
empty_label = tk.Label(frame, text="") #Empty space for margin
empty_label.pack()


add_button = tk.Button(frame, text='Посмотреть все расходы', command=view_all_expenses)
add_button.pack()

empty_label = tk.Label(frame, text="")
empty_label.pack()
add_button = tk.Button(frame, text='УДАЛИТЬ ДАННЫЕ', bg='#ff4122',fg='white', pady=5, command=ask_if_ok)
add_button.pack()
empty_label = tk.Label(frame, text="")
empty_label.pack()



#Запуск
if __name__ == '__main__':
    create_database()

    parser = ArgumentParser(description="Управление расходами")
    subparsers = parser.add_subparsers(dest = "command")

    #Сабпарсер для добавления расходов
    add_parser = subparsers.add_parser("add", help='Добавить расход')
    add_parser.add_argument("--name", required=True, help='Название расхода')
    add_parser.add_argument("--amount", required=True, type=int, help='Сумма расхода')
    add_parser.add_argument("--category", required=True, help='Категория расхода')
    add_parser.add_argument("--date", required=True, help='Дата расхода в формате ГГГГ-ММ-ДД')

    #Сабпарсеры для просмотра расходов по датам
    view_date_parser = subparsers.add_parser("view_by_date", help='Просмотр расходов по датам')
    view_date_parser.add_argument("--start_date", required=True)
    view_date_parser.add_argument("--end_date", required=True)

    #Сабпарсер для просмотра расходов в категории
    view_category_parser = subparsers.add_parser("view_by_category", help='Просмотр расходов по категориям')
    view_category_parser.add_argument("--category", required=True)
    
    #Сабпарсер для просмотра всей базы данных
    view_all_expenses_parser = subparsers.add_parser("view_all_expenses", help='Просмотр всех записей в базе данных')

    #Сабпарсер для суммы всех расходов в заданный период
    view_sum_by_date_parser = subparsers.add_parser("view_sum_by_date", help='Просмотр суммы всех расходов за указанный период')
    view_sum_by_date_parser.add_argument("--start_date", required=True)
    view_sum_by_date_parser.add_argument("--end_date", required=True)
    
    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.name, args.amount, args.category, args.date)
    elif args.command == "view_by_date":
        view_expenses_by_date(args.start_date, args.end_date)
    elif args.command == "view_by_category":
        view_expenses_by_category(args.category)
    elif args.command == "view_all_expenses":
        view_all_expenses()
    elif args.command == "view_sum_by_date":
        view_sum_by_date(args.start_date, args.end_date)

    root.mainloop()
