import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import database_operations as db_ops

class CardTypeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("会员卡类型管理")
        self.geometry("800x500")
        self.parent = parent

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        form_frame = ttk.LabelFrame(self, text="添加/编辑会员卡类型")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="类型名称:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="价格 (元):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.price_entry = ttk.Entry(form_frame, width=15)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(form_frame, text="有效期 (天):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(form_frame, width=15)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="描述:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(form_frame, width=30)
        self.description_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        self.add_button = ttk.Button(form_frame, text="添加类型", command=self.add_card_type)
        self.add_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        # 搜索框架
        search_frame = ttk.LabelFrame(self, text="搜索会员卡类型")
        search_frame.pack(padx=10, pady=(0,5), fill="x")

        ttk.Label(search_frame, text="搜索 (类型名称):").pack(side=tk.LEFT, padx=(5,0))
        self.search_card_type_entry = ttk.Entry(search_frame, width=30)
        self.search_card_type_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        self.search_card_type_entry.bind("<Return>", self.search_card_type)

        self.search_card_type_button = ttk.Button(search_frame, text="搜索", command=self.search_card_type)
        self.search_card_type_button.pack(side=tk.LEFT, padx=5)

        self.show_all_card_types_button = ttk.Button(search_frame, text="显示全部", command=self.load_card_types)
        self.show_all_card_types_button.pack(side=tk.LEFT, padx=5)

        list_frame = ttk.LabelFrame(self, text="会员卡类型列表")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("id", "name", "price", "duration_days", "description")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="类型名称")
        self.tree.heading("price", text="价格 (元)")
        self.tree.heading("duration_days", text="有效期 (天)")
        self.tree.heading("description", text="描述")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("price", width=100, anchor=tk.E)
        self.tree.column("duration_days", width=100, anchor=tk.CENTER)
        self.tree.column("description", width=200)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=5, fill="x")

        self.refresh_button = ttk.Button(action_frame, text="刷新列表", command=self.load_card_types)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(action_frame, text="编辑选中类型", command=self.edit_selected_card_type)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(action_frame, text="删除选中类型", command=self.delete_selected_card_type)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.load_card_types()
        self.tree.bind("<Double-1>", self.on_double_click_edit)


    def on_double_click_edit(self, event):
        self.edit_selected_card_type()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.name_entry.focus()

    def validate_inputs(self, name, price_str, duration_str):
        if not name:
            messagebox.showerror("错误", "类型名称不能为空！", parent=self)
            return False, None, None
        try:
            price = float(price_str)
            if price < 0:
                messagebox.showerror("错误", "价格不能为负数！", parent=self)
                return False, None, None
        except ValueError:
            messagebox.showerror("错误", "价格必须是有效的数字！", parent=self)
            return False, None, None
        try:
            duration_days = int(duration_str)
            if duration_days <= 0:
                messagebox.showerror("错误", "有效期天数必须是正整数！", parent=self)
                return False, None, None
        except ValueError:
            messagebox.showerror("错误", "有效期天数必须是有效的整数！", parent=self)
            return False, None, None
        return True, price, duration_days


    def add_card_type(self):
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        duration_str = self.duration_entry.get().strip()
        description = self.description_entry.get().strip()

        is_valid, price, duration_days = self.validate_inputs(name, price_str, duration_str)
        if not is_valid:
            return

        success, message = db_ops.add_card_type(name, price, duration_days, description)
        if success:
            messagebox.showinfo("成功", message, parent=self)
            self.load_card_types()
            self.clear_form()
        else:
            messagebox.showerror("失败", message, parent=self)

    def load_card_types(self, search_term=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            card_types = db_ops.search_card_types(search_term)
            if not card_types:
                messagebox.showinfo("搜索结果", f"未找到与 '{search_term}'相关的会员卡类型。", parent=self)
        else:
            self.search_card_type_entry.delete(0, tk.END) # 清空搜索框
            card_types = db_ops.get_all_card_types()

        for ct in card_types:
            self.tree.insert("", tk.END, values=ct)

    def search_card_type(self, event=None):
        search_term = self.search_card_type_entry.get().strip()
        if not search_term:
            messagebox.showwarning("提示", "请输入搜索关键词。", parent=self)
            return
        self.load_card_types(search_term=search_term)

    def get_selected_card_type_id(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个会员卡类型。", parent=self)
            return None
        return self.tree.item(selected_item)['values'][0]

    def edit_selected_card_type(self):
        card_type_id = self.get_selected_card_type_id()
        if card_type_id is None:
            return

        card_type_data = db_ops.get_card_type_by_id(card_type_id)
        if not card_type_data:
            messagebox.showerror("错误", "无法获取会员卡类型信息。", parent=self)
            return

        edit_dialog = EditCardTypeDialog(self, "编辑会员卡类型", card_type_data)
        if edit_dialog.result:
            self.load_card_types()

    def delete_selected_card_type(self):
        card_type_id = self.get_selected_card_type_id()
        if card_type_id is None:
            return
        
        type_name = ""
        selected_item = self.tree.focus()
        if selected_item:
            type_name = self.tree.item(selected_item)['values'][1]

        if messagebox.askyesno("确认删除", f"确定要删除会员卡类型 '{type_name}' (ID: {card_type_id}) 吗？\n此操作不可恢复，且如果该类型已被使用，可能删除失败。", parent=self):
            success, message = db_ops.delete_card_type(card_type_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_card_types()
            else:
                messagebox.showerror("失败", message, parent=self)

class EditCardTypeDialog(simpledialog.Dialog):
    def __init__(self, parent, title, card_type_data):
        self.card_type_data = card_type_data # (id, name, price, duration_days, description)
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="类型名称:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ttk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, self.card_type_data[1])

        ttk.Label(master, text="价格 (元):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.price_entry = ttk.Entry(master, width=30)
        self.price_entry.grid(row=1, column=1, padx=5, pady=2)
        self.price_entry.insert(0, str(self.card_type_data[2]))

        ttk.Label(master, text="有效期 (天):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.duration_entry = ttk.Entry(master, width=30)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2)
        self.duration_entry.insert(0, str(self.card_type_data[3]))

        ttk.Label(master, text="描述:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.description_entry = ttk.Entry(master, width=30)
        self.description_entry.grid(row=3, column=1, padx=5, pady=2)
        self.description_entry.insert(0, self.card_type_data[4] if self.card_type_data[4] else "")
        
        return self.name_entry 

    def validate_inputs(self, name, price_str, duration_str):
        if not name:
            messagebox.showerror("错误", "类型名称不能为空！", parent=self)
            return False, None, None
        try:
            price = float(price_str)
            if price < 0:
                messagebox.showerror("错误", "价格不能为负数！", parent=self)
                return False, None, None
        except ValueError:
            messagebox.showerror("错误", "价格必须是有效的数字！", parent=self)
            return False, None, None
        try:
            duration_days = int(duration_str)
            if duration_days <= 0:
                messagebox.showerror("错误", "有效期天数必须是正整数！", parent=self)
                return False, None, None
        except ValueError:
            messagebox.showerror("错误", "有效期天数必须是有效的整数！", parent=self)
            return False, None, None
        return True, price, duration_days

    def apply(self):
        card_type_id = self.card_type_data[0]
        name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        duration_str = self.duration_entry.get().strip()
        description = self.description_entry.get().strip()

        is_valid, price, duration_days = self.validate_inputs(name, price_str, duration_str)
        if not is_valid:
            self.result = False # Prevent dialog from closing
            return


        success, message = db_ops.update_card_type(card_type_id, name, price, duration_days, description)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent)
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False
