import tkinter as tk
import analysis

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("News Sentiment Analysis")
        self.configure(bg="#2190ea")

        self.geometry("400x200")
        self.resizable(False, False)

        self.set_up_ui()

    def set_up_ui(self):
        self.label = tk.Label(self, text= "Welcome to News Sentiment Analysis App", font=("Arial", 14))
        self.label.pack(pady=20)
        self.label.configure(bg="#2190ea")

        self.search_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.search_var, font=("Arial", 14))
        self.entry.pack(pady=10, fill="x", padx=10)
        self.search_button = tk.Button(self, text="Search" , command=self.search)
        self.search_button.pack(pady=10)

    
    def search(self):
        keyword = self.search_var.get()
        analysis.main(keyword)




if __name__ == "__main__":
    app = App()
    app.mainloop()