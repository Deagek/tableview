from tkinter import *
import tableview
from tkinter import ttk

root = Tk()
root.title("Tableview")
root.geometry("1400x900+0+0")
root.configure(background='white')

tasks_frame=Frame(root, background='white')
tasks_lf=LabelFrame(tasks_frame, text=" Tasks ", font=('Calibri bold', 14), borderwidth=0, background='alice blue')
label=Label(tasks_lf,text='test')
label.grid(row=0, column=0)
tasks_lf.pack(fill='both', expand=True, padx=10, pady=(5, 10), side='top')

column_headers = ['Contact', 'Company', 'Task','Due', 'Status']
column_widths = [265, 265, 355, 120, 210]

table_color_map = {
    'header_background': 'grey70',
    'header_foreground': 'black',
    'tree_background': 'white',
    'tree_foreground': 'grey',
    'item_foreground': 'black',
    'tree_erase_background': 'white',
    'selected_row_bg_color': 'grey90',
    'selected_row_text_color': 'black',
    'separator_color':'red',
    }

def print_it(event, values, cell):

    print('Values:', values)
    print(f'Cell:\nRow:{cell[1]}\nColumn:{cell[0]} clicked')

tableview.setup_columns(tasks_lf,column_headers, column_widths, table_height=20, frame_height=650, column_height=200, header_height=40, table_color_map=table_color_map, xpad=0, ypad=0, header_font=('Calibri bold',12))
tableview.insert_item(0, text='Test', bind=print_it, font=('Calibri',12))
tableview.insert_item(1, text='ABC Corp')
tableview.insert_item(2, text='Do something')
tableview.insert_item(3, text='01/01/2023')
tableview.insert_item(4, text='Open')
tableview.pack()
tableview.highlight_cell(column=1, row=0, bg='blue', fg='yellow')
tasks_frame.grid(row=0, column=0)

def rh():
    tableview.remove_highlight(column=1, row=0)

root.after(1000,rh)

root.mainloop()
