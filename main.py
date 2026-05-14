import streamlit as st  

st.set_page_config(
    page_title="Integración númerica",
    page_icon="🧮",
    layout="centered",
)

st.title("Integración numérica")
st.write("App para calcular integrales númericas con varios metodos diferentes")
st.markdown("---")

st.subheader("Datos para la integral")
funcion_texto = st.text_input("Ingrese la función f(x) a integrar (en términos de x):", "x**2")
col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Límite inferior (a):")
with col2:
    b = st.number_input("Límite superior (b):")
    
st.markdown("---")

st.subheader("Seleccione el método de integración")
metodo = st.radio("Escoge un método:", ("Romberg",  "Cuadratura de gauss"), horizontal=True)

st.markdown("Ingrese los parametros necesarios para el método seleccionado:")
if metodo == "Cuadratura de gauss":
    n = st.number_input("Número de puntos (n):", min_value=2, max_value=6, value=2, step=1)
    st.info("💡La cuadratura de Gauss con n puntos tiene una precisión de orden 2n-1.")

else:
    tolerancia = st.number_input("Tolerancia:")
    st.info("💡La Integración de Romberg usa extrapolación sobre la regla del trapecio .")