import tkinter as tk
from tkinter import ttk, messagebox
from .member_window import MemberWindow
from .card_type_window import CardTypeWindow
from .trainer_window import TrainerWindow
from .course_window import CourseWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("健身房会员管理系统")
        self.geometry("800x600")

        # 设置主题 (可选, 'clam', 'alt', 'default', 'classic')
        try:
            self.style = ttk.Style(self)
            available_themes = self.style.theme_names()
            # print(f"Available themes: {available_themes}")
            if 'clam' in available_themes:
                self.style.theme_use('clam')
            elif 'vista' in available_themes: # Windows
                 self.style.theme_use('vista')
        except tk.TclError:
            print("ttk themes not available or 'clam' theme not found. Using default.")


        # 主菜单栏
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="退出", command=self.quit_app) # 更改这里以调用 quit_app
        menubar.add_cascade(label="文件", menu=file_menu)

        # 管理菜单
        manage_menu = tk.Menu(menubar, tearoff=0)
        manage_menu.add_command(label="会员管理", command=self.open_member_management)
        manage_menu.add_command(label="课程管理", command=self.open_course_management) 
        manage_menu.add_command(label="教练管理", command=self.open_trainer_management) 
        manage_menu.add_separator()
        manage_menu.add_command(label="会员卡类型管理", command=self.open_card_type_management) 
        menubar.add_cascade(label="管理", menu=manage_menu)
        
        # 欢迎标签
        welcome_label = ttk.Label(self, text="欢迎使用健身房会员管理系统", font=("Helvetica", 16))
        welcome_label.pack(pady=50)

        # 快捷按钮区域
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        member_btn = ttk.Button(button_frame, text="会员管理", command=self.open_member_management, width=20, style="Accent.TButton")
        member_btn.grid(row=0, column=0, padx=10, pady=10, ipady=10)

        course_btn = ttk.Button(button_frame, text="课程管理", command=self.open_course_management, width=20, style="Accent.TButton") 
        course_btn.grid(row=0, column=1, padx=10, pady=10, ipady=10)
        
        trainer_btn = ttk.Button(button_frame, text="教练管理", command=self.open_trainer_management, width=20, style="Accent.TButton") 
        trainer_btn.grid(row=1, column=0, padx=10, pady=10, ipady=10)

        card_type_btn = ttk.Button(button_frame, text="会员卡类型", command=self.open_card_type_management, width=20, style="Accent.TButton") 
        card_type_btn.grid(row=1, column=1, padx=10, pady=10, ipady=10)

        # 状态栏 (可选)
        self.status_bar = ttk.Label(self, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 定义一些样式 (可选)
        self.style.configure("Accent.TButton", font=('Helvetica', 10, 'bold'), padding=5)


    def open_module_window(self, WindowClass):
        """通用函数，用于打开模块窗口并隐藏主窗口"""
        self.withdraw() # 隐藏主窗口
        module_win = WindowClass(self) # 将主窗口实例传递给子窗口
        module_win.grab_set() 
        # 子窗口关闭时，通过协议或按钮回调重新显示主窗口

    def show_main_window(self):
        """重新显示主窗口"""
        self.deiconify()
        self.update_status("返回主页")


    def open_member_management(self):
        self.open_module_window(MemberWindow)
        self.update_status("打开会员管理模块")

    def open_course_management(self):
        self.open_module_window(CourseWindow)
        self.update_status("打开课程管理模块")


    def open_trainer_management(self):
        self.open_module_window(TrainerWindow)
        self.update_status("打开教练管理模块")

    def open_card_type_management(self):
        self.open_module_window(CardTypeWindow)
        self.update_status("打开会员卡类型管理模块")

    def update_status(self, message):
        self.status_bar.config(text=message)

    def quit_app(self): # <--- 添加或确保此方法存在且正确
        if messagebox.askokcancel("退出", "确定要退出系统吗？", parent=self): # 添加 parent=self
            self.quit() # 停止 Tkinter 主循环
            self.destroy() # 销毁主窗口
