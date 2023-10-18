import tkinter as tk
import tableview

root = tk.Tk()
root.title("Tableview")
root.geometry("1400x900+0+0")
root.configure(background='white')

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
    }

def print_it(event, values, cell):

    print('Values:', values)
    print(f'Cell:\nRow:{cell[1]}\nColumn:{cell[0]} clicked')

tableview.setup_columns(root,column_headers, column_widths, table_height=20, frame_height=650, column_height=200, header_height=40, table_color_map=table_color_map)
tableview.insert_item(0, text='Test', bind=print_it)
tableview.insert_item(1, text='ABC Corp')
tableview.insert_item(2, text='Do something')
tableview.insert_item(3, text='01/01/2023')
tableview.insert_item(4, text='Open')
tableview.pack()
tableview.highlight_cell(column=1, row=0, bg='blue', fg='yellow')

root.mainloop()