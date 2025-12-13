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
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as file:
            file.write("TASKS :\n")
        mode = "a"
    else:
        mode = "a"

    with open("tasks.txt", mode) as file:
        lineCount = countLinesInFile("tasks.txt")
        if lineCount == 0:
            iD = 1
        else:
            iD = lineCount // 3 + 1
        file.write(f"{iD}. Task: {name}\n...Description: {description}\n...Priority level: {priority}\n")

    if not os.path.exists("NotDone.txt"):
        with open("NotDone.txt", "w") as file:
            file.write("TASK STATUS: NOT DONE:\n")
        mode = "a"
    else:
        mode = "a"

    with open("NotDone.txt", mode) as file:
        file.write(f"{iD}. Task: {name}\n...Description: {description}\n...Priority level: {priority}\n")

def logic_viewTasks(filename):
    if not os.path.exists(filename):
        if filename == "tasks.txt": return "No tasks found. Add a task to begin."
        elif filename == "bin.txt": return "No deleted tasks found in the bin."
        elif filename == "Done.txt": return "No tasks marked as done yet."
        elif filename == "NotDone.txt": return "All tasks are currently done or the file is empty."
        else: return "File not found or empty."

    content = ""
    with open(filename, 'r') as viewFile:
        for line in viewFile:
            content += line
    return content

def logic_deleteTask(toDelete):
    l = countLinesInFile("tasks.txt")
    totalTasks = (l - 1) // 3
    
    if totalTasks == 0: return False, "No tasks available to delete."
    if toDelete < 1 or toDelete > totalTasks: return False, f"Invalid task number. Please enter a number between 1 and {totalTasks}."
    if not os.path.exists("tasks.txt"): return False, "No tasks found."

    with open("tasks.txt", "r") as temp:
        lines = temp.readlines()

    with open("tasks.txt", "w") as file:
        file.write("TASKS :\n")

    i = 1 
    iD = 1
    while i < len(lines):
        if (i - 1) // 3 + 1 == toDelete:
            if not os.path.exists("bin.txt"):
                with open("bin.txt", "w") as bin_file:
                    bin_file.write("DELETED TASKS :\n")
            with open("bin.txt", "a") as bin_file:
                tsk = lines[i][3:]; i += 1
                desc = lines[i]; i += 1
                prio = lines[i]; i += 1
                lineCount = countLinesInFile("bin.txt")
                BiD = 1 if lineCount == 0 else lineCount // 3 + 1
                bin_file.write(f"{BiD}. {tsk}{desc}{prio}")
            continue
        else:
            with open("tasks.txt", "a") as file:
                tsk = lines[i][3:]; i += 1
                desc = lines[i]; i += 1
                prio = lines[i]; i += 1
                file.write(f"{iD}. {tsk}{desc}{prio}")
                iD += 1
    return True, "Task deleted successfully."

def logic_changeTaskStatus(toChange):
    count_not_done = countLinesInFile("NotDone.txt")
    totalTasks = (count_not_done - 1) // 3
    
    if totalTasks == 0: return False, "No tasks are currently pending."
    if toChange < 1 or toChange > totalTasks: return False, f"Invalid task number. Please enter a number between 1 and {totalTasks}."
    if not os.path.exists("NotDone.txt"): return False, "No tasks found in the 'Not Done' list."

    with open("NotDone.txt", "r") as temp:
        lines = temp.readlines()

    with open("NotDone.txt", "w") as file:
        file.write("TASK STATUS: NOT DONE:\n")

    i = 1; iD = 1; lc = len(lines)
    while i < lc:
        if (i - 1) // 3 + 1 == toChange:
            if not os.path.exists("Done.txt"):
                with open("Done.txt", "w") as done:
                    done.write("TASK STATUS: DONE:\n")
            with open("Done.txt", "a") as done:
                tsk = lines[i][3:]; i += 1
                desc = lines[i]; i += 1
                prio = lines[i]; i += 1
                lineCount = countLinesInFile("Done.txt")
                DiD = 1 if lineCount == 0 else lineCount // 3 + 1
                done.write(f"{DiD}. {tsk}{desc}{prio}")
            continue
        else:
            with open("NotDone.txt", "a") as file:
                tsk = lines[i][3:]; i += 1
                desc = lines[i]; i += 1
                prio = lines[i]; i += 1
                file.write(f"{iD}. {tsk}{desc}{prio}")
                iD += 1
    return True, "Task successfully marked as DONE."

def logic_sortTasks(filename):
    if not os.path.exists(filename) or countLinesInFile(filename) <= 1:
        return f"Cannot sort: '{filename}' is empty."

    with open(filename, 'r') as file:
        lines = file.readlines()

    with open("SortedTasks.txt", "w") as sortedFile:
        sortedFile.write("SORTED TASKS :\n")
        for p in range(5, 0, -1):
            has_tasks_in_prio = False
            for i in range(3, len(lines), 3):
                try: prio_val = int(lines[i].strip().split()[-1])
                except ValueError: prio_val = 0
                if prio_val == p:
                    has_tasks_in_prio = True; break
            
            if has_tasks_in_prio:
                 sortedFile.write(f"\n--* PRIORITY: {p} *--\n")
                 Sid = 1
                 for i in range(3, len(lines), 3):
                    try: prio_val = int(lines[i].strip().split()[-1])
                    except ValueError: prio_val = 0
                    if prio_val == p:
                        name_line = lines[i-2][1:]
                        sortedFile.write(f"{Sid}{name_line}{lines[i-1]}{lines[i]}")
                        Sid += 1
    return logic_viewTasks("SortedTasks.txt")

# =============================================================================
# GUI IMPLEMENTATION
# =============================================================================

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoApp Task Manager")
        self.root.geometry("620x550")
        self.root.configure(bg='#f0f0f0')

        tk.Label(root, text="🚀 Simple ToDoApp Manager", font=("Arial", 18, "bold"), bg='#f0f0f0', fg='#333333').pack(pady=10)
        self.btn_frame = tk.Frame(root, bg='#f0f0f0')
        self.btn_frame.pack(pady=5, padx=10)
        
        b_style = {'width': 18, 'height': 1, 'font': ('Arial', 10), 'bg': '#e0e0e0', 'fg': '#000000'}
        
        tk.Button(self.btn_frame, text="➕ Add Task", **b_style, command=self.gui_addTask).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="❌ Delete Task", **b_style, command=self.gui_deleteTask).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="✅ Change Status", **b_style, command=self.gui_changeStatus).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.btn_frame, text="📋 View All Tasks", **b_style, command=lambda: self.gui_viewFile("tasks.txt")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="🗑️ View Bin", **b_style, command=lambda: self.gui_viewFile("bin.txt")).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="📊 Sort Tasks", **b_style, command=self.gui_sortTasks).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.btn_frame, text="👀 Check: Done", **b_style, command=lambda: self.gui_viewFile("Done.txt")).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.btn_frame, text="👀 Check: Pending", **b_style, command=lambda: self.gui_viewFile("NotDone.txt")).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.btn_frame, text="🚪 Exit Program", **b_style, command=root.quit).grid(row=2, column=2, padx=5, pady=5)

        tk.Label(root, text="Task Display Area:", font=("Arial", 12), bg='#f0f0f0', fg='#333333').pack(pady=(5, 2))
        self.display_area = scrolledtext.ScrolledText(root, width=75, height=20, font=("Courier", 10), bg='#ffffff', fg='#000000')
        self.display_area.pack(pady=10)
        self.gui_viewFile("tasks.txt")

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
        self.gui_viewFile("tasks.txt")

    def gui_viewFile(self, filename):
        self.update_display(logic_viewTasks(filename))

    def gui_deleteTask(self):
        self.gui_viewFile("tasks.txt")
        val = simpledialog.askinteger("Input", "Enter the task number to delete:")
        if val is None: return
        success, msg = logic_deleteTask(val)
        if success: messagebox.showinfo("Success", msg); self.gui_viewFile("tasks.txt")
        else: messagebox.showerror("Error", msg)

    def gui_changeStatus(self):
        self.gui_viewFile("NotDone.txt")
        val = simpledialog.askinteger("Input", "Enter task number to mark DONE:")
        if val is None: return
        success, msg = logic_changeTaskStatus(val)
        if success: messagebox.showinfo("Success", msg); self.gui_viewFile("NotDone.txt")
        else: messagebox.showerror("Error", msg)

    def gui_sortTasks(self):
        choice = simpledialog.askinteger("Sort", "1: Completed Tasks\n2: Pending Tasks\n3: All Tasks\n\nEnter choice:", minvalue=1, maxvalue=3)
        if choice == 1: fn = "Done.txt"
        elif choice == 2: fn = "NotDone.txt"
        elif choice == 3: fn = "tasks.txt"
        else: return
        res = logic_sortTasks(fn)
        if "Cannot sort" in res: messagebox.showerror("Error", res)
        else: messagebox.showinfo("Success", "Tasks sorted."); self.update_display(res)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()