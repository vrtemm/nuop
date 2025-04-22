import tkinter as tk
from tkinter import messagebox, filedialog
from diagnostics import diagnose_aircraft

def diagnose():
    try:
        fuel_level = float(entry_fuel.get())
        fuel_consumption = float(entry_consumption.get())
        result_text, color = diagnose_aircraft(fuel_level, fuel_consumption)
        output.delete("1.0", tk.END)
        output.insert(tk.END, result_text + "\n", color)
    except ValueError:
        messagebox.showerror("Помилка", "Введіть правильні числові значення у всі поля!")

def clear():
    entry_fuel.delete(0, tk.END)
    entry_consumption.delete(0, tk.END)
    output.delete("1.0", tk.END)

def save_report():
    file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file:
        with open(file, "w") as f:
            f.write(output.get("1.0", tk.END))

def restart():
    clear()

root = tk.Tk()
root.title("Оцінка запасу пального літака")

tk.Label(root, text="Рівень пального (%):").pack()
entry_fuel = tk.Entry(root)
entry_fuel.pack()

tk.Label(root, text="Витрати пального (л/год):").pack()
entry_consumption = tk.Entry(root)
entry_consumption.pack()

tk.Button(root, text="Запустити діагностику", command=diagnose).pack(pady=5)
tk.Button(root, text="Очистити дані", command=clear).pack(pady=5)
tk.Button(root, text="Зберегти звіт", command=save_report).pack(pady=5)
tk.Button(root, text="Перезапустити діагностику", command=restart).pack(pady=5)

output = tk.Text(root, height=10, width=60)
output.pack()

output.tag_config("red", foreground="red")
output.tag_config("green", foreground="green")

root.mainloop()