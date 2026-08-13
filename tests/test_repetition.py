from v_astra.compression.repetition import collapse_consecutive_duplicates
def test_collapse():
    assert collapse_consecutive_duplicates("A\nA\nA\nB\n") == "A [x3]\nB"
