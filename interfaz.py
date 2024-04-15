import tkinter as tk
from tkinter import ttk
import analizador
import sys

class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert('end', str)
        self.widget.see('end')
        self.widget.configure(state='disabled')

    def flush(self):
        pass


def check_code():
    # Limpia las tablas de tokens y errores antes de una nueva ejecución
    for item in token_table.get_children():
        token_table.delete(item)
    for item in error_table.get_children():
        error_table.delete(item)

    code = txt.get("1.0", tk.END).strip()
    if not code:
        result_label.config(text="No hay código para verificar.")
        return  

    # Realiza el análisis y obtiene los errores y tokens
    errores, tokens = analizador.analizar(code)  
    
    # Muestra los errores y tokens en la interfaz gráfica
    for error in errores:
        error_table.insert('', 'end', values=(error,))
    for token_type, token_value in tokens:
        token_table.insert('', 'end', values=(token_type, token_value))
    
    if not errores:
        result_label.config(text="La sintaxis es correcta.")
    else:
        result_label.config(text="Se encontraron errores de sintaxis.")



root = tk.Tk()
root.title("Analizador Léxico y Sintáctico")

# Definir el tamaño mínimo de la ventana para asegurar que todo se muestre adecuadamente
root.minsize(600, 550)
codigo = '''numero => int(99)'''
# Configuración del área de texto para ingresar código
txt = tk.Text(root, width=50, height=15)
txt.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
txt.insert(tk.END, codigo)

# Configuración de la consola de salida para mostrar los resultados de los análisis semánticos
output_console = tk.Text(root, state='disabled', width=50, height=15)
output_console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)

# Redirigir stdout
sys.stdout = TextRedirector(output_console)

# Frame para tokens y errores
info_frame = tk.Frame(root)
info_frame.pack(fill=tk.BOTH, expand=True)

# Configuración del área para mostrar los tokens identificados
token_frame = ttk.LabelFrame(info_frame, text="Tokens", padding=10)
token_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

token_table = ttk.Treeview(token_frame, columns=('Type', 'Value'), show='headings')
token_table.heading('Type', text='Token')
token_table.heading('Value', text='Valor')
token_table.pack(fill=tk.BOTH, expand=True)

# Configuración del área para mostrar los errores sintácticos
error_frame = ttk.LabelFrame(info_frame, text="Errores de Sintaxis", padding=10)
error_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

error_table = ttk.Treeview(error_frame, columns=('Error',), show='headings')
error_table.heading('Error', text='Mensaje de Error')
error_table.pack(fill=tk.BOTH, expand=True)

# Botón para iniciar el análisis
btn = tk.Button(root, text="Analizar", command=check_code)
btn.pack(pady=5)

# Etiqueta para mostrar el resultado del análisis
result_label = tk.Label(root, text="", fg="blue")
result_label.pack()

root.mainloop()