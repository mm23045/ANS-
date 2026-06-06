import streamlit as st
import sympy as sp
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Integración Numérica", page_icon="🧮", layout="centered")

# --- LÓGICA MATEMÁTICA ---

def preparar_funcion(texto_funcion):
    """Convierte el texto del usuario en una función matemática evaluable."""
    x = sp.Symbol('x')
    expresion = sp.sympify(texto_funcion)
    # Usamos numpy para que soporte arreglos y sea rapidísimo
    f_ejecutable = sp.lambdify(x, expresion, 'numpy')
    return f_ejecutable

def cuadratura_gauss(f, a, b, n):
    """Calcula la integral usando Cuadratura de Gauss-Legendre."""
    # np.polynomial.legendre.leggauss nos da las raíces y los pesos automáticamente
    raices, pesos = np.polynomial.legendre.leggauss(int(n))
    
    # Cambio de intervalo de [-1, 1] a [a, b]
    t = 0.5 * (raices * (b - a) + (b + a))
    
    # Evaluar la función y multiplicar por los pesos
    integral = 0.5 * (b - a) * np.sum(pesos * f(t))
    return integral

def integracion_romberg(f, a, b, tolerancia=1e-6, max_iter=10):
    """Calcula la integral usando el método de Romberg."""
    R = np.zeros((max_iter, max_iter))
    h = b - a
    
    # Primera estimación (Trapecio simple)
    R[0, 0] = 0.5 * h * (f(a) + f(b))
    
    for i in range(1, max_iter):
        h = h / 2.0
        suma = 0.0
        
        # Sumamos los nuevos puntos
        for k in range(1, 2**i, 2):
            suma += f(a + k * h)
            
        R[i, 0] = 0.5 * R[i-1, 0] + h * suma
        
        # Extrapolación de Richardson
        for j in range(1, i + 1):
            R[i, j] = R[i, j-1] + (R[i, j-1] - R[i-1, j-1]) / ((4**j) - 1)
            
        # Revisamos si ya alcanzamos la tolerancia deseada
        error_actual = abs(R[i, i] - R[i-1, i-1])
        if error_actual < tolerancia:
            return R[i, i], error_actual, i
            
    return R[max_iter-1, max_iter-1], error_actual, max_iter

# --- INTERFAZ GRÁFICA ---

st.title("🧮 Análisis Numérico - Integración")
st.markdown("---")

st.subheader("1. Configuración de la Integral")
# Nota: agregué una pequeña validación visual en el placeholder
funcion_texto = st.text_input("Ingresa la función f(x) (Usa ** para potencias):", value="x**2 + sin(x)")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Límite inferior (a):", value=0.0)
with col2:
    b = st.number_input("Límite superior (b):", value=1.0)

st.markdown("---")

st.subheader("2. Selección del Método")
metodo = st.radio(
    "¿Qué método vas a usar?",
    ("Cuadratura de Gauss", "Integración de Romberg"),
    horizontal=True
)

st.markdown("### Parámetros Específicos")
if metodo == "Cuadratura de Gauss":
    n_puntos = st.number_input("Número de Puntos (n):", min_value=2, max_value=10, value=2, step=1)
    st.info("💡 La Cuadratura de Gauss evalúa la función en puntos óptimos para máxima precisión.")
else:
    # Usamos text_input para permitir notación científica como 1e-6
    tolerancia_str = st.text_input("Tolerancia (Error máximo permitido):", value="1e-6")
    st.info("💡 Romberg refina el cálculo hasta que la diferencia entre iteraciones es menor a la tolerancia.")

st.markdown("---")

st.subheader("3. Resultados")

if st.button("Calcular Integral", type="primary", use_container_width=True):
    try:
        # Preparamos la función
        f = preparar_funcion(funcion_texto)
        
        # Verificamos que los límites tengan sentido
        if a >= b:
            st.error("El límite inferior (a) debe ser menor que el límite superior (b).")
        else:
            if metodo == "Cuadratura de Gauss":
                # Llamada al método de Gauss
                resultado = cuadratura_gauss(f, a, b, n_puntos)
                
                st.success("¡Cálculo por Cuadratura de Gauss completado!")
                st.metric(label=f"Valor Aproximado (n={n_puntos})", value=f"{resultado:.6f}")
                
            elif metodo == "Integración de Romberg":
                # Convertimos el texto de tolerancia a número (float)
                tol = float(tolerancia_str)
                
                # Llamada al método de Romberg
                resultado, error_final, iteraciones = integracion_romberg(f, a, b, tol)
                
                st.success("¡Cálculo por Integración de Romberg completado!")
                col_res1, col_res2, col_res3 = st.columns(3)
                
                col_res1.metric(label="Valor Aproximado", value=f"{resultado:.6f}")
                col_res2.metric(label="Error Estimado", value=f"{error_final:.2e}")
                col_res3.metric(label="Iteraciones", value=iteraciones)
                
            st.balloons()

    except Exception as e:
        st.error(f"¡Revisá la función! Hubo un error al interpretar las matemáticas: {e}")