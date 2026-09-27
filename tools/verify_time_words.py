"""Verify time-to-words mapping logic (mirrors WFF expressions in watchface.xml)."""
HOUR_WORDS = {
    1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
    7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve",
}
TEENS = {
    10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
    15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen",
}
ONES = {
    1: " One", 2: " Two", 3: " Three", 4: " Four", 5: " Five",
    6: " Six", 7: " Seven", 8: " Eight", 9: " Nine",
}

def hour_word(h):
    return HOUR_WORDS[h]

def minute_words(m):
    # mirrors MIN_TENS_EXPR + MIN_ONES_EXPR with Template "%s%s"
    if m == 0:
        tens = "O'Clock"
    elif m < 10:
        tens = "O"
    elif m < 20:
        tens = TEENS[m]
    elif m < 30:
        tens = "Twenty"
    elif m < 40:
        tens = "Thirty"
    elif m < 50:
        tens = "Forty"
    else:
        tens = "Fifty"
    if m == 0:
        ones = ""
    elif 10 <= m < 20:
        ones = ""
    elif m % 10 == 0:
        ones = ""
    else:
        ones = ONES[m % 10]
    return tens + ones

def main():
    assert hour_word(6) == "Six"
    assert minute_words(28) == "Twenty Eight", minute_words(28)
    assert minute_words(0) == "O'Clock", minute_words(0)
    # full sweep
    seen = set()
    for h in range(1, 13):
        assert hour_word(h), h
        for m in range(60):
            s = f"{hour_word(h)} {minute_words(m)}"
            assert '"' not in s and s.strip() == s and "  " not in s, s
            seen.add(s)
    # spot checks
    checks = {
        (12, 0): "Twelve O'Clock",
        (1, 1): "One O One",
        (2, 10): "Two Ten",
        (3, 13): "Three Thirteen",
        (4, 20): "Four Twenty",
        (5, 30): "Five Thirty",
        (6, 28): "Six Twenty Eight",
        (11, 45): "Eleven Forty Five",
        (12, 59): "Twelve Fifty Nine",
        (9, 5): "Nine O Five",
    }
    for (h, m), exp in checks.items():
        got = f"{hour_word(h)} {minute_words(m)}"
        assert got == exp, f"{h}:{m:02d} got {got!r} want {exp!r}"
    print(f"OK: 12 hours x 60 minutes = {len(seen)} unique phrases, all spot checks pass")

if __name__ == "__main__":
    main()
