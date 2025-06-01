import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import database_operations as db_ops
from tkcalendar import DateEntry # 需要 pip install tkcalendar
from .member_detail_window import MemberDetailWindow # 新增导入

class MemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("会员管理")
        self.geometry("1000x650") # 稍微增加高度以容纳返回按钮
        self.parent = parent # parent 是 MainWindow 实例

        # 样式
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # 注册会员的表单框架
        form_frame = ttk.LabelFrame(self, text="注册新会员")
        form_frame.pack(padx=10, pady=10, fill="x")

        # 姓名
        ttk.Label(form_frame, text="姓名:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # 性别
        ttk.Label(form_frame, text="性别:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["男", "女", "其他"], state="readonly", width=10)
        self.gender_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.gender_combo.set("男")

        # 生日
        ttk.Label(form_frame, text="生日:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.birth_date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.birth_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # 电话
        ttk.Label(form_frame, text="电话:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # 紧急联系人姓名
        ttk.Label(form_frame, text="紧急联系人:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.emergency_name_entry = ttk.Entry(form_frame, width=30)
        self.emergency_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # 紧急联系人电话
        ttk.Label(form_frame, text="紧急电话:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.emergency_phone_entry = ttk.Entry(form_frame, width=30)
        self.emergency_phone_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        
        # 健康状况备注
        ttk.Label(form_frame, text="健康备注:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.health_notes_entry = ttk.Entry(form_frame, width=30)
        self.health_notes_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        # 注册按钮
        self.register_button = ttk.Button(form_frame, text="注册会员", command=self.register_member)
        self.register_button.grid(row=4, column=0, columnspan=4, padx=5, pady=10)

        # 搜索框架
        search_frame = ttk.LabelFrame(self, text="搜索会员")
        search_frame.pack(padx=10, pady=(0,5), fill="x")

        ttk.Label(search_frame, text="搜索 (姓名/电话):").pack(side=tk.LEFT, padx=(5,0))
        self.search_member_entry = ttk.Entry(search_frame, width=30)
        self.search_member_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        self.search_member_entry.bind("<Return>", self.search_member) 
        
        self.search_member_button = ttk.Button(search_frame, text="搜索", command=self.search_member)
        self.search_member_button.pack(side=tk.LEFT, padx=5)
        
        self.show_all_members_button = ttk.Button(search_frame, text="显示全部", command=self.load_members)
        self.show_all_members_button.pack(side=tk.LEFT, padx=5)


        # 会员列表框架
        list_frame = ttk.LabelFrame(self, text="会员列表")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview 用于显示会员列表
        columns = ("id", "name", "gender", "birth_date", "phone", "emergency_contact_name", "emergency_contact_phone", "health_notes", "join_date", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="姓名")
        self.tree.heading("gender", text="性别")
        self.tree.heading("birth_date", text="生日")
        self.tree.heading("phone", text="电话")
        self.tree.heading("emergency_contact_name", text="紧急联系人")
        self.tree.heading("emergency_contact_phone", text="紧急电话")
        self.tree.heading("health_notes", text="健康备注")
        self.tree.heading("join_date", text="入会日期")
        self.tree.heading("status", text="状态")

        self.tree.column("id", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=100)
        self.tree.column("gender", width=50, anchor=tk.CENTER)
        self.tree.column("birth_date", width=100, anchor=tk.CENTER)
        self.tree.column("phone", width=120)
        self.tree.column("emergency_contact_name", width=100)
        self.tree.column("emergency_contact_phone", width=120)
        self.tree.column("health_notes", width=150)
        self.tree.column("join_date", width=150, anchor=tk.CENTER)
        self.tree.column("status", width=80, anchor=tk.CENTER)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # 操作按钮框架
        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=5, fill="x")

        self.refresh_button = ttk.Button(action_frame, text="刷新列表", command=self.load_members)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(action_frame, text="编辑选中会员", command=self.edit_selected_member)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(action_frame, text="删除选中会员 (逻辑)", command=self.delete_selected_member)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.detail_button = ttk.Button(action_frame, text="查看选中会员详情", command=self.open_member_details)
        self.detail_button.pack(side=tk.LEFT, padx=5)

        self.return_button = ttk.Button(action_frame, text="返回主页", command=self.close_and_return_to_main)
        self.return_button.pack(side=tk.RIGHT, padx=5)


        self.load_members()
        self.tree.bind("<Double-1>", lambda e: self.open_member_details()) # 双击打开详情
        self.protocol("WM_DELETE_WINDOW", self.close_and_return_to_main) # 覆盖关闭按钮行为

    def close_and_return_to_main(self):
        self.parent.show_main_window() # 调用父窗口的方法来显示它
        self.destroy() # 关闭当前窗口

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.gender_combo.set("男")
        self.birth_date_entry.set_date(None) # 清空日期选择器
        self.phone_entry.delete(0, tk.END)
        self.emergency_name_entry.delete(0, tk.END)
        self.emergency_phone_entry.delete(0, tk.END)
        self.health_notes_entry.delete(0, tk.END)
        self.name_entry.focus()

    def register_member(self):
        name = self.name_entry.get().strip()
        gender = self.gender_var.get()
        birth_date = self.birth_date_entry.get_date().strftime('%Y-%m-%d') if self.birth_date_entry.get_date() else ""
        phone = self.phone_entry.get().strip()
        emergency_name = self.emergency_name_entry.get().strip()
        emergency_phone = self.emergency_phone_entry.get().strip()
        health_notes = self.health_notes_entry.get().strip()

        if not name or not phone:
            messagebox.showerror("错误", "姓名和电话不能为空！", parent=self)
            return

        success, message = db_ops.add_member(name, gender, birth_date, phone, emergency_name, emergency_phone, health_notes)
        if success:
            messagebox.showinfo("成功", message, parent=self)
            self.load_members()
            self.clear_form()
        else:
            messagebox.showerror("失败", message, parent=self)

    def load_members(self, search_term=None):
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if search_term:
            members = db_ops.search_members(search_term)
            if not members:
                messagebox.showinfo("搜索结果", f"未找到与 '{search_term}'相关的会员。", parent=self)
        else:
            self.search_member_entry.delete(0, tk.END) # 清空搜索框
            members = db_ops.get_all_members()
            
        for member in members:
            self.tree.insert("", tk.END, values=member)

    def search_member(self, event=None): # event=None使其可以被按钮和回车调用
        search_term = self.search_member_entry.get().strip()
        if not search_term:
            messagebox.showwarning("提示", "请输入搜索关键词。", parent=self)
            return
        self.load_members(search_term=search_term)

    def get_selected_member_id(self):
        selected_item = self.tree.focus() # 获取选中的项
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个会员。", parent=self)
            return None
        member_details = self.tree.item(selected_item)
        return member_details['values'][0] # ID 在第一列

    def get_selected_member_id_and_name(self):
        selected_item = self.tree.focus() 
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个会员。", parent=self)
            return None, None
        member_details_list = self.tree.item(selected_item)['values']
        member_id = member_details_list[0] 
        member_name = member_details_list[1]
        return member_id, member_name

    def open_member_details(self):
        member_id, member_name = self.get_selected_member_id_and_name()
        if member_id is None:
            return
        
        # Hide current MemberWindow, show it back when MemberDetailWindow closes (handled by MemberDetailWindow)
        self.parent.withdraw() # Withdraw MainWindow
        # self.withdraw() # Withdraw MemberWindow itself if MemberDetailWindow's parent is MainWindow
        
        # The MemberDetailWindow's parent should be the MainWindow for consistent return behavior
        detail_win = MemberDetailWindow(self.parent, member_id, member_name)
        # No grab_set here if MemberWindow is hidden, or make MemberDetailWindow modal to MainWindow

    def edit_selected_member(self):
        member_id, member_name = self.get_selected_member_id_and_name()
        if member_id is None:
            return

        member_data = db_ops.get_member_by_id(member_id) # (id, name, gender, ...)
        if not member_data:
            messagebox.showerror("错误", "无法获取会员信息。", parent=self)
            return

        # 创建编辑对话框 (可以使用 simpledialog 或自定义 Toplevel)
        edit_dialog = EditMemberDialog(self, "编辑会员信息", member_data)
        if edit_dialog.result: # 如果用户点击了保存
            self.load_members() # 刷新列表

    def delete_selected_member(self):
        member_id = self.get_selected_member_id()
        if member_id is None:
            return
        
        member_name = ""
        selected_item = self.tree.focus()
        if selected_item:
            member_name = self.tree.item(selected_item)['values'][1]


        if messagebox.askyesno("确认删除", f"确定要将会员 '{member_name}' (ID: {member_id}) 设为非活动状态吗？\n（此操作为逻辑删除）", parent=self):
            success, message = db_ops.delete_member_logically(member_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_members()
            else:
                messagebox.showerror("失败", message, parent=self)


class EditMemberDialog(simpledialog.Dialog):
    def __init__(self, parent, title, member_data):
        self.member_data = member_data # (id, name, gender, birth_date, phone, emergency_contact_name, emergency_contact_phone, health_notes, join_date, status)
        self.result = None # 用于存储编辑结果
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text="姓名:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)
        self.name_entry.insert(0, self.member_data[1])

        ttk.Label(master, text="性别:").grid(row=1, column=0, sticky="w")
        self.gender_var = tk.StringVar(value=self.member_data[2])
        self.gender_combo = ttk.Combobox(master, textvariable=self.gender_var, values=["男", "女", "其他"], state="readonly", width=10)
        self.gender_combo.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(master, text="生日 (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.birth_date_entry = ttk.Entry(master, width=30) # 简单起见，用Entry，实际可用DateEntry
        self.birth_date_entry.grid(row=2, column=1, padx=5, pady=2)
        self.birth_date_entry.insert(0, self.member_data[3] if self.member_data[3] else "")


        ttk.Label(master, text="电话:").grid(row=3, column=0, sticky="w")
        self.phone_entry = ttk.Entry(master, width=30)
        self.phone_entry.grid(row=3, column=1, padx=5, pady=2)
        self.phone_entry.insert(0, self.member_data[4])

        ttk.Label(master, text="紧急联系人:").grid(row=4, column=0, sticky="w")
        self.emergency_name_entry = ttk.Entry(master, width=30)
        self.emergency_name_entry.grid(row=4, column=1, padx=5, pady=2)
        self.emergency_name_entry.insert(0, self.member_data[5])

        ttk.Label(master, text="紧急电话:").grid(row=5, column=0, sticky="w")
        self.emergency_phone_entry = ttk.Entry(master, width=30)
        self.emergency_phone_entry.grid(row=5, column=1, padx=5, pady=2)
        self.emergency_phone_entry.insert(0, self.member_data[6])
        
        ttk.Label(master, text="健康备注:").grid(row=6, column=0, sticky="w")
        self.health_notes_entry = ttk.Entry(master, width=30)
        self.health_notes_entry.grid(row=6, column=1, padx=5, pady=2)
        self.health_notes_entry.insert(0, self.member_data[7])

        ttk.Label(master, text="状态:").grid(row=7, column=0, sticky="w")
        self.status_var = tk.StringVar(value=self.member_data[9])
        self.status_combo = ttk.Combobox(master, textvariable=self.status_var, values=["active", "inactive", "frozen"], state="readonly", width=10)
        self.status_combo.grid(row=7, column=1, padx=5, pady=2, sticky="ew")

        return self.name_entry # initial focus

    def apply(self):
        member_id = self.member_data[0]
        name = self.name_entry.get().strip()
        gender = self.gender_var.get()
        birth_date = self.birth_date_entry.get().strip() # 简单处理，未做严格日期校验
        phone = self.phone_entry.get().strip()
        emergency_name = self.emergency_name_entry.get().strip()
        emergency_phone = self.emergency_phone_entry.get().strip()
        health_notes = self.health_notes_entry.get().strip()
        status = self.status_var.get()

        if not name or not phone:
            messagebox.showerror("错误", "姓名和电话不能为空！", parent=self)
            self.result = False # 阻止对话框关闭
            return

        success, message = db_ops.update_member(member_id, name, gender, birth_date, phone, emergency_name, emergency_phone, health_notes, status)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent) # 显示在父窗口上
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False # 阻止对话框关闭
