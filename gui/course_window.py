import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import database_operations as db_ops

class CourseWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("课程管理")
        self.geometry("800x500")
        self.parent = parent

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        form_frame = ttk.LabelFrame(self, text="添加/编辑课程")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="课程名称:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="默认时长 (分钟):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(form_frame, width=15)
        self.duration_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="描述:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(form_frame, width=30) # ttk.Text(form_frame, width=30, height=3) for multiline
        self.description_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        self.add_button = ttk.Button(form_frame, text="添加课程", command=self.add_course)
        self.add_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        list_frame = ttk.LabelFrame(self, text="课程列表")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("id", "name", "description", "default_duration_minutes", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="课程名称")
        self.tree.heading("description", text="描述")
        self.tree.heading("default_duration_minutes", text="默认时长 (分)")
        self.tree.heading("status", text="状态")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("description", width=250)
        self.tree.column("default_duration_minutes", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=5, fill="x")

        self.refresh_button = ttk.Button(action_frame, text="刷新列表", command=self.load_courses)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(action_frame, text="编辑选中课程", command=self.edit_selected_course)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(action_frame, text="删除选中课程 (逻辑)", command=self.delete_selected_course)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.load_courses()
        self.tree.bind("<Double-1>", self.on_double_click_edit)

    def on_double_click_edit(self, event):
        self.edit_selected_course()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.name_entry.focus()

    def validate_inputs(self, name, duration_str):
        if not name:
            messagebox.showerror("错误", "课程名称不能为空！", parent=self)
            return False, None
        
        default_duration_minutes = None
        if duration_str: # 时长可选
            try:
                default_duration_minutes = int(duration_str)
                if default_duration_minutes <= 0:
                    messagebox.showerror("错误", "默认时长必须是正整数！", parent=self)
                    return False, None
            except ValueError:
                messagebox.showerror("错误", "默认时长必须是有效的整数！", parent=self)
                return False, None
        return True, default_duration_minutes


    def add_course(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        duration_str = self.duration_entry.get().strip()

        is_valid, duration_minutes = self.validate_inputs(name, duration_str)
        if not is_valid:
            return

        success, message = db_ops.add_course(name, description, duration_minutes)
        if success:
            messagebox.showinfo("成功", message, parent=self)
            self.load_courses()
            self.clear_form()
        else:
            messagebox.showerror("失败", message, parent=self)

    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        courses = db_ops.get_all_courses()
        for course in courses:
            self.tree.insert("", tk.END, values=course)

    def get_selected_course_id(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个课程。", parent=self)
            return None
        return self.tree.item(selected_item)['values'][0]

    def edit_selected_course(self):
        course_id = self.get_selected_course_id()
        if course_id is None:
            return

        course_data = db_ops.get_course_by_id(course_id)
        if not course_data:
            messagebox.showerror("错误", "无法获取课程信息。", parent=self)
            return

        edit_dialog = EditCourseDialog(self, "编辑课程信息", course_data)
        if edit_dialog.result:
            self.load_courses()

    def delete_selected_course(self):
        course_id = self.get_selected_course_id()
        if course_id is None:
            return
        
        course_name = ""
        selected_item = self.tree.focus()
        if selected_item:
            course_name = self.tree.item(selected_item)['values'][1]

        if messagebox.askyesno("确认操作", f"确定要将会课程 '{course_name}' (ID: {course_id}) 设为非活动状态吗？", parent=self):
            success, message = db_ops.delete_course_logically(course_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_courses()
            else:
                messagebox.showerror("失败", message, parent=self)

class EditCourseDialog(simpledialog.Dialog):
    def __init__(self, parent, title, course_data):
        self.course_data = course_data # (id, name, description, default_duration_minutes, status)
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="课程名称:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ttk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, self.course_data[1])

        ttk.Label(master, text="描述:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.description_entry = ttk.Entry(master, width=30)
        self.description_entry.grid(row=1, column=1, padx=5, pady=2)
        self.description_entry.insert(0, self.course_data[2] if self.course_data[2] else "")

        ttk.Label(master, text="默认时长 (分钟):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.duration_entry = ttk.Entry(master, width=30)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2)
        self.duration_entry.insert(0, str(self.course_data[3]) if self.course_data[3] is not None else "")
        
        ttk.Label(master, text="状态:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.status_var = tk.StringVar(value=self.course_data[4])
        self.status_combo = ttk.Combobox(master, textvariable=self.status_var, values=["active", "inactive"], state="readonly", width=27)
        self.status_combo.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        
        return self.name_entry

    def validate_inputs(self, name, duration_str): # Copied from CourseWindow for consistency
        if not name:
            messagebox.showerror("错误", "课程名称不能为空！", parent=self)
            return False, None
        
        default_duration_minutes = None
        if duration_str:
            try:
                default_duration_minutes = int(duration_str)
                if default_duration_minutes <= 0:
                    messagebox.showerror("错误", "默认时长必须是正整数！", parent=self)
                    return False, None
            except ValueError:
                messagebox.showerror("错误", "默认时长必须是有效的整数！", parent=self)
                return False, None
        return True, default_duration_minutes

    def apply(self):
        course_id = self.course_data[0]
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        duration_str = self.duration_entry.get().strip()
        status = self.status_var.get()

        is_valid, duration_minutes = self.validate_inputs(name, duration_str)
        if not is_valid:
            self.result = False
            return

        success, message = db_ops.update_course(course_id, name, description, duration_minutes, status)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent)
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False
