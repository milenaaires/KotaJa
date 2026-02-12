from unittest.mock import MagicMock

import app.bootstrap as bootstrap_module


def test_bootstrap_calls_streamlit_markdown_with_css(monkeypatch):
    # Arrange
    markdown_mock = MagicMock()
    monkeypatch.setattr(bootstrap_module.st, "markdown", markdown_mock)

    # Act
    bootstrap_module.bootstrap()

    # Assert
    markdown_mock.assert_called_once()
    css_arg = markdown_mock.call_args.args[0]
    kwargs = markdown_mock.call_args.kwargs

    assert kwargs.get("unsafe_allow_html") is True

    # “assinaturas” do CSS pra garantir que foi o bloco certo
    assert "--kj-orange" in css_arg
    assert ".kj-topbar" in css_arg
    assert "[data-testid=\"stHeader\"]" in css_arg
    assert "header, footer" in css_arg
