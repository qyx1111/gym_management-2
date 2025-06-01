import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import database_operations as db_ops
from tkcalendar import DateEntry
from datetime import datetime, timedelta

class MemberDetailWindow(tk.Toplevel):
    def __init__(self, parent, member_id, member_name):
        super().__init__(parent)
        self.parent = parent # MainWindow instance
        self.member_id = member_id
        self.member_name = member_name

        self.title(f"会员信息详情 - {self.member_name} (ID: {self.member_id})")
        self.geometry("900x700")
        self.grab_set()

        # Top frame for basic member info (can be expanded later)
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(info_frame, text=f"会员: {self.member_name} (ID: {self.member_id})", font=('Helvetica', 14, 'bold')).pack(side=tk.LEFT)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # --- Member Cards Tab ---
        self.cards_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cards_tab, text="会员卡管理")
        self.setup_cards_tab()

        # --- Member Courses Tab (Stub) ---
        self.courses_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.courses_tab, text="已报课程")
        self.setup_courses_tab() # Changed from stub

        # --- Member Trainers Tab (Stub) ---
        self.trainers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trainers_tab, text="指派教练")
        self.setup_trainers_tab() # Changed from stub

        # Bottom frame for close button
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(pady=10, fill="x", side=tk.BOTTOM)
        ttk.Button(bottom_frame, text="关闭窗口", command=self.close_window).pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        self.parent.show_main_window()
        self.destroy()

    def setup_cards_tab(self):
        # Frame for adding/editing card
        card_form_frame = ttk.LabelFrame(self.cards_tab, text="会员卡操作")
        card_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(card_form_frame, text="为该会员办理新卡", command=self.add_new_member_card).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(card_form_frame, text="编辑选中卡信息", command=self.edit_selected_member_card).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(card_form_frame, text="删除选中卡", command=self.delete_selected_member_card).pack(side=tk.LEFT, padx=5, pady=5)

        # Frame for listing cards
        card_list_frame = ttk.LabelFrame(self.cards_tab, text="会员拥有的卡列表")
        card_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("card_instance_id", "card_type_name", "purchase_date", "activation_date", "expiry_date", "status", "notes")
        self.cards_tree = ttk.Treeview(card_list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.cards_tree.heading("card_instance_id", text="卡实例ID")
        self.cards_tree.heading("card_type_name", text="卡类型")
        self.cards_tree.heading("purchase_date", text="购买日期")
        self.cards_tree.heading("activation_date", text="激活日期")
        self.cards_tree.heading("expiry_date", text="失效日期")
        self.cards_tree.heading("status", text="状态")
        self.cards_tree.heading("notes", text="备注")

        self.cards_tree.column("card_instance_id", width=60, anchor=tk.CENTER)
        self.cards_tree.column("card_type_name", width=120)
        self.cards_tree.column("purchase_date", width=100, anchor=tk.CENTER)
        self.cards_tree.column("activation_date", width=100, anchor=tk.CENTER)
        self.cards_tree.column("expiry_date", width=100, anchor=tk.CENTER)
        self.cards_tree.column("status", width=100, anchor=tk.CENTER)
        self.cards_tree.column("notes", width=200)

        scrollbar = ttk.Scrollbar(card_list_frame, orient="vertical", command=self.cards_tree.yview)
        self.cards_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.cards_tree.pack(fill="both", expand=True)
        self.cards_tree.bind("<Double-1>", lambda e: self.edit_selected_member_card())


        self.load_member_cards()

    def load_member_cards(self):
        for item in self.cards_tree.get_children():
            self.cards_tree.delete(item)
        cards = db_ops.get_cards_for_member(self.member_id)
        for card in cards:
            # card format: (mc.id, mct.name, mc.purchase_date, mc.activation_date, mc.expiry_date, mc.status, mc.notes, mc.card_type_id)
            self.cards_tree.insert("", tk.END, values=card[:-1]) # Exclude card_type_id from display

    def add_new_member_card(self):
        dialog = ManageMemberCardDialog(self, "办理新会员卡", member_id=self.member_id)
        if dialog.result:
            self.load_member_cards()

    def edit_selected_member_card(self):
        selected_item = self.cards_tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一张会员卡进行编辑。", parent=self)
            return
        
        member_card_id = self.cards_tree.item(selected_item)['values'][0]
        dialog = ManageMemberCardDialog(self, "编辑会员卡信息", member_id=self.member_id, member_card_id=member_card_id)
        if dialog.result:
            self.load_member_cards()
            
    def delete_selected_member_card(self):
        selected_item = self.cards_tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一张会员卡进行删除。", parent=self)
            return
        
        member_card_id = self.cards_tree.item(selected_item)['values'][0]
        card_type_name = self.cards_tree.item(selected_item)['values'][1]

        if messagebox.askyesno("确认删除", f"确定要删除会员 '{self.member_name}' 的这张 '{card_type_name}' (ID: {member_card_id}) 吗？", parent=self):
            success, message = db_ops.delete_member_card(member_card_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_member_cards()
            else:
                messagebox.showerror("失败", message, parent=self)

    def setup_courses_tab(self):
        # Frame for enrolling/editing course enrollment
        course_form_frame = ttk.LabelFrame(self.courses_tab, text="课程报名操作")
        course_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(course_form_frame, text="为该会员报名新课程", command=self.enroll_new_course_for_member).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(course_form_frame, text="编辑选中报名信息", command=self.edit_selected_enrollment).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(course_form_frame, text="取消选中课程报名", command=self.unenroll_selected_course).pack(side=tk.LEFT, padx=5, pady=5)

        # Frame for listing enrolled courses
        course_list_frame = ttk.LabelFrame(self.courses_tab, text="会员已报名课程列表")
        course_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("enrollment_id", "course_name", "enrollment_date", "status", "notes")
        self.enrollments_tree = ttk.Treeview(course_list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.enrollments_tree.heading("enrollment_id", text="报名ID")
        self.enrollments_tree.heading("course_name", text="课程名称")
        self.enrollments_tree.heading("enrollment_date", text="报名日期")
        self.enrollments_tree.heading("status", text="状态")
        self.enrollments_tree.heading("notes", text="备注")

        self.enrollments_tree.column("enrollment_id", width=60, anchor=tk.CENTER)
        self.enrollments_tree.column("course_name", width=200)
        self.enrollments_tree.column("enrollment_date", width=100, anchor=tk.CENTER)
        self.enrollments_tree.column("status", width=100, anchor=tk.CENTER)
        self.enrollments_tree.column("notes", width=200)

        scrollbar = ttk.Scrollbar(course_list_frame, orient="vertical", command=self.enrollments_tree.yview)
        self.enrollments_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.enrollments_tree.pack(fill="both", expand=True)
        self.enrollments_tree.bind("<Double-1>", lambda e: self.edit_selected_enrollment())

        self.load_member_enrollments()

    def load_member_enrollments(self):
        for item in self.enrollments_tree.get_children():
            self.enrollments_tree.delete(item)
        enrollments = db_ops.get_enrollments_for_member(self.member_id)
        # enrollments format: (mce.id, c.name, mce.enrollment_date, mce.status, mce.notes, mce.course_id)
        for enroll in enrollments:
            self.enrollments_tree.insert("", tk.END, values=enroll[:-1]) # Exclude course_id from display

    def enroll_new_course_for_member(self):
        dialog = ManageMemberCourseEnrollmentDialog(self, "报名新课程", member_id=self.member_id)
        if dialog.result:
            self.load_member_enrollments()

    def edit_selected_enrollment(self):
        selected_item = self.enrollments_tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个课程报名记录进行编辑。", parent=self)
            return
        
        enrollment_id = self.enrollments_tree.item(selected_item)['values'][0]
        dialog = ManageMemberCourseEnrollmentDialog(self, "编辑课程报名信息", member_id=self.member_id, enrollment_id=enrollment_id)
        if dialog.result:
            self.load_member_enrollments()
            
    def unenroll_selected_course(self):
        selected_item = self.enrollments_tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个课程报名记录进行取消。", parent=self)
            return
        
        enrollment_id = self.enrollments_tree.item(selected_item)['values'][0]
        course_name = self.enrollments_tree.item(selected_item)['values'][1]

        if messagebox.askyesno("确认取消报名", f"确定要取消会员 '{self.member_name}' 的课程 '{course_name}' (报名ID: {enrollment_id}) 吗？", parent=self):
            success, message = db_ops.unenroll_member_from_course(enrollment_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_member_enrollments()
            else:
                messagebox.showerror("失败", message, parent=self)

    def setup_trainers_tab(self):
        # Frame for assigning/editing trainer assignment
        trainer_form_frame = ttk.LabelFrame(self.trainers_tab, text="教练指派操作")
        trainer_form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(trainer_form_frame, text="为该会员指派新教练", command=self.assign_new_trainer_to_member).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(trainer_form_frame, text="编辑选中指派信息", command=self.edit_selected_assignment).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(trainer_form_frame, text="解除选中教练指派", command=self.unassign_selected_trainer).pack(side=tk.LEFT, padx=5, pady=5)

        # Frame for listing assigned trainers
        trainer_list_frame = ttk.LabelFrame(self.trainers_tab, text="会员已指派教练列表")
        trainer_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("assignment_id", "trainer_name", "assignment_date", "assignment_type", "notes")
        self.assignments_tree = ttk.Treeview(trainer_list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.assignments_tree.heading("assignment_id", text="指派ID")
        self.assignments_tree.heading("trainer_name", text="教练姓名")
        self.assignments_tree.heading("assignment_date", text="指派日期")
        self.assignments_tree.heading("assignment_type", text="指派类型")
        self.assignments_tree.heading("notes", text="备注")

        self.assignments_tree.column("assignment_id", width=60, anchor=tk.CENTER)
        self.assignments_tree.column("trainer_name", width=150)
        self.assignments_tree.column("assignment_date", width=100, anchor=tk.CENTER)
        self.assignments_tree.column("assignment_type", width=150)
        self.assignments_tree.column("notes", width=200)

        scrollbar = ttk.Scrollbar(trainer_list_frame, orient="vertical", command=self.assignments_tree.yview)
        self.assignments_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.assignments_tree.pack(fill="both", expand=True)
        self.assignments_tree.bind("<Double-1>", lambda e: self.edit_selected_assignment())

        self.load_member_assignments()

    def load_member_assignments(self):
        for item in self.assignments_tree.get_children():
            self.assignments_tree.delete(item)
        assignments = db_ops.get_assignments_for_member(self.member_id)
        # assignments format: (mta.id, t.name, mta.assignment_date, mta.assignment_type, mta.notes, mta.trainer_id)
        for assign in assignments:
            self.assignments_tree.insert("", tk.END, values=assign[:-1]) # Exclude trainer_id from display

    def assign_new_trainer_to_member(self):
        dialog = ManageMemberTrainerAssignmentDialog(self, "指派新教练", member_id=self.member_id)
        if dialog.result:
            self.load_member_assignments()

    def edit_selected_assignment(self):
        selected_item = self.assignments_tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个教练指派记录进行编辑。", parent=self)
            return
        
        assignment_id = self.assignments_tree.item(selected_item)['values'][0]
        dialog = ManageMemberTrainerAssignmentDialog(self, "编辑教练指派信息", member_id=self.member_id, assignment_id=assignment_id)
        if dialog.result:
            self.load_member_assignments()
            
    def unassign_selected_trainer(self):
        selected_item = self.assignments_tree.focus()
        if not selected_item:
            messagebox.showwarning("提示", "请先选择一个教练指派记录进行解除。", parent=self)
            return
        
        assignment_id = self.assignments_tree.item(selected_item)['values'][0]
        trainer_name = self.assignments_tree.item(selected_item)['values'][1]

        if messagebox.askyesno("确认解除", f"确定要解除会员 '{self.member_name}' 与教练 '{trainer_name}' (指派ID: {assignment_id}) 的指派关系吗？", parent=self):
            success, message = db_ops.unassign_trainer_from_member(assignment_id)
            if success:
                messagebox.showinfo("成功", message, parent=self)
                self.load_member_assignments()
            else:
                messagebox.showerror("失败", message, parent=self)


class ManageMemberCardDialog(simpledialog.Dialog):
    def __init__(self, parent, title, member_id, member_card_id=None):
        self.member_id = member_id
        self.member_card_id = member_card_id # If None, it's an "add" operation
        self.card_types = db_ops.get_all_card_types() # Fetch available card types
        self.card_type_map = {ct[1]: ct[0] for ct in self.card_types} # Name to ID
        self.card_type_details_map = {ct[0]: ct for ct in self.card_types} # ID to full details

        self.existing_data = None
        if self.member_card_id:
            self.existing_data = db_ops.get_member_card_details(self.member_card_id)
            if not self.existing_data:
                messagebox.showerror("错误", "无法加载会员卡数据。", parent=parent)
                # This dialog should not proceed if data loading fails for edit
                self.result = False 
                # super().__init__ might not be called, so handle destruction carefully
                # For simplicity, we let it proceed and it will likely fail on apply or show empty fields
                # A better approach would be to prevent the dialog from showing.
        
        super().__init__(parent, title)

    def body(self, master):
        row_idx = 0
        ttk.Label(master, text="会员卡类型:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.card_type_var = tk.StringVar()
        self.card_type_combo = ttk.Combobox(master, textvariable=self.card_type_var, 
                                            values=[ct[1] for ct in self.card_types], state="readonly", width=27)
        self.card_type_combo.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        if self.card_types:
            self.card_type_combo.current(0) # Default to first card type
        self.card_type_combo.bind("<<ComboboxSelected>>", self.on_card_type_selected)
        row_idx += 1

        ttk.Label(master, text="购买日期:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.purchase_date_entry = DateEntry(master, width=12, date_pattern='yyyy-mm-dd', state="readonly")
        self.purchase_date_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        self.purchase_date_entry.set_date(datetime.now())
        row_idx += 1
        
        ttk.Label(master, text="激活日期:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.activation_date_entry = DateEntry(master, width=12, date_pattern='yyyy-mm-dd')
        self.activation_date_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        row_idx += 1

        ttk.Label(master, text="失效日期:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.expiry_date_entry = DateEntry(master, width=12, date_pattern='yyyy-mm-dd', state="readonly")
        self.expiry_date_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        row_idx += 1

        ttk.Label(master, text="状态:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(master, textvariable=self.status_var, 
                                         values=["pending_activation", "active", "frozen", "expired", "cancelled"], 
                                         state="readonly", width=27)
        self.status_combo.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        self.status_combo.set("pending_activation")
        row_idx += 1

        ttk.Label(master, text="备注:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.notes_entry = ttk.Entry(master, width=30)
        self.notes_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        row_idx += 1

        if self.existing_data: # Populate fields for editing
            # existing_data: (id, member_id, card_type_id, purchase_date, activation_date, expiry_date, status, notes)
            try:
                card_type_name = next(name for name, id_val in self.card_type_map.items() if id_val == self.existing_data[2])
                self.card_type_var.set(card_type_name)
            except StopIteration:
                messagebox.showwarning("警告", "无法匹配现有会员卡类型。", parent=self)

            if self.existing_data[3]: self.purchase_date_entry.set_date(datetime.strptime(self.existing_data[3], '%Y-%m-%d %H:%M:%S').date() if ' ' in self.existing_data[3] else datetime.strptime(self.existing_data[3], '%Y-%m-%d').date())
            if self.existing_data[4]: self.activation_date_entry.set_date(datetime.strptime(self.existing_data[4], '%Y-%m-%d').date())
            if self.existing_data[5]: self.expiry_date_entry.set_date(datetime.strptime(self.existing_data[5], '%Y-%m-%d').date())
            if self.existing_data[6]: self.status_var.set(self.existing_data[6])
            if self.existing_data[7]: self.notes_entry.insert(0, self.existing_data[7])
        else: # For new card, auto-calculate expiry based on selected card type
            self.on_card_type_selected(None)


        return self.card_type_combo # initial focus

    def on_card_type_selected(self, event):
        selected_card_name = self.card_type_var.get()
        if not selected_card_name:
            return
        
        card_type_id = self.card_type_map.get(selected_card_name)
        if not card_type_id:
            return
            
        card_details = self.card_type_details_map.get(card_type_id) # (id, name, price, duration_days, description)
        if not card_details:
            return

        duration_days = card_details[3]
        
        # Auto-calculate expiry date if activation date is set, or from purchase date
        base_date_str = self.activation_date_entry.get()
        base_date_obj = None

        if base_date_str:
            try:
                base_date_obj = datetime.strptime(base_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass # Invalid date format, ignore for now
        
        if not base_date_obj: # If activation date not set or invalid, use purchase date
            try:
                base_date_obj = self.purchase_date_entry.get_date() # tkcalendar DateEntry
            except AttributeError: # If it's a simple Entry
                 try:
                     base_date_obj = datetime.strptime(self.purchase_date_entry.get(), '%Y-%m-%d').date()
                 except ValueError:
                     base_date_obj = datetime.now().date() # Fallback to today

        if base_date_obj:
            expiry_date = base_date_obj + timedelta(days=duration_days)
            self.expiry_date_entry.set_date(expiry_date)


    def validate(self):
        if not self.card_type_var.get():
            messagebox.showerror("错误", "请选择会员卡类型。", parent=self)
            return 0
        if not self.purchase_date_entry.get():
            messagebox.showerror("错误", "购买日期不能为空。", parent=self)
            return 0
        # Activation date can be null initially
        if not self.expiry_date_entry.get():
            messagebox.showerror("错误", "失效日期不能为空。", parent=self)
            return 0
        if not self.status_var.get():
            messagebox.showerror("错误", "状态不能为空。", parent=self)
            return 0
        return 1

    def apply(self):
        card_type_name = self.card_type_var.get()
        card_type_id = self.card_type_map.get(card_type_name)
        
        purchase_date_obj = self.purchase_date_entry.get_date()
        purchase_date_str = purchase_date_obj.strftime('%Y-%m-%d %H:%M:%S') if purchase_date_obj else None # Store with time for consistency if needed

        activation_date_obj = self.activation_date_entry.get_date()
        activation_date_str = activation_date_obj.strftime('%Y-%m-%d') if activation_date_obj else None
        
        expiry_date_obj = self.expiry_date_entry.get_date()
        expiry_date_str = expiry_date_obj.strftime('%Y-%m-%d') if expiry_date_obj else None
        
        status = self.status_var.get()
        notes = self.notes_entry.get().strip()

        if self.member_card_id: # Edit existing card
            success, message = db_ops.update_member_card_details(self.member_card_id, card_type_id, purchase_date_str, activation_date_str, expiry_date_str, status, notes)
        else: # Add new card
            success, message = db_ops.assign_card_to_member(self.member_id, card_type_id, purchase_date_str, activation_date_str, expiry_date_str, status, notes)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent)
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False

class ManageMemberTrainerAssignmentDialog(simpledialog.Dialog):
    def __init__(self, parent, title, member_id, assignment_id=None):
        self.member_id = member_id
        self.assignment_id = assignment_id # If None, it's an "add" operation
        
        self.active_trainers = db_ops.get_all_trainers(active_only=True) # Fetch active trainers
        self.trainer_map = {t[1]: t[0] for t in self.active_trainers} # Name to ID

        self.existing_data = None
        if self.assignment_id:
            self.existing_data = db_ops.get_member_assignment_details(self.assignment_id)
            # existing_data: (id, member_id, trainer_id, assignment_date, assignment_type, notes)
            if not self.existing_data:
                messagebox.showerror("错误", "无法加载教练指派数据。", parent=parent)
                # This dialog should not proceed if data loading fails for edit
                self.result = False 
        
        super().__init__(parent, title)

    def body(self, master):
        row_idx = 0
        ttk.Label(master, text="选择教练:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.trainer_var = tk.StringVar()
        self.trainer_combo = ttk.Combobox(master, textvariable=self.trainer_var, 
                                          values=[t[1] for t in self.active_trainers], state="readonly", width=27)
        self.trainer_combo.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        if self.active_trainers:
            self.trainer_combo.current(0) 
        row_idx += 1

        ttk.Label(master, text="指派日期:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.assignment_date_entry = DateEntry(master, width=12, date_pattern='yyyy-mm-dd')
        self.assignment_date_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        self.assignment_date_entry.set_date(datetime.now())
        row_idx += 1
        
        ttk.Label(master, text="指派类型:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.assignment_type_entry = ttk.Entry(master, width=30)
        self.assignment_type_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        row_idx += 1

        ttk.Label(master, text="备注:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.notes_entry = ttk.Entry(master, width=30)
        self.notes_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        row_idx += 1

        if self.existing_data: 
            # existing_data: (id, member_id, trainer_id, assignment_date, assignment_type, notes)
            try:
                trainer_name = next(name for name, id_val in self.trainer_map.items() if id_val == self.existing_data[2])
                self.trainer_var.set(trainer_name)
            except StopIteration:
                # If trainer is inactive, they won't be in self.active_trainers. Handle this gracefully.
                # For now, we'll just not set the combobox, or you could fetch the specific trainer's name.
                inactive_trainer_data = db_ops.get_trainer_by_id(self.existing_data[2])
                if inactive_trainer_data:
                    self.trainer_combo.config(values=[inactive_trainer_data[1]] + [t[1] for t in self.active_trainers if t[0] != self.existing_data[2]])
                    self.trainer_var.set(inactive_trainer_data[1])
                else:
                    messagebox.showwarning("警告", "无法匹配现有指派的教练（可能已删除或非活动）。", parent=self)


            if self.existing_data[3]: self.assignment_date_entry.set_date(datetime.strptime(self.existing_data[3], '%Y-%m-%d').date())
            if self.existing_data[4]: self.assignment_type_entry.insert(0, self.existing_data[4])
            if self.existing_data[5]: self.notes_entry.insert(0, self.existing_data[5])
        
        return self.trainer_combo

    def validate(self):
        if not self.trainer_var.get():
            messagebox.showerror("错误", "请选择教练。", parent=self)
            return 0
        if not self.assignment_date_entry.get():
            messagebox.showerror("错误", "指派日期不能为空。", parent=self)
            return 0
        return 1

    def apply(self):
        trainer_name = self.trainer_var.get()
        trainer_id = self.trainer_map.get(trainer_name)
        
        # If trainer_id is None, it might be an inactive trainer selected during edit
        if trainer_id is None and self.existing_data and self.existing_data[2]:
             trainer_id = self.existing_data[2] # Use the original trainer_id for update

        if trainer_id is None: # Still none, means no valid trainer selected
            messagebox.showerror("错误", "无效的教练选择。", parent=self)
            self.result = False
            return

        assignment_date_obj = self.assignment_date_entry.get_date()
        assignment_date_str = assignment_date_obj.strftime('%Y-%m-%d') if assignment_date_obj else None
        
        assignment_type = self.assignment_type_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if self.assignment_id: # Edit existing assignment
            success, message = db_ops.update_assignment_details(self.assignment_id, trainer_id, assignment_date_str, assignment_type, notes)
        else: # Add new assignment
            success, message = db_ops.assign_trainer_to_member(self.member_id, trainer_id, assignment_date_str, assignment_type, notes)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent)
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False

class ManageMemberCourseEnrollmentDialog(simpledialog.Dialog):
    def __init__(self, parent, title, member_id, enrollment_id=None):
        self.member_id = member_id
        self.enrollment_id = enrollment_id # If None, it's an "add" operation
        
        self.active_courses = db_ops.get_all_courses(active_only=True) # Fetch active courses
        self.course_map = {c[1]: c[0] for c in self.active_courses} # Name to ID

        self.existing_data = None
        if self.enrollment_id:
            self.existing_data = db_ops.get_member_enrollment_details(self.enrollment_id)
            # existing_data: (id, member_id, course_id, enrollment_date, status, notes)
            if not self.existing_data:
                messagebox.showerror("错误", "无法加载课程报名数据。", parent=parent)
                self.result = False 
        
        super().__init__(parent, title)

    def body(self, master):
        row_idx = 0
        ttk.Label(master, text="选择课程:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.course_var = tk.StringVar()
        self.course_combo = ttk.Combobox(master, textvariable=self.course_var, 
                                          values=[c[1] for c in self.active_courses], state="readonly", width=27)
        self.course_combo.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        if self.active_courses:
            self.course_combo.current(0) 
        row_idx += 1

        ttk.Label(master, text="报名日期:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.enrollment_date_entry = DateEntry(master, width=12, date_pattern='yyyy-mm-dd')
        self.enrollment_date_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        self.enrollment_date_entry.set_date(datetime.now())
        row_idx += 1
        
        ttk.Label(master, text="报名状态:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(master, textvariable=self.status_var, 
                                         values=["enrolled", "completed", "dropped", "pending_payment"], 
                                         state="readonly", width=27)
        self.status_combo.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        self.status_combo.set("enrolled")
        row_idx += 1

        ttk.Label(master, text="备注:").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
        self.notes_entry = ttk.Entry(master, width=30)
        self.notes_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")
        row_idx += 1

        if self.existing_data: 
            # existing_data: (id, member_id, course_id, enrollment_date, status, notes)
            try:
                course_name = next(name for name, id_val in self.course_map.items() if id_val == self.existing_data[2])
                self.course_var.set(course_name)
            except StopIteration:
                inactive_course_data = db_ops.get_course_by_id(self.existing_data[2])
                if inactive_course_data:
                    self.course_combo.config(values=[inactive_course_data[1]] + [c[1] for c in self.active_courses if c[0] != self.existing_data[2]])
                    self.course_var.set(inactive_course_data[1])
                else:
                    messagebox.showwarning("警告", "无法匹配现有报名的课程（可能已删除或非活动）。", parent=self)

            if self.existing_data[3]: self.enrollment_date_entry.set_date(datetime.strptime(self.existing_data[3], '%Y-%m-%d').date())
            if self.existing_data[4]: self.status_var.set(self.existing_data[4])
            if self.existing_data[5]: self.notes_entry.insert(0, self.existing_data[5])
        
        return self.course_combo

    def validate(self):
        if not self.course_var.get():
            messagebox.showerror("错误", "请选择课程。", parent=self)
            return 0
        if not self.enrollment_date_entry.get():
            messagebox.showerror("错误", "报名日期不能为空。", parent=self)
            return 0
        if not self.status_var.get():
            messagebox.showerror("错误", "报名状态不能为空。", parent=self)
            return 0
        return 1

    def apply(self):
        course_name = self.course_var.get()
        course_id = self.course_map.get(course_name)

        if course_id is None and self.existing_data and self.existing_data[2]:
            course_id = self.existing_data[2] 

        if course_id is None:
            messagebox.showerror("错误", "无效的课程选择。", parent=self)
            self.result = False
            return

        enrollment_date_obj = self.enrollment_date_entry.get_date()
        enrollment_date_str = enrollment_date_obj.strftime('%Y-%m-%d') if enrollment_date_obj else None
        
        status = self.status_var.get()
        notes = self.notes_entry.get().strip()

        if self.enrollment_id: # Edit existing enrollment
            success, message = db_ops.update_enrollment_details(self.enrollment_id, course_id, enrollment_date_str, status, notes)
        else: # Add new enrollment
            success, message = db_ops.enroll_member_in_course(self.member_id, course_id, enrollment_date_str, status, notes)
        
        if success:
            messagebox.showinfo("成功", message, parent=self.parent)
            self.result = True
        else:
            messagebox.showerror("失败", message, parent=self)
            self.result = False
