"""
🎉 Cumpleaños Sorpresa - Coordinador de Aportes
Aplicación Streamlit con backend Supabase.
Archivo único: app.py
"""

import streamlit as st
from supabase import create_client, Client
import time
import random

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
# ESTILOS GLOBALES (PALETA PACHAMÁMICA Y MINIMALISTA)
# ─────────────────────────────────────────────

def inject_styles():
    st.markdown("""
    <style>
    /* ── Fuentes y base ── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Fondo suave tierra/arena */
    .stApp {
        background-color: #F9F6F0;
        min-height: 100vh;
    }

    /* Ocultar elementos nativos innecesarios */
    #MainMenu, footer { visibility: hidden; }
    header { background: transparent !important; }

    /* ── Corrección de Espacios (Ocultar stNumberInput) ── */
    [data-testid="stNumberInput"] { display: none !important; }
    [data-testid="stElementContainer"]:has([data-testid="stNumberInput"]) {
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
        border: none !important;
    }
    [data-testid="stVerticalBlock"]:has([data-testid="stNumberInput"]) {
        gap: 0 !important;
    }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    .hero-emoji {
        font-size: 3.5rem;
        line-height: 1;
        margin-bottom: 0.8rem;
        display: block;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #3E362E; /* Café muy oscuro */
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        font-size: 1rem;
        color: #7A6F62; /* Tierra suave */
        margin-top: 0.4rem;
        font-weight: 500;
    }

    /* ── Botones generales ── */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        min-height: 48px !important;
        border: 1px solid #D6CFC4 !important;
        color: #3E362E !important;
        background: #FFFFFF !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        border-color: #401D06 !important;
        color: #401D06 !important;
    }
    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* Botón confirmar (Verde Musgo) */
    .confirm-btn > button {
        background-color: #401D06 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(92, 110, 79, 0.2) !important;
    }
    .confirm-btn > button:hover {
        background-color: #4A593F !important;
        box-shadow: 0 6px 16px rgba(92, 110, 79, 0.3) !important;
        color: white !important;
    }

    /* ── Alertas y Cajas ── */
    .reingreso-alert {
        background-color: #F4EFE6;
        border-left: 4px solid #D9A05B; /* Acento ocre */
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
    }
    .reingreso-alert b { color: #401D06; }
    .reingreso-alert p { color: #7A6F62; margin: 0; font-size: 0.95rem; margin-top: 4px;}

    .extras-box {
        background-color: #FFFFFF;
        border: 1px solid #E6E2D6;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1.5rem 0 1rem;
        text-align: center;
    }
    .extras-title {
        font-weight: 600;
        color: #8C5E45; /* Terracota */
        font-size: 1.05rem;
    }
    .extras-subtitle {
        color: #7A6F62;
        font-size: 0.85rem;
        margin-top: 4px;
    }

    .success-box {
        background-color: #EAECE6; /* Verde musgo ultra claro */
        border: 1px solid #BCC4B7;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .success-box h3 { color: #3C4A31; margin: 0; font-size: 1.2rem; }
    .success-box p  { color: #401D06; margin: 0.5rem 0 0; font-size: 0.95rem; }

    /* ── Divider ── */
    .divider {
        border: none;
        border-top: 1px solid #E6E2D6;
        margin: 1.5rem 0;
    }

    /* ── Admin badge ── */
    .admin-badge {
        display: inline-block;
        background: #3E362E;
        color: #F9F6F0;
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }

    /* Progress section */
    .progress-label { font-weight: 600; color: #3E362E; font-size: 0.95rem; }
    .progress-sub { font-size: 0.85rem; color: #7A6F62; }

    /* Inputs de Streamlit */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #D6CFC4 !important;
        color: #3E362E !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #401D06 !important;
        box-shadow: 0 0 0 2px rgba(92, 110, 79, 0.1) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #4A3F35 !important; }
    [data-testid="stSidebar"] * { color: #E6E2D6 !important; }
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: #3E362E !important;
        border-color: #401D06 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS DE BASE DE DATOS
# ─────────────────────────────────────────────

@st.cache_data(ttl=15)
def fetch_progreso():
    res = supabase.table("vista_progreso_items").select("*").order("id").execute()
    return res.data or []


def fetch_aportes_invitado(nombre: str):
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
    pass


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

def init_session():
    defaults = {
        "nombre":          None,
        "buffer":          {},
        "extra_texto":     "",
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
        <span class="hero-emoji">🌿</span>
        <h1 class="hero-title">¡Es el cumple de Luz!</h1>
        <p class="hero-sub">Celebremos juntos y armemos algo lindo 🤎</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    with st.container():
        st.markdown("**¿Cuál es tu nombre?**")
        nombre_input = st.text_input(
            "Nombre",
            placeholder="Ej: Pedro Marquinez",
            label_visibility="collapsed",
            key="input_nombre",
        )

        col_esp, col_btn = st.columns([2, 1])
        with col_btn:
            st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
            entrar = st.button("Entrar ✨", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
        <a href="?admin=1" target="_self"
           style="font-size:0.75rem; color:#A89F91; text-decoration:none; opacity:0.7;">
            ⚙️ Admin
        </a>
    </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("admin") == "1":
        st.info("👈 Ingresa tu contraseña en el panel lateral para acceder.")

    if entrar:
        nombre = nombre_input.strip()
        if not nombre:
            st.warning("¡Escribe tu nombre para continuar! 😊")
            return
        if len(nombre.split()) < 2:
            st.warning("¡Por favor incluye tu apellido para no confundirte! 😊")
            return

        aportes_prev = fetch_aportes_invitado(nombre)
        st.session_state["nombre"] = nombre

        if aportes_prev:
            st.session_state["buffer"] = { a["item_id"]: a["cantidad"] for a in aportes_prev }
            lista = ", ".join(f"{a['items']['emoji']} {a['items']['nombre']} ×{a['cantidad']}" for a in aportes_prev)
            st.session_state["reingreso_msg"] = (nombre, lista)
        else:
            st.session_state["buffer"] = {}
            st.session_state.pop("reingreso_msg", None)

        st.rerun()


# ─────────────────────────────────────────────
# VISTA DE INVITADOS
# ─────────────────────────────────────────────

def vista_invitados():
    nombre = st.session_state["nombre"]

    st.markdown(f"""
    <div class="hero">
        <span class="hero-emoji">🧺</span>
        <h1 class="hero-title">¡Hola, {nombre.split()[0]}!</h1>
        <p class="hero-sub">Elige qué vas a traer para compartir</p>
    </div>
    """, unsafe_allow_html=True)

    if "reingreso_msg" in st.session_state:
        n, lista = st.session_state["reingreso_msg"]
        st.markdown(f"""
        <div class="reingreso-alert">
            <b>¡Qué bueno verte de nuevo! 👋</b>
            <p>Ya estabas anotado con: <b>{lista}</b>.<br>
            Puedes ajustar tus aportes si lo necesitas.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    items = fetch_progreso()

    if not items:
        st.info("Aún no hay ítems en la lista. ¡Vuelve pronto!")
    else:
        st.markdown("<p style='color:#7A6F62; font-size:0.9rem; text-align:center;'>Ajusta las cantidades con los botones <b>＋</b> y <b>－</b></p>", unsafe_allow_html=True)
        
        buffer = st.session_state["buffer"]
        needs_rerun = False

        # Generar inputs invisibles de Streamlit
        for item in items:
            iid = item["id"]
            ph  = st.empty()
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
                needs_rerun = True
        
        if needs_rerun:
            st.rerun()

        # Construir el HTML Minimalista de las tarjetas
        tarjetas_html = ""
        for item in items:
            iid      = item["id"]
            emoji_i  = item["emoji"] or "🪴"
            meta     = item["cantidad_meta"]
            asignado = item["total_asignado"] or 0
            faltan   = max(0, meta - asignado)
            meta_ok  = asignado >= meta
            unidad_i = item.get("unidad") or ""
            ud       = f" {unidad_i}" if unidad_i else ""
            mi_qty   = buffer.get(iid, 0)

            if meta_ok and mi_qty == 0:
                estado_html   = '<div class="estado done">✅ Completado</div>'
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
                gap: 12px;
                width: 100%;
                padding: 4px;
            }}

            .card {{
                background: #FFFFFF;
                border: 1px solid #E6E2D6;
                border-radius: 12px;
                padding: 16px 12px;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
                box-shadow: 0 2px 6px rgba(62, 54, 46, 0.04);
            }}

            .card-emoji  {{ font-size: 3rem; line-height: 1; margin-bottom: 4px; }}
            .card-nombre {{
                font-weight: 600; font-size: 0.95rem;
                color: #3E362E; text-align: center;
            }}
            .estado {{
                font-size: 0.75rem; color: #7A6F62;
                text-align: center; margin-bottom: 8px;
            }}
            .estado.done {{ color: #401D06; font-weight: 600; }}

            .card-controls {{
                display: flex; align-items: center;
                gap: 8px; width: 100%; justify-content: center;
            }}
            .btn-ctrl {{
                width: 32px; height: 32px;
                border-radius: 6px;
                background: #F9F6F0;
                border: 1px solid #D6CFC4;
                color: #401D06;
                font-size: 1.1rem; font-weight: 600;
                cursor: pointer;
                display: flex; align-items: center; justify-content: center;
                transition: all 0.2s ease;
            }}
            .btn-ctrl:hover:not(:disabled)  {{ background: #EAECE6; border-color: #401D06; }}
            .btn-ctrl:disabled {{ opacity: 0.3; cursor: default; }}

            .qty-input {{
                width: 44px; height: 32px;
                text-align: center;
                font-size: 1rem; font-weight: 600;
                color: #3E362E;
                background: transparent;
                border: none;
                outline: none;
                -moz-appearance: textfield;
            }}
            .qty-input::-webkit-outer-spin-button,
            .qty-input::-webkit-inner-spin-button {{ -webkit-appearance: none; margin: 0; }}
        </style>
        </head>
        <body>
        <div class="grid">
            {tarjetas_html}
        </div>
        <script>
        // ── Sincronizar con Streamlit y Corregir DOM ──────────────
        try {{
            var doc = window.parent.document;
            var stInputs = doc.querySelectorAll('[data-testid="stNumberInput"]');
            stInputs.forEach(function(inp) {{
                var container = inp.closest('[data-testid="stElementContainer"]');
                if (container) {{
                    container.style.position = 'absolute';
                    container.style.height = '0px';
                    container.style.minHeight = '0px';
                    container.style.margin = '0px';
                    container.style.padding = '0px';
                    container.style.visibility = 'hidden';
                    container.style.border = 'none';
                }}
                var verticalBlock = inp.closest('[data-testid="stVerticalBlock"]');
                if (verticalBlock) {{
                    verticalBlock.style.gap = '0px';
                }}
            }});
        }} catch(e) {{}}

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

        var qtys = {{}};
        {chr(10).join(f"        qtys[{item['id']}] = {buffer.get(item['id'], 0)};" for item in items)}

        function syncCard(iid) {{
            var card  = document.querySelector('.card[data-iid="' + iid + '"]');
            var inp   = document.getElementById('qty-' + iid);
            var minus = card.querySelector('.minus');
            inp.value = qtys[iid];
            minus.disabled = qtys[iid] <= 0;
            setStInput(iid, qtys[iid]);
        }}

        document.querySelectorAll('.btn-ctrl').forEach(function(btn) {{
            btn.addEventListener('click', function() {{
                var iid  = parseInt(this.getAttribute('data-iid'));
                var paso = this.classList.contains('plus') ? 1 : -1;
                qtys[iid] = Math.max(0, (qtys[iid] || 0) + paso);
                syncCard(iid);
            }});
        }});

        document.querySelectorAll('.qty-input').forEach(function(inp) {{
            inp.addEventListener('input', function() {{
                var iid = parseInt(this.getAttribute('data-iid'));
                var val = parseInt(this.value) || 0;
                val = Math.max(0, Math.min(999, val));
                qtys[iid] = val;
                var card = document.querySelector('.card[data-iid="' + iid + '"]');
                card.querySelector('.minus').disabled = val <= 0;
                setStInput(iid, val);
            }});
            inp.addEventListener('blur', function() {{
                var iid = parseInt(this.getAttribute('data-iid'));
                this.value = qtys[iid];
            }});
        }});
        </script>
        </body>
        </html>
        """, height=((len(items) + 1) // 2) * 175 + 20, scrolling=False)


    # ── Sección extras ──
    st.markdown("""
    <div class="extras-box">
        <div class="extras-title">💡 ¿Se te ocurre algo más?</div>
        <div class="extras-subtitle">Una torta, guirnaldas, o un detalle especial.</div>
    </div>
    """, unsafe_allow_html=True)

    extra_texto = st.text_area(
        "Tu propuesta",
        placeholder="Ej: Puedo llevar mi cámara de fotos...",
        label_visibility="collapsed",
        value=st.session_state["extra_texto"],
        height=80,
        key="input_extra",
    )
    st.session_state["extra_texto"] = extra_texto

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="confirm-btn">', unsafe_allow_html=True)
    confirmar = st.button("Confirmar mi Aporte 🌿", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if confirmar:
        alguna_qty = any(v > 0 for v in st.session_state["buffer"].values())
        hay_extra  = bool(st.session_state["extra_texto"].strip())

        if not alguna_qty and not hay_extra:
            st.warning("⚠️ Agrega al menos un ítem o una propuesta antes de confirmar.")
        else:
            with st.spinner("Guardando... ✨"):
                emojis_aportes = []
                for item in (fetch_progreso() or []):
                    iid = item["id"]
                    qty = st.session_state["buffer"].get(iid, 0)
                    if qty > 0:
                        emojis_aportes.append(item["emoji"] or "🪴")

                for iid, qty in st.session_state["buffer"].items():
                    if qty >= 0: # Check de seguridad añadido
                        upsert_aporte(nombre, iid, qty)

                if hay_extra:
                    insertar_extra(nombre, extra_texto.strip())

            emojis_base = ["🤎", "🌿", "✨", "🍂", "🪴"]
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
        for _ in range(50):
            e     = random.choice(st.session_state["emojis_lluvia"])
            left  = random.randint(0, 100)
            dur   = random.uniform(2.5, 4.5)
            delay = random.uniform(0, 1.5)
            size  = random.randint(20, 40)
            lluvia_html += (
                f'<div class="emoji-drop" style="left:{left}vw;'
                f'animation-duration:{dur}s;animation-delay:{delay}s;'
                f'font-size:{size}px;">{e}</div>'
            )
        st.markdown(lluvia_html, unsafe_allow_html=True)
        st.markdown("""
        <div class="success-box">
            <h3>✨ ¡Aporte guardado!</h3>
            <p>Gracias por sumar tu granito de arena.<br>
            Puedes volver a modificarlo cuando quieras.</p>
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
        st.markdown("### 🌿 Panel Admin")

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
        <span class="hero-emoji">📋</span>
        <h1 class="hero-title">Panel de Control</h1>
        <p class="hero-sub">Estado de los preparativos</p>
    </div>
    """, unsafe_allow_html=True)

    tab_dashboard, tab_aportes, tab_extras, tab_agregar = st.tabs([
        "📊 Dashboard", "🧺 Aportes", "💡 Extras", "➕ Nuevo"
    ])

    with tab_dashboard:
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
                            f"<br><span style='color:#7A6F62;font-size:0.85rem;'>"
                            f"Faltan {meta-asignado}{ud_label}</span>",
                            unsafe_allow_html=True,
                        )
                st.markdown("")

    with tab_aportes:
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
                    "Ítem":     st.column_config.TextColumn("🧺 Ítem"),
                    "Cantidad": st.column_config.TextColumn("🔢 Cant."),
                },
            )
            st.caption(f"Total de registros: {len(rows)}")

    with tab_extras:
        extras = fetch_extras()
        if not extras:
            st.info("Nadie ha propuesto extras aún.")
        else:
            for ex in extras:
                with st.container():
                    st.markdown(f"**{ex['nombre_invitado']}** — {ex['descripcion']}")
                    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    with tab_agregar:
        with st.form("form_nuevo_item", clear_on_submit=True):
            col_e, col_n = st.columns([1, 4])
            with col_e:
                emoji_nuevo = st.text_input("Emoji", value="🪴", max_chars=4)
            with col_n:
                nombre_nuevo = st.text_input("Nombre", placeholder="Ej: Hummus")

            col_meta, col_unidad = st.columns([1, 2])
            with col_meta:
                meta_nueva = st.number_input("Cantidad", min_value=1, max_value=9999, value=5)
            with col_unidad:
                unidad_nueva = st.text_input("Unidad", placeholder="Ej: potes, bolsas...")
            
            submitted = st.form_submit_button("Agregar ítem 🌿", use_container_width=True)

        if submitted:
            if nombre_nuevo.strip():
                insertar_item(nombre_nuevo.strip(), int(meta_nueva), emoji_nuevo.strip(), unidad_nueva.strip())
                fetch_progreso.clear()
                st.success(f"¡'{nombre_nuevo}' agregado! ✨")
                st.rerun()
            else:
                st.warning("El nombre no puede estar vacío.")


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
