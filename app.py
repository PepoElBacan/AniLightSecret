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
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 16px rgba(100, 60, 180, 0.13) !important;
    }

    /* Centrado vertical de todas las columnas dentro de la tarjeta */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {
        align-items: center !important;
    }
    /* Cada celda de columna: flex centrado */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* Primera columna (info): alinear a la izquierda */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] > div:first-child {
        justify-content: flex-start !important;
    }

    /* Botones +/- dentro de tarjeta: círculo morado suave */
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        min-height: 42px !important;
        min-width: 42px !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto !important;
        background: #f3eeff !important;
        color: #6d28d9 !important;
        border: 1.5px solid #ddd6fe !important;
        box-shadow: none !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
        background: #ede0ff !important;
        border-color: #a78bfa !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:disabled {
        opacity: 0.3 !important;
    }

    /* Number input editable: badge morado, sin flechas nativas */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInput"] {
        margin: 0 !important;
        width: 100% !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInput"] input {
        background: #f3eeff !important;
        border: 1.5px solid #ddd6fe !important;
        border-radius: 10px !important;
        color: #6d28d9 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-align: center !important;
        padding: 0 !important;
        height: 42px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInput"] input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    }
    /* Ocultar flechas nativas del number_input */
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInputStepDown"],
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stNumberInputStepUp"] {
        display: none !important;
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

    /* ── Botones +/- ── */
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
        .item-card   { padding: 0.85rem 0.9rem; }
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
    """
    Inserta o actualiza el aporte de un invitado para un ítem.
    Si cantidad == 0, elimina el registro para mantener la tabla limpia.
    """
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


# ─────────────────────────────────────────────────────
# SIMULACIÓN DE NOTIFICACIÓN AL ADMIN
# ─────────────────────────────────────────────────────

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
        if len(nombre.split()) < 2:
            st.warning("¡Por favor incluye tu apellido para no confundirte con otro invitado! 😊")
            return
        if not nombre:
            st.warning("¡Escribe tu nombre para continuar! 😊")
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
# VISTA DE INVITADOS
# ─────────────────────────────────────────────

def inyectar_animacion_clic():
    st.html("""
    <script>
    try {
        const doc = window.parent.document;
        if (!doc.getElementById('animacion-clic-luz')) {
            doc.addEventListener('click', function(e) {
                if (e.target.tagName === 'BUTTON' && e.target.innerText.includes('＋')) {
                    const emojis = ['✨', '🎉', '💖', '🥳', '🎈'];
                    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const el = doc.createElement('div');
                    
                    // Estilos del emoji flotante
                    el.style.position = 'fixed';
                    el.style.pointerEvents = 'none';
                    el.style.zIndex = '99999';
                    el.style.fontSize = '2.2rem';
                    el.style.left = e.clientX + 'px';
                    el.style.top = e.clientY + 'px';
                    el.style.transition = 'all 0.6s cubic-bezier(0.25, 1, 0.5, 1)';
                    el.style.transform = 'translate(-50%, -50%) scale(0.5)';
                    el.style.opacity = '1';
                    el.innerText = emoji;
                    doc.body.appendChild(el);
                    
                    // Forzar el repintado del navegador para que tome la transición
                    void el.offsetWidth;
                    
                    // Mover hacia arriba y desvanecer
                    el.style.transform = 'translate(-50%, -120px) scale(1.5)';
                    el.style.opacity = '0';
                    
                    // Limpiar el DOM
                    setTimeout(() => el.remove(), 600);
                }
            });
            const flag = doc.createElement('div');
            flag.id = 'animacion-clic-luz';
            doc.body.appendChild(flag);
        }
    } catch (err) {
        console.log("No se pudo inyectar la animación.");
    }
    </script>
    """)
    
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
        st.caption("Toca **＋** o **－** para ajustar tu aporte. Los cambios se guardan al final.")
        st.markdown("")

        buffer: dict = st.session_state["buffer"]

        # Llamamos a la animación justo antes de renderizar los ítems
        inyectar_animacion_clic()

        # Reemplaza la definición de renderizar_fila dentro de vista_invitados
        @st.fragment
        def renderizar_fila(item):
            iid = item["id"]
            nombre_i = item["nombre"]
            emoji_i = item["emoji"] or "📦"
            meta = item["cantidad_meta"]
            asignado = item["total_asignado"] or 0
            faltan = max(0, meta - asignado)
            unidad_i = item.get("unidad") or ""
            ud = f" {unidad_i}" if unidad_i else ""

            mi_qty = st.session_state["buffer"].get(iid, 0)

            with st.container(border=True):
                # Emoji grande centrado
                st.markdown(f'<div style="text-align:center; font-size:3rem; margin-bottom:0.5rem;">{emoji_i}</div>', unsafe_allow_html=True)
                # Título
                st.markdown(f'<div style="text-align:center; font-weight:700; color:#2d1b4e; font-size:1.1rem;">{nombre_i}</div>', unsafe_allow_html=True)
                # Info estado
                st.markdown(f'<div style="text-align:center; font-size:0.85rem; color:#7c6fa0; margin-bottom:1rem;">Faltan {faltan}{ud}</div>', unsafe_allow_html=True)
                
                # Input centralizado (Streamlit manejará sus propios botones +/- nativos)
                st.number_input(
                    "Cantidad", min_value=0, max_value=999, value=mi_qty, step=1,
                    key=f"qty_input_{iid}", label_visibility="collapsed",
                    on_change=lambda: st.session_state["buffer"].update({iid: st.session_state[f"qty_input_{iid}"]})
                )

        # ── Implementación de la cuadrícula de 3 columnas ──
        columnas_grid = st.columns(3)
        
        # Iteramos sobre los ítems
        for idx, item in enumerate(items):
            # Usamos el módulo (%) para distribuir en esas 3 columnas
            with columnas_grid[idx % 3]:
                renderizar_fila(item)
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
                for item in items:
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

            time.sleep(0.6)

            st.session_state["extra_texto"] = ""
            st.session_state.pop("reingreso_msg", None)
            st.session_state["mostrar_exito"] = True
            st.rerun()

    if st.session_state.get("mostrar_exito"):
        # Generar animación CSS de lluvia de emojis
        lluvia_html = """
        <style>
        .emoji-drop {
            position: fixed;
            top: -10vh;
            z-index: 999999;
            animation-name: fall;
            animation-timing-function: linear;
            animation-fill-mode: forwards;
            pointer-events: none;
            user-select: none;
        }
        @keyframes fall {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; }
            80% { opacity: 1; }
            100% { transform: translateY(115vh) rotate(360deg); opacity: 0; }
        }
        </style>
        """
        
        for _ in range(60):
            e = random.choice(st.session_state["emojis_lluvia"])
            left = random.randint(0, 100)
            dur = random.uniform(2.5, 4.5)
            delay = random.uniform(0, 1.5)
            size = random.randint(25, 45)
            lluvia_html += f'<div class="emoji-drop" style="left:{left}vw; animation-duration:{dur}s; animation-delay:{delay}s; font-size:{size}px;">{e}</div>'
        
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
            total_meta     = sum(i["cantidad_meta"]   for i in items)
            total_asignado = sum(i["total_asignado"]  for i in items)
            items_ok       = sum(1 for i in items if i["total_asignado"] >= i["cantidad_meta"])

            m1, m2, m3 = st.columns(3)
            m1.metric("Ítems en lista",    len(items))
            m2.metric("Ítems cubiertos",   f"{items_ok}/{len(items)}")
            m3.metric("Unidades totales",  f"{total_asignado}/{total_meta}")

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
                        st.markdown(f"<br><span style='color:#7c6fa0;font-size:0.85rem;'>Faltan {meta-asignado}{ud_label}</span>", unsafe_allow_html=True)

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
                    "Invitado":  a["nombre_invitado"],
                    "Ítem":      f"{a['items']['emoji']} {a['items']['nombre']}",
                    "Cantidad":  cant_str,
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
                    "Cantidad": st.column_config.NumberColumn("🔢 Cant.", format="%d"),
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
                    st.markdown(
                        f"**{ex['nombre_invitado']}** — {ex['descripcion']}"
                    )
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
                    help="Se mostrará junto a la cantidad. Puedes escribir lo que quieras.",
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
