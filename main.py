import os
from db import database_setup
from gui.main_window import MainWindow

def ensure_db_directory():
    """确保数据库目录存在"""
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            print(f"目录 '{db_dir}' 已创建。")
        except OSError as e:
            print(f"创建目录 '{db_dir}' 失败: {e}")
            # 如果目录创建失败，后续数据库操作可能会失败，这里可以决定是否退出程序
            # exit(1) 

def delete_database_file_if_exists():
    """删除现有的数据库文件以强制重新创建"""
    db_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'gym_management.db')
    if os.path.exists(db_file_path):
        try:
            os.remove(db_file_path)
            print(f"旧数据库文件 '{db_file_path}' 已删除。")
        except OSError as e:
            print(f"删除旧数据库文件 '{db_file_path}' 失败: {e}")
            # 根据需要决定是否在此处退出
            # exit(1)

if __name__ == "__main__":
    # 1. 确保数据库目录存在
    ensure_db_directory()

    # !! 重要：在初始化数据库之前删除旧数据库文件 !!
    # !! 这将清除所有现有数据。仅用于开发阶段解决模式问题。!!
    # !! 在部署或数据重要时，请注释掉下面这行或移除此功能。!!
    delete_database_file_if_exists() 

    # 2. 初始化数据库 (创建表，如果它们还不存在)
    print("正在初始化数据库...")
    database_setup.create_tables()
    print("数据库初始化完成。")

    # 3. 启动GUI应用程序
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.quit_app) # 处理窗口关闭按钮
    app.mainloop()
