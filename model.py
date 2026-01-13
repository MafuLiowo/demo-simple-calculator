import re
import ast
import operator

class CalculatorModel:
    def __init__(self):
        # 支持的二元运算符映射
        self._bin_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            # 你可以在这里轻松添加更多操作，比如 ast.Pow: operator.pow
        }
        # 支持的一元运算符映射
        self._unary_ops = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

    def evaluate(self, expression: str, mode: str) -> tuple[str, str]:
        """
        对外主接口：执行计算并返回 (显示文本, 辅助文本)
        """
        if expression == '233': # 彩蛋
            return "哈哈哈", ""
            
        if not expression:
            return "", ""

        is_hex_mode = (mode == "Programmer")

        try:
            # 1. 核心计算
            result = self._compute(expression, is_hex_mode)
            
            # 2. 结果格式化
            return self._format_result(result, is_hex_mode)

        except ZeroDivisionError:
            return "Error: Div 0", ""
        except Exception as e:
            # 实际开发中建议记录日志: print(f"Calc Error: {e}")
            return "Error", ""

    def convert_hex_preview(self, hex_str: str) -> str:
        """程序员模式实时预览"""
        try:
            # 使用更严格的正则，或者直接利用int()的异常捕获
            if hex_str and re.fullmatch(r'[0-9A-Fa-f]+', hex_str):
                return f"DEC: {int(hex_str, 16)}"
        except ValueError:
            pass
        return ""

    # ================= 内部逻辑方法 =================

    def _compute(self, expression: str, is_hex: bool):
        """解析字符串并计算数值"""
        if is_hex:
            expression = self._preprocess_hex(expression)

        # 构建 AST
        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError:
            raise ValueError("语法错误")

        return self._eval_node(tree.body, is_hex)

    def _preprocess_hex(self, expression: str) -> str:
        """将十六进制字符串替换为十进制字符串，以便 AST 解析"""
        # 注意：这里假设所有连续的 [0-9A-F] 都是数字。
        # 如果表达式包含变量名（如 Add），这会导致误判，需根据实际需求调整正则边界。
        return re.sub(
            r'\b[0-9A-Fa-f]+\b', 
            lambda m: str(int(m.group(0), 16)), 
            expression
        )

    def _eval_node(self, node, is_hex: bool):
        """递归遍历 AST 节点进行计算"""
        
        # 1. 处理常数 (Python 3.8+ ast.Constant, 旧版 ast.Num)
        if isinstance(node, ast.Constant):
            return node.value

        # 2. 处理二元运算 (A + B)
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left, is_hex)
            right = self._eval_node(node.right, is_hex)
            op_type = type(node.op)

            if op_type in self._bin_ops:
                # 特殊处理：程序员模式下的除法通常是整除
                if op_type == ast.Div:
                    if right == 0: raise ZeroDivisionError
                    return left // right if is_hex else left / right
                
                return self._bin_ops[op_type](left, right)

        # 3. 处理一元运算 (-A)
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand, is_hex)
            op_type = type(node.op)
            
            if op_type in self._unary_ops:
                return self._unary_ops[op_type](operand)

        raise ValueError(f"不支持的语法节点: {type(node)}")

    def _format_result(self, result, is_hex: bool) -> tuple[str, str]:
        """将数值结果转换为 UI 显示所需的字符串"""
        display_text = ""
        sub_text = ""

        if is_hex:
            int_res = int(result)
            # 使用 f-string 格式化十六进制，移除 '0x' 并转大写
            display_text = f"{int_res:X}"
            sub_text = f"DEC: {int_res}"
        else:
            # 浮点数处理：保留精度并去除多余的 .0
            if isinstance(result, float):
                # 限制最大精度，防止无限小数撑爆UI
                result = round(result, 10)
                # 利用 str() 的特性，或者判定 is_integer
                if result.is_integer():
                    display_text = str(int(result))
                else:
                    display_text = str(result)
            else:
                display_text = str(result)
        
        return display_text, sub_text