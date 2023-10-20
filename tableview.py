import tkinter as tk
from tkinter import ttk
root = None
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
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            h_canvas.configure(scrollregion=(0, 0, content_width, table_height))
            hsb.set(0, total_width)
    
def setup_columns(root,window,column_headers, column_widths, table_height, frame_height, column_height, header_height,table_color_map=None, xpad=None, ypad=None, header_font=None, grid_row=None):
   
    """
    Raplacement treeview/table with sort.

    Parameters:

    tableview.setup_columns():
    - tkinter master window: The tkinter window.
    - column_headers: A list of column header labels.
    - column_widths: A list of column widths.
    - table_height: The visual viewport height.
    - frame_height: The height of the frame containing the table.
    - column_height: The inside-viewport height (scrollable height).
    - header_height: The height of the header row.
    - tableview.pack(): Ensures all columns and row are populated (must pack)
    - xpad: x padding relative to container/frame
    - ypad: x padding relative to container/frame
    - header_font: ('font name', fontsize), eg:('Calibri',12)

    - tableview.clear(): clears table
    - tableview.remove_highlight(column, row): Removes the highlight from a cell at the designated coordinates
    
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
        'separator_color': 'grey',
        }

    - tabelview.insert_item():
      - font=('font name', fontsize), eg:('Calibri',12) when calling tableview.insert_item()
    """

    global header_background, header_foreground, tree_background, tree_foreground, item_foreground, tree_erase_background, selected_row_bg_color, selected_row_text_color #colours
    
    if table_color_map==None:
        table_color_map = {
            'header_background': 'grey70',
            'header_foreground': 'black',
            'tree_background': 'white',
            'tree_foreground': 'grey',
            'item_foreground': 'black',
            'tree_erase_background': 'white',
            'selected_row_bg_color': 'grey90',
            'selected_row_text_color': 'black',
            'separator_color':'grey',
            }

    if len(table_color_map) !=9:
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
    separator_color = table_color_map['separator_color']
   
    if header_font==None or header_font=='':
        header_font=('Calibri bold',12)

    global canvas, hsb, h_canvas, columns, max_widths, max_item_widths, row_indices, column_data, frame, frame_columns, main_canvas
    

    if len(column_headers) != len(column_widths):
        raise ValueError("The number of column headers must match the number of column widths.")
    frame_width=sum(column_widths)+60
    if grid_row==None:
        grid_row=0
    frame=tk.Frame(window, width=frame_width, height=frame_height, background=tree_background, bd=0, highlightthickness=0, border=None)
    frame.grid(row=grid_row, column=0, sticky='nsew', padx=xpad,pady=ypad)
    frame.grid_propagate(False)
    frame.columnconfigure(0,weight=1)
    frame_columns = tk.Frame(frame, background=tree_erase_background, bd=0, highlightthickness=0, border=None)
    frame_columns.grid(row=0, column=0, sticky='nesw')
    frame_columns.columnconfigure(0, weight=1)
    frame_columns.propagate(False)

    columns=len(column_headers)
    column_data = [[] for _ in range(columns)]
    max_widths = [0] * columns  # Initialize max_widths list
    max_item_widths = [0] * columns  # Initialize max_item_widths list
    row_indices = [0] * columns  # Initialize row indices for each column
    #table height is the visual viewport height, column height is the inside-viewport height (scrollable height)
    table_height = table_height * 10

    table_width=sum(column_widths)
    main_canvas = tk.Canvas(frame_columns, height=table_height, width=table_width, background=tree_background, bd=0, highlightthickness=0)

    vsb = ttk.Scrollbar(frame, orient="vertical", command=main_canvas.yview)
    main_canvas.configure(yscrollcommand=vsb.set)
    main_canvas.grid(row=1, column=0, sticky='nsew', columnspan=1000)
    vsb.grid(row=0, column=1000, sticky='nsw', rowspan=1000, pady=(header_height,15))

    # Create a table frame to hold the data
    table_frame = tk.Frame(main_canvas, background=tree_erase_background)
    main_canvas.create_window(0, 0, window=table_frame, anchor='nw')

    h_canvas = tk.Canvas(frame_columns, height=header_height, width=table_width, background=tree_erase_background, bd=0, highlightthickness=0)
    h_canvas.grid(row=0, column=0, sticky='nsew')
  
    # Create a table frame to hold the headers 
    header_frame = tk.Frame(h_canvas, background=tree_erase_background, bd=0, highlightthickness=0, border=None)
    h_canvas.create_window((0, 0), window=header_frame, anchor='nw')

    hsb = ttk.Scrollbar(frame, orient="horizontal")
    main_canvas.configure(xscrollcommand=hsb.set)
    h_canvas.configure(xscrollcommand=hsb.set)
    hsb.grid(row=2, column=0, sticky='sew', columnspan=3, padx=(0,0))

    # Create headers
    for i, item in enumerate(column_headers):

        header_canvas = tk.Canvas(header_frame, height=header_height, width=column_widths[i], background=header_background, bd=0, highlightthickness=0)
        header_canvas.grid(row=0, column=i, sticky='new', padx=0)
        header_label = tk.Label(header_frame, text=item, font=header_font, background=header_background, foreground=header_foreground, bd=0, highlightthickness=0)
        header_label.update_idletasks()

        hlh=header_label.winfo_reqheight()//2
        label_height=(header_height//2)-hlh
        header_canvas.create_window(5, label_height, window=header_label, anchor='nw')

        if column_widths[i] >0:
            rhs_frame = tk.Frame(header_frame, background=separator_color, width=2, height=header_height, cursor='sb_h_double_arrow')
            rhs_frame.grid(row=0, column=i, sticky='nse')
            rhs_frame.bind("<ButtonPress-1>", lambda event, index=i: on_button_press(event, index))
            rhs_frame.bind("<ButtonRelease-1>", lambda event, index=i: on_button_release(event, index))
            rhs_frame.bind("<B1-Motion>", lambda event, index=i, table_height=table_height: on_mouse_motion(event, index, table_height))
            rhs_frame.bind("<Double-1>", lambda event, index=i: on_double_click(event, index))
            rhs_frame.start_x = None

        header_canvas.update_idletasks()        
        column_width=header_label.winfo_reqwidth()+rhs_frame.winfo_reqwidth()
        min_widths.append(column_width) 
        header_canvas.bind("<Button-1>", lambda event, index=i: sort_rows(index))
        header_label.bind("<Button-1>", lambda event, index=i: sort_rows(index))
        header_list.append(header_canvas)
    
    for i in range(0,len(column_headers)):

        if i==len(column_headers)-1:

            canvas_col = tk.Canvas(table_frame, background=tree_background, width=column_widths[i], highlightthickness=0,
                                height=column_height)
        if i==0:
            canvas_col = tk.Canvas(table_frame, background=tree_background, width=column_widths[i], highlightthickness=0,
                                height=column_height)    
            canvas_col.grid(row=1, column=i, sticky='e', padx=0)
        else:
            canvas_col = tk.Canvas(table_frame, background=tree_background, width=column_widths[i], highlightthickness=0,
                    height=column_height)
            canvas_col.grid(row=1, column=i, sticky='w', padx=0)

        canvas_list.append(canvas_col)
        frame_list.append(table_frame)
        table_frame.update_idletasks()
        main_canvas.config(scrollregion=main_canvas.bbox("all"))
    global initial_window_width
    initial_window_width=frame.winfo_width()
    initial_window_height=frame.winfo_height()
    
    root.update()

    def on_scroll(*args):
        for widget in (main_canvas, h_canvas):
            widget.xview(*args)

    hsb.config(command=on_scroll)

    def resize_window(event):
        new_width_list=[]
        if event.widget is root:
           
            new_width = event.width  # Get the new width of the window
            new_height = event.height  # Get the new height of the window
            xratio = root.winfo_width() / initial_window_width
            new_height=new_height-95

            for width in column_widths:
                new_width_list.append(width*xratio)

            for i, canvas in enumerate(header_list):
                canvas.configure(width=new_width_list[i])
            
            for i, canvas in enumerate(canvas_list):
                canvas.configure(width=new_width_list[i], height=column_height)

            for i, item_frame in enumerate(item_frame_list):
                item_frame[1].configure(width=1900) #set all frames to maximum

            table_width = new_width - 30  # Adjust as needed
            main_canvas.configure(width=table_width, height=new_height)
            h_canvas.configure(width=table_width)
            frame.configure(width=new_width, height=new_height+110)
            
    root.bind("<Configure>", resize_window)
    
    def on_mouse_scroll(event):
        scroll_units = .05  # Adjust the scrolling speed as needed

        if event.delta > 0:
            # Scrolling up
            new_y = main_canvas.yview()[0] - scroll_units
        elif event.delta < 0:
            # Scrolling down
            new_y = main_canvas.yview()[0] + scroll_units

        new_y = max(0, min(new_y, 1))  # Ensure new_y is within the valid range
        main_canvas.yview_moveto(new_y)

    root.bind("<MouseWheel>", on_mouse_scroll)

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
        font_formatting=[]

        #Firstly remove selected line highlight
        for col in range(columns): 
            for row_index in range(len(column_data[col])):
                label = column_data[col][row_index][1]
                label.configure(background=tree_background)
        
        #Save any custom highlights
        for col in range(columns): 
            for row_index in range(len(column_data[col])):
                label = column_data[col][row_index][1]
                font=label.cget('font')
                text=label.cget('text')
                font_formatting.append((text,font))
                
                highlighted_cell_content = label.cget("text")
                highlighted_bg_color = label.cget("background")
                highlighted_fg_color = label.cget("foreground")
                highlighted.append((highlighted_cell_content,highlighted_bg_color, highlighted_fg_color ))
        
        #Create rows from the columns            
        for row_index in range(len(data)):
            row_data = []
            
            for col in range(columns):
                data = column_data[col]
                if row_index < len(data):
                    row_data.append(data[row_index])
                  
            rows.append(row_data)
        
        #Sort by text
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
        
        #Reinitialize lists & dicts
        row_indices = [0] * columns 
        column_data = [[] for _ in range(columns)] 
        label_dict.clear()

        #Find any bindings & create new item labels including bindings
        for i, item in enumerate(sorted_rows):

            for a, line in enumerate(item):
                
                binding=line[4]
                if binding=='':
                    binding=None
                insert_item(int(line[2]),line[0],binding)
        
        #Redo custom cell highlights
        for (column, row), label in label_dict.items():        
            for data in highlighted:

                if label.cget('text') == data[0] :
                    label.configure(background=data[1], foreground=data[2])
                    label.update()
                    highlighted_cells.append((column+1, row, data[1],data[2]))
                    
                else:
                    if label.cget('foreground')==item_foreground and label.cget('background')==tree_background:
                        label.configure(background=tree_background, foreground=item_foreground)
        
        #Format fonts
        for (column, row), label in label_dict.items():        
            for data in font_formatting:
                if label.cget('text') == data[0] :
                    label.configure(font=data[1])

def highlight_row(event):
    exclude_row=None



    for (col, row), item in label_dict.items():
            label=item
            if exclude_row!=row:
                label.configure(background=tree_background)   

            if label == event.widget:
                try:
                    for c in range(0,columns):
                        font=label_dict.get((c, row)).cget('font')
                        label_dict.get((c, row)).configure(background=selected_row_bg_color, foreground=selected_row_text_color, font=font)
                        exclude_row=row
                          
                        
                        
                                
                        for cells in highlighted_cells:
                            if row == cells[1] and c == cells[0]-1:
                                font=label_dict.get((c, row)).cget('font')
                                label_dict.get((c, row)).configure(foreground=cells[3], font=font)
                except:
                    raise Exception('Did you forget to pack?')
           
            for cells in highlighted_cells:
                if row == cells[1] and col == cells[0]-1:
                    font=label_dict.get((col, row)).cget('font')
                    label_dict.get((col, row)).configure(foreground=cells[3], font=font)
             
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

def insert_item(column, text, bind=None, font=None):
    global item_frame_list,  row_indices
    try:
        row = row_indices[column]
        canvas = canvas_list[column]
    except:
        raise ValueError("Attempting to insert a row value in a column that doesn't exist! Check the number of columns in tableview.setup_columns")
    frame = tk.Frame(canvas, background=tree_background, width=canvas.winfo_reqwidth(), height=25) 
    frame.pack()
    frame.pack_propagate(False)

    item_frame_list.append((column,frame))
    canvas.create_window(0, row * 25, window=frame, anchor='nw')
    label = tk.Label(frame, text=" "+str(text), anchor='w',  foreground=item_foreground,background=tree_background, font=font)
    label.pack(fill='both', expand=True, padx=0)  
    label.bind('<ButtonRelease-1>', highlight_row)
    label.bind("<Double-1>",lambda event, bind=bind: on_double(event, bind))
    
    item_width = label.winfo_reqwidth()
    max_item_widths[column] = item_width
    label_dict[(column, row)]=label
    column_data[column].append((text,label,column,row,bind))
    row_indices[column] += 1
    label.update()

def clear():
    global row_indices, column_data, label_dict, highlighted_cells

    row_indices = [0] * columns  # Initialize row indices for each column
    column_data = [[] for _ in range(columns)] #reinit 
    label_dict.clear()
    highlighted_cells=[]

    for column, frame in item_frame_list:
        frame.destroy()
    item_frame_list.clear()


def pack():#insert blank items
    for col in range(columns):
        for _ in range(row_indices[col], len(column_data[0])):
            canvas = canvas_list[col]
            frame = tk.Frame(canvas, background=tree_background, width=canvas.winfo_reqwidth()+10, height=25) 
            frame.pack()
            frame.pack_propagate(False)
            item_frame_list.append((col,frame))
            canvas.create_window(0, row_indices[col] * 25, window=frame, anchor='nw')
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

def remove_highlight(column, row):
    column=column-1
    for i, item in enumerate(highlighted_cells):
        if item[0]==column+1 and item[1]==row:
            highlighted_cells.pop(i)
            label = label_dict[(column, row)]
            label.configure(background=tree_background, foreground=item_foreground)
            label.update()

def resize_window(event, root, column_widths, column_height, neg_padx, neg_pady):
   
    new_width_list=[]
    new_width = event.width-neg_pady  # Get the new width of the window
    new_height = event.height  # Get the new height of the window
    xratio = root.winfo_width() / initial_window_width
    new_height=new_height-90-neg_pady

    for width in column_widths:
        new_width_list.append(width*xratio)

    for i, canvas in enumerate(header_list):
        canvas.configure(width=new_width_list[i])
    
    for i, canvas in enumerate(canvas_list):
        canvas.configure(width=new_width_list[i], height=column_height)

    for i, item_frame in enumerate(item_frame_list):
        item_frame[1].configure(width=1900) #set all frames to maximum

    table_width = new_width - 30  # Adjust as needed
    main_canvas.configure(width=table_width, height=new_height)
    h_canvas.configure(width=table_width)
    frame.configure(width=new_width, height=new_height+115)
