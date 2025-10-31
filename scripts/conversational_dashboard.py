
# --- Ensure professional import style: always allow 'from scripts...' ---
import sys
import pathlib
project_root = pathlib.Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


import streamlit as st
import os
import requests

st.set_page_config(page_title="Maestro Rector - Sistema ML Artístico", layout="wide")

TABS = [
    "Panel ML/YOLO/COCO",
    "Gestión de Secrets/Config",
    "APIs y Orquestación",
    "Monitoreo & Logs",
    "Chat Artista (demo)",
]

tab1, tab2, tab3, tab4, tab5 = st.tabs(TABS)

# ========== TAB 1: ML/YOLO/COCO ==========
with tab1:
    st.header("ML Core: YOLOv8 & COCO")
    st.write("""
    - Entrena, infiere y visualiza modelos YOLOv8
    - Gestiona el dataset COCO (descarga, muestra, estadísticas)
    - Integra y prueba pipelines ML
    """)
    if st.button("Descargar COCO (train/val)"):
        os.system("python scripts/download_coco_dataset.py")
        st.success("COCO descargado en /app/data/datasets/coco/")
    st.info("Próximamente: visualización de imágenes COCO, stats y control de modelos ML desde la UI.")

# ========== TAB 2: Secrets/Config ==========
with tab2:
    st.header("Gestión de Secrets y Configuración")
    st.write("""
    - Visualiza y edita variables de entorno y secrets críticos
    - Valida configuración de APIs y credenciales
    - (Próximamente: edición segura y persistente desde la UI)
    """)
    for k, v in os.environ.items():
        if any(x in k.lower() for x in ["key", "token", "secret", "pass", "email"]):
            st.write(f"**{k}**: {v if v else '[NO DEFINIDO]'}")


# ========== TAB 3: APIs y Orquestación ==========
with tab3:
    st.header("Orquestación de APIs y Servicios")
    st.write("""
    - Lanza/parar servicios (FastAPI, ML, Device Farm, etc)
    - Consulta y prueba endpoints internos
    - Triggers de campañas Meta Ads y workflows
    """)
    api_url = os.getenv("ML_CORE_API_URL", "http://localhost:8000")
    st.write(f"ML Core API: {api_url}")
    if st.button("Probar /health ML API"):
        try:
            r = requests.get(f"{api_url}/health", timeout=5)
            st.json(r.json())
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Trigger: Lanzar Campaña Meta Ads (Demo)")
    from scripts.meta_ads_production_manager import MetaAdsProductionManager
    campaign_name = st.text_input("Nombre de campaña", "Stakas Drill Viral Test")
    video_url = st.text_input("URL/ID de video", "stakas_drill_video.mp4")
    youtube_url = st.text_input("YouTube URL", "https://youtube.com/watch?v=UCgohgqLVu1QPdfa64Vkrgeg")
    artist_name = st.text_input("Artista", "Stakas")
    if st.button("Lanzar campaña Meta Ads"):
        manager = MetaAdsProductionManager()
        result = manager.launch_complete_campaign(
            campaign_name=campaign_name,
            video_url=video_url,
            youtube_url=youtube_url,
            artist_name=artist_name
        )
        if 'error' not in result:
            st.success(f"Campaña lanzada: {result['campaign_id']}")
            st.json(result)
        else:
            st.error(f"Error: {result['error']}")

# ========== TAB 4: Monitoreo & Logs ==========
with tab4:
    st.header("Monitoreo, Logs y Estado del Sistema")
    st.write("""
    - Visualiza logs recientes, estado de jobs y salud de servicios
    - (Próximamente: integración con Grafana, alertas y métricas en tiempo real)
    """)
    log_path = "logs/system.log"
    if os.path.exists(log_path):
        with open(log_path) as f:
            st.text(f.read()[-5000:])
    else:
        st.info("No hay logs disponibles aún.")

# ========== TAB 5: Chat Artista (demo) ==========
with tab5:
    st.header("Chat Artista (demo)")
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.write("Bienvenido/a. Soy tu asesor ML para proyectos artísticos. Hazme preguntas sobre promoción, campañas, horarios, contenido, presupuesto, etc.")
    user_input = st.text_input("¿En qué puedo ayudarte hoy?", "", key="input")
    if st.button("Enviar", key="send") and user_input:
        st.session_state["history"].append(("Artista", user_input))
        answer = "Respuesta de prueba: el backend no está disponible."
        st.session_state["history"].append(("Asesor ML", answer))
    for speaker, msg in st.session_state["history"]:
        st.markdown(f"**{speaker}:** {msg}")
    st.info("Puedes pedir: recomendaciones de contenido, horarios óptimos, análisis de campañas, optimización de presupuesto, etc. El asesor responde adaptado a artistas con nivel tecnológico medio.")
