import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# =============================================================================
# CORE LOGIC
# =============================================================================

def countLinesInFile(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r') as file:
        return sum(1 for line in file)

def logic_addTask(name, description, priority, deadline):
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as file:
            file.write("TASKS :\n")
    
    with open("tasks.txt", "a") as file:
        lineCount = countLinesInFile("tasks.txt")
        if lineCount <= 1:
            iD = 1
        else:
            iD = (lineCount - 1) // 5 + 1
        file.write(f"{iD}. Task: {name}\n...Description: {description}\n...Priority level: {priority}\n...Status: Not Done\n...Due: {deadline}\n")

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
            if i+4 < len(lines):
                file_id = (i - 1) // 5 + 1
                
                raw_name = lines[i].strip()
                raw_desc = lines[i+1].strip()
                raw_prio = lines[i+2].strip()
                raw_stat = lines[i+3].strip()
                raw_date = lines[i+4].strip()

                name = raw_name.split('.', 1)[1].strip() if '.' in raw_name else raw_name
                desc = raw_desc.replace("...Description:", "").strip()
                prio = raw_prio.replace("...Priority level:", "").strip()
                stat = raw_stat.replace("...Status:", "").strip()
                date = raw_date.replace("...Due:", "").strip()

                tasks.append({
                    'file_id': file_id,
                    'name': name,
                    'desc': desc,
                    'prio': int(prio),
                    'status': stat,
                    'date': date
                })
        except IndexError:
            break
        except ValueError:
            pass 
        i += 5
    return tasks

def logic_deleteTask(file_id):
    l = countLinesInFile("tasks.txt")
    totalTasks = (l - 1) // 5
    
    if totalTasks == 0: return False, "No tasks available."
    
    with open("tasks.txt", "r") as temp:
        lines = temp.readlines()

    with open("tasks.txt", "w") as file:
        file.write("TASKS :\n")

    i = 1 
    iD = 1
    deleted = False
    
    while i < len(lines):
        current_task_index = (i - 1) // 5 + 1
        
        if current_task_index == file_id:
            if not os.path.exists("bin.txt"):
                with open("bin.txt", "w") as bin_file:
                    bin_file.write("DELETED TASKS :\n")
            with open("bin.txt", "a") as bin_file:
                bin_file.write(f"DEL. {lines[i][3:]}{lines[i+1]}{lines[i+2]}{lines[i+3]}{lines[i+4]}")
            deleted = True
            i += 5
        else:
            with open("tasks.txt", "a") as file:
                if i+4 < len(lines):
                    tsk = lines[i].split('.', 1)[1] if '.' in lines[i] else lines[i]
                    desc = lines[i+1]
                    prio = lines[i+2]
                    stat = lines[i+3]
                    date = lines[i+4]
                    file.write(f"{iD}.{tsk}{desc}{prio}{stat}{date}")
                    iD += 1
            i += 5
    
    if deleted: return True, "Task deleted."
    else: return False, "Task not found."

# --- UPDATED: Unified Status Change Logic ---
def logic_setTaskStatus(file_id, target_status):
    """
    target_status: "Done" or "Not Done"
    """
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
    
    target_line_idx = 1 + (file_id - 1) * 5 + 3
    
    if target_line_idx < len(lines):
        current_line = lines[target_line_idx]
        
        if target_status == "Done":
            if "Not Done" in current_line:
                 lines[target_line_idx] = "...Status: Done\n"
                 with open("tasks.txt", "w") as f: f.writelines(lines)
                 return True, "Marked as Done."
            else: return False, "Task is already Done."
            
        elif target_status == "Not Done":
            # Check if it IS "Done" (and avoid matching "Not Done" substring)
            if "Done" in current_line and "Not" not in current_line:
                 lines[target_line_idx] = "...Status: Not Done\n"
                 with open("tasks.txt", "w") as f: f.writelines(lines)
                 return True, "Marked as Undone."
            else: return False, "Task is already Not Done."
            
    return False, "Error finding task."

def logic_editTask(file_id, new_name, new_desc, new_prio, new_date):
    if not os.path.exists("tasks.txt"): return False, "File not found."
    
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
        
    start_idx = 1 + (file_id - 1) * 5
    
    if start_idx + 4 >= len(lines):
        return False, "Task not found."
        
    current_line = lines[start_idx]
    if ". " in current_line:
        id_part = current_line.split(". ", 1)[0] + ". "
    else:
        id_part = f"{file_id}. "
        
    lines[start_idx] = f"{id_part}Task: {new_name}\n"
    lines[start_idx+1] = f"...Description: {new_desc}\n"
    lines[start_idx+2] = f"...Priority level: {new_prio}\n"
    lines[start_idx+4] = f"...Due: {new_date}\n"
    
    with open("tasks.txt", "w") as f:
        f.writelines(lines)
        
    return True, "Task updated successfully."

# =============================================================================
# GUI IMPLEMENTATION
# =============================================================================

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoApp")
        self.root.geometry("850x600")
        self.root.configure(bg='#f4f4f4')
        
        self.highlighted_ids = self.load_highlights()

        # --- Header ---
        header_frame = tk.Frame(root, bg='#f4f4f4')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        title_box = tk.Frame(header_frame, bg='#f4f4f4')
        title_box.pack(side='left')
        
        tk.Label(title_box, text="ToDoApp", font=("Segoe UI", 20, "bold"), bg='#f4f4f4', fg='#333').pack(anchor='w')
        tk.Label(title_box, text="Manage your tasks efficiently", font=("Segoe UI", 10), bg='#f4f4f4', fg='#777').pack(anchor='w')
        
        self.lbl_pending = tk.Label(header_frame, text="Pending Tasks: 0", font=("Arial", 10, "bold"), bg='#f4f4f4', fg='#000000')
        self.lbl_pending.pack(side='right', pady=5)

        # --- Controls ---
        control_frame = tk.Frame(root, bg='#f4f4f4')
        control_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Label(control_frame, text="🔍 Search:", bg='#f4f4f4', font=("Arial", 11)).pack(side='left')
        self.search_entry = tk.Entry(control_frame, font=("Arial", 11), width=20)
        self.search_entry.pack(side='left', padx=(5, 15))
        self.search_entry.bind('<KeyRelease>', self.apply_filters)

        tk.Label(control_frame, text="🔃 Sort By:", bg='#f4f4f4', font=("Arial", 11)).pack(side='left')
        self.sort_options = [
            "Default (Order Added)", 
            "Priority (High -> Low)", 
            "Priority (Low -> High)",
            "Status (Pending First)",
            "Date (Earliest Due)"
        ]
        self.sort_var = tk.StringVar(value=self.sort_options[0])
        self.sort_menu = ttk.Combobox(control_frame, textvariable=self.sort_var, values=self.sort_options, state="readonly", width=25)
        self.sort_menu.pack(side='left', padx=5)
        self.sort_menu.bind("<<ComboboxSelected>>", self.apply_filters)

        # --- Table ---
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=5)

        cols = ('id', 'name', 'desc', 'prio', 'date', 'status')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=15)
        
        self.tree.column('id', width=40, anchor='center')
        self.tree.column('name', width=140, anchor='w')
        self.tree.column('desc', width=220, anchor='w')
        self.tree.column('prio', width=60, anchor='center')
        self.tree.column('date', width=100, anchor='center')
        self.tree.column('status', width=90, anchor='center')

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Task Name')
        self.tree.heading('desc', text='Description')
        self.tree.heading('prio', text='Priority')
        self.tree.heading('date', text='Due Date')
        self.tree.heading('status', text='Status')

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Tags
        self.tree.tag_configure('done', foreground='gray')
        self.tree.tag_configure('highlight', background='#fff9c4') 
        self.tree.tag_configure('overdue', foreground='red')
        self.tree.tag_configure('today', foreground='#d35400')

        # --- Context Menu ---
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="✏️ Edit Task", command=self.context_edit)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="⭐ Highlight / Unhighlight", command=self.context_toggle_highlight)
        self.context_menu.add_command(label="✅ Mark as Done", command=self.context_mark_done)
        self.context_menu.add_command(label="↩️ Mark as Undone", command=self.context_mark_undone) # NEW OPTION
        self.context_menu.add_separator()
        self.context_menu.add_command(label="❌ Delete Task", command=self.context_delete)
        self.tree.bind("<Button-3>", self.show_context_menu) 

        # --- Buttons ---
        btn_frame = tk.Frame(root, bg='#f4f4f4')
        btn_frame.pack(fill='x', pady=15)
        
        b_style = {'width': 15, 'bg': '#e1e1e1', 'font': ('Arial', 10)}
        tk.Button(btn_frame, text="➕ Add Task", **b_style, command=self.gui_addTask).pack(side='left', padx=20)
        tk.Button(btn_frame, text="♻️ Refresh", **b_style, command=self.refresh_table).pack(side='left', padx=5)

        self.all_tasks = []
        self.refresh_table()

    # --- Helpers ---
    def load_highlights(self):
        if not os.path.exists("highlights.txt"): return set()
        with open("highlights.txt", "r") as f:
            content = f.read().strip()
            if not content: return set()
            try: return set(map(int, content.split(',')))
            except ValueError: return set()

    def save_highlights(self, id_set):
        with open("highlights.txt", "w") as f:
            f.write(",".join(map(str, id_set)))

    def get_date_status(self, date_str):
        try:
            due = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            if due < today: return 'overdue'
            elif due == today: return 'today'
            return 'normal'
        except ValueError:
            return 'normal'

    # --- GUI Logic ---

    def refresh_table(self):
        self.all_tasks = logic_get_tasks_data() 
        self.apply_filters(None) 
        self.update_stats_label() 

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
        elif sort_mode == "Status (Pending First)":
            filtered_data.sort(key=lambda x: 0 if "Not" in x['status'] else 1)
        elif sort_mode == "Date (Earliest Due)":
             filtered_data.sort(key=lambda x: x['date'])
        else:
            filtered_data.sort(key=lambda x: x['file_id'])

        self.update_tree(filtered_data)

    def update_tree(self, tasks_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for t in tasks_list:
            tag_list = []
            
            # 1. Status Check
            if t['status'] == 'Done': 
                tag_list.append('done')
            else:
                d_stat = self.get_date_status(t['date'])
                if d_stat == 'overdue': tag_list.append('overdue')
                elif d_stat == 'today': tag_list.append('today')

            # 2. Highlight Check
            if t['file_id'] in self.highlighted_ids: 
                tag_list.append('highlight')
            
            self.tree.insert('', 'end', values=(t['file_id'], t['name'], t['desc'], t['prio'], t['date'], t['status']), tags=tuple(tag_list))

    def update_stats_label(self):
        if not self.all_tasks: pending_count = 0
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
        date = simpledialog.askstring("Input", "Due Date (YYYY-MM-DD):")
        if not date: date = "2025-12-31" 
        
        logic_addTask(name, desc, str(prio), date)
        self.refresh_table()

    def context_edit(self):
        file_id = self.get_selected_id()
        if not file_id: return
        
        vals = self.tree.item(self.tree.selection()[0])['values']
        
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Task")
        edit_win.geometry("300x320")
        
        tk.Label(edit_win, text="Task Name:").pack(pady=(5, 0))
        entry_name = tk.Entry(edit_win, width=30); entry_name.pack(pady=2)
        entry_name.insert(0, vals[1])
        
        tk.Label(edit_win, text="Description:").pack()
        entry_desc = tk.Entry(edit_win, width=30); entry_desc.pack(pady=2)
        entry_desc.insert(0, vals[2])
        
        tk.Label(edit_win, text="Priority (1-5):").pack()
        entry_prio = tk.Entry(edit_win, width=10); entry_prio.pack(pady=2)
        entry_prio.insert(0, vals[3])

        tk.Label(edit_win, text="Due Date (YYYY-MM-DD):").pack()
        entry_date = tk.Entry(edit_win, width=15); entry_date.pack(pady=2)
        entry_date.insert(0, vals[4])
        
        def save_changes():
            n, d, dt = entry_name.get(), entry_desc.get(), entry_date.get()
            try:
                p = int(entry_prio.get())
                if p < 1 or p > 5: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Priority must be 1-5")
                return
            
            if n and d and dt:
                success, msg = logic_editTask(file_id, n, d, str(p), dt)
                if success:
                    self.refresh_table()
                    edit_win.destroy()
                else: messagebox.showerror("Error", msg)
            else: messagebox.showerror("Error", "Fields cannot be empty")

        tk.Button(edit_win, text="💾 Save", command=save_changes, bg='#e1e1e1').pack(pady=15)

    def context_toggle_highlight(self):
        file_id = self.get_selected_id()
        if file_id:
            if file_id in self.highlighted_ids: self.highlighted_ids.remove(file_id)
            else: self.highlighted_ids.add(file_id)
            self.save_highlights(self.highlighted_ids)
            self.refresh_table()

    def context_mark_done(self):
        file_id = self.get_selected_id()
        if file_id:
            # Passes "Done" as the target state
            success, msg = logic_setTaskStatus(file_id, "Done")
            if success: 
                if file_id in self.highlighted_ids:
                    self.highlighted_ids.remove(file_id)
                    self.save_highlights(self.highlighted_ids)
                self.refresh_table()
            else: messagebox.showwarning("Info", msg)

    # --- NEW: Context Mark Undone Method ---
    def context_mark_undone(self):
        file_id = self.get_selected_id()
        if file_id:
            # 1. Ask for confirmation
            confirm = messagebox.askyesno("Confirm", "Are you sure to mark this task undone?")
            if confirm:
                # 2. Passes "Not Done" as target state
                success, msg = logic_setTaskStatus(file_id, "Not Done")
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
                    self.save_highlights(self.highlighted_ids)
                messagebox.showinfo("Result", msg)
                self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()