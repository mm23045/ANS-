import customtkinter as ctk

class AppIntegracion(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Integración Numérica")
        self.geometry("600x450")
        ctk.set_appearance_mode("dark") # Se va a ver de toque en tu Debian

        # Título
        self.label = ctk.CTkLabel(self, text="Analisis Numérico - Integración", font=("Arial", 20))
        self.label.pack(pady=20)

        # Campo para la Función
        self.entry_f = ctk.CTkEntry(self, placeholder_text="Ingrese f(x) ej: x**2 + sin(x)")
        self.entry_f.pack(pady=10, padx=20, fill="x")

        # Límites a y b
        self.entry_a = ctk.CTkEntry(self, placeholder_text="Límite inferior (a)")
        self.entry_a.pack(pady=5)
        self.entry_b = ctk.CTkEntry(self, placeholder_text="Límite superior (b)")
        self.entry_b.pack(pady=5)

        # Botón de calcular
        self.btn_calcular = ctk.CTkButton(self, text="Calcular Integral", command=self.calcular)
        self.btn_calcular.pack(pady=20)

        # Resultado
        self.lbl_resultado = ctk.CTkLabel(self, text="Resultado: -", font=("Arial", 16))
        self.lbl_resultado.pack(pady=10)

    def calcular(self):
        # Aquí llamarás a tus funciones de metodos/avanzados.py
        print("Calculando...")

if __name__ == "__main__":
    app = AppIntegracion()
    app.mainloop()