import tkinter as tk
from tkinter import messagebox


def show_notification_at_position(title, message, x=100, y=100):
    """在指定位置显示通知框"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.geometry(f"+{x}+{y}")  # 设置窗口位置
    messagebox.showinfo(title, message)
    root.destroy()


# 使用示例
show_notification_at_position(
    "通知", "这这是一个测试通知这是一个测试通知这是一个测试通知这是一个测试通知这是一个测试通知这是一个测试通知这是一个测试通知是一个测试通知！", 500, 300)
