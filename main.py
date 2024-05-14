#--------------------------------------------------------import---------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import customtkinter as ctk
import tkinter as tk
import threading
import pyperclip
import requests
import base64
import shutil
import time
import os
import re
import io

#--------------------------------------------------------global---------------------------------------------------------
# 初始化图片计数器
img_counter = 0

# 创建一个空列表来保存所有的图片链接
img_urls = []

# 输出文件夹名
output_dir = 'ins_output'

# 目标ins链接
URL = ''

# 创建一个事件对象
url_event = threading.Event()

# Base64格式保存图标
# Base64 图标字符串
icon_base64 = """
    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
"""
# 解码 Base64 字符串为二进制数据
icon_data = base64.b64decode(icon_base64)
# 创建 BytesIO 对象以便 PIL.Image 使用
icon_stream = io.BytesIO(icon_data)
# 创建 PIL.Image 对象
icon_image = Image.open(icon_stream)

#--------------------------------------------------------def---------------------------------------------------------
def download_image(url, filepath):
    """从给定的 URL 下载图像并将其保存到给定的文件路径。"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.content)
            print(f"{filepath}下载完成")
        else:
            print(f"下载失败: {url}")
    except requests.exceptions.SSLError:
        print(f"SSL 错误: {url}")


def check_connection(url):
    """检查网络连接"""
    try:
        response = requests.get(url, timeout=5)  # 设置超时为5秒
        response.raise_for_status()  # 如果发生错误（例如网络连接问题），则抛出异常
    except requests.exceptions.RequestException as e:
        print("网络连接有问题: ", e)
        return False
    return True


def openFile():
    """打开ins_output文件夹"""
    output_dir = 'ins_output'
    if os.path.exists(output_dir):
        os.startfile(output_dir)
    else:
        print(f"文件夹 {output_dir} 不存在.")


def clear_directory(directory):
    """清除指定目录下的所有文件"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # 删除文件
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除目录
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def edge_open():
    """Edge浏览器打开操作"""
    edge_options = Options()
    edge_options.add_argument("--no-first-run")
    edge_options.add_argument("--disable-extensions")
    edge_options.add_argument("--mute-audio")
    edge_options.add_argument("--disable-sync")
    edge_options.add_argument("--metrics-recording-only")
    edge_options.add_argument("--disable-default-apps")
    edge_options.add_argument("--safebrowsing-disable-auto-update")
    edge_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    edge_service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=edge_service, options=edge_options)
    return driver


def main():
    global img_counter, img_urls, URL
    while True:

        # os.system('cls')
        print("===============PASSER的ins图片提取脚本===============")
        print("注意：脚本运行时会自动打开浏览器，请勿操作该浏览器，稍后会自动关闭！！！")
        # 要求用户提供链接
        # URL = input("在此处粘贴ins链接(回车继续)：")
        print("外部GUI已打开，请在外部GUI内粘贴ins链接！")
        # 等待事件被设置
        url_event.wait()
        while not URL.strip() or 'www.instagram.com' not in URL:
            if not URL.strip():
                print("链接不能为空，请重新输入。")
                button_text.set("提交")
                url_event.clear()  # 重置事件
            if 'www.instagram.com' not in URL:
                print("链接格式错误，正确的格式应该包含 'www.instagram.com'，请重新输入。")
                button_text.set("提交")
                url_event.clear()  # 重置事件
            # URL = input("在此处粘贴ins链接：")
            url_event.wait()
        print("链接格式正确，开始检查网络连接")


        if not check_connection(URL):
            print("无法连接到Instagram，请检查你的网络连接或者URL地址，你挂梯子了嘛~")
            button_text.set("提交")
            url_event.clear()  # 重置事件
            continue
        print("网络连接Instagram页面正常，开始执行脚本...")


        # 创建文件夹
        if not os.path.exists(output_dir):
            print("未找到output_dir文件夹，开始创建...")
            os.makedirs(output_dir)
            print("创建完成")

        # 清空文件夹
        print("开始清空ins_output文件夹...")
        clear_directory(output_dir)
        print("清空完成")

        # 将img_urls定义为一个set
        img_urls = set()

        # 开启浏览器
        print("开启浏览器...")
        driver = edge_open()
        # 打开链接
        driver.get(URL)




        # 等待页面加载完成
        wait = WebDriverWait(driver, 5)
        try:
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li._acaz"))
            )
        except TimeoutException:
            print("只有一张图片或浏览器内容获取失败")
            # 获取第一张图片链接
            print("尝试获取单张图片")
            html_code = driver.page_source
            pyperclip.copy(html_code)
            soup = BeautifulSoup(html_code, 'html.parser')
            # print(soup)
            class_regex = re.compile('^_aagu .*_aato$')  # 以 _aagu 开始并以 _aato 结束的 div 元素
            li_elements = soup.find_all("div", class_=class_regex)
            # print(li_elements)
            for li_element in li_elements:
                img_elements = li_element.find_all("img")
                for img_element in img_elements:
                    img_counter += 1
                    print(f"第{img_counter}条链接：{img_element['src']}")
                    img_urls.add(img_element['src'])

        # 定位“下一步”按钮
        next_button_xpath = '//button[@aria-label="下一步"]'

        # 使用WebDriverWait与expected_conditions来周期性地检查下一步按钮是否可见且可点击
        wait = WebDriverWait(driver, 3)  # 等待最多3秒
        while True:
            try:
                # 使用Selenium提取HTML代码
                html_code = driver.page_source

                # 使用Python的pyperclip库将HTML代码复制到剪贴板
                pyperclip.copy(html_code)

                # 创建BeautifulSoup对象
                soup = BeautifulSoup(html_code, 'html.parser')

                # 找到所有符合条件的<li>元素
                li_elements = soup.find_all("li", class_="_acaz")

                # 对每个<li>元素，找到里面的所有<img>图片元素
                for li_element in li_elements:
                    img_elements = li_element.find_all("img")

                    # 打印每个<img>元素的src属性，也就是图片的URL
                    for img_element in img_elements:
                        # 每找到一张图片，计数器增加1
                        img_counter += 1
                        print(f"第{img_counter}条链接：{img_element['src']}")
                        img_urls.add(img_element['src'])

                # 点击“下一步”按钮加载更多图片
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
                next_button.click()
                time.sleep(0.5)  # 暂停0.5秒
            except:
                print("图片到顶，无法继续点击“下一步”按钮")
                break  # 跳出循环


        # 总共找到的图片数量
        print(f"一共获取了{img_counter}条链接。")

        # 退出浏览器
        driver.quit()

        # 把set变回list以便我们可以enumerate它
        print("开始整理链接")
        img_urls = list(img_urls)
        print("总共图片数量:", len(img_urls))
        print("开始下载图片")
        for i, url in enumerate(img_urls, start=1):
            print(f"正在下载图片：{i}/{len(img_urls)}")
            download_image(url, os.path.join(output_dir, f"image_{i}.jpg"))  # 下载图片

        # 清空剪贴板
        print("清空剪贴板...")
        pyperclip.copy('')
        print("图片已存放至根目录ins_output文件夹中")
        print("OVER:脚本执行完毕  :)")

        button_text.set("提交链接")  # 更新按钮的文字为 "提交"
        root.update()  # 更新GUI界面

        url_event.clear()  # 重置事件
        img_counter = 0  # 重置链接计数器

        # input("按下回车后继续...")
        # os.system('cls')


def GUI():
    global URL, input_event, root, button_text

    def submit():
        global URL
        URL = entry.get()  # 获取文本框的内容
        button_text.set("加载中...")  # 更新按钮的文字为 "加载中..."
        url_event.set()

    def on_closing():
        os._exit(0)  # 结束程序

    # 创建一个新的 tkinter 窗口
    root = ctk.CTk()

    # 设置窗口大小
    root.geometry("300x100")

    # 设置窗口图标
    icon_image.save('icon.ico', format='ICO', sizes=[(32, 32)])  # 保存为临时图标
    root.iconbitmap('icon.ico')  # 使用临时图标
    os.remove('icon.ico')  # 删除临时图标

    # 设置标题
    root.title("Ins图片提取")

    # 禁止窗口大小调整
    root.resizable(False, False)

    # 当点击窗口的关闭按钮时调用 on_closing 函数
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 创建一个标签和一个文本框
    label = ctk.CTkLabel(root, text="在此处粘贴 ins 链接:")

    entry = ctk.CTkEntry(root, width=200)

    # 创建一个StringVar对象
    button_text = tk.StringVar()
    button_text.set("提交链接")  # 初始化按钮的文字
    # 创建按钮,使用 `textvariable` 替换 `text`
    submit_button = ctk.CTkButton(root, textvariable=button_text, command=submit)

    # 创建一个打开文件夹按钮，将触发打开文件夹函数
    openFile_button = ctk.CTkButton(root, text="打开输出文件夹", command=openFile)

    # 将标签，文本框和按钮添加到窗口中，设置 padx 和 pady 属性
    root.columnconfigure(0, weight=1)
    label.grid(row=0, column=0, padx=2)  # 标题文字
    entry.grid(row=1, column=0, padx=2)  # 文本输入框
    submit_button.grid(row=2, column=0, padx=(0, 150), pady=(10, 0))  # 提交按钮
    openFile_button.grid(row=2, column=0, padx=(150, 0), pady=(10, 0))  # 打开文件夹按钮

    # 启动 tk 窗口的主循环
    root.mainloop()

#--------------------------------------------------------main---------------------------------------------------------
if __name__ == '__main__':
    # 创建GUI线程
    gui_thread = threading.Thread(target=GUI)
    # 设置守护线程，当主线程结束后，GUI线程也会结束
    gui_thread.daemon = True
    # 启动GUI线程
    gui_thread.start()
    # 主线程中运行主程序
    main()




