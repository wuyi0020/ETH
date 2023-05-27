import tkinter as tk
from threading import Thread
import threading
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_subprice(driver):
    # 創建一個事件對象
    event = threading.Event()
    p=0
    def get_subprice_thread():
        nonlocal p
        
        try:
            sub_price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "subPrice"))
            )
            p = float(sub_price_element.text.strip().replace(",", "").replace("$", ""))
            print(p)
        except Exception as e:
            print(f"Failed to fetch Sub Price: {e}")
            p = None

        # 設置事件對象狀態為已完成
        event.set()

    getsubprice_thread = Thread(target=get_subprice_thread)
    getsubprice_thread.start()

    # 等待事件對象被設置為已完成，最多等待 10 秒鐘
    event.wait(10)
    return p







# 設定ChromeDriver的路徑
chrome_driver_path = "./chromedriver"

# 設定Chrome瀏覽器的選項
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

service = ChromeService(chrome_driver_path)
service.creation_flags = CREATE_NO_WINDOW

# 創建一個Chrome瀏覽器實例，並啟用無頭模式
driver = webdriver.Chrome(service=service,executable_path=chrome_driver_path, options=chrome_options)
url = "https://www.binance.com/zh-TC/trade/ETH_USDT?theme=dark&type=spot"
driver.get(url)

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x200")
        self.master.configure(bg='black')
        self.master.title("ETH最新價格")
        self.master.wm_attributes('-topmost', False)
        self.last_price = None
        self.top = False


        self.price_label = tk.Label(self.master, text="", font=('Arial', 50), bg='black', fg='red', bd=0)
        self.update_button = tk.Button(self.master, text="更新", command=self.update_price)
        self.entry = tk.Entry(self.master , font=('Arial', 50), bg='lightgray', fg='black', bd=0 ,width=8,justify='center')
        self.TOP_button = tk.Button(self.master, text="TOP", font=('Arial',20),bg='orange', fg='white', bd=0, highlightthickness=0,command=self.top_app)


        self.price_label.place(relx=0.5, rely=0.2, anchor="n")
        self.update_button.place(relx=0.5, rely=0, anchor="n")
        self.entry.place(relx=0.5, rely=1, anchor="s")
        self.TOP_button.place(relx=1, y=0,anchor="ne")
        u = Thread(target=self.update_price_loop, daemon=True)
        u.start()
    
    def restart_driver(self):
        global driver
        driver.quit()
        driver = webdriver.Chrome(service=service, executable_path=chrome_driver_path, options=chrome_options)
        driver.get(url)

    def top_app(self):
        self.top = not self.top
        print(self.top)
        color = "blue" if self.top else "orange"
        self.TOP_button.config(bg=color)
        self.master.wm_attributes('-topmost', self.top)

    def update_price(self):
        t = Thread(target=self.fetch_price, daemon=True)
        t.start()

    def fetch_price(self):
        def fetch_price_thread():
            try:
                sub_price = get_subprice(driver)
                if sub_price:
                    self.price_label.config(text=sub_price)
                    color = "red" if self.last_price is None or sub_price > self.last_price else "green"
                    self.price_label.config(text=f"${sub_price:.2f}", fg=color)
                else:
                    self.price_label.config(text="Failed to fetch Sub Price")
            except Exception as e:
                print(f"Error fetching price: {e}")
                self.restart_driver()
                fetch_price_thread()
        fetch_thread = Thread(target=fetch_price_thread, daemon=True)
        fetch_thread.start()

    def update_price_loop(self):
        def update_price_thread():
            try:
                price = get_subprice(driver)
                self.price_label.config(text=price)
                color = "red" if self.last_price is None or price > self.last_price else "green"
                self.price_label.config(text=f"${price:.2f}", fg=color)
                self.last_price = price
                self.master.after(1000, update_price_thread)
            except Exception as e:
                print(f"Error updating price: {e}")
                self.restart_driver()
                update_price_thread()
        update_thread = Thread(target=update_price_thread, daemon=True)
        update_thread.start()

        
    def on_closing(self):
        driver.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    # 添加一個函數來處理窗口關閉事件
    def on_closing():
        driver.quit()
        root.destroy()

    # 將窗口關閉事件與上面的函數綁定
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

    # 程序結束後退出 driver
   
