
from pynput import mouse
import tkinter as tk
import threading
import time
import pyautogui


class NotifyWindow:
    def __init__(self):
        self._root = None

    def close_window(self, event=None):
        self._root.quit()
        self._root.destroy()

    def create_window(self, title, message, x, y):
        self._root = tk.Tk()
        self._root.title(title)

        # 设置窗口位置和大小
        self._root.geometry(f"300x120+{x}+{y}")

        # 设置窗口为无边框、置顶
        self._root.overrideredirect(True)  # 无边框
        self._root.attributes('-topmost', True)  # 置顶
        self._root.attributes('-alpha', 0.95)  # 透明度

        # 设置背景色
        self._root.configure(bg='#2c3e50')

        # 创建框架
        frame = tk.Frame(self._root, bg='#2c3e50', padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            frame,
            text=title,
            font=("Microsoft YaHei", 10, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(anchor='w', pady=(0, 5))

        message_label = tk.Label(
            frame,
            text=message,
            font=("Microsoft YaHei", 9),
            fg='#bdc3c7',
            bg='#2c3e50',
            wraplength=280,
            justify='left'
        )
        message_label.pack(anchor='w')

    def get_position(self, type=None):
        if type == "Mouse":
            x, y = pyautogui.position()
            # _mouse = mouse.Controller()
            # x, y = _mouse.position
            # print(f"{x} {y}")
        else:
            x = 0
            y = 0
        return [x, y]

    def close_window_after_timeout(self, timeout):
        def _close_after_timeout(timeout):
            time.sleep(timeout)
            self.close_window()
        timer_thread = threading.Thread(
            target=_close_after_timeout, args=(timeout,), daemon=True)
        timer_thread.start()

    def show(self, title=None, message="", follow_mouse=True, timeout=5, show_progress=True):
        if follow_mouse:
            position_type = 'Mouse'
        else:
            position_type = 'other'
        position = self.get_position(type=position_type)
        self.create_window(title=title, message=message,
                           x=position[0], y=position[1])
        if show_progress:
            self.show_progress(timeout=timeout)
        self._root.bind("<Button-1>", self.close_window)
        self.close_window_after_timeout(timeout=timeout)

        try:
            self._root.mainloop()
        except Exception as e:
            print(e)

    def show_progress(self, timeout):
        progress = tk.Frame(self._root, bg='#3498db', height=3)
        progress.place(x=0, y=115, width=300, height=3)

        def update_progress(remaining_time):
            width = int(300 * remaining_time / timeout)
            progress.place(width=width)

            if remaining_time > 0:
                self._root.after(1000, update_progress, remaining_time - 1)

        update_progress(timeout)


def show_simple_notification(title, message, x=100, y=100, show_time=3):
    """显示一个简洁的无按钮通知，自动消失"""

    def close_window():
        """关闭窗口"""
        time.sleep(show_time)
        root.quit()
        root.destroy()

    # 创建窗口
    root = tk.Tk()
    root.title(title)

    # 设置窗口位置和大小
    root.geometry(f"300x120+{x}+{y}")

    # 设置窗口为无边框、置顶
    root.overrideredirect(True)  # 无边框
    root.attributes('-topmost', True)  # 置顶
    root.attributes('-alpha', 0.95)  # 透明度

    # 设置背景色
    root.configure(bg='#2c3e50')

    # 创建框架
    frame = tk.Frame(root, bg='#2c3e50', padx=10, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    # 标题
    title_label = tk.Label(
        frame,
        text=title,
        font=("Microsoft YaHei", 10, "bold"),
        fg='#ecf0f1',
        bg='#2c3e50'
    )
    title_label.pack(anchor='w', pady=(0, 5))

    # 消息
    message_label = tk.Label(
        frame,
        text=message,
        font=("Microsoft YaHei", 9),
        fg='#bdc3c7',
        bg='#2c3e50',
        wraplength=280,
        justify='left'
    )
    message_label.pack(anchor='w')

    # 进度条（显示剩余时间）
    if show_time > 0:
        progress = tk.Frame(root, bg='#3498db', height=3)
        progress.place(x=0, y=115, width=300, height=3)

        def update_progress(remaining_time):
            """更新进度条"""
            width = int(300 * remaining_time / show_time)
            progress.place(width=width)

            if remaining_time > 0:
                root.after(1000, update_progress, remaining_time - 1)

        update_progress(show_time)

    # 点击窗口任意位置立即关闭
    def on_click(event):
        root.quit()
        root.destroy()

    root.bind("<Button-1>", on_click)

    # 自动关闭线程
    if show_time > 0:
        timer_thread = threading.Thread(target=close_window, daemon=True)
        timer_thread.start()

    # 进入消息循环
    try:
        root.mainloop()
    except:
        pass


# 使用示例

notify_window = NotifyWindow()
notify_window.show(
    message="文文文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成文件保存完成件保存完成！")
