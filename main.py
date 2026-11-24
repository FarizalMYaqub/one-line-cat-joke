"""One-Line Cat Joke That Lands entry.

Writes one original one-line joke about cats to /output/entry.txt.
The joke is a fixed string on purpose: the program is deterministic, so
every run produces exactly the same entry the judge will read.
"""

import os

JOKE = "My cat knocked my coffee off the table, looked me dead in the eye, and waited for me to apologize."

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
CHAR_LIMIT = 200


def validate(joke):
    """The gate only accepts UTF-8 text of 1 to 200 chars, not only whitespace,
    and the brief wants a single line: no newline may sneak in."""
    if not joke.strip():
        raise ValueError("joke is blank")
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if len(joke) > CHAR_LIMIT:
        raise ValueError(f"joke is {len(joke)} chars, over the {CHAR_LIMIT} limit")
    joke.encode("utf-8")
    return joke


def write_entry(joke, path):
    """Write the validated joke to path atomically, so a reader never sees
    a half-written entry: write a temp file beside it, then replace."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(joke)
    os.replace(tmp_path, path)
    # Read-back verification: what landed on disk must be exactly the joke.
    with open(path, "r", encoding="utf-8") as handle:
        if handle.read() != joke:
            raise ValueError("entry on disk does not match the joke")
    return len(joke)


def main():
    joke = validate(JOKE)
    count = write_entry(joke, OUTPUT_PATH)
    print(f"Wrote {count} chars to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
