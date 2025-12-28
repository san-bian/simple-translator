import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Menu
import json
import os
import sys
from collections import deque
from datetime import datetime
import threading
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw


class SimpleTranslationTray:
    def __init__(self):
        # 创建隐藏的主窗口
        self.root = tk.Tk()
        self.root.withdraw()

        # 配置文件
        self.config_file = "translation_config.json"
        self.config = self.load_config()

        # 创建窗口
        self.setting_window = None
        self.history_window = None

        # 启动托盘
        self.start_tray()

    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_config()
        return self.default_config()

    def default_config(self):
        """默认配置"""
        return {
            "secret_id": "",
            "secret_key": "",
            "source_language": "en",
            "target_language": "zh",
            "server_client": "baidu",
            "history": []
        }

    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def add_history(self, source, target):
        """添加历史记录"""
        if "history" not in self.config:
            self.config["history"] = []

        record = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": source,
            "target": target
        }

        # 只保留最近10条
        self.config["history"].insert(0, record)
        if len(self.config["history"]) > 10:
            self.config["history"] = self.config["history"][:10]

        self.save_config()

    def start_tray(self):
        """启动系统托盘"""
        # 创建托盘图标
        icon_image = self.create_icon()

        # 创建菜单
        menu = (
            item('设置', self.show_settings, default=True),
            item('历史记录', self.show_history),
            item('退出', self.quit_app)
        )

        # 启动托盘
        self.icon = pystray.Icon("translation", icon_image, "翻译工具", menu)

        # 在后台线程运行托盘
        thread = threading.Thread(target=self.icon.run, daemon=True)
        thread.start()

    def create_icon(self):
        """创建托盘图标"""
        # 创建一个简单的图标
        image = Image.new('RGB', (64, 64), 'white')
        draw = ImageDraw.Draw(image)

        # 画一个翻译图标
        draw.rectangle([20, 15, 44, 45], outline='blue', width=3)
        draw.line([32, 20, 32, 40], fill='black', width=2)
        draw.line([25, 25, 32, 20], fill='black', width=2)
        draw.line([39, 25, 32, 20], fill='black', width=2)
        draw.line([25, 35, 32, 40], fill='black', width=2)
        draw.line([39, 35, 32, 40], fill='black', width=2)

        return image

    def show_settings(self, icon=None, item=None):
        """显示设置窗口"""
        if self.setting_window and self.setting_window.winfo_exists():
            self.setting_window.deiconify()
            self.setting_window.focus_force()
            return

        self.setting_window = tk.Toplevel()
        self.setting_window.title("翻译设置")
        self.setting_window.geometry("400x300")

        # 居中显示
        self.center_window(self.setting_window, 400, 300)

        # 设置关闭按钮行为
        self.setting_window.protocol("WM_DELETE_WINDOW",
                                     lambda: self.setting_window.withdraw())

        # 创建界面
        self.create_settings_ui()

    def show_history(self, icon=None, item=None):
        """显示历史记录窗口"""
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.deiconify()
            self.history_window.focus_force()
            return

        self.history_window = tk.Toplevel()
        self.history_window.title("翻译历史")
        self.history_window.geometry("500x400")

        # 居中显示
        self.center_window(self.history_window, 500, 400)

        # 设置关闭按钮行为
        self.history_window.protocol("WM_DELETE_WINDOW",
                                     lambda: self.history_window.withdraw())

        # 创建界面
        self.create_history_ui()

    def create_settings_ui(self):
        """创建设置界面"""
        frame = ttk.Frame(self.setting_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Secret ID:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.secret_id_var = tk.StringVar(
            value=self.config.get("secret_id", ""))
        ttk.Entry(frame, textvariable=self.secret_id_var,
                  width=30).grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Secret Key:").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.secret_key_var = tk.StringVar(
            value=self.config.get("secret_key", ""))
        ttk.Entry(frame, textvariable=self.secret_key_var,
                  width=30, show="*").grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="源语言:").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar(
            value=self.config.get("source_language", "en"))
        ttk.Combobox(frame, textvariable=self.source_var,
                     values=["auto", "zh", "en", "ja", "ko"], width=28).grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="目标语言:").grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.target_var = tk.StringVar(
            value=self.config.get("target_language", "zh"))
        ttk.Combobox(frame, textvariable=self.target_var,
                     values=["zh", "en", "ja", "ko"], width=28).grid(row=3, column=1, pady=5)

        ttk.Label(frame, text="翻译服务:").grid(
            row=4, column=0, sticky=tk.W, pady=5)
        self.service_var = tk.StringVar(
            value=self.config.get("server_client", "baidu"))
        ttk.Combobox(frame, textvariable=self.service_var,
                     values=["baidu", "google", "youdao"], width=28).grid(row=4, column=1, pady=5)

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="保存", command=self.save_settings).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="测试", command=self.test_connection).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="关闭",
                   command=lambda: self.setting_window.withdraw()).pack(side=tk.LEFT, padx=5)

    def create_history_ui(self):
        """创建历史记录界面"""
        main_frame = ttk.Frame(self.history_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(main_frame, text="最近翻译记录",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        # 文本显示区域
        self.history_text = scrolledtext.ScrolledText(
            main_frame, height=20, width=60)
        self.history_text.pack(fill=tk.BOTH, expand=True)

        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="刷新", command=self.refresh_history).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空", command=self.clear_history).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="关闭",
                   command=lambda: self.history_window.withdraw()).pack(side=tk.RIGHT, padx=5)

        # 加载历史记录
        self.refresh_history()

    def save_settings(self):
        """保存设置"""
        self.config.update({
            "secret_id": self.secret_id_var.get(),
            "secret_key": self.secret_key_var.get(),
            "source_language": self.source_var.get(),
            "target_language": self.target_var.get(),
            "server_client": self.service_var.get()
        })
        self.save_config()
        messagebox.showinfo("成功", "设置已保存！")

    def test_connection(self):
        """测试连接"""
        messagebox.showinfo("提示", "连接测试需要根据具体的翻译API实现")

    def refresh_history(self):
        """刷新历史记录"""
        if not self.history_window:
            return

        self.history_text.delete(1.0, tk.END)
        history = self.config.get("history", [])

        if not history:
            self.history_text.insert(tk.END, "暂无翻译记录")
            return

        for i, record in enumerate(history, 1):
            self.history_text.insert(tk.END,
                                     f"{i}. [{record.get('date', '')} {record.get('time', '')}]\n")
            self.history_text.insert(
                tk.END, f"   原文: {record.get('source', '')}\n")
            self.history_text.insert(
                tk.END, f"   译文: {record.get('target', '')}\n\n")

    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？"):
            self.config["history"] = []
            self.save_config()
            self.refresh_history()

    def center_window(self, window, width, height):
        """窗口居中显示"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def quit_app(self, icon=None, item=None):
        """退出应用"""
        if self.setting_window:
            self.setting_window.destroy()
        if self.history_window:
            self.history_window.destroy()
        if hasattr(self, 'icon'):
            self.icon.stop()
        self.root.quit()
        sys.exit(0)

    def run(self):
        """运行主循环"""
        self.root.mainloop()


def main_simple():
    app = SimpleTranslationTray()
    app.run()


if __name__ == "__main__":
    main_simple()
