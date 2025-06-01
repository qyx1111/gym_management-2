import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import database_operations as db_ops

class TrainerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("教练管理")
        self.geometry("800x500")
        self.parent = parent

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        form_frame = ttk.LabelFrame(self, text="添加/编辑教练")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="姓名:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="专长:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.specialty_entry = ttk.Entry(form_frame, width=30)
        self.specialty_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="联系方式:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.contact_entry = ttk.Entry(form_frame, width=30)
        self.contact_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        self.add_button = ttk.Button(form_frame, text="添加教练", command=self.add_trainer)
        self.add_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        # 搜索框架
        search_frame = ttk.LabelFrame(self, text="搜索教练")
        search_frame.pack(padx=10, pady=(0,5), fill="x")

        ttk.Label(search_frame, text="搜索 (姓名/专长):").pack(side=tk.LEFT, padx=(5,0))
        self.search_trainer_entry = ttk.Entry(search_frame, width=30)
        self.search_trainer_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        self.search_trainer_entry.bind("<Return>", self.search_trainer)

        self.search_trainer_button = ttk.Button(search_frame, text="搜索", command=self.search_trainer)
        self.search_trainer_button.pack(side=tk.LEFT, padx=5)

        self.show_all_trainers_button = ttk.Button(search_frame, text="显示全部", command=self.load_trainers)
        self.show_all_trainers_button.pack(side=tk.LEFT, padx=5)

        list_frame = ttk.LabelFrame(self, text="教练列表")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("id", "name", "specialty", "contact_info", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="姓名")
        self.tree.heading("specialty", text="专长")
        self.tree.heading("contact_info", text="联系方式")
        self.tree.heading("status", text="状态")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("specialty", width=200)
        self.tree.column("contact_info", width=200)
        self.tree.column("status", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=5, fill="x")

        self.refresh_button = ttk.Button(action_frame, text="刷新列表", command=self.load_trainers)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(action_frame, text="编辑选中教练", command=self.edit_selected_trainer)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(action_frame, text="删除选中教练 (逻辑)", command=self.delete_selected_trainer)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.load_trainers()
        self.tree.bind("<Double-1>", self.on_double_click_edit)

    def on_double_click_edit(self, event):
        self.edit_selected_trainer()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.specialty_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.name_entry.focus()

    def add_trainer(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        contact_info = self.contact_entry.get().strip()

        if not name:
            messagebox.showerror("错误", "教练姓名不能为空！", parent=self)
            return

        success, message = db_ops.add_trainer(name, specialty, contact_info)
        if success:
            messagebox.showinfo("成功", message, parent=self)
            self.load_trainers()
            self.clear_form()
        else:
            messagebox.showerror("失败", message, parent=self)

    def load_trainers(self, search_term=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            trainers = db_ops.search_trainers(search_term)
            if not trainers:
                messagebox.showinfo("搜索结果", f"未找到与 '{search_term}'相关的教练。", parent=self)
        else:
            self.search_trainer_entry.delete(0, tk.END) # 清空搜索框
            trainers = db_ops.get_all_trainers()
            
        for trainer in trainers:
            self.tree.insert("", tk.END, values=trainer)

    def search_trainer(self, event=None):
        search_term = self.search_trainer_entry.get().strip()
        if not search_term:
            messagebox.showwarning("提示", "请输入搜索关键词。", parent=self)
            return
        self.load_trainers(search_term=search_term)

    def get_selected_trainer_id(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个教练。", parent=self)
            return None
        return self.tree.item(selected_item)['values'][0]

    def edit_selected_trainer(self):
        trainer_id = self.get_selected_trainer_id()
        if trainer_id is None:
            return

        trainer_data = db_ops.get_trainer_by_id(trainer_id)
        if not trainer_data:
            messagebox.showerror("错误", "无法获取教练信息。", parent=self)
            return

        edit_dialog = EditTrainerDialog(self, "编辑教练信息", trainer_data)
        if edit_dialog.result:
            self.load_trainers()

    def delete_selected_trainer(self):
        trainer_id = self.get_selected_trainer_id()
        if trainer_id is None:
            return
        
        trainer_name = ""
        selected_item = self.tree.focus()
        if selected_item:
            trainer_name = self.tree.item(selected_item)['values'][1]

        if messagebox.askyesno("确认操作", f"确定要将会教练 '{trainer_name}' (ID: {trainer_id}) 设为非活动状态吗？", parent=self):
            success, message = db_ops.delete_trainer_logically(trainer_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_trainers()
            else:
                messagebox.showerror("失败", message, parent=self)

class EditTrainerDialog(simpledialog.Dialog):
    def __init__(self, parent, title, trainer_data):
        self.trainer_data = trainer_data # (id, name, specialty, contact_info, status)
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="姓名:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ttk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, self.trainer_data[1])

        ttk.Label(master, text="专长:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.specialty_entry = ttk.Entry(master, width=30)
        self.specialty_entry.grid(row=1, column=1, padx=5, pady=2)
        self.specialty_entry.insert(0, self.trainer_data[2] if self.trainer_data[2] else "")

        ttk.Label(master, text="联系方式:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.contact_entry = ttk.Entry(master, width=30)
        self.contact_entry.grid(row=2, column=1, padx=5, pady=2)
        self.contact_entry.insert(0, self.trainer_data[3] if self.trainer_data[3] else "")
        
        ttk.Label(master, text="状态:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.status_var = tk.StringVar(value=self.trainer_data[4])
        self.status_combo = ttk.Combobox(master, textvariable=self.status_var, values=["active", "inactive"], state="readonly", width=27)
        self.status_combo.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        
        return self.name_entry 

    def apply(self):
        trainer_id = self.trainer_data[0]
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip()
        contact_info = self.contact_entry.get().strip()
        status = self.status_var.get()

        if not name:
            messagebox.showerror("错误", "教练姓名不能为空！", parent=self)
            self.result = False 
            return

        success, message = db_ops.update_trainer(trainer_id, name, specialty, contact_info, status)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent)
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False
