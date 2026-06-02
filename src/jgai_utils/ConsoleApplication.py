"""# 用sap22000 生成 一根梁在一个荷载作用下支座弯矩、变形数据
"""
import os,sys,itertools
import csv, glob
import time


if __name__ == "__main__":
    sys.path.append("..")


import os
import time
# 定义ANSI颜色码
class _C: # AnsiColor:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BBLACK = "\033[40m"
    BRED = "\033[41m"
    BGREEN = "\033[42m"
    BYELLOW = "\033[43m"
    BBLUE = "\033[44m"
    BPURPLE = "\033[45m"
    BCYAN = "\033[46m"
    BWHITE = "\033[47m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
    CLINE = "\033[K"

class ConsoleApplication:
    def __init__(self):
        pass
    def init(self,tsk,cls_after_task=False):
        self.running = True
        self.current = None
        self.tasks = tsk
        self.cls_after_task = cls_after_task
        self.tasks["x"]=("Exit", self.exit_program)

    def clear_screen(self):
        """清空控制台屏幕"""
        os.system("cls" if os.name == "nt" else "clear")

    def display_menu(self):
        """显示主菜单界面"""
        # print("=" * 50)
        # print()

        for k in self.tasks.keys():
            print(f"  [ {_C.RED}{k}{_C.END} ] {self.tasks[k][0]}")

    def exit_program(self):
        """退出程序"""
        print("\nGood boy!")
        self.running = False

    def run(self):
        """运行主程序"""
        while self.running:
            self.clear_screen() if self.cls_after_task else 0
            self.display_menu()

            choice = input(f"{_C.BYELLOW}{_C.GREEN}Please select task:{_C.END} ").strip()
            self.current = choice
            if choice in self.tasks:
                self.clear_screen() if self.cls_after_task else 0
                self.tasks[choice][1]()
            else:
                print(f"{_C.YELLOW}Invalid. Please input {_C.RED}[", "/".join(self.tasks.keys()), f"]{_C.END}")
                time.sleep(1) if self.cls_after_task else 0

if __name__ == "__main__":
    print("Start   ...")
    def f1():
        print("功能1")

    def f2():
        print("功能2")

    def f3():
        print("功能3")

    app = ConsoleApplication()
    app.init(
        {
            "1": ("从字符串验证", f1),
            "f2": ("从字符串验证(循环)", f2),
            "G3": ("从CSV文件名", f3),
        }
    )
    app.run()


    print(f"done.1", time.strftime("@%y.%m.%d-%H:%M:%S", time.localtime()))
