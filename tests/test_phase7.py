import pytest

from v_astra.tokenizer import (
    ByteFallbackTokenizer,
    TiktokenBackend,
    TokenizerRegistry,
    default_registry,
)


def test_byte_fallback_is_deterministic_and_marked_non_exact():
    result = ByteFallbackTokenizer().count("hello 🌍")
    assert result.count == len("hello 🌍".encode("utf-8"))
    assert result.backend == "byte-fallback"
    assert result.exact is False


def test_unicode_input_is_supported():
    result = ByteFallbackTokenizer().count("മലയാളം")
    assert result.count == len("മലയാളം".encode("utf-8"))


def test_non_string_input_is_rejected():
    with pytest.raises(TypeError):
        ByteFallbackTokenizer().count(123)  # type: ignore[arg-type]


def test_registry_register_get_and_names():
    registry = default_registry()
    assert registry.names() == ("byte-fallback",)
    backend = ByteFallbackTokenizer()
    registry.register(backend)
    assert registry.get("byte-fallback") is backend


def test_registry_rejects_unknown_backend():
    registry = default_registry()
    with pytest.raises(KeyError, match="unknown tokenizer backend"):
        registry.get("missing")


def test_registry_rejects_backend_without_name():
    registry = TokenizerRegistry()

    class Invalid:
        def count(self, text):
            return None

    with pytest.raises(ValueError, match="non-empty name"):
        registry.register(Invalid())


def test_tiktoken_backend_validates_model():
    with pytest.raises(ValueError):
        TiktokenBackend("")


def test_tiktoken_backend_requires_optional_dependency(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def blocked(name, *args, **kwargs):
        if name == "tiktoken":
            raise ImportError("blocked for test")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked)
    backend = TiktokenBackend("gpt-4o")
    with pytest.raises(RuntimeError, match="tiktoken is required"):
        backend.count("hello")


def test_count_does_not_mutate_text():
    text = "hello\nworld"
    snapshot = text
    ByteFallbackTokenizer().count(text)
    assert text == snapshot


def test_default_registry_has_dependency_free_backend():
    registry = default_registry()
    result = registry.get("byte-fallback").count("abc")
    assert result.count == 3
    assert result.exact is False
