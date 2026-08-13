from v_astra.safety.guards import preserve_critical


def test_critical_marker_is_preserved():
    original = "normal\nERROR: do not remove"
    optimized = "normal"
    assert preserve_critical(original, optimized, ["ERROR:"]) == original


def test_safe_optimization():
    original = "hello"
    optimized = "hi"
    assert preserve_critical(original, optimized, ["ERROR:"]) == optimized
