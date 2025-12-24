import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# =============================================================================
# CORE LOGIC
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
    tasks = []
    if not os.path.exists("tasks.txt"):
        return tasks

    with open("tasks.txt", "r") as f:
        lines = f.readlines()

    if len(lines) <= 1:
        return tasks

    i = 1
    while i < len(lines):
        try:
            if i+3 < len(lines):
                file_id = (i - 1) // 4 + 1
                
                raw_name = lines[i].strip()
                raw_desc = lines[i+1].strip()
                raw_prio = lines[i+2].strip()
                raw_stat = lines[i+3].strip()

                name = raw_name.split('.', 1)[1].strip() if '.' in raw_name else raw_name
                desc = raw_desc.replace("...Description:", "").strip()
                prio = raw_prio.replace("...Priority level:", "").strip()
                stat = raw_stat.replace("...Status:", "").strip()

                tasks.append({
                    'file_id': file_id,
                    'name': name,
                    'desc': desc,
                    'prio': int(prio),
                    'status': stat
                })
        except IndexError:
            break
        except ValueError:
            pass 
        i += 4
    return tasks

def logic_deleteTask(file_id):
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
            if not os.path.exists("bin.txt"):
                with open("bin.txt", "w") as bin_file:
                    bin_file.write("DELETED TASKS :\n")
            with open("bin.txt", "a") as bin_file:
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
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
        
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
# HIGHLIGHT PERSISTENCE
# =============================================================================

def load_highlights():
    if not os.path.exists("highlights.txt"):
        return set()
    with open("highlights.txt", "r") as f:
        content = f.read().strip()
        if not content: return set()
        try:
            return set(map(int, content.split(',')))
        except ValueError:
            return set()

def save_highlights(id_set):
    with open("highlights.txt", "w") as f:
        f.write(",".join(map(str, id_set)))

# =============================================================================
# GUI IMPLEMENTATION
# =============================================================================

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoApp")
        self.root.geometry("750x600")
        self.root.configure(bg='#f4f4f4')
        
        self.highlighted_ids = load_highlights()

        # --- 1. Header & Pending Count ---
        header_frame = tk.Frame(root, bg='#f4f4f4')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        # Title Container
        title_box = tk.Frame(header_frame, bg='#f4f4f4')
        title_box.pack(side='left')
        
        tk.Label(title_box, text="ToDoApp", font=("Segoe UI", 20, "bold"), bg='#f4f4f4', fg='#333').pack(anchor='w')
        tk.Label(title_box, text="Manage your tasks efficiently", font=("Segoe UI", 10), bg='#f4f4f4', fg='#777').pack(anchor='w')
        
        # Pending Counter (Replaces Progress Bar)
        self.lbl_pending = tk.Label(header_frame, text="Pending Tasks: 0", font=("Arial", 10, "bold"), bg='#f4f4f4', fg="#000000")
        self.lbl_pending.pack(side='right', pady=5)

        # --- 2. Search & Sort Bar ---
        control_frame = tk.Frame(root, bg='#f4f4f4')
        control_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # SEARCH
        tk.Label(control_frame, text="🔍 Search:", bg='#f4f4f4', font=("Arial", 11)).pack(side='left')
        self.search_entry = tk.Entry(control_frame, font=("Arial", 11), width=25)
        self.search_entry.pack(side='left', padx=(5, 20))
        self.search_entry.bind('<KeyRelease>', self.apply_filters)

        # SORTING
        tk.Label(control_frame, text="🔃 Sort By:", bg='#f4f4f4', font=("Arial", 11)).pack(side='left')
        
        self.sort_options = ["Default (Order Added)", "Priority (High -> Low)", "Priority (Low -> High)"]
        self.sort_var = tk.StringVar(value=self.sort_options[0])
        
        self.sort_menu = ttk.Combobox(control_frame, textvariable=self.sort_var, values=self.sort_options, state="readonly", width=22)
        self.sort_menu.pack(side='left', padx=5)
        self.sort_menu.bind("<<ComboboxSelected>>", self.apply_filters)

        # --- 3. Treeview Table ---
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=5)

        cols = ('id', 'name', 'desc', 'prio', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=15)
        
        self.tree.column('id', width=40, anchor='center')
        self.tree.column('name', width=150, anchor='w')
        self.tree.column('desc', width=250, anchor='w')
        self.tree.column('prio', width=60, anchor='center')
        self.tree.column('status', width=100, anchor='center')

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Task Name')
        self.tree.heading('desc', text='Description')
        self.tree.heading('prio', text='Priority')
        self.tree.heading('status', text='Status')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.tag_configure('done', foreground='gray')
        self.tree.tag_configure('highlight', background='#fff9c4') # Light Yellow

        # --- 4. Right-Click Menu ---
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="⭐ Highlight / Unhighlight", command=self.context_toggle_highlight)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✅ Mark as Done", command=self.context_mark_done)
        self.context_menu.add_command(label="❌ Delete Task", command=self.context_delete)
        self.tree.bind("<Button-3>", self.show_context_menu) 

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg='#f4f4f4')
        btn_frame.pack(fill='x', pady=15)
        
        b_style = {'width': 15, 'bg': '#e1e1e1', 'font': ('Arial', 10)}
        tk.Button(btn_frame, text="➕ Add Task", **b_style, command=self.gui_addTask).pack(side='left', padx=20)
        tk.Button(btn_frame, text="♻️ Refresh", **b_style, command=self.refresh_table).pack(side='left', padx=5)
        # Removed View Stats Button

        self.all_tasks = []
        self.refresh_table()

    # --- GUI Logic ---

    def refresh_table(self):
        self.all_tasks = logic_get_tasks_data() 
        self.apply_filters(None) 
        self.update_stats_label() # Updates pending count

    def apply_filters(self, event):
        query = self.search_entry.get().lower()
        if query:
            filtered_data = [t for t in self.all_tasks if query in t['name'].lower() or query in t['desc'].lower()]
        else:
            filtered_data = self.all_tasks.copy()

        sort_mode = self.sort_var.get()
        if sort_mode == "Priority (High -> Low)":
            filtered_data.sort(key=lambda x: x['prio'], reverse=True)
        elif sort_mode == "Priority (Low -> High)":
            filtered_data.sort(key=lambda x: x['prio'], reverse=False)
        else:
            filtered_data.sort(key=lambda x: x['file_id'])

        self.update_tree(filtered_data)

    def update_tree(self, tasks_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for t in tasks_list:
            tag_list = []
            if t['status'] == 'Done': tag_list.append('done')
            if t['file_id'] in self.highlighted_ids: tag_list.append('highlight')
            
            self.tree.insert('', 'end', values=(t['file_id'], t['name'], t['desc'], t['prio'], t['status']), tags=tuple(tag_list))

    def update_stats_label(self):
        """ Calculates Pending tasks and updates label """
        if not self.all_tasks:
            pending_count = 0
        else:
            done_count = sum(1 for t in self.all_tasks if t['status'] == 'Done')
            pending_count = len(self.all_tasks) - done_count
        
        self.lbl_pending.config(text=f"Pending Tasks: {pending_count}")

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def get_selected_id(self):
        selected_item = self.tree.selection()
        if not selected_item: return None
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

    def context_toggle_highlight(self):
        file_id = self.get_selected_id()
        if file_id:
            if file_id in self.highlighted_ids:
                self.highlighted_ids.remove(file_id)
            else:
                self.highlighted_ids.add(file_id)
            save_highlights(self.highlighted_ids)
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
                if file_id in self.highlighted_ids:
                    self.highlighted_ids.remove(file_id)
                    save_highlights(self.highlighted_ids)
                messagebox.showinfo("Result", msg)
                self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()