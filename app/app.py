from __future__ import annotations

import sys
from pathlib import Path

from datetime import date
from uuid import UUID

import streamlit as st

from src.domain.quote_models import QuoteFilters  # noqa: E402
from src.repositories.catalog_repository import CatalogRepository  # noqa: E402
from src.repositories.log_repository import LogRepository  # noqa: E402
from src.repositories.public_query_repository import PublicQueryRepository  # noqa: E402
from src.services.quote_service import QuoteService  # noqa: E402

# =========================
# CONFIG + THEME
# =========================
st.set_page_config(
    page_title="KotaJá",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ORANGE = "#ff8a00"
BG = "#0b0f14"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent

DOCS_URL = "https://milenaaires.github.io/KotaJa/"
LOGO_PATH = str((ROOT_DIR / "docs" / "assets" / "logo" / "fusca.png").resolve())

st.markdown(
    f"""
<style>
[data-testid="stSidebar"] {{ display: none !important; }}
.block-container {{
  padding-top: 1.6rem;
  padding-bottom: 2rem;
  max-width: 1200px;
}}
.stApp {{
  background: radial-gradient(1200px 700px at 20% 0%, rgba(255,138,0,0.10), transparent 60%),
              radial-gradient(900px 600px at 90% 15%, rgba(255,138,0,0.08), transparent 55%),
              {BG};
  color: {TEXT};
}}
.kj-top {{
  margin-top: 0.4rem;
  margin-bottom: 1.2rem;
  padding: 14px 16px;
  border: 1px solid rgba(255,138,0,0.20);
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(255,138,0,0.10), rgba(15,23,42,0.35));
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}}
.kj-top .row {{
  display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;
}}
.kj-badge {{
  color: {ORANGE};
  font-weight: 700;
  letter-spacing: .08em;
}}
.kj-sub {{
  color: {MUTED};
  font-size: 0.92rem;
}}
.kj-actions {{
  display:flex; align-items:center; gap:10px; flex-wrap:wrap;
}}
.kj-chip {{
  display:inline-flex; align-items:center; gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,138,0,0.35);
  color: {TEXT};
  background: rgba(15,23,42,0.55);
}}
.kj-chip a {{ color: {TEXT}; text-decoration:none; }}
.kj-chip:hover {{ border-color: rgba(255,138,0,0.70); }}

.kj-card {{
  border: 1px solid rgba(148,163,184,0.15);
  border-radius: 18px;
  background: rgba(15,23,42,0.55);
  padding: 18px;
}}

.stButton > button {{
  border-radius: 14px !important;
  border: 1px solid rgba(255,138,0,0.55) !important;
  background: rgba(255,138,0,0.10) !important;
  color: {TEXT} !important;
}}
.stButton > button:hover {{
  border-color: rgba(255,138,0,0.95) !important;
  background: rgba(255,138,0,0.16) !important;
}}

[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{
  background: rgba(2,6,23,0.45) !important;
  color: {TEXT} !important;
}}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# HELPERS
# =========================
def _supports_dialog() -> bool:
    return hasattr(st, "dialog")


def _safe_session_id() -> str | None:
    # Streamlit muda APIs internas; isso aqui tenta sem quebrar
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
        if ctx and getattr(ctx, "session_id", None):
            return ctx.session_id
    except Exception:
        pass
    return None


def _index_of(options: list[str], wanted: str) -> int:
    try:
        return options.index(wanted)
    except ValueError:
        return 0


def _db_ok() -> bool:
    """Ping simples no banco pra badge da topbar."""
    try:
        from src.db.connection import get_conn

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return True
    except Exception:
        return False


# =========================
# STATE
# =========================
if "open_filters" not in st.session_state:
    st.session_state.open_filters = False
if "open_details" not in st.session_state:
    st.session_state.open_details = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None


def _init_filters_from_db() -> None:
    """Inicializa filtros só na 1ª vez, usando o 1º item real do catálogo."""
    if "filters" in st.session_state and st.session_state.filters:
        return  # já existe

    cat0 = CatalogRepository()

    regions = cat0.list_regions()
    if not regions:
        st.error("Sem regiões cadastradas no banco (regions). Cadastre pelo menos 1.")
        st.stop()

    brands = cat0.list_brands()
    if not brands:
        st.error("Sem marcas cadastradas no banco (brands). Cadastre pelo menos 1.")
        st.stop()

    brand_id = UUID(str(brands[0]["id"]))
    models = cat0.list_models(brand_id)
    if not models:
        st.error("Sem modelos cadastrados para a primeira marca (vehicle_models).")
        st.stop()

    model_id = UUID(str(models[0]["id"]))
    variants = cat0.list_variants(model_id)
    if not variants:
        st.error("Sem variantes cadastradas para o primeiro modelo (vehicle_variants).")
        st.stop()

    st.session_state.filters = {
        "month_ref": date(2026, 2, 1),

        # IDs (interno)
        "region_id": str(regions[0]["id"]),
        "brand_id": str(brand_id),
        "model_id": str(model_id),
        "vehicle_variant_id": str(variants[0]["id"]),

        # Labels (UI) — para NÃO mostrar UUID na tela
        "region_name": str(regions[0]["name"]),
        "brand_name": str(brands[0]["name"]),
        "model_name": str(models[0]["name"]),
        "variant_label": str(variants[0]["label"]),
    }


# cria defaults reais (sem UUID fixo)
_init_filters_from_db()

# =========================
# DIALOGS
# =========================
if _supports_dialog():

    @st.dialog("Filtros de consulta")
    def filters_dialog(cat: CatalogRepository):
        f = st.session_state.filters

        # ------ Mês ------
        month_ref = st.date_input(
            "Mês de referência",
            value=f["month_ref"],
            key="dlg_month_ref",
        )

        # ------ Região ------
        regions = cat.list_regions()
        if not regions:
            st.error("Sem regiões cadastradas.")
            st.stop()

        region_labels = [r["name"] for r in regions]
        region_map = {r["name"]: str(r["id"]) for r in regions}

        saved_region_id = f.get("region_id")
        saved_region_label = next(
            (r["name"] for r in regions if str(r["id"]) == str(saved_region_id)),
            region_labels[0],
        )

        region_label = st.selectbox(
            "Região",
            options=region_labels,
            index=_index_of(region_labels, saved_region_label),
            key="dlg_region",
        )

        # ------ Marca ------
        brands = cat.list_brands()
        if not brands:
            st.error("Sem marcas cadastradas.")
            st.stop()

        brand_labels = [b["name"] for b in brands]
        brand_map = {b["name"]: str(b["id"]) for b in brands}

        saved_brand_id = f.get("brand_id")
        saved_brand_label = next(
            (b["name"] for b in brands if str(b["id"]) == str(saved_brand_id)),
            brand_labels[0],
        )

        brand_label = st.selectbox(
            "Marca",
            options=brand_labels,
            index=_index_of(brand_labels, saved_brand_label),
            key="dlg_brand",
        )
        brand_id = UUID(brand_map[brand_label])

        # ------ Modelo (depende da marca) ------
        models = cat.list_models(brand_id)
        if not models:
            st.warning("Sem modelos para essa marca.")
            st.stop()

        model_labels = [m["name"] for m in models]
        model_map = {m["name"]: str(m["id"]) for m in models}

        saved_model_id = f.get("model_id")
        saved_model_label = next(
            (m["name"] for m in models if str(m["id"]) == str(saved_model_id)),
            model_labels[0],
        )

        model_label = st.selectbox(
            "Modelo",
            options=model_labels,
            index=_index_of(model_labels, saved_model_label),
            key="dlg_model",
        )
        model_id = UUID(model_map[model_label])

        # ------ Variante (depende do modelo) ------
        variants = cat.list_variants(model_id)
        if not variants:
            st.warning("Sem variantes para esse modelo.")
            st.stop()

        variant_labels = [v["label"] for v in variants]
        variant_map = {v["label"]: str(v["id"]) for v in variants}

        saved_variant_id = f.get("vehicle_variant_id")
        saved_variant_label = next(
            (v["label"] for v in variants if str(v["id"]) == str(saved_variant_id)),
            variant_labels[0],
        )

        variant_label = st.selectbox(
            "Variante",
            options=variant_labels,
            index=_index_of(variant_labels, saved_variant_label),
            key="dlg_variant",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salvar", use_container_width=True, key="dlg_save"):
                st.session_state.filters = {
                    "month_ref": month_ref,

                    # IDs (interno)
                    "region_id": region_map[region_label],
                    "brand_id": str(brand_id),
                    "model_id": str(model_id),
                    "vehicle_variant_id": variant_map[variant_label],

                    # Labels (UI)
                    "region_name": region_label,
                    "brand_name": brand_label,
                    "model_name": model_label,
                    "variant_label": variant_label,
                }
                st.session_state.open_filters = False
                st.rerun()

        with col2:
            if st.button("Cancelar", use_container_width=True, key="dlg_cancel"):
                st.session_state.open_filters = False
                st.rerun()

    @st.dialog("Detalhes da consulta")
    def details_dialog():
        r = st.session_state.last_result
        if not r:
            st.info("Nenhum resultado para mostrar ainda.")
        else:
            st.json(r)
        if st.button("Fechar", key="dlg_close_details"):
            st.session_state.open_details = False
            st.rerun()


# =========================
# TOP BAR
# =========================
db_ok = _db_ok()

col_logo, col_mid, col_right = st.columns([0.12, 0.68, 0.20])

with col_logo:
    try:
        st.image(LOGO_PATH, width=96)
    except Exception:
        st.write("🚗")

with col_mid:
    st.markdown(
        f"""
<div class="kj-top">
  <div class="row">
    <div>
      <div style="font-size:1.7rem;font-weight:850;line-height:1.1;">KotaJá</div>
      <div class="kj-sub">Cotações públicas por médias mensais • Preto + laranja • Postgres (Neon)</div>
    </div>
    <div class="kj-actions">
      <span class="kj-chip">✅ MVP</span>
      <span class="kj-chip">{'🟢 DB conectado ✅' if db_ok else '🔴 DB indisponível'}</span>
      <span class="kj-chip"><a href="{DOCS_URL}" target="_blank">📚 Docs (GitHub Pages)</a></span>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown("<div class='kj-badge' style='text-align:right;'>MVP</div>", unsafe_allow_html=True)


# =========================
# NAV (sem sidebar)
# =========================
tab_inicio, tab_consulta, tab_login, tab_sobre = st.tabs(
    ["🏠 Início", "🔎 Consulta Pública", "🔐 Login (em breve)", "🧩 Sobre"]
)

# =========================
# INÍCIO
# =========================
with tab_inicio:
    st.markdown("## Plataforma KotaJá")
    st.markdown(
        "Um MVP para **consulta pública de preços por médias mensais** (região + variante), "
        "com trilha de auditoria (logs) e base pronta para evoluir."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='kj-card'><h3>🔎 Consulta</h3><ul><li>Sem login</li><li>Rápida</li><li>Registra log</li></ul></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            "<div class='kj-card'><h3>🗄️ Dados</h3><ul><li>PostgreSQL (Neon)</li><li>Índices + constraints</li><li>Catálogo consistente</li></ul></div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            "<div class='kj-card'><h3>🧱 Arquitetura</h3><ul><li>UI (Streamlit)</li><li>Services/Repos</li><li>Testes com pytest</li></ul></div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Roadmap")
    st.info("✅ Consulta pública • 🟠 Login (em breve) • 🟠 Backoffice (em breve) • 🟠 Batch mensal (em breve)")


# =========================
# CONSULTA
# =========================
with tab_consulta:
    st.markdown("## 🔎 Consulta Pública — KotaJá")
    st.caption("Médias mensais por **região** e **variante**. Sem login.")

    top_actions = st.columns([0.70, 0.30])
    with top_actions[1]:
        if st.button("🔧 Filtros (pop-up)", use_container_width=True, key="btn_open_filters"):
            st.session_state.open_details = False
            st.session_state.open_filters = True
            st.rerun()

    # fonte única de verdade:
    f = st.session_state.filters

    # resumo (dashboard) — MOSTRA NOMES, não UUID
    a, b, c = st.columns(3)
    a.metric("Mês", f["month_ref"].isoformat())
    b.metric("Região", f.get("region_name") or "—")
    c.metric("Variante", f.get("variant_label") or "—")

    st.markdown("---")

    if st.button("Consultar", use_container_width=True, key="btn_run_query"):
        try:
            # filtros para consulta
            region_id = UUID(f["region_id"])
            vehicle_variant_id = UUID(f["vehicle_variant_id"]) if f.get("vehicle_variant_id") else None

            filters = QuoteFilters(
                month_ref=f["month_ref"],
                region_id=region_id,
                vehicle_variant_id=vehicle_variant_id,
            )

            # 1) consulta (service simples)
            svc = QuoteService()
            result = svc.get_quote(filters, user_agent=_safe_session_id())
            st.session_state.last_result = result

            # 2) logging (com brand/model)
            brand_id = UUID(f["brand_id"]) if f.get("brand_id") else None
            model_id = UUID(f["model_id"]) if f.get("model_id") else None

            LogRepository().insert_public_query_log(
                filters=filters,
                user_agent=_safe_session_id(),
                ip=None,  # sem IP no MVP
                brand_id=brand_id,
                model_id=model_id,
            )

            if not result:
                st.warning("Sem resultados para os filtros.")
            else:
                st.success("Consulta realizada!")
                avg = float(result["avg_price"])
                br = f"{avg:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                st.metric("Preço médio", f"R$ {br}")
                st.caption(f"Amostra: {result.get('sample_size', '-')}")

        except Exception as e:
            st.error("Sistema indisponível no momento. Tente novamente mais tarde.")
            st.exception(e)

    # botão detalhes
    if st.session_state.last_result:
        cols = st.columns([0.75, 0.25])
        with cols[1]:
            if st.button("📄 Detalhes (pop-up)", use_container_width=True, key="btn_open_details"):
                st.session_state.open_filters = False
                st.session_state.open_details = True
                st.rerun()

    st.markdown("---")
    st.markdown("### Histórico (últimas consultas)")
    st.caption("Enriquecido com nomes do catálogo (região/veículo/variante).")

    try:
        history = PublicQueryRepository().list_recent_enriched(limit=10)
        if not history:
            st.info("Ainda não há histórico.")
        else:
            st.dataframe(history, use_container_width=True, hide_index=True)
    except Exception as e:
        st.warning("Não foi possível carregar o histórico agora.")
        st.exception(e)


# =========================
# LOGIN (placeholder)
# =========================
with tab_login:
    st.markdown("## 🔐 Login")
    st.caption("Esta área é um placeholder para evolução do MVP.")
    st.warning("Ainda não implementado no MVP.")


# =========================
# SOBRE
# =========================
with tab_sobre:
    st.markdown("## 🧩 Sobre")
    st.markdown(
        "- **Objetivo:** consulta pública por média mensal\n"
        "- **Dados:** Neon Postgres\n"
        "- **Arquitetura:** UI → Service → Repository → DB\n"
        "- **Auditoria:** registro de consultas (logs)\n"
    )
    st.markdown(f"📚 Documentação completa: {DOCS_URL}")


# =========================
# ABRE DIALOGS (no final)
# =========================
if _supports_dialog():
    cat = CatalogRepository()
    if st.session_state.open_filters:
        filters_dialog(cat)
    elif st.session_state.open_details:
        details_dialog()
else:
    st.info("Seu Streamlit não tem suporte a pop-up (st.dialog). Atualize: pip install -U streamlit")
