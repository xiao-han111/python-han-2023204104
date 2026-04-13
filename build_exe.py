"""打包脚本"""
import os
import sys
import shutil
from PyInstaller.__main__ import run as run_pyinstaller

# 清理旧的打包文件
def clean_old_build():
    """清理旧的打包文件"""
    for dir_name in ['dist', 'build']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理 {dir_name} 目录")

# 运行PyInstaller
def run_build():
    """运行PyInstaller进行打包"""
    args = [
        'PID仿真系统.spec',
        '--clean'
    ]
    print(f"运行命令: pyinstaller {' '.join(args)}")
    run_pyinstaller(args)

# 复制必要的文件
def copy_files():
    """复制必要的文件到打包目录"""
    dist_dir = 'dist\PID温度控制仿真系统'
    if os.path.exists(dist_dir):
        # 复制使用说明
        if os.path.exists('使用说明.txt'):
            shutil.copy('使用说明.txt', dist_dir)
            print("已复制使用说明.txt")
        else:
            # 创建默认的使用说明
            with open(os.path.join(dist_dir, '使用说明.txt'), 'w', encoding='utf-8') as f:
                f.write("PID温度控制仿真系统使用说明\n\n")
                f.write("1. 登录系统：\n")
                f.write("   - 管理员账号：admin / admin123\n")
                f.write("   - 普通用户账号：user / user123\n\n")
                f.write("2. 功能说明：\n")
                f.write("   - 实时波形：显示设定值、过程值、控制量和干扰\n")
                f.write("   - 控制策略：支持5种控制策略切换\n")
                f.write("   - 手动/自动模式：支持无扰动切换\n")
                f.write("   - 干扰施加：可施加方波干扰\n")
                f.write("   - 历史曲线：查看和导出历史数据\n\n")
                f.write("3. 注意事项：\n")
                f.write("   - 请确保有足够的权限读写数据目录\n")
                f.write("   - 如有问题，请查看data/logs目录下的错误日志\n")
            print("已创建使用说明.txt")

if __name__ == '__main__':
    print("开始打包PID温度控制仿真系统...")
    clean_old_build()
    run_build()
    copy_files()
    print("打包完成！")
