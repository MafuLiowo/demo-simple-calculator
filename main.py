import customtkinter as ctk
import re

# 设置全局主题
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 窗口基础设置 ---
        self.title("简易计算器")
        self.geometry("340x520") 
        self.resizable(False, False)

        # 状态存储
        self.current_value = ""
        self.mode = "Standard" 

        # --- 1. 顶部模式切换 ---
        self.mode_segment = ctk.CTkSegmentedButton(
            self, 
            values=["标准模式", "程序员(Hex)"], 
            command=self.change_mode
        )
        self.mode_segment.pack(pady=(10, 5))
        self.mode_segment.set("标准模式")

        # --- 2. 显示区域 ---
        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.pack(padx=20, pady=(10, 10), fill="x")

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
        
        self.sub_label = ctk.CTkLabel(self.display_frame, text="", font=("Inter", 12), text_color="gray")
        self.sub_label.pack(anchor="e", padx=5)

        # --- 3. 按钮区域容器 ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.setup_standard_buttons()

    def clear_button_frame(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def change_mode(self, value):
        self.current_value = ""
        self.update_display("0")
        self.sub_label.configure(text="")
        self.clear_button_frame()

        if value == "标准模式":
            self.mode = "Standard"
            self.geometry("340x520")
            self.setup_standard_buttons()
        else:
            self.mode = "Programmer"
            self.geometry("500x520")
            self.setup_programmer_buttons()

    def setup_standard_buttons(self):
        """标准模式布局"""
        # 修改点1：将 'C' 改为 'CLEAR'，用于内部逻辑区分
        buttons = [
            ('CLEAR', 0, 0, "danger"), ('Backspace', 0, 1, "action", 2), ('/', 0, 3, "action"),
            ('7', 1, 0, "normal"), ('8', 1, 1, "normal"), ('9', 1, 2, "normal"), ('*', 1, 3, "action"),
            ('4', 2, 0, "normal"), ('5', 2, 1, "normal"), ('6', 2, 2, "normal"), ('-', 2, 3, "action"),
            ('1', 3, 0, "normal"), ('2', 3, 1, "normal"), ('3', 3, 2, "normal"), ('+', 3, 3, "action"),
            ('0', 4, 0, "normal", 2), ('.', 4, 2, "normal"), ('=', 4, 3, "success")
        ]
        self._create_grid(buttons, cols=4)

    def setup_programmer_buttons(self):
        """程序员模式布局"""
        # 修改点2：红色清除键使用 'CLEAR'，左侧 Hex C 键保持 'C'
        buttons = [
            # Row 0
            ('A', 0, 0, "hex"), ('B', 0, 1, "hex"), 
            ('CLEAR', 0, 2, "danger"), ('Backspace', 0, 3, "action", 2), ('/', 0, 5, "action"),
            
            # Row 1
            ('C', 1, 0, "hex"), ('D', 1, 1, "hex"), 
            ('7', 1, 2, "normal"), ('8', 1, 3, "normal"), ('9', 1, 4, "normal"), ('*', 1, 5, "action"),
            
            # Row 2
            ('E', 2, 0, "hex"), ('F', 2, 1, "hex"), 
            ('4', 2, 2, "normal"), ('5', 2, 3, "normal"), ('6', 2, 4, "normal"), ('-', 2, 5, "action"),
            
            # Row 3
            ('(', 3, 0, "hex"), (')', 3, 1, "hex"), 
            ('1', 3, 2, "normal"), ('2', 3, 3, "normal"), ('3', 3, 4, "normal"), ('+', 3, 5, "action"),
            
            # Row 4
            ('0', 4, 2, "normal", 3), ('=', 4, 5, "success")
        ]
        self._create_grid(buttons, cols=6)

    def _create_grid(self, buttons, cols):
        for i in range(cols):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)

        for btn_data in buttons:
            text = btn_data[0]
            row = btn_data[1]
            col = btn_data[2]
            style = btn_data[3]
            colspan = btn_data[4] if len(btn_data) > 4 else 1
            self.create_button(text, row, col, colspan, style)

    def create_button(self, text, row, col, colspan, style):
        colors = {
            "danger": ("#FF6B6B", "#EE5253"),
            "action": ("#54a0ff", "#2e86de"),
            "success": ("#1dd1a1", "#10ac84"),
            "normal": ("#576574", "#222f3e"),
            "hex":    ("#a5b1c2", "#4b6584") 
        }
        
        # 修改点3：显示逻辑分离
        # 如果内部指令是 'CLEAR'，按钮上依然显示 'C'，否则显示原文本
        display_text = "C" if text == "CLEAR" else text

        btn = ctk.CTkButton(
            self.button_frame,
            text=display_text, 
            corner_radius=8,
            font=("Inter", 18, "bold"),
            fg_color=colors.get(style, colors["normal"]),
            command=lambda t=text: self.on_button_click(t) # 注意：这里传入的是 text (包含 CLEAR)
        )
        btn.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3, sticky="nsew")

    def on_button_click(self, char):
        current_text = self.entry.get()
        
        if "Error" in current_text or "error" in current_text or current_text == "哈哈哈":
            self.current_value = ""
            self.update_display("0")
            if char in ["=", "CLEAR", "Backspace"]: return # 注意这里改为了 CLEAR

        # 修改点4：处理逻辑修改
        # 检测 CLEAR 指令，而不是检测字符 'C'
        if char == 'CLEAR':
            self.current_value = ""
            self.update_display("0")
            self.sub_label.configure(text="")
            
        elif char == '=':
            self.calculate()
        elif char == 'Backspace':
            self.current_value = self.current_value[:-1]
            self.update_display(self.current_value if self.current_value else "0")
            if self.mode == "Programmer" and self.current_value:
                try:
                      val = int(self.current_value, 16)
                      self.sub_label.configure(text=f"DEC: {val}")
                except:
                      self.sub_label.configure(text="")
        else:
            # 这里的逻辑不需要变
            # 此时如果 char 是 'C' (Hex C键)，它不等于 'CLEAR'，也不等于 '='，
            # 所以会直接流转到下面的代码，被当做普通字符添加到 current_value 中。
            
            if char in "+-*/":
                if not self.current_value: return
                if self.current_value[-1] in "+-*/": return 
            
            if self.mode == "Programmer" and char in [".", "(", ")"]:
                return

            self.current_value += str(char)
            self.update_display(self.current_value)
            
            # 程序员模式实时预览输入数字的十进制
            if self.mode == "Programmer" and char not in "+-*/":
                 try:
                      # 简单的实时预览逻辑，仅针对纯Hex数字有效
                      if re.fullmatch(r'[0-9A-Fa-f]+', self.current_value):
                          val = int(self.current_value, 16)
                          self.sub_label.configure(text=f"DEC: {val}")
                 except: pass

    def update_display(self, text):
        self.entry.delete(0, "end")
        self.entry.insert(0, text)

    def safe_parse_and_compute(self, expression, is_hex=False):
        if is_hex:
            tokens_raw = re.findall(r'[0-9A-Fa-f]+|[-+*/]', expression)
        else:
            tokens_raw = re.findall(r'\d+\.?\d*|[-+*/]', expression)
        
        tokens = []
        for t in tokens_raw:
            if t in "+-*/":
                tokens.append(t)
            else:
                if is_hex:
                    tokens.append(int(t, 16))
                else:
                    tokens.append(float(t))

        if not tokens: return 0

        stack = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '*' or token == '/':
                if not stack: raise ValueError
                prev_val = stack.pop()
                next_val = tokens[i+1]
                
                if token == '*':
                    res = prev_val * next_val
                else:
                    if next_val == 0: raise ZeroDivisionError
                    res = prev_val // next_val if is_hex else prev_val / next_val
                
                stack.append(res)
                i += 2
            else:
                stack.append(token)
                i += 1

        result = stack[0]
        i = 1
        while i < len(stack):
            op = stack[i]
            val = stack[i+1]
            if op == '+': result += val
            elif op == '-': result -= val
            i += 2
            
        return result

    def calculate(self):
        if not self.current_value: return
        
        if self.current_value == '233':
            self.current_value = "哈哈哈"
            self.update_display("哈哈哈")
            return

        try:
            is_hex_mode = (self.mode == "Programmer")
            result = self.safe_parse_and_compute(self.current_value, is_hex=is_hex_mode)
            
            if is_hex_mode:
                int_res = int(result)
                hex_res = hex(int_res).upper().replace("0X", "")
                self.current_value = hex_res
                self.update_display(hex_res)
                self.sub_label.configure(text=f"DEC: {int_res}")
            else:
                if isinstance(result, float):
                    result = round(result, 10)
                    if result.is_integer():
                        self.current_value = str(int(result))
                    else:
                        self.current_value = str(result)
                else:
                    self.current_value = str(result)
                self.update_display(self.current_value)

        except ZeroDivisionError:
            self.current_value = ""
            self.update_display("Error: Div 0")
        except Exception as e:
            self.current_value = ""
            self.update_display("Error")

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()