"""
🎉 Cumpleaños Sorpresa - Coordinador de Aportes
Aplicación Streamlit con backend Supabase.
Archivo único: app.py
"""

import streamlit as st
from supabase import create_client, Client
import time
import random
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# CONFIGURACIÓN Y CONEXIÓN
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="🎂 Cumple Luz",
    page_icon="🎉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ADMIN_PASSWORD = "l4luzesco0l"


@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = get_supabase()


# ─────────────────────────────────────────────
# ESTILOS GLOBALES
# ─────────────────────────────────────────────

def inject_styles():
    st.markdown("""
    <style>
    /* ── Fuentes y base ── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fondo suave festivo */
    .stApp {
        background: linear-gradient(160deg, #fef9f0 0%, #fff5fb 100%);
        min-height: 100vh;
    }

    /* Header transparente y visible; ocultar solo menu y footer */
    #MainMenu, footer { visibility: hidden; }
    header { background: transparent !important; }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 2.2rem 1rem 1.2rem;
    }
    .hero-emoji {
        font-size: 3.8rem;
        line-height: 1;
        margin-bottom: 0.4rem;
        display: block;
    }
    .hero-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #2d1b4e;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 0.95rem;
        color: #7c6fa0;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* ── Tarjeta de ítem — st.container(border=True) ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1.5px solid #ede6ff !important;
        box-shadow: 0 2px 8px rgba(100, 60, 180, 0.07) !important;
        background: #ffffff !important;
        margin-bottom: 0.6rem !important;
        transition: box-shadow 0.2s !important;
        height: 100% !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 16px rgba(100, 60, 180, 0.13) !important;
    }

    /* Centrado vertical de todas las columnas dentro de la tarjeta */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div:first-child {
        justify-content: flex-start !important;
    }

    /* Number input en tarjeta */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInput"] {
        margin: 0 auto !important;
        width: 90% !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInput"] input {
        background: #f3eeff !important;
        border: 1.5px solid #ddd6fe !important;
        border-radius: 10px !important;
        color: #6d28d9 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-align: center !important;
        height: 42px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInput"] input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    }
    /* Botones nativos del number_input: estilo circular morado */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInputStepDown"],
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInputStepUp"] {
        border-radius: 50% !important;
        background: #f3eeff !important;
        border: 1.5px solid #ddd6fe !important;
        color: #6d28d9 !important;
        font-weight: 700 !important;
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInputStepDown"]:hover,
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInputStepUp"]:hover {
        background: #ede0ff !important;
        border-color: #a78bfa !important;
    }

    .item-name {
        font-weight: 700;
        font-size: 1.05rem;
        color: #2d1b4e;
    }
    .item-status {
        font-size: 0.82rem;
        color: #7c6fa0;
        margin-top: 1px;
    }
    .item-done {
        font-size: 0.82rem;
        color: #22c55e;
        font-weight: 600;
    }

    /* ── Botones generales ── */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        min-height: 44px !important;
        min-width: 44px !important;
        border: none !important;
        transition: transform 0.1s, box-shadow 0.1s !important;
    }
    .stButton > button:active {
        transform: scale(0.95) !important;
    }

    /* Botón confirmar */
    .confirm-btn > button {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%) !important;
        color: white !important;
        width: 100% !important;
        border-radius: 16px !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        padding: 0.85rem !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35) !important;
        letter-spacing: 0.2px !important;
        min-height: 56px !important;
    }
    .confirm-btn > button:hover {
        box-shadow: 0 6px 28px rgba(124, 58, 237, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Alerta de reingreso ── */
    .reingreso-alert {
        background: linear-gradient(135deg, #fefce8, #fef9c3);
        border: 1.5px solid #fde047;
        border-radius: 16px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.2rem;
    }
    .reingreso-alert b { color: #78350f; }
    .reingreso-alert p { color: #92400e; margin: 0; font-size: 0.93rem; }

    /* ── Sección extras ── */
    .extras-box {
        background: linear-gradient(135deg, #fdf4ff, #fce7f3);
        border: 1.5px dashed #e879f9;
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        margin: 1.5rem 0 1rem;
    }
    .extras-title {
        font-weight: 700;
        color: #86198f;
        font-size: 1rem;
        margin-bottom: 0.2rem;
    }
    .extras-subtitle {
        color: #a21caf;
        font-size: 0.83rem;
    }

    /* ── Divider ── */
    .divider {
        border: none;
        border-top: 1.5px solid #f0e8ff;
        margin: 1.4rem 0;
    }

    /* ── Admin badge ── */
    .admin-badge {
        display: inline-block;
        background: #2d1b4e;
        color: #e9d5ff;
        border-radius: 8px;
        padding: 2px 12px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }

    /* ── Progress section ── */
    .progress-label {
        font-weight: 600;
        color: #2d1b4e;
        font-size: 0.95rem;
    }
    .progress-sub {
        font-size: 0.8rem;
        color: #7c6fa0;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #e9d5ff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
    }

    /* Streamlit metric */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
        padding: 0.8rem;
        border: 1.5px solid #f0e8ff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #2d1b4e !important;
    }
    [data-testid="stSidebar"] * {
        color: #e9d5ff !important;
    }
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #3d2a6e !important;
        border-color: #6d28d9 !important;
        color: white !important;
    }

    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1.5px solid #86efac;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
    }
    .success-box h3 { color: #15803d; margin: 0; font-size: 1.2rem; }
    .success-box p  { color: #166534; margin: 0.4rem 0 0; font-size: 0.9rem; }

    /* Mobile tweaks */
    @media (max-width: 480px) {
        .hero-title  { font-size: 1.45rem; }
        .hero-emoji  { font-size: 3rem; }
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS DE BASE DE DATOS
# ─────────────────────────────────────────────

@st.cache_data(ttl=15)
def fetch_progreso():
    """Lee la vista vista_progreso_items (caché de 15 s)."""
    res = supabase.table("vista_progreso_items").select("*").order("id").execute()
    return res.data or []


def fetch_aportes_invitado(nombre: str):
    """Aportes actuales de un invitado específico."""
    res = (
        supabase.table("aportes")
        .select("item_id, cantidad, items(nombre, emoji)")
        .eq("nombre_invitado", nombre)
        .execute()
    )
    return res.data or []


def fetch_todos_aportes():
    res = (
        supabase.table("aportes")
        .select("nombre_invitado, cantidad, items(nombre, emoji, unidad)")
        .order("nombre_invitado")
        .execute()
    )
    return res.data or []


def fetch_extras():
    res = supabase.table("extras").select("*").order("id", desc=True).execute()
    return res.data or []


def upsert_aporte(nombre: str, item_id: int, cantidad: int):
    if cantidad <= 0:
        supabase.table("aportes").delete().eq("nombre_invitado", nombre).eq("item_id", item_id).execute()
    else:
        supabase.table("aportes").upsert(
            {"nombre_invitado": nombre, "item_id": item_id, "cantidad": cantidad},
            on_conflict="nombre_invitado,item_id",
        ).execute()


def insertar_item(nombre: str, cantidad_meta: int, emoji: str, unidad: str = ""):
    supabase.table("items").insert(
        {"nombre": nombre, "cantidad_meta": cantidad_meta, "emoji": emoji, "unidad": unidad}
    ).execute()


def insertar_extra(nombre: str, descripcion: str):
    supabase.table("extras").insert(
        {"nombre_invitado": nombre, "descripcion": descripcion}
    ).execute()


def notificar_admin_extra(nombre_invitado: str, descripcion: str):
    print(f"[NOTIF] Extra de '{nombre_invitado}': {descripcion}")


# ─────────────────────────────────────────────
# SESSION STATE — INICIALIZACIÓN
# ─────────────────────────────────────────────

def init_session():
    defaults = {
        "nombre":          None,
        "buffer":          {},
        "extra_texto":     "",
        "enviado":         False,
        "admin_ok":        False,
        "mostrar_exito":   False,
        "emojis_lluvia":   [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ─────────────────────────────────────────────
# PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────

def pantalla_bienvenida():
    st.markdown("""
    <div class="hero">
        <span class="hero-emoji">🎂</span>
        <h1 class="hero-title">¡Es el cumple de Luz!</h1>
        <p class="hero-sub">La sorpresa más rica necesita tu ayuda 🥳</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    with st.container():
        st.markdown("**¿Cómo te llamas?**")
        nombre_input = st.text_input(
            "Nombre",
            placeholder="Ej: Juan Pérez (Nombre y Apellido)",
            label_visibility="collapsed",
            key="input_nombre",
        )

        col_esp, col_btn = st.columns([2, 1])
        with col_btn:
            st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
            entrar = st.button("Entrar 🎉", use_container_width=True, type="primary")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
        <a href="?admin=1" target="_self"
           style="font-size:0.75rem; color:#c4b5d4; text-decoration:none;
                  letter-spacing:0.5px; opacity:0.6;">
            ⚙️ Admin
        </a>
    </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("admin") == "1":
        st.markdown("""
        <script>
        const btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
        if (btn) btn.click();
        </script>
        """, unsafe_allow_html=True)
        st.info("👈 Ingresa tu contraseña en el panel lateral para acceder.")

    if entrar:
        nombre = nombre_input.strip()
        if not nombre:
            st.warning("¡Escribe tu nombre para continuar! 😊")
            return
        if len(nombre.split()) < 2:
            st.warning("¡Por favor incluye tu apellido para no confundirte con otro invitado! 😊")
            return

        aportes_prev = fetch_aportes_invitado(nombre)
        st.session_state["nombre"] = nombre

        if aportes_prev:
            st.session_state["buffer"] = {
                a["item_id"]: a["cantidad"] for a in aportes_prev
            }
            lista = ", ".join(
                f"{a['items']['emoji']} {a['items']['nombre']} ×{a['cantidad']}"
                for a in aportes_prev
            )
            st.session_state["reingreso_msg"] = (nombre, lista)
        else:
            st.session_state["buffer"] = {}
            st.session_state.pop("reingreso_msg", None)

        st.rerun()


# ─────────────────────────────────────────────
# ANIMACIÓN DE CLIC
# ─────────────────────────────────────────────

def inyectar_animacion_clic():
    st.html("""
    <script>
    try {
        const doc = window.parent.document;
        if (!doc.getElementById('animacion-clic-luz')) {
            doc.addEventListener('click', function(e) {
                const btn = e.target.closest('button');
                if (!btn) return;
                const emojis = ['✨', '🎉', '💖', '🥳', '🎈'];
                const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                const el = doc.createElement('div');
                el.style.cssText = `
                    position:fixed; pointer-events:none; z-index:99999;
                    font-size:2.2rem; left:${e.clientX}px; top:${e.clientY}px;
                    transition: all 0.6s cubic-bezier(0.25,1,0.5,1);
                    transform:translate(-50%,-50%) scale(0.5); opacity:1;
                `;
                el.innerText = emoji;
                doc.body.appendChild(el);
                void el.offsetWidth;
                el.style.transform = 'translate(-50%,-120px) scale(1.5)';
                el.style.opacity = '0';
                setTimeout(() => el.remove(), 650);
            });
            const flag = doc.createElement('div');
            flag.id = 'animacion-clic-luz';
            doc.body.appendChild(flag);
        }
    } catch(e) {}
    </script>
    """)


# ─────────────────────────────────────────────
# VISTA DE INVITADOS
# ─────────────────────────────────────────────

def vista_invitados():
    nombre = st.session_state["nombre"]

    st.markdown(f"""
    <div class="hero">
        <span class="hero-emoji">🎊</span>
        <h1 class="hero-title">¡Hola, {nombre.split()[0]}!</h1>
        <p class="hero-sub">Elige qué vas a traer para la completada 🍻</p>
    </div>
    """, unsafe_allow_html=True)

    if "reingreso_msg" in st.session_state:
        n, lista = st.session_state["reingreso_msg"]
        st.markdown(f"""
        <div class="reingreso-alert">
            <b>¡Ey, ya estabas por acá! 👋</b>
            <p>Actualmente estás anotado para llevar: <b>{lista}</b>.<br>
            Puedes ajustar las cantidades y confirmar de nuevo sin problema.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    items = fetch_progreso()

    if not items:
        st.info("El administrador todavía no ha cargado la lista de ítems. ¡Vuelve pronto!")
    else:
        st.markdown("### 🛒 ¿Qué vas a traer?")
        st.caption("Ajusta la cantidad de cada ítem con los botones **＋** y **－**.")
        st.markdown("")

        inyectar_animacion_clic()

        # ── Construir HTML del grid completo ──
        # Las tarjetas son HTML puro dentro de components.html → grid real en cualquier browser.
        # Los number_input de Streamlit quedan debajo (ocultos con CSS) para manejar el estado.
        # JS dentro del componente escucha clicks en +/- y dispara eventos en los inputs reales.

        buffer = st.session_state["buffer"]

        # 1. Renderizar number_inputs de Streamlit en contenedores st.empty()
        #    st.empty() ocupa exactamente 0px de altura en el DOM — sin espacio en blanco.
        placeholders = {}
        for item in items:
            iid = item["id"]
            ph  = st.empty()
            placeholders[iid] = ph
            mi_qty = buffer.get(iid, 0)
            nuevo  = ph.number_input(
                f"qty_{iid}",
                min_value=0, max_value=999,
                value=mi_qty, step=1,
                key=f"qty_input_{iid}",
                label_visibility="collapsed",
            )
            if nuevo != mi_qty:
                st.session_state["buffer"][iid] = nuevo
                st.rerun()

        # CSS para colapsar los st.empty wrappers a cero altura real
        st.markdown("""
        <style>
        /* Colapsar todos los stNumberInput y sus wrappers a altura 0 */
        [data-testid="stNumberInput"] {
            position: absolute !important;
            opacity: 0 !important;
            pointer-events: none !important;
            height: 0 !important;
            overflow: hidden !important;
        }
        /* También el div padre que Streamlit envuelve alrededor del empty */
        [data-testid="stVerticalBlock"] > div:has([data-testid="stNumberInput"]) {
            height: 0 !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # 2. Construir el HTML puro del grid
        tarjetas_html = ""
        for item in items:
            iid      = item["id"]
            emoji_i  = item["emoji"] or "📦"
            meta     = item["cantidad_meta"]
            asignado = item["total_asignado"] or 0
            faltan   = max(0, meta - asignado)
            meta_ok  = asignado >= meta
            unidad_i = item.get("unidad") or ""
            ud       = f" {unidad_i}" if unidad_i else ""
            mi_qty   = buffer.get(iid, 0)

            if meta_ok and mi_qty == 0:
                estado_html   = '<div class="estado done">✅ ¡Meta cumplida!</div>'
                disabled_plus = "disabled"
            else:
                estado_html   = f'<div class="estado">{faltan}{ud} disponibles</div>'
                disabled_plus = ""

            disabled_minus = "disabled" if mi_qty <= 0 else ""

            tarjetas_html += f"""
            <div class="card" data-iid="{iid}">
                <div class="card-emoji">{emoji_i}</div>
                <div class="card-nombre">{item['nombre']}</div>
                {estado_html}
                <div class="card-controls">
                    <button class="btn-ctrl minus" data-iid="{iid}" {disabled_minus}>－</button>
                    <input class="qty-input" id="qty-{iid}" type="number"
                           value="{mi_qty}" min="0" max="999"
                           data-iid="{iid}" inputmode="numeric">
                    <button class="btn-ctrl plus" data-iid="{iid}" {disabled_plus}>＋</button>
                </div>
            </div>
            """

        import streamlit.components.v1 as components
        components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background: transparent; font-family: 'Plus Jakarta Sans', sans-serif; }}

            .grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                width: 100%;
                padding: 4px 2px;
            }}

            .card {{
                background: #ffffff;
                border: 1.5px solid #ede6ff;
                border-radius: 16px;
                box-shadow: 0 2px 8px rgba(100,60,180,0.07);
                padding: 14px 10px 12px;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 4px;
                transition: box-shadow 0.2s;
            }}
            .card:hover {{ box-shadow: 0 4px 16px rgba(100,60,180,0.13); }}

            .card-emoji  {{ font-size: 2.4rem; line-height: 1; }}
            .card-nombre {{
                font-weight: 700; font-size: 0.95rem;
                color: #2d1b4e; text-align: center;
            }}
            .estado {{
                font-size: 0.75rem; color: #7c6fa0;
                text-align: center; margin-bottom: 4px;
            }}
            .estado.done {{ color: #22c55e; font-weight: 600; }}

            .card-controls {{
                display: flex; align-items: center;
                gap: 8px; margin-top: 4px;
            }}
            .btn-ctrl {{
                width: 36px; height: 36px;
                border-radius: 50%;
                background: #f3eeff;
                border: 1.5px solid #ddd6fe;
                color: #6d28d9;
                font-size: 1.1rem; font-weight: 700;
                cursor: pointer;
                display: flex; align-items: center; justify-content: center;
                transition: background 0.15s;
                flex-shrink: 0;
                -webkit-tap-highlight-color: transparent;
            }}
            .btn-ctrl:hover:not(:disabled)  {{ background: #ede0ff; border-color: #a78bfa; }}
            .btn-ctrl:active:not(:disabled) {{ transform: scale(0.92); }}
            .btn-ctrl:disabled {{ opacity: 0.3; cursor: default; }}

            /* Input de cantidad editable */
            .qty-input {{
                width: 52px;
                height: 36px;
                text-align: center;
                font-size: 1.05rem;
                font-weight: 800;
                color: #6d28d9;
                background: #f3eeff;
                border: 1.5px solid #ddd6fe;
                border-radius: 10px;
                outline: none;
                /* Ocultar flechas nativas */
                -moz-appearance: textfield;
            }}
            .qty-input::-webkit-outer-spin-button,
            .qty-input::-webkit-inner-spin-button {{ -webkit-appearance: none; margin: 0; }}
            .qty-input:focus {{
                border-color: #7c3aed;
                box-shadow: 0 0 0 3px rgba(124,58,237,0.15);
            }}
        </style>
        </head>
        <body>
        <div class="grid">
            {tarjetas_html}
        </div>
        <script>
        // ── Sincronizar con Streamlit ──────────────────────────────
        function setStInput(iid, val) {{
            try {{
                var doc = window.parent.document;
                var inputs = doc.querySelectorAll('input[type="number"]');
                var found = null;
                inputs.forEach(function(inp) {{
                    if (inp.getAttribute('aria-label') === 'qty_' + iid) found = inp;
                }});
                if (found) {{
                    var setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value').set;
                    setter.call(found, val);
                    found.dispatchEvent(new Event('input',  {{ bubbles: true }}));
                    found.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }} catch(e) {{}}
        }}

        // Estado local sincronizado desde Python
        var qtys = {{}};
        {chr(10).join(f"        qtys[{item['id']}] = {buffer.get(item['id'], 0)};" for item in items)}

        function syncCard(iid) {{
            var card  = document.querySelector('.card[data-iid="' + iid + '"]');
            var inp   = document.getElementById('qty-' + iid);
            var plus  = card.querySelector('.plus');
            var minus = card.querySelector('.minus');
            inp.value     = qtys[iid];
            minus.disabled = qtys[iid] <= 0;
            setStInput(iid, qtys[iid]);
        }}

        // ── Botones +/- ────────────────────────────────────────────
        document.querySelectorAll('.btn-ctrl').forEach(function(btn) {{
            btn.addEventListener('click', function() {{
                var iid  = parseInt(this.getAttribute('data-iid'));
                var paso = this.classList.contains('plus') ? 1 : -1;
                qtys[iid] = Math.max(0, (qtys[iid] || 0) + paso);
                syncCard(iid);
            }});
        }});

        // ── Input editable directo ──────────────────────────────────
        document.querySelectorAll('.qty-input').forEach(function(inp) {{
            inp.addEventListener('input', function() {{
                var iid = parseInt(this.getAttribute('data-iid'));
                var val = parseInt(this.value) || 0;
                val = Math.max(0, Math.min(999, val));
                qtys[iid] = val;
                // Actualizar botones sin tocar el input (el usuario lo está editando)
                var card  = document.querySelector('.card[data-iid="' + iid + '"]');
                card.querySelector('.minus').disabled = val <= 0;
                setStInput(iid, val);
            }});
            // Al salir del campo, asegurar valor limpio
            inp.addEventListener('blur', function() {{
                var iid = parseInt(this.getAttribute('data-iid'));
                this.value = qtys[iid];
            }});
        }});
        </script>
        </body>
        </html>
        """, height=((len(items) + 1) // 2) * 185 + 20, scrolling=False)


    # ── Sección extras ──
    st.markdown("""
    <div class="extras-box">
        <div class="extras-title">💡 ¿Tienes una idea genial?</div>
        <div class="extras-subtitle">Algo que no esté en la lista y quieras traer ✨</div>
    </div>
    """, unsafe_allow_html=True)

    extra_texto = st.text_area(
        "Tu propuesta",
        placeholder="Ej: una torta de maracuyá, guirnaldas de luces, una sorpresa especial...",
        label_visibility="collapsed",
        value=st.session_state["extra_texto"],
        height=90,
        key="input_extra",
    )
    st.session_state["extra_texto"] = extra_texto

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
    confirmar = st.button(
        "🎉 Confirmar mi Aporte",
        use_container_width=True,
        type="primary",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if confirmar:
        alguna_qty = any(v > 0 for v in st.session_state["buffer"].values())
        hay_extra  = bool(st.session_state["extra_texto"].strip())

        if not alguna_qty and not hay_extra:
            st.warning("⚠️ Agrega al menos un ítem o una propuesta antes de confirmar.")
        else:
            with st.spinner("Guardando tu aporte... 🎊"):
                emojis_aportes = []
                for item in (fetch_progreso() or []):
                    iid = item["id"]
                    qty = st.session_state["buffer"].get(iid, 0)
                    if qty > 0:
                        emojis_aportes.append(item["emoji"] or "📦")

                for iid, qty in st.session_state["buffer"].items():
                    upsert_aporte(nombre, iid, qty)

                if hay_extra:
                    insertar_extra(nombre, extra_texto.strip())
                    notificar_admin_extra(nombre, extra_texto.strip())

            emojis_base = ["🎂", "🥳", "🎉", "🎈", "✨"]
            st.session_state["emojis_lluvia"] = list(set(emojis_aportes + emojis_base))
            fetch_progreso.clear()
            time.sleep(0.4)
            st.session_state["extra_texto"] = ""
            st.session_state.pop("reingreso_msg", None)
            st.session_state["mostrar_exito"] = True
            st.rerun()

    if st.session_state.get("mostrar_exito"):
        lluvia_html = """
        <style>
        .emoji-drop {
            position: fixed; top: -10vh; z-index: 999999;
            animation-name: fall; animation-timing-function: linear;
            animation-fill-mode: forwards; pointer-events: none; user-select: none;
        }
        @keyframes fall {
            0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
            80%  { opacity: 1; }
            100% { transform: translateY(115vh) rotate(360deg); opacity: 0; }
        }
        </style>
        """
        for _ in range(60):
            e     = random.choice(st.session_state["emojis_lluvia"])
            left  = random.randint(0, 100)
            dur   = random.uniform(2.5, 4.5)
            delay = random.uniform(0, 1.5)
            size  = random.randint(25, 45)
            lluvia_html += (
                f'<div class="emoji-drop" style="left:{left}vw;'
                f'animation-duration:{dur}s;animation-delay:{delay}s;'
                f'font-size:{size}px;">{e}</div>'
            )
        st.markdown(lluvia_html, unsafe_allow_html=True)
        st.markdown("""
        <div class="success-box">
            <h3>🥳 ¡Listo, estás anotado!</h3>
            <p>Gracias por hacer este cumple especial.<br>
            Puedes volver a modificar tu aporte cuando quieras.</p>
        </div>
        """, unsafe_allow_html=True)
        st.session_state["mostrar_exito"] = False

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Cambiar nombre", use_container_width=False):
        st.session_state["nombre"] = None
        st.session_state["buffer"] = {}
        st.session_state.pop("reingreso_msg", None)
        st.rerun()


# ─────────────────────────────────────────────
# VISTA DE ADMINISTRADOR
# ─────────────────────────────────────────────

def sidebar_admin():
    with st.sidebar:
        st.markdown("### 👑 Panel Admin")

        if not st.session_state["admin_ok"]:
            pw = st.text_input("Contraseña", type="password", key="admin_pw")
            if st.button("Acceder", use_container_width=True):
                if pw == ADMIN_PASSWORD:
                    st.session_state["admin_ok"] = True
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
        else:
            st.markdown('<span class="admin-badge">ADMIN ACTIVO</span>', unsafe_allow_html=True)
            if st.button("Cerrar sesión", use_container_width=True):
                st.session_state["admin_ok"] = False
                st.rerun()


def vista_admin():
    st.markdown("""
    <div class="hero">
        <span class="hero-emoji">👑</span>
        <h1 class="hero-title">Panel de Control</h1>
        <p class="hero-sub">Estado en tiempo real de la fiesta 🎉</p>
    </div>
    """, unsafe_allow_html=True)

    tab_dashboard, tab_aportes, tab_extras, tab_agregar = st.tabs([
        "📊 Dashboard", "📋 Aportes", "💡 Extras", "➕ Nuevo ítem"
    ])

    with tab_dashboard:
        st.markdown("#### Progreso por ítem")
        items = fetch_progreso()
        if not items:
            st.info("Sin ítems aún. Agrégalos en la pestaña ➕.")
        else:
            total_meta     = sum(i["cantidad_meta"]  for i in items)
            total_asignado = sum(i["total_asignado"] for i in items)
            items_ok       = sum(1 for i in items if i["total_asignado"] >= i["cantidad_meta"])

            m1, m2, m3 = st.columns(3)
            m1.metric("Ítems en lista",   len(items))
            m2.metric("Ítems cubiertos",  f"{items_ok}/{len(items)}")
            m3.metric("Unidades totales", f"{total_asignado}/{total_meta}")
            st.markdown("<br>", unsafe_allow_html=True)

            for item in items:
                meta     = item["cantidad_meta"]
                asignado = item["total_asignado"] or 0
                pct      = min(1.0, asignado / meta) if meta > 0 else 0
                emoji_i  = item["emoji"] or "📦"
                unidad   = item.get("unidad") or ""
                ud_label = f" {unidad}" if unidad else ""

                col_l, col_r = st.columns([5, 1])
                with col_l:
                    st.markdown(
                        f'<div class="progress-label">{emoji_i} {item["nombre"]}</div>'
                        f'<div class="progress-sub">{asignado}{ud_label} de {meta}{ud_label} — {int(pct*100)}%</div>',
                        unsafe_allow_html=True,
                    )
                    st.progress(pct)
                with col_r:
                    if asignado >= meta:
                        st.markdown("<br>✅", unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f"<br><span style='color:#7c6fa0;font-size:0.85rem;'>"
                            f"Faltan {meta-asignado}{ud_label}</span>",
                            unsafe_allow_html=True,
                        )
                st.markdown("")

    with tab_aportes:
        st.markdown("#### ¿Quién lleva qué?")
        aportes = fetch_todos_aportes()
        if not aportes:
            st.info("Nadie ha confirmado aportes todavía.")
        else:
            rows = []
            for a in aportes:
                unidad_a = a["items"].get("unidad") or ""
                cant_str = f"{a['cantidad']} {unidad_a}".strip()
                rows.append({
                    "Invitado": a["nombre_invitado"],
                    "Ítem":     f"{a['items']['emoji']} {a['items']['nombre']}",
                    "Cantidad": cant_str,
                })
            import pandas as pd
            df = pd.DataFrame(rows)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Invitado": st.column_config.TextColumn("👤 Invitado"),
                    "Ítem":     st.column_config.TextColumn("🛒 Ítem"),
                    "Cantidad": st.column_config.TextColumn("🔢 Cant."),
                },
            )
            st.caption(f"Total de registros: {len(rows)}")

    with tab_extras:
        st.markdown("#### 💡 Propuestas de los invitados")
        extras = fetch_extras()
        if not extras:
            st.info("Nadie ha propuesto extras aún.")
        else:
            for ex in extras:
                with st.container():
                    st.markdown(f"**{ex['nombre_invitado']}** — {ex['descripcion']}")
                    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    with tab_agregar:
        st.markdown("#### ➕ Nuevo ítem para la lista")
        with st.form("form_nuevo_item", clear_on_submit=True):
            col_e, col_n = st.columns([1, 4])
            with col_e:
                emoji_nuevo = st.text_input("Emoji", value="🍕", max_chars=4)
            with col_n:
                nombre_nuevo = st.text_input("Nombre del ítem", placeholder="Ej: Empanadas")

            col_meta, col_unidad = st.columns([1, 2])
            with col_meta:
                meta_nueva = st.number_input("Cantidad meta", min_value=1, max_value=9999, value=10)
            with col_unidad:
                unidad_nueva = st.text_input(
                    "Tipo de unidad",
                    placeholder="Ej: litros, bolsas, unidades, gramos…",
                    help="Se mostrará junto a la cantidad.",
                )
            submitted = st.form_submit_button("Agregar ítem ✅", use_container_width=True)

        if submitted:
            if nombre_nuevo.strip():
                insertar_item(
                    nombre_nuevo.strip(),
                    int(meta_nueva),
                    emoji_nuevo.strip(),
                    unidad_nueva.strip(),
                )
                fetch_progreso.clear()
                st.success(f"¡Ítem '{nombre_nuevo}' agregado exitosamente! 🎊")
                st.rerun()
            else:
                st.warning("El nombre del ítem no puede estar vacío.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    inject_styles()
    init_session()
    sidebar_admin()

    if st.session_state["admin_ok"]:
        vista_admin()
        return

    if st.session_state["nombre"] is None:
        pantalla_bienvenida()
    else:
        vista_invitados()


if __name__ == "__main__":
    main()
