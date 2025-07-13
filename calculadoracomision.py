import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk 
import os 
import sys 

# --- CONFIGURACIÓN INICIAL DE CUSTOMTKINTER ---
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("dark-blue") 

# --- FUNCIÓN DE CÁLCULO ---
def calcular_porcentaje():
    try:
        valor_total = float(entrada_valor_total.get())
        porcentaje_a_aplicar = float(entrada_porcentaje.get())

        if porcentaje_a_aplicar < 0:
            messagebox.showwarning("Advertencia", "El porcentaje no puede ser negativo.", parent=app)
            return
        if porcentaje_a_aplicar > 100 and valor_total > 0:
            messagebox.showwarning("Advertencia", "Aplicar un porcentaje mayor al 100% puede dar resultados inesperados si esperas una resta.", parent=app)

        valor_a_restar = valor_total * (porcentaje_a_aplicar / 100)
        valor_final = valor_total - valor_a_restar

        # Formatear el texto del resultado con más precisión si es necesario
        # Usamos f-string y limitamos a 2 decimales para divisas
        label_resultado.configure(text=f"Ecuación: ${valor_total:.2f} * ({porcentaje_a_aplicar:.2f} / 100)\n"
                                       f"Valor a Restar: ${valor_a_restar:.2f}\n"
                                       f"Valor Final: ${valor_final:.2f}")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.", parent=app)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}", parent=app)

# --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
app = ctk.CTk()
app.title("Calculadora de Comision y Porcentaje")
app.resizable(False, False)

window_width = 400
window_height = 650 
app.geometry(f"{window_width}x{window_height}")

# Centrar ventana en la pantalla
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_pos = (screen_width // 2) - (window_width // 2)
y_pos = (screen_height // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# --- RUTA BASE DE LAS IMÁGENES ---
# Determina la ruta base de las imágenes de forma dinámica
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    image_base_path = sys._MEIPASS
else:
    image_base_path = os.path.dirname(os.path.abspath(__file__))

# Asegúrate de que favicon.ico y porcentaje.png estén en la misma carpeta que el script Python.

# --- FAVICON (ICO) ---
try:
    # MODIFICADO: Cambiada la extensión del favicon a .ico
    favicon_path = os.path.join(image_base_path, "favicon.ico") 
    pil_favicon = Image.open(favicon_path)
    desired_favicon_size = 32 
    pil_favicon = pil_favicon.resize((desired_favicon_size, desired_favicon_size), Image.LANCZOS)
    ctk_favicon = ImageTk.PhotoImage(pil_favicon)
    app.wm_iconphoto(True, ctk_favicon)
    app.icon_photo_reference = ctk_favicon 
except Exception as e:
    print(f"Error al cargar el favicon '{favicon_path}': {e}. "
          f"Asegúrate de que la ruta sea correcta y el archivo exista y sea un ICO válido (ej. 32x32).")


# --- FUENTE POPPINS ---
FONT_FAMILY = "Poppins"
FONT_SIZE_TITLE = 20
FONT_SIZE_LABEL = 14
FONT_SIZE_BUTTON = 14
FONT_SIZE_RESULT = 14

title_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_TITLE, weight="bold")
label_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_LABEL)
button_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_BUTTON, weight="bold")
result_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_RESULT)


# --- FRAME PRINCIPAL ---
main_frame = ctk.CTkFrame(app, corner_radius=10)
main_frame.pack(pady=(40, 40), padx=20, fill="both", expand=True) 

# --- IMAGEN PRINCIPAL (porcentaje.png) ---
try:
    # Usar la ruta base dinámica para la imagen principal
    image_path = os.path.join(image_base_path, "porcentaje.png")
    pil_image = Image.open(image_path)
    desired_width = 120
    desired_height = 120
    original_width, original_height = pil_image.size
    ratio = min(desired_width / original_width, desired_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    ctk_image = ImageTk.PhotoImage(pil_image)

    image_label = ctk.CTkLabel(main_frame, image=ctk_image, text="")
    image_label.pack(pady=(40, 20)) 
except Exception as e:
    print(f"Error al cargar la imagen principal '{image_path}': {e}. "
          f"Asegúrate de que la ruta sea correcta y el archivo exista y sea un PNG válido.")
    ctk.CTkLabel(main_frame, text="Calculadora de Porcentaje", font=title_font).pack(pady=(40, 20))


# --- CAMPOS DE ENTRADA ---
ctk.CTkLabel(main_frame, text="Valor Total:", font=label_font).pack(pady=(5, 0))
entrada_valor_total = ctk.CTkEntry(main_frame, width=200, height=30, placeholder_text="Ej: 100", font=label_font)
entrada_valor_total.pack(pady=5)
entrada_valor_total.insert(0, "100")

ctk.CTkLabel(main_frame, text="Porcentaje a Aplicar (%):", font=label_font).pack(pady=(10, 0))
entrada_porcentaje = ctk.CTkEntry(main_frame, width=200, height=30, placeholder_text="Ej: 10", font=label_font)
entrada_porcentaje.pack(pady=15)
entrada_porcentaje.insert(0, "20") 

# --- BOTÓN CALCULAR ---
PINK_COLOR = "#FF69B4"
HOVER_PINK_COLOR = "#DB55A0"

boton_calcular = ctk.CTkButton(main_frame, text="Calcular", command=calcular_porcentaje,
                               font=button_font, height=40, corner_radius=8,
                               fg_color=PINK_COLOR,
                               hover_color=HOVER_PINK_COLOR,
                               text_color="#FFFFFF"
                              )
boton_calcular.pack(pady=5)

# --- ETIQUETA DE RESULTADO ---
label_resultado = ctk.CTkLabel(main_frame, text="", font=result_font, justify="left")
label_resultado.pack(pady=(55, 55), padx=10, fill="x") 

# --- INICIAR APLICACIÓN ---
app.mainloop()

# Solución alternativa para el favicon en Windows (Tkinter)
# Algunos sistemas requieren el método 'iconbitmap' para mostrar el favicon correctamente.
try:
    app.iconbitmap(os.path.join(image_base_path, "favicon.ico"))
except Exception as e:
    print(f"iconbitmap fallback error: {e}")