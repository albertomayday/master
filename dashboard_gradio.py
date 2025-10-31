

import gradio as gr
import os
import requests

# Placeholder para futura integración GoLogin/anonimato
GOLOGIN_ENABLED = False  # Cambiar a True cuando se integre GoLogin
GOLOGIN_STATUS = "No configurado"

# ========== TAB 1: ML/YOLO/COCO ==========
def download_coco():
    os.system("python scripts/download_coco_dataset.py")
    return "COCO descargado en /app/data/datasets/coco/"

def tab1_content():
    return gr.Column([
        gr.Markdown("""
        # ML Core: Ultralytics YOLOv8 & COCO
        - Entrena, infiere y visualiza modelos YOLOv8 (Ultralytics)
        - Gestiona el dataset COCO (descarga, muestra, estadísticas)
        - Integra y prueba pipelines ML
        """),
        gr.Button("Descargar COCO (train/val)", elem_id="download_coco_btn"),
        gr.Markdown("Próximamente: visualización de imágenes COCO, stats y control de modelos ML desde la UI."),
        gr.Markdown("""
        ---
        **GoLogin/Anonimato:**
        - Estado: {gologin_status}
        - (Próximamente: integración para navegación y triggers anónimos)
        """.format(gologin_status=GOLOGIN_STATUS))
    ])

# ========== TAB 2: Secrets/Config ==========
def tab2_content():
    envs = [f"**{k}**: {v if v else '[NO DEFINIDO]'}" for k, v in os.environ.items() if any(x in k.lower() for x in ["key", "token", "secret", "pass", "email"])]
    return gr.Column([
        gr.Markdown("# Gestión de Secrets y Configuración\n- Visualiza y edita variables de entorno y secrets críticos\n- Valida configuración de APIs y credenciales\n- (Próximamente: edición segura y persistente desde la UI)"),
        gr.Markdown("\n".join(envs))
    ])

# ========== TAB 3: APIs y Orquestación ==========
def health_check(api_url):
    try:
        r = requests.get(f"{api_url}/health", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def trigger_n8n_workflow(workflow_url, payload=None):
    try:
        r = requests.post(workflow_url, json=payload or {}, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def tab3_content():
    api_url = os.getenv("ML_CORE_API_URL", "http://localhost:8000")
    n8n_url = os.getenv("N8N_TRIGGER_URL", "http://localhost:5678/webhook/test")
    return gr.Column([
        gr.Markdown(f"""
        # Orquestación de APIs y Servicios
        - Lanza/parar servicios (FastAPI, ML, Device Farm, etc)
        - Consulta y prueba endpoints internos
        - Triggers de campañas Meta Ads y workflows
        - Triggers n8n Railway (anónimo con GoLogin)
        ML Core API: {api_url}
        n8n Trigger URL: {n8n_url}
        """),
        gr.Button("Probar /health ML API", elem_id="health_btn"),
        gr.JSON(label="Respuesta /health", visible=False, elem_id="health_json"),
        gr.Markdown("Trigger: Lanzar Campaña Meta Ads (Demo)"),
        gr.Textbox(label="Nombre de campaña", value="Stakas Drill Viral Test", elem_id="campaign_name"),
        gr.Textbox(label="URL/ID de video", value="stakas_drill_video.mp4", elem_id="video_url"),
        gr.Textbox(label="YouTube URL", value="https://youtube.com/watch?v=UCgohgqLVu1QPdfa64Vkrgeg", elem_id="youtube_url"),
        gr.Textbox(label="Artista", value="Stakas", elem_id="artist_name"),
        gr.Button("Lanzar campaña Meta Ads", elem_id="launch_campaign_btn"),
        gr.JSON(label="Resultado campaña", visible=False, elem_id="campaign_json"),
        gr.Markdown("---"),
        gr.Markdown("Trigger: Lanzar workflow n8n (Railway, anónimo)", elem_id="n8n_trigger_label"),
        gr.Button("Trigger n8n workflow", elem_id="n8n_trigger_btn"),
        gr.JSON(label="Respuesta n8n", visible=False, elem_id="n8n_json")
    ])

# ========== TAB 4: Monitoreo & Logs ==========
def tab4_content():
    log_path = "logs/system.log"
    logs = "No hay logs disponibles aún."
    if os.path.exists(log_path):
        with open(log_path) as f:
            logs = f.read()[-5000:]
    return gr.Column([
        gr.Markdown("# Monitoreo, Logs y Estado del Sistema\n- Visualiza logs recientes, estado de jobs y salud de servicios\n- (Próximamente: integración con Grafana, alertas y métricas en tiempo real)"),
        gr.Textbox(label="Logs", value=logs, lines=15)
    ])

# ========== TAB 5: Chat Artista (demo) ==========
chat_history = []
def chat_artist(user_input):
    chat_history.append(("Artista", user_input))
    answer = "Respuesta de prueba: el backend no está disponible."
    chat_history.append(("Asesor ML", answer))
    return chat_history

def tab5_content():
    return gr.ChatInterface(fn=chat_artist, chatbot=gr.Chatbot(label="Chat Artista (demo)"), textbox=gr.Textbox(label="¿En qué puedo ayudarte hoy?"))

with gr.Blocks() as demo:
    with gr.Tab("Panel ML/YOLO/COCO"):
        tab1 = tab1_content()
    with gr.Tab("Gestión de Secrets/Config"):
        tab2 = tab2_content()
    with gr.Tab("APIs y Orquestación"):
        tab3 = tab3_content()
    with gr.Tab("Monitoreo & Logs"):
        tab4 = tab4_content()
    with gr.Tab("Chat Artista (demo)"):
        tab5 = tab5_content()

    # --- Lógica de callbacks para triggers HTTP ---
    def on_health_click():
        api_url = os.getenv("ML_CORE_API_URL", "http://localhost:8000")
        return health_check(api_url)

    def on_launch_campaign(campaign_name, video_url, youtube_url, artist_name):
        api_url = os.getenv("ML_CORE_API_URL", "http://localhost:8000")
        try:
            r = requests.post(f"{api_url}/launch_campaign", json={
                "campaign_name": campaign_name,
                "video_url": video_url,
                "youtube_url": youtube_url,
                "artist_name": artist_name
            }, timeout=10)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def on_n8n_trigger():
        n8n_url = os.getenv("N8N_TRIGGER_URL", "http://localhost:5678/webhook/test")
        return trigger_n8n_workflow(n8n_url)

    demo.get_component("health_btn").click(
        fn=on_health_click,
        outputs=demo.get_component("health_json")
    )
    demo.get_component("launch_campaign_btn").click(
        fn=on_launch_campaign,
        inputs=[demo.get_component("campaign_name"), demo.get_component("video_url"), demo.get_component("youtube_url"), demo.get_component("artist_name")],
        outputs=demo.get_component("campaign_json")
    )
    demo.get_component("n8n_trigger_btn").click(
        fn=on_n8n_trigger,
        outputs=demo.get_component("n8n_json")
    )

demo.launch()
