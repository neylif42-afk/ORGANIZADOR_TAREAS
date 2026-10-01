import streamlit as st
import json
import os

DB_FILE = "tareas.json"

# Cargar tareas guardadas
def cargar_tareas():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guardar tareas
def guardar_tareas(tareas):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="Mi Organizador", page_icon="📝")
st.title("📝 Organizador de Tareas")

tareas = cargar_tareas()

# Formulario para agregar tarea
with st.form("form_nueva_tarea", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        nueva_tarea = st.text_input("Nueva tarea:", placeholder="Ej. Estudiar para el examen...")
    with col2:
        prioridad = st.selectbox("Prioridad", ["Baja", "Media", "Alta"])
    
    enviado = st.form_submit_button("Agregar")
    if enviado and nueva_tarea.strip():
        tareas.append({"nombre": nueva_tarea.strip(), "prioridad": prioridad, "completada": False})
        guardar_tareas(tareas)
        st.rerun()

st.write("---")

# Lista de tareas
if not tareas:
    st.info("No tienes tareas pendientes.")
else:
    for i, t in enumerate(tareas):
        col_check, col_texto, col_prio, col_del = st.columns([0.5, 3, 1, 0.8])
        
        completada = col_check.checkbox("", value=t["completada"], key=f"check_{i}")
        if completada != t["completada"]:
            tareas[i]["completada"] = completada
            guardar_tareas(tareas)
            st.rerun()

        if t["completada"]:
            col_texto.markdown(f"~~{t['nombre']}~~")
        else:
            col_texto.write(t["nombre"])

        col_prio.caption(f"📌 {t['prioridad']}")

        if col_del.button("❌", key=f"del_{i}"):
            tareas.pop(i)
            guardar_tareas(tareas)
            st.rerun()
