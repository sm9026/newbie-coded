import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# =============================================================================
# CORE LOGIC (Updated to return structured data for the GUI)
# =============================================================================

def countLinesInFile(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r') as file:
        return sum(1 for line in file)

def logic_addTask(name, description, priority):
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as file:
            file.write("TASKS :\n")
    
    with open("tasks.txt", "a") as file:
        lineCount = countLinesInFile("tasks.txt")
        if lineCount <= 1:
            iD = 1
        else:
            iD = (lineCount - 1) // 4 + 1
        file.write(f"{iD}. Task: {name}\n...Description: {description}\n...Priority level: {priority}\n...Status: Not Done\n")

def logic_get_tasks_data():
    """
    Parses the file and returns a list of dictionaries.
    This is essential for the Treeview and Search features.
    """
    tasks = []
    if not os.path.exists("tasks.txt"):
        return tasks

    with open("tasks.txt", "r") as f:
        lines = f.readlines()

    if len(lines) <= 1:
        return tasks

    # i starts at 1 to skip header, step 4 lines per task
    i = 1
    while i < len(lines):
        try:
            if i+3 < len(lines):
                # Calculate the "File ID" (1-based index)
                file_id = (i - 1) // 4 + 1
                
                # Extract Raw Text
                raw_name = lines[i].strip()
                raw_desc = lines[i+1].strip()
                raw_prio = lines[i+2].strip()
                raw_stat = lines[i+3].strip()

                # Clean Text
                name = raw_name.split('.', 1)[1].strip() if '.' in raw_name else raw_name
                desc = raw_desc.replace("...Description:", "").strip()
                prio = raw_prio.replace("...Priority level:", "").strip()
                stat = raw_stat.replace("...Status:", "").strip()

                tasks.append({
                    'file_id': file_id,
                    'name': name,
                    'desc': desc,
                    'prio': prio,
                    'status': stat
                })
        except IndexError:
            break
        i += 4
    return tasks

def logic_deleteTask(file_id):
    # logic_deleteTask expects the Nth task number
    l = countLinesInFile("tasks.txt")
    totalTasks = (l - 1) // 4
    
    if totalTasks == 0: return False, "No tasks available."
    
    with open("tasks.txt", "r") as temp:
        lines = temp.readlines()

    with open("tasks.txt", "w") as file:
        file.write("TASKS :\n")

    i = 1 
    iD = 1
    deleted = False
    
    while i < len(lines):
        current_task_index = (i - 1) // 4 + 1
        
        if current_task_index == file_id:
            # Add to BIN
            if not os.path.exists("bin.txt"):
                with open("bin.txt", "w") as bin_file:
                    bin_file.write("DELETED TASKS :\n")
            with open("bin.txt", "a") as bin_file:
                # Write to bin
                tsk = lines[i][3:] 
                desc = lines[i+1]
                prio = lines[i+2]
                stat = lines[i+3]
                l_bin = countLinesInFile("bin.txt")
                BiD = 1 if l_bin <= 1 else (l_bin - 1) // 4 + 1
                bin_file.write(f"{BiD}. {tsk}{desc}{prio}{stat}")
            
            deleted = True
            i += 4 
        else:
            # Keep task
            with open("tasks.txt", "a") as file:
                if i+3 < len(lines):
                    tsk = lines[i].split('.', 1)[1] if '.' in lines[i] else lines[i]
                    desc = lines[i+1]
                    prio = lines[i+2]
                    stat = lines[i+3]
                    file.write(f"{iD}.{tsk}{desc}{prio}{stat}")
                    iD += 1
            i += 4
    
    if deleted: return True, "Task deleted."
    else: return False, "Task not found."

def logic_changeTaskStatus(file_id):
    # This function needs the 'file_id' to locate the exact line
    # The original logic used 'Nth Pending Task', we are changing it to use 'Nth Absolute Task'
    # which is safer for the GUI interaction.
    
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
        
    # Calculate line index: Header(1) + (ID-1)*4 + 3(Status Line is 4th in block)
    # But wait, lines list is 0-indexed.
    # Task 1 starts at index 1. Status is at index 4.
    # Task 2 starts at index 5. Status is at index 8.
    # Formula: index = 1 + (file_id - 1)*4 + 3
    
    target_line_idx = 1 + (file_id - 1) * 4 + 3
    
    if target_line_idx < len(lines):
        if "Not Done" in lines[target_line_idx]:
             lines[target_line_idx] = "...Status: Done\n"
             with open("tasks.txt", "w") as f:
                 f.writelines(lines)
             return True, "Marked as Done."
        else:
            return False, "Task is already Done."
    return False, "Error finding task."

# =============================================================================
# GUI IMPLEMENTATION
# =============================================================================

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoApp Pro Upgrade")
        self.root.geometry("700x600")
        self.root.configure(bg='#f4f4f4')

        # --- 1. Header & Progress Bar ---
        header_frame = tk.Frame(root, bg='#f4f4f4')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(header_frame, text="🚀 Interactive Task Manager", font=("Segoe UI", 18, "bold"), bg='#f4f4f4', fg='#333').pack(side='left')
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(header_frame, variable=self.progress_var, maximum=100, length=200)
        self.progress_bar.pack(side='right', pady=5)
        self.lbl_progress = tk.Label(header_frame, text="0%", bg='#f4f4f4', font=("Arial", 10))
        self.lbl_progress.pack(side='right', padx=5)

        # --- 2. Search Bar ---
        search_frame = tk.Frame(root, bg='#f4f4f4')
        search_frame.pack(fill='x', padx=20, pady=(0, 10))
        tk.Label(search_frame, text="🔍 Search:", bg='#f4f4f4', font=("Arial", 11)).pack(side='left')
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.search_entry.pack(side='left', fill='x', expand=True, padx=10)
        self.search_entry.bind('<KeyRelease>', self.filter_tasks) # Real-time search

        # --- 3. Treeview Table (Replaces Text Box) ---
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=5)

        cols = ('id', 'name', 'desc', 'prio', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=15)
        
        # Configure Columns
        self.tree.column('id', width=40, anchor='center')
        self.tree.column('name', width=150, anchor='w')
        self.tree.column('desc', width=250, anchor='w')
        self.tree.column('prio', width=60, anchor='center')
        self.tree.column('status', width=100, anchor='center')

        # Headings
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Task Name')
        self.tree.heading('desc', text='Description')
        self.tree.heading('prio', text='Priority')
        self.tree.heading('status', text='Status')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Tags for Color Coding
        self.tree.tag_configure('done', foreground='gray')
        self.tree.tag_configure('high_prio', background='#ffcccc') # Light red for priority 5

        # --- 4. Right-Click Menu ---
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="✅ Mark as Done", command=self.context_mark_done)
        self.context_menu.add_command(label="❌ Delete Task", command=self.context_delete)
        self.tree.bind("<Button-3>", self.show_context_menu) # Right-click bind

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg='#f4f4f4')
        btn_frame.pack(fill='x', pady=15)
        
        b_style = {'width': 15, 'bg': '#e1e1e1', 'font': ('Arial', 10)}
        tk.Button(btn_frame, text="➕ Add Task", **b_style, command=self.gui_addTask).pack(side='left', padx=20)
        tk.Button(btn_frame, text="♻️ Refresh", **b_style, command=self.refresh_table).pack(side='left', padx=5)
        tk.Button(btn_frame, text="📊 View Stats", **b_style, command=self.show_stats).pack(side='right', padx=20)

        # Initial Load
        self.refresh_table()

    # --- GUI Logic ---

    def refresh_table(self):
        """ Clears and re-populates the treeview from file """
        self.all_tasks = logic_get_tasks_data() # Store in memory for searching
        self.update_tree(self.all_tasks)
        self.update_progress()

    def update_tree(self, tasks_list):
        """ Helper to insert rows into Treeview """
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for t in tasks_list:
            tag = 'normal'
            if t['status'] == 'Done': tag = 'done'
            elif t['prio'] == '5': tag = 'high_prio'
            
            self.tree.insert('', 'end', values=(t['file_id'], t['name'], t['desc'], t['prio'], t['status']), tags=(tag,))

    def filter_tasks(self, event):
        """ Search Logic """
        query = self.search_entry.get().lower()
        if not query:
            self.update_tree(self.all_tasks)
            return

        filtered = [t for t in self.all_tasks if query in t['name'].lower() or query in t['desc'].lower()]
        self.update_tree(filtered)

    def update_progress(self):
        """ Updates the progress bar """
        total = len(self.all_tasks)
        if total == 0:
            pct = 0
        else:
            done_count = sum(1 for t in self.all_tasks if t['status'] == 'Done')
            pct = (done_count / total) * 100
        
        self.progress_var.set(pct)
        self.lbl_progress.config(text=f"{int(pct)}%")

    def show_context_menu(self, event):
        """ Selects the row under mouse and shows menu """
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def get_selected_id(self):
        """ Returns the 'file_id' of the selected row """
        selected_item = self.tree.selection()
        if not selected_item: return None
        # The values are (id, name, desc...) - ID is index 0
        vals = self.tree.item(selected_item)['values']
        return int(vals[0])

    # --- Actions ---

    def gui_addTask(self):
        name = simpledialog.askstring("Input", "Task Name:")
        if not name: return
        desc = simpledialog.askstring("Input", "Description:")
        if not desc: return
        prio = simpledialog.askinteger("Input", "Priority (1-5):", minvalue=1, maxvalue=5)
        if prio is None: return
        
        logic_addTask(name, desc, str(prio))
        self.refresh_table()

    def context_mark_done(self):
        file_id = self.get_selected_id()
        if file_id:
            success, msg = logic_changeTaskStatus(file_id)
            if success:
                self.refresh_table()
            else:
                messagebox.showwarning("Info", msg)

    def context_delete(self):
        file_id = self.get_selected_id()
        if file_id:
            if messagebox.askyesno("Confirm", f"Delete Task ID {file_id}?"):
                success, msg = logic_deleteTask(file_id)
                messagebox.showinfo("Result", msg)
                self.refresh_table()

    def show_stats(self):
        # A simple popup stat feature
        total = len(self.all_tasks)
        done = sum(1 for t in self.all_tasks if t['status'] == 'Done')
        msg = f"Total Tasks: {total}\nCompleted: {done}\nPending: {total - done}"
        messagebox.showinfo("Statistics", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()