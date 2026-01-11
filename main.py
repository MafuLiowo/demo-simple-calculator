import customtkinter as ctk
from tkinter import messagebox

# 设置全局主题
ctk.set_appearance_mode("dark")  # 开启深色模式
ctk.set_default_color_theme("blue") # 主题色：蓝色

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 窗口基础设置 ---
        self.title("简易计算器")
        self.geometry("340x480")
        self.resizable(False, False)

        # 运算状态存储
        self.current_value = ""
        self.formula = ""

        # --- 1. 显示区域 ---
        # 使用 Frame 包裹 Entry 增加边距感
        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.pack(padx=20, pady=(30, 10), fill="x")

        self.entry = ctk.CTkEntry(
            self.display_frame, 
            height=60, 
            font=("Inter", 32, "bold"), 
            justify="right",
            corner_radius=10,
            border_width=2
        )
        self.entry.pack(fill="x")
        self.entry.insert(0, "0")

        # --- 2. 按钮区域 ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # 按钮配置表 (文字, 行, 列, 颜色类型)
        buttons = [
            ('C', 0, 0, "danger"), ('/', 0, 3, "action"),
            ('7', 1, 0, "normal"), ('8', 1, 1, "normal"), ('9', 1, 2, "normal"), ('*', 1, 3, "action"),
            ('4', 2, 0, "normal"), ('5', 2, 1, "normal"), ('6', 2, 2, "normal"), ('-', 2, 3, "action"),
            ('1', 3, 0, "normal"), ('2', 3, 1, "normal"), ('3', 3, 2, "normal"), ('+', 3, 3, "action"),
            ('0', 4, 0, "normal", 2), ('.', 4, 2, "normal"), ('=', 4, 3, "success")
        ]

        # 配置网格权重，使按钮均匀分布
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)

        # 循环创建按钮
        for btn_data in buttons:
            text, row, col, style = btn_data[0:4]
            colspan = btn_data[4] if len(btn_data) > 4 else 1
            
            self.create_button(text, row, col, colspan, style)

    def create_button(self, text, row, col, colspan, style):
        # 根据不同风格设置颜色
        colors = {
            "danger": ("#FF6B6B", "#EE5253"),  # 清除键
            "action": ("#54a0ff", "#2e86de"),  # 运算符
            "success": ("#1dd1a1", "#10ac84"), # 等号
            "normal": ("#576574", "#222f3e")   # 数字
        }
        
        btn = ctk.CTkButton(
            self.button_frame,
            text=text,
            corner_radius=8,
            font=("Inter", 18, "bold"),
            fg_color=colors[style],
            command=lambda t=text: self.on_button_click(t)
        )
        btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")

    def on_button_click(self, char):
        """处理按钮点击逻辑"""
        if char == 'C':
            self.current_value = ""
            self.update_display("0")
        elif char == '=':
            self.calculate()
        else:
            # 简单的输入限制（防止多个小数点等）
            if char in "+-*/" and (not self.current_value or self.current_value[-1] in "+-*/"):
                return
            self.current_value += str(char)
            self.update_display(self.current_value)

    def update_display(self, text):
        self.entry.delete(0, "end")
        self.entry.insert(0, text)

    def calculate(self):
        try:
            # 安全提示：在实际信安工具中，建议使用解析器代替 eval
            # 这里为了演示核心逻辑，先使用 eval，但加入了错误处理
            result = str(eval(self.current_value))
            self.update_display(result)
            self.current_value = result
        except ZeroDivisionError:
            messagebox.showerror("错误", "数学错误：除数不能为零")
            self.on_button_click('C')
        except Exception:
            messagebox.showerror("错误", "输入非法")
            self.on_button_click('C')

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()