import sys
import types
import runpy
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4


class _SessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value


class _Ctx:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _Column(_Ctx):
    """
    Coluna do Streamlit:
    - pode ser usada com `with col:`
    - pode ser usada como objeto: `col.metric(...)`
    Aqui a gente só repassa para funções do st (mocks).
    """
    def __init__(self, st_module):
        self._st = st_module

    def metric(self, *args, **kwargs):
        return self._st.metric(*args, **kwargs)

    def markdown(self, *args, **kwargs):
        return self._st.markdown(*args, **kwargs)

    def caption(self, *args, **kwargs):
        return self._st.caption(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self._st.write(*args, **kwargs)

    def image(self, *args, **kwargs):
        return self._st.image(*args, **kwargs)

    def button(self, *args, **kwargs):
        return self._st.button(*args, **kwargs)


def _make_fake_streamlit():
    st = types.ModuleType("streamlit")
    st.session_state = _SessionState()

    # funções usadas no app (no-op + rastreáveis)
    st.set_page_config = MagicMock()
    st.markdown = MagicMock()
    st.caption = MagicMock()
    st.metric = MagicMock()
    st.write = MagicMock()
    st.image = MagicMock()
    st.json = MagicMock()
    st.dataframe = MagicMock()
    st.info = MagicMock()
    st.warning = MagicMock()
    st.success = MagicMock()
    st.error = MagicMock()
    st.exception = MagicMock()

    # ações que não queremos disparar no teste
    st.button = MagicMock(return_value=False)
    st.stop = MagicMock(side_effect=RuntimeError("st.stop called"))
    st.rerun = MagicMock()

    # layout helpers
    def columns(spec):
        n = spec if isinstance(spec, int) else len(spec)
        return [_Column(st) for _ in range(n)]

    def tabs(labels):
        return tuple(_Ctx() for _ in labels)

    st.columns = columns
    st.tabs = tabs

    # inputs usados só dentro do dialog (não será chamado, mas deixamos)
    st.date_input = MagicMock()
    st.selectbox = MagicMock()

    # garante que _supports_dialog() retorne False (assim não define dialogs)
    # (se você quiser testar dialog, aí é outro teste)
    if hasattr(st, "dialog"):
        delattr(st, "dialog")

    return st


def _install_stub_module(monkeypatch, module_name: str, **attrs):
    mod = types.ModuleType(module_name)
    for k, v in attrs.items():
        setattr(mod, k, v)
    monkeypatch.setitem(sys.modules, module_name, mod)
    return mod


def test_app_runs_without_crashing_and_initializes_filters(monkeypatch):
    # --- fake streamlit ---
    fake_st = _make_fake_streamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    # --- stubs de repos para não acessar DB ---
    region_id = str(uuid4())
    brand_id = str(uuid4())
    model_id = str(uuid4())
    variant_id = str(uuid4())

    class CatalogRepositoryStub:
        def list_regions(self):
            return [{"id": region_id, "name": "DF"}]

        def list_brands(self):
            return [{"id": brand_id, "name": "VW"}]

        def list_models(self, _brand_uuid):
            return [{"id": model_id, "name": "Fusca"}]

        def list_variants(self, _model_uuid):
            return [{"id": variant_id, "label": "2026 • Gasolina • Base • Manual"}]

    class PublicQueryRepositoryStub:
        def list_recent_enriched(self, limit: int = 10):
            return []  # sem histórico no teste

    _install_stub_module(
        monkeypatch,
        "src.repositories.catalog_repository",
        CatalogRepository=CatalogRepositoryStub,
    )
    _install_stub_module(
        monkeypatch,
        "src.repositories.public_query_repository",
        PublicQueryRepository=PublicQueryRepositoryStub,
    )

    # stuba QuoteService e LogRepository (no app só rodam se clicar, mas ok)
    class QuoteServiceStub:
        def get_quote(self, *args, **kwargs):
            return None

    class LogRepositoryStub:
        def insert_public_query_log(self, *args, **kwargs):
            return None

    _install_stub_module(monkeypatch, "src.services.quote_service", QuoteService=QuoteServiceStub)
    _install_stub_module(monkeypatch, "src.repositories.log_repository", LogRepository=LogRepositoryStub)

    # --- executa app.py como script ---
    project_root = Path(__file__).resolve().parents[1]
    app_path = project_root / "app" / "app.py"
    assert app_path.exists(), f"Não achei {app_path}"

    runpy.run_path(str(app_path), run_name="__main__")

    # --- asserts: app subiu e inicializou filtros ---
    fake_st.set_page_config.assert_called_once()

    assert "filters" in fake_st.session_state
    f = fake_st.session_state["filters"]
    assert f["region_id"] == region_id
    assert f["brand_id"] == brand_id
    assert f["model_id"] == model_id
    assert f["vehicle_variant_id"] == variant_id
