tableview.py

Python tkinter based tableview

The reason I created this is that I needed a widget similar to ttk.treeview but one that allows me to highlight specific cells, which treeview can't do.
I also wanted to have a similar look and feel so the feel is somewhat consistent (you can change the column separators should you wish).

tableview is a table that allows for cell highlights and sorting. Similar to treeview, albeit you're unable to move items within.
Some features:

 * You can bind functions to the cells individually and have complete control over each cell.
 * As with treeview you can also stretch out each column. 
 * Double-clicking on the column separator will snap the column to the minimum size (column header text).
 * Clicking on the column itself will sort the column.


   
![image](https://github.com/Deagek/tableview/assets/148296186/51e2b946-c413-4c14-b671-54b759eaa2b9)

tableview.py:
<pre><Code>
 Parameters:
    - tkinter master window: The tkinter window.
    - column_headers: A list of column header labels.
    - column_widths: A list of column widths.
    - table_height: The visual viewport height.
    - frame_height: The height of the frame containing the table.
    - column_height: The inside-viewport height (scrollable height).
    - header_height: The height of the header row.
    - tableview.pack(): Ensures all columns and row are populated (must pack)
    - custom colours - create dict per below:
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

</Code></pre>
Example usage:
<pre><Code>  

  import tkinter as tk
  import tableview
  
  root = tk.Tk()
  root.title("Tableview")
  root.geometry("1400x900+0+0")
  root.configure(background='white')
  
  #Setup column headers
  column_headers = ['Contact', 'Company', 'Task','Due', 'Status']
  #Setup column widths
  column_widths = [265, 265, 355, 120, 210]
  
  #Select our colour preferences
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
  
  #Function to return to once clicked on a cell
  def print_it(event, values, cell):
  
      print('Values:', values)
      print(f'Cell:\nRow:{cell[1]}\nColumn:{cell[0]} clicked')
  
  tableview.setup_columns(root,column_headers, column_widths, table_height=20, frame_height=650, column_height=200, header_height=40, table_color_map=table_color_map)
  
  #tableview.insert(column= column number to insert this into, text= text to insert, bind= bind to what function)
  
  tableview.insert_item(0, text='Test', bind=print_it)
  tableview.insert_item(1, text='ABC Corp')
  tableview.insert_item(2, text='Do something')
  tableview.insert_item(3, text='01/01/2023')
  tableview.insert_item(4, text='Open')
  tableview.pack()
  #Here we'd like to highlight a specific cell: (bg is the background colour, fg is the foreground or text colour)
  tableview.highlight_cell(column=1, row=0, bg='blue', fg='yellow')
  
  root.mainloop()
  
</Code>
