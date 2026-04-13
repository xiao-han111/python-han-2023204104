"""最基本的PyQt5测试脚本"""
import sys

print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

print("尝试导入PyQt5...")
try:
    from PyQt5.QtWidgets import QApplication, QWidget
    print("PyQt5导入成功！")
except Exception as e:
    print(f"PyQt5导入失败: {e}")
    sys.exit(1)

print("创建应用程序...")
app = QApplication(sys.argv)
print("应用程序创建成功")

print("创建窗口...")
window = QWidget()
window.setWindowTitle("测试窗口")
window.resize(400, 300)
print("窗口创建成功")

print("显示窗口...")
window.show()
print("窗口显示成功")

print("进入事件循环...")
sys.exit(app.exec_())
