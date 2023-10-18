import tkinter as tk

highlighted_cells=[]
item_frame_list=[]
canvas_list = []
frame_list = []
label_dict = {}
min_widths = []
sorting_orders = {}
header_list=[]


def on_double_click(event, index):
    canvas = canvas_list[index]
    canvas.configure(width=min_widths[index])
    header_canvas=header_list[index]
    header_canvas.configure(width=min_widths[index])
    canvas.configure(scrollregion=canvas.bbox("all"))
    h_canvas.configure(scrollregion=canvas.bbox("all"))
            
def on_button_press(event, index):
    frame_list[index].start_x = event.x

def on_button_release(event, index):
    frame_list[index].start_x = None

def on_mouse_motion(event, index, table_height):
    global item_frame_list
    if frame_list[index].start_x is not None:
        delta_x = event.x - frame_list[index].start_x
        new_canvas_width = canvas_list[index].winfo_width() + delta_x
        min_width = min_widths[index]
        width = 0
   
        for i, item in enumerate(canvas_list):
            if i != index:
                width = width + item.winfo_width()

        total_width = width + new_canvas_width

        if new_canvas_width >= min_width + 1:
            for i, item in enumerate(item_frame_list):
                if item[0] == index:
                    item_label=item_frame_list[i][1]
                    item_label.configure(width=new_canvas_width)
            
            canvas_list[index].configure(width=new_canvas_width)
            header_list[index].configure(width=new_canvas_width)
            content_width = total_width
            canvas.configure(scrollregion=canvas.bbox("all"))
            h_canvas.configure(scrollregion=(0, 0, content_width, table_height))
            hsb.set(0, total_width)
    
def setup_columns(root,column_headers, column_widths, table_height, frame_height, column_height, header_height,table_color_map):
    """
    Raplacement treeview/table with sort.

    Parameters:
    - tkinter master window: The tkinter window.
    - column_headers: A list of column header labels.
    - column_widths: A list of column widths.
    - table_height: The visual viewport height.
    - frame_height: The height of the frame containing the table.
    - column_height: The inside-viewport height (scrollable height).
    - header_height: The height of the header row.
    - tableview.pack(): Ensures all columns and row are populated (must pack)
    - custom colours - create dict per below:\n
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
    """

    global header_background, header_foreground, tree_background, tree_foreground, item_foreground, tree_erase_background, selected_row_bg_color, selected_row_text_color #colours
    
    if len(table_color_map) !=8:
        print('tableview - Error: Please populate all the colours in the table_color_map"')
        raise ValueError("Populate all the colours in the table_color_map")
    
    #Map colours
    header_background = table_color_map['header_background']
    header_foreground = table_color_map['header_foreground']
    tree_background = table_color_map['tree_background']
    tree_foreground = table_color_map['tree_foreground']
    item_foreground = table_color_map['item_foreground']
    tree_erase_background = table_color_map['tree_erase_background']
    selected_row_bg_color = table_color_map['selected_row_bg_color']
    selected_row_text_color = table_color_map['selected_row_text_color']

    global canvas, hsb, h_canvas, columns, max_widths, max_item_widths, row_indices, column_data, frame, frame_columns
    
    if len(column_headers) != len(column_widths):
        raise ValueError("The number of column headers must match the number of column widths.")
    frame_width=sum(column_widths)+60

    frame=tk.Frame(root, width=frame_width,height=frame_height, background='white')
    frame.grid(row=0, column=0, sticky='w')
    frame.grid_propagate(False)
   
    frame_columns = tk.Frame(frame, background=tree_erase_background)
    frame_columns.grid(row=0, column=0, sticky='w')
   
    columns=len(column_headers)
    column_data = [[] for _ in range(columns)]
    max_widths = [0] * columns  # Initialize max_widths list
    max_item_widths = [0] * columns  # Initialize max_item_widths list
    row_indices = [0] * columns  # Initialize row indices for each column
    #table height is the visual viewport height, column height is the inside-viewport height (scrollable height)
    table_height = table_height * 10

    table_width=sum(column_widths)
    canvas = tk.Canvas(frame_columns, height=table_height, width=table_width, background=tree_erase_background, bd=0, highlightthickness=0)
    
    vsb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    canvas.grid(row=1, column=0, sticky='nsw', columnspan=1000)
    vsb.grid(row=0, column=1000, sticky='nsw', rowspan=1000)

    # Create a table frame to hold the data
    table_frame = tk.Frame(canvas, background=tree_erase_background)
    canvas.create_window((0, 0), window=table_frame, anchor='nw')

    h_canvas = tk.Canvas(frame_columns, height=header_height, width=table_width, background=tree_erase_background, bd=0, highlightthickness=0)
    h_canvas.grid(row=0, column=0, sticky='nsw')
  
    # Create a table frame to hold the headers 
    header_frame = tk.Frame(h_canvas, background=tree_erase_background)
    h_canvas.create_window((0, 0), window=header_frame, anchor='nw')

    hsb = tk.Scrollbar(frame, orient="horizontal")
    canvas.configure(xscrollcommand=hsb.set)
    h_canvas.configure(xscrollcommand=hsb.set)
    hsb.grid(row=2, column=0, sticky='sew', columnspan=3)

    # Create headers
    for i, item in enumerate(column_headers):

        header_canvas = tk.Canvas(header_frame, height=header_height, width=column_widths[i], background=header_background, bd=0, highlightthickness=0)
        header_canvas.grid(row=0, column=i, sticky='nw', padx=0)
        header_label = tk.Label(header_frame, text=item, font=('Calibri', 12), background=header_background, foreground=header_foreground, bd=0, highlightthickness=0)
        header_label.update_idletasks()
        hlh=header_label.winfo_reqheight()//2
        label_height=(header_height//2)-hlh
        header_canvas.create_window(5 , label_height, window=header_label, anchor='nw')

        #Configure column header spacing & drag bar / separator
        ltree_backgroundspace = tk.Frame(header_frame, background=tree_erase_background, width=2, height=header_height)
        ltree_backgroundspace.grid(row=0, column=i, sticky='w')

        rhs_frame = tk.Frame(header_frame, background='grey', width=2, height=header_height, cursor='sb_h_double_arrow')
        rhs_frame.grid(row=0, column=i, sticky='nse')

        rtree_backgroundspace = tk.Frame(header_frame, background=tree_erase_background, width=2, height=header_height)
        rtree_backgroundspace.grid(row=0, column=i, sticky='w')

        rhs_frame.bind("<ButtonPress-1>", lambda event, index=i: on_button_press(event, index))
        rhs_frame.bind("<ButtonRelease-1>", lambda event, index=i: on_button_release(event, index))
        rhs_frame.bind("<B1-Motion>", lambda event, index=i, table_height=table_height: on_mouse_motion(event, index, table_height))

        rhs_frame.bind("<Double-1>", lambda event, index=i: on_double_click(event, index))
        rhs_frame.start_x = None

        header_canvas.update_idletasks()        
        column_width=5+header_label.winfo_reqwidth()+ltree_backgroundspace.winfo_reqwidth()+rhs_frame.winfo_reqwidth()+rtree_backgroundspace.winfo_reqwidth()
        min_widths.append(column_width) 
        header_canvas.bind("<Button-1>", lambda event, index=i: sort_rows(index))
        header_label.bind("<Button-1>", lambda event, index=i: sort_rows(index))
        header_list.append(header_canvas)
    
    for i in range(0,len(column_headers)):
        if i==len(column_headers)-1:
            canvas_col = tk.Canvas(table_frame, background=tree_background, width=column_widths[i], highlightthickness=0,
                                height=column_height)
        else:
            
            canvas_col = tk.Canvas(table_frame, background=tree_background, width=column_widths[i], highlightthickness=0,
                                height=column_height)
            
        canvas_col.grid(row=1, column=i, sticky='w')
        canvas_list.append(canvas_col)
        frame_list.append(table_frame)
        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def on_scroll(*args):
        for widget in (canvas, h_canvas):
            widget.xview(*args)

    hsb.config(command=on_scroll)

def sort_rows(column_index):
    global column_data, highlighted_cells, label_dict, row_indices

    rows = []
    if column_data[column_index]:
        data = column_data[column_index]

        highlighted_cell_content = None
        highlighted_bg_color = None
        highlighted_fg_color = None
        highlighted=[] #clear highlighted cells
        highlighted_cells=[]

        for col in range(columns): 
            for row_index in range(len(column_data[col])):
                label = column_data[col][row_index][1]
                if label.cget("background") != tree_background and label.cget("background")!=selected_row_bg_color and label.cget("foreground") !=selected_row_text_color:
                    highlighted_cell_content = label.cget("text")
                    highlighted_bg_color = label.cget("background")
                    highlighted_fg_color = label.cget("foreground")
                    highlighted.append((highlighted_cell_content,highlighted_bg_color, highlighted_fg_color ))
                    
        for row_index in range(len(data)):
            row_data = []
            
            for col in range(columns):
                data = column_data[col]
                if row_index < len(data):
                    row_data.append(data[row_index])
                  
            rows.append(row_data)

        current_order = sorting_orders.get(column_index, True)
        sorting_key = lambda row: row[0][0][0].lower()
        sorted_rows = sorted(rows, key=sorting_key, reverse=not current_order)
        sorting_orders[column_index] = not current_order


        #Delete old labels
        for col in range(columns):
            data=column_data[col]
            
            for i, label in enumerate(data):
                label=data[i][1]
                label.pack_forget()
                label.destroy()
                
        row_indices = [0] * columns  # Initialize row indices for each column
        column_data = [[] for _ in range(columns)] #reinit 
        label_dict.clear()

        for i, item in enumerate(sorted_rows):

            for a, line in enumerate(item):
                
                binding=line[4]
                if binding=='':
                    binding=None
                insert_item(int(line[2]),line[0],binding)
        
        for (column, row), label in label_dict.items():        
            for data in highlighted:

                if label.cget('text') == data[0] :
                    label.configure(background=data[1], foreground=data[2])
                    label.update()
                    highlighted_cells.append((column+1, row, data[1],data[2]))
                    
                else:
                    if label.cget('foreground')==item_foreground and label.cget('background')==tree_background:
                        label.configure(background=tree_background, foreground=item_foreground)

def highlight_row(event):
    exclude_row=None

    for (col, row), item in label_dict.items():
            label=item
            if exclude_row!=row:
                label.configure(background=tree_background)   

            if label == event.widget:
                try:
                    for c in range(0,columns):
                        label_dict.get((c, row)).configure(background=selected_row_bg_color, foreground=selected_row_text_color)
                        exclude_row=row
                                
                        for cells in highlighted_cells:
                            if row == cells[1] and c == cells[0]-1:
                                label_dict.get((c, row)).configure(background=cells[2], foreground=cells[3])
                except:
                    raise Exception('Did you forget to pack?')
            for cells in highlighted_cells:
                if row == cells[1] and col == cells[0]-1:
                    label_dict.get((col, row)).configure(background=cells[2], foreground=cells[3])
             
def on_double(event, bind=None):
    widget=event.widget
    values=''
    for (col, row), label in label_dict.items():
        if widget==label:
            cell=(col+1, row+1)
    
            for c in range(0,columns):
                if c==0:
                    values=label_dict.get((c, row)).cget('text')
                    
                else:
                    values=values+","+label_dict.get((c, row)).cget('text')
    if bind!=None:            
        bind(event=None, values=values, cell=cell)

def insert_item(column, text, bind=None):
    global item_frame_list,  row_indices
    row = row_indices[column]
    canvas = canvas_list[column]
   
    frame = tk.Frame(canvas, background=tree_background, width=canvas.winfo_reqwidth(), height=25) 
    frame.pack()
    frame.pack_propagate(False)
    item_frame_list.append((column,frame))
    canvas.create_window(5, row * 25, window=frame, anchor='nw')
    label = tk.Label(frame, text=text, anchor='w',  foreground=item_foreground,background=tree_background, font=('Calibri', 12))
    label.pack(fill='both', expand=True)  
    label.bind('<ButtonRelease-1>', highlight_row)
    label.bind("<Double-1>",lambda event, bind=bind: on_double(event, bind))
    
    item_width = label.winfo_reqwidth()
    max_item_widths[column] = item_width
    label_dict[(column, row)]=label
    column_data[column].append((text,label,column,row,bind))
    row_indices[column] += 1
    label.update()


def pack():
    for col in range(columns):
        for _ in range(row_indices[col], len(column_data[0])):
            canvas = canvas_list[col]
            frame = tk.Frame(canvas, background=tree_background, width=canvas.winfo_reqwidth(), height=25) 
            frame.pack()
            frame.pack_propagate(False)
            item_frame_list.append((col,frame))
            canvas.create_window(5, row_indices[col] * 25, window=frame, anchor='nw')
            label = tk.Label(frame, text='', anchor='w',  foreground=item_foreground,background=tree_background, font=('Calibri', 12))
            label.pack(fill='both', expand=True)  
            label.bind('<Button-1>', highlight_row)
            text=''
            
            label_dict[(col, row_indices[col])] = label
            column_data[col].append((text,label,col,row_indices[col],''))
            row_indices[col] += 1

def highlight_cell(column, row, bg,fg):
    column=column-1
    label = label_dict[(column, row)]
    label.configure(background=bg, foreground=fg)
    highlighted_cells.append((column+1, row, bg,fg))
    label.update()
