"""PyQt6测试脚本"""
import sys
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

try:
    from PyQt6.QtWidgets import QApplication
    print("PyQt6导入成功！")
except Exception as e:
    print(f"PyQt6导入失败: {e}")
    import traceback
    traceback.print_exc()
