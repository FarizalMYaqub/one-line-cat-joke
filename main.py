"""The One-Line Cat Joke That Lands — entry program.

The program writes exactly one original joke about cats to
/output/entry.txt and nothing else. The joke is a fixed string, so the
program is deterministic: every run produces the same entry the judge
reads, byte for byte.
"""

import os

# The entry itself: one line, under 200 characters, setup then turn.
JOKE = "My cat knocked my coffee off the table, looked me dead in the eye, and waited for me to apologize."

# Where the judge looks for the entry. Override with ENTRY_OUTPUT.
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# The competition gate: 1 to 200 characters of UTF-8 text, one line.
CHAR_LIMIT = 200


def check_joke(joke):
    """Reject anything the gate would refuse: blank, multi-line, too
    long, or not valid UTF-8. Returns the joke unchanged when it passes."""
    if not joke.strip():
        raise ValueError("joke is blank")
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if len(joke) > CHAR_LIMIT:
        raise ValueError(
            "joke is %d chars, over the %d limit" % (len(joke), CHAR_LIMIT)
        )
    joke.encode("utf-8")
    return joke


def save_entry(joke, path):
    """Write the joke to path atomically, then read it straight back:
    a reader must never see a half-written entry, and what landed on
    disk must be exactly the joke that was validated."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(joke)
    os.replace(tmp_path, path)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != joke:
        raise ValueError("entry on disk does not match the joke")
    return len(written)


def build_entry():
    """Validate the joke, then write it. Returns (chars, path)."""
    joke = check_joke(JOKE)
    count = save_entry(joke, OUTPUT_PATH)
    return count, OUTPUT_PATH


def main():
    count, path = build_entry()
    print("Wrote %d chars to %s" % (count, path))


if __name__ == "__main__":
    main()
