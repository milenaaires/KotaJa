# app/bootstrap.py
from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]  # .../KotaJa
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def bootstrap():
    # Identidade visual (preto + laranja)
    st.markdown(
        """
        <style>
          :root { --kj-orange: #f59e0b; }
          .block-container { padding-top: 1.2rem; }
          header, footer { visibility: hidden; }
          /* remove espaço do header padrão */
          [data-testid="stHeader"] { display: none; }
          /* botões e inputs */
          .stButton button { border: 1px solid var(--kj-orange) !important; }
          .stButton button:hover { box-shadow: 0 0 0 2px rgba(245,158,11,.25) !important; }
          /* “top bar” fake */
          .kj-topbar {
            position: sticky; top: 0; z-index: 99;
            display: flex; align-items: center; justify-content: space-between;
            padding: .75rem 1rem; margin: 0 0 1rem 0;
            border-radius: 14px;
            background: rgba(20,20,20,.85);
            border: 1px solid rgba(245,158,11,.35);
            backdrop-filter: blur(10px);
          }
          .kj-brand { display:flex; gap:.75rem; align-items:center; }
          .kj-brand img { height: 34px; width: 34px; border-radius: 10px; }
          .kj-title { font-weight: 800; font-size: 1.05rem; }
          .kj-sub { opacity:.75; font-size: .85rem; }
          .kj-pill {
            padding: .35rem .6rem;
            border-radius: 999px;
            border: 1px solid rgba(245,158,11,.45);
            color: rgba(245,158,11,.95);
            font-weight: 700;
            font-size: .82rem;
            white-space: nowrap;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
