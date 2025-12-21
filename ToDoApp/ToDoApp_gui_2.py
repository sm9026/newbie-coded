import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# =============================================================================
# CORE LOGIC
# =============================================================================

def countLinesInFile(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r') as file:
        return sum(1 for line in file)

def logic_addTask(name, description, priority):
    # Mode is always append to the main file
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as file:
            file.write("TASKS :\n")
    
    with open("tasks.txt", "a") as file:
        lineCount = countLinesInFile("tasks.txt")
        # Header is 1 line. Each task is now 4 lines.
        if lineCount <= 1:
            iD = 1
        else:
            iD = (lineCount - 1) // 4 + 1
            
        # Standard 4-line DB format
        file.write(f"{iD}. Task: {name}\n...Description: {description}\n...Priority level: {priority}\n...Status: Not Done\n")

def logic_viewTasks(mode):
    # Modes: "ALL", "PENDING", "DONE", "BIN"
    # Note: This function handles the standard 4-line DB format.
    
    target_file = "bin.txt" if mode == "BIN" else "tasks.txt"

    if not os.path.exists(target_file):
        return "File not found or empty."

    with open(target_file, 'r') as viewFile:
        lines = viewFile.readlines()

    if len(lines) <= 1:
        return "No tasks found."

    content = ""
    i = 1
    display_id = 1
    
    while i < len(lines):
        try:
            line_name = lines[i]
            line_desc = lines[i+1]
            line_prio = lines[i+2]
            line_stat = lines[i+3]
            
            # Logic to filter based on status line
            include_task = False
            
            if mode == "ALL" or mode == "BIN":
                include_task = True
            elif mode == "PENDING" and "Not Done" in line_stat:
                include_task = True
            elif mode == "DONE" and "Not Done" not in line_stat and "Done" in line_stat:
                include_task = True
                
            if include_task:
                # Clean the ID for display
                split_name = line_name.split('.', 1)
                clean_name = split_name[1] if len(split_name) > 1 else line_name
                
                content += f"{display_id}.{clean_name}{line_desc}{line_prio}{line_stat}"
                display_id += 1
            
            i += 4
        except IndexError:
            break 

    if content == "":
        return f"No tasks found for category: {mode}"
        
    return content

def logic_deleteTask(toDelete):
    l = countLinesInFile("tasks.txt")
    totalTasks = (l - 1) // 4
    
    if totalTasks == 0: return False, "No tasks available to delete."
    if toDelete < 1 or toDelete > totalTasks: return False, f"Invalid task number. Please enter a number between 1 and {totalTasks}."

    with open("tasks.txt", "r") as temp:
        lines = temp.readlines()

    with open("tasks.txt", "w") as file:
        file.write("TASKS :\n")

    i = 1 
    iD = 1
    
    while i < len(lines):
        current_task_index = (i - 1) // 4 + 1
        
        if current_task_index == toDelete:
            # Add to BIN
            if not os.path.exists("bin.txt"):
                with open("bin.txt", "w") as bin_file:
                    bin_file.write("DELETED TASKS :\n")
            
            with open("bin.txt", "a") as bin_file:
                tsk = lines[i][3:] # Strip old ID
                desc = lines[i+1]
                prio = lines[i+2]
                stat = lines[i+3]
                
                l_bin = countLinesInFile("bin.txt")
                BiD = 1 if l_bin <= 1 else (l_bin - 1) // 4 + 1
                bin_file.write(f"{BiD}. {tsk}{desc}{prio}{stat}")
            
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

    return True, "Task deleted successfully."

def logic_changeTaskStatus(toChange):
    with open("tasks.txt", "r") as f:
        lines = f.readlines()
        
    pending_indices = [] 
    
    i = 1
    while i < len(lines):
        if i+3 < len(lines):
            if "Not Done" in lines[i+3]:
                pending_indices.append(i)
        i += 4
        
    totalPending = len(pending_indices)
    
    if totalPending == 0: return False, "No pending tasks found."
    if toChange < 1 or toChange > totalPending: return False, f"Invalid selection. Only {totalPending} pending tasks."

    target_line_index = pending_indices[toChange - 1] 
    status_line_index = target_line_index + 3
    
    lines[status_line_index] = "...Status: Done\n"
    
    with open("tasks.txt", "w") as f:
        f.writelines(lines)
        
    return True, "Task marked as DONE."

def logic_sortTasks(mode_filter="ALL"):
    filename = "tasks.txt"
    if not os.path.exists(filename) or countLinesInFile(filename) <= 1:
        return f"Cannot sort: '{filename}' is empty."

    with open(filename, 'r') as file:
        lines = file.readlines()

    # We write a custom visual format to SortedTasks.txt
    with open("SortedTasks.txt", "w") as sortedFile:
        sortedFile.write("SORTED TASKS :\n")
        
        # Iterate priorities 5 down to 1
        for p in range(5, 0, -1):
            
            found_tasks = []
            
            i = 1
            while i < len(lines):
                if i+3 < len(lines):
                    try: 
                        prio_line = lines[i+2].strip()
                        prio_val = int(prio_line.split(':')[-1].strip())
                    except ValueError: 
                        prio_val = 0
                    
                    status_line = lines[i+3]
                    
                    is_match = False
                    if prio_val == p:
                        if mode_filter == "ALL": is_match = True
                        elif mode_filter == "PENDING" and "Not Done" in status_line: is_match = True
                        elif mode_filter == "DONE" and "Done" in status_line and "Not" not in status_line: is_match = True
                    
                    if is_match:
                        # Grab lines: Name, Desc, Status (Skip Priority line for display as requested)
                        found_tasks.append((lines[i], lines[i+1], lines[i+3]))
                        
                i += 4
            
            # Write block if tasks exist for this priority
            if found_tasks:
                sortedFile.write(f"\n--* PRIORITY: {p} *--\n")
                Sid = 1 # Reset ID for each priority level
                for t in found_tasks:
                    # Clean the Name line (remove Old ID)
                    raw_name = t[0].strip()
                    if '.' in raw_name:
                        # "1. Task: Name" -> "Task: Name"
                        clean_name = raw_name.split('.', 1)[1].strip()
                    else:
                        clean_name = raw_name
                    
                    # Clean Description and Status for custom formatting
                    # t[1] = "...Description: abc" -> we want to ensure "....Description: abc"
                    raw_desc = t[1].strip()
                    desc_text = raw_desc.replace("...", "").replace("....", "").strip() 
                    if desc_text.startswith("Description:"): desc_text = desc_text[12:].strip()
                    
                    # t[2] = "...Status: abc"
                    raw_stat = t[2].strip()
                    stat_text = raw_stat.replace("...", "").replace("....", "").strip()
                    if stat_text.startswith("Status:"): stat_text = stat_text[7:].strip()

                    # Write in specific requested format
                    sortedFile.write(f"{Sid}. {clean_name}\n")
                    sortedFile.write(f"....Description: {desc_text}\n")
                    sortedFile.write(f"....Status: {stat_text}\n")
                    
                    Sid += 1
    
    # Return the content directly, do not use logic_viewTasks which expects different format
    with open("SortedTasks.txt", "r") as f:
        return f.read()

# =============================================================================
# GUI IMPLEMENTATION
# =============================================================================

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoApp Task Manager (Unified File)")
        self.root.geometry("620x600")
        self.root.configure(bg='#f0f0f0')

        tk.Label(root, text="🚀 Unified Task Manager", font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#333333').pack(pady=10)
        self.btn_frame = tk.Frame(root, bg='#f0f0f0')
        self.btn_frame.pack(pady=5, padx=10)
        
        b_style = {'width': 18, 'height': 1, 'font': ('Arial', 10), 'bg': '#e0e0e0', 'fg': '#000000'}
        
        tk.Button(self.btn_frame, text="➕ Add Task", **b_style, command=self.gui_addTask).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="❌ Delete (Any)", **b_style, command=self.gui_deleteTask).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="✅ Mark Done", **b_style, command=self.gui_changeStatus).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(self.btn_frame, text="📋 View All", **b_style, command=lambda: self.gui_viewFile("ALL")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="⏳ View Pending", **b_style, command=lambda: self.gui_viewFile("PENDING")).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="☑️ View Completed", **b_style, command=lambda: self.gui_viewFile("DONE")).grid(row=1, column=2, padx=5, pady=5)
        
        tk.Button(self.btn_frame, text="🗑️ View Bin", **b_style, command=lambda: self.gui_viewFile("BIN")).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="📊 Sort (All)", **b_style, command=self.gui_sortTasks).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="🚪 Exit", **b_style, command=root.quit).grid(row=2, column=2, padx=5, pady=5)

        tk.Label(root, text="Task Display Area:", font=("Arial", 12), bg='#f0f0f0', fg='#333333').pack(pady=(5, 2))
        self.display_area = scrolledtext.ScrolledText(root, width=75, height=20, font=("Courier", 10), bg='#ffffff', fg='#000000')
        self.display_area.pack(pady=10)
        
        self.gui_viewFile("ALL")

    def update_display(self, text):
        self.display_area.delete(1.0, tk.END)
        self.display_area.insert(tk.END, text)

    def gui_addTask(self):
        name = simpledialog.askstring("Input", "Enter the name of the task:")
        if not name: return
        desc = simpledialog.askstring("Input", "Enter task description:")
        if not desc: return
        prio = simpledialog.askinteger("Input", "Enter task priority (1-5):", minvalue=1, maxvalue=5)
        if prio is None: return
        
        logic_addTask(name, desc, str(prio))
        messagebox.showinfo("Success", "Task added successfully!")
        self.gui_viewFile("ALL")

    def gui_viewFile(self, mode):
        self.update_display(logic_viewTasks(mode))

    def gui_deleteTask(self):
        self.gui_viewFile("ALL")
        val = simpledialog.askinteger("Input", "Enter the task number (from 'View All') to delete:")
        if val is None: return
        success, msg = logic_deleteTask(val)
        if success: 
            messagebox.showinfo("Success", msg)
            self.gui_viewFile("ALL")
        else: 
            messagebox.showerror("Error", msg)

    def gui_changeStatus(self):
        self.gui_viewFile("PENDING")
        val = simpledialog.askinteger("Input", "Enter PENDING task number to mark DONE:")
        if val is None: return
        success, msg = logic_changeTaskStatus(val)
        if success: 
            messagebox.showinfo("Success", msg)
            self.gui_viewFile("PENDING")
        else: 
            messagebox.showerror("Error", msg)

    def gui_sortTasks(self):
        choice = simpledialog.askinteger("Sort", "1: All Tasks\n2: Pending Only\n3: Done Only\n\nEnter choice:", minvalue=1, maxvalue=3)
        if choice == 1: mode = "ALL"
        elif choice == 2: mode = "PENDING"
        elif choice == 3: mode = "DONE"
        else: return
        
        res = logic_sortTasks(mode)
        if "Cannot sort" in res: messagebox.showerror("Error", res)
        else: 
            messagebox.showinfo("Success", "Tasks sorted.")
            self.update_display(res)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()