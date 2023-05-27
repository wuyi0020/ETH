import tkinter as tk
import requests

def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data.get("ethereum", {}).get("usd", "N/A")

class App:
    def __init__(self, master):
        self.master = master

        self.master.geometry("300x200")    # 設置視窗大小
        self.master.configure(bg='black') # 設置視窗背景色
        self.master.wm_attributes('-topmost', False)

        self.master.title("ETH最新價格")
        self.last_price = None
        self.top = False
        self.label = tk.Label(self.master, text="ETH價格：")

         # 添加關閉按鈕
        self.close_button = tk.Button(
            self.master, text="x", font=('Arial', 20),
            bg='red', fg='white', bd=0, highlightthickness=0,
            command=self.close_app
        )
        root.update()
        width = self.master.winfo_width()-22
        height = self.master.winfo_height()
        

        self.TOP_button = tk.Button(
            self.master, text="TOP", font=('Arial',20),
            bg='orange', fg='white', bd=0, highlightthickness=0,
            command=self.top_app
        )
        root.update()




        # 綁定鼠標事件
        self.master.bind("<ButtonPress-1>", self.start_move)
        self.master.bind("<ButtonRelease-1>", self.stop_move)
        self.master.bind("<B1-Motion>", self.on_move)

        self.master_x = 0
        self.master_y = 0
        
        self.price_label = tk.Label(self.master, text=get_eth_price(),font=('Arial', 50),bg='black', fg='white', bd=0)

        self.update_button = tk.Button(self.master, text="更新", command=self.update_price)

        self.update_price_loop()

        self.entry = tk.Entry(self.master, font=('Arial', 32),width=6)
        root.update()

        self.update_button.place(relx=0.5, y=20, anchor="center")
        self.label.place(relx=0.5, rely=0.4, anchor="center")
        self.price_label.place(relx=0.5, rely=0.5, anchor="center")
        self.close_button.place(relx=1, y=0,anchor="ne")
        self.TOP_button.place(relx=0.9, y=0,anchor="ne")
        self.entry.place(relx=0.5, rely=1,anchor="s")

        
    def top_app(self):
        self.top = not self.top
        print(self.top)
        color = "blue" if self.top else "orange"
        self.TOP_button.config(bg=color)
        self.master.wm_attributes('-topmost', self.top)

    def close_app(self):
        self.master.destroy()

    def start_move(self, event):
        # 記錄鼠標按下時的視窗位置
        self.master_x = event.x
        self.master_y = event.y

    def stop_move(self, event):
        # 清空視窗位置
        self.master_x = None
        self.master_y = None

    def on_move(self, event):
        # 計算視窗位置的變化量
        delta_x = event.x - self.master_x
        delta_y = event.y - self.master_y

        # 移動視窗
        x = self.master.winfo_x() + delta_x
        y = self.master.winfo_y() + delta_y
        self.master.geometry(f"+{x}+{y}")
    
    def update_price(self):
        self.price_label.config(text=get_eth_price())

    def update_price_loop(self):
        price = get_eth_price()
        self.price_label.config(text=price)
        color = "red" if self.last_price is None or price > self.last_price else "green"
        self.price_label.config(text=f"${price:.2f}", fg=color)
        self.last_price = price
        self.master.after(10000, self.update_price_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
