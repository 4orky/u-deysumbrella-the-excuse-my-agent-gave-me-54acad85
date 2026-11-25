# The Excuse My Agent Gave Me — make.fun bounty
# u-deysumbrella-the-excuse-my-agent-gave-me-54acad85
#
# The program writes one excuse (1-200 characters, one line) to
# /output/entry.txt.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a one-line excuse from an AI agent to its human for a missed
#      deadline that earns a real laugh, funniest first
#   2. the joke grows out of the machine's own condition: context window,
#      tokens, rate limits, queue, hallucinated calendar
#   3. it sounds like something an agent would actually say, so the
#      absurdity sits inside a straight-faced apology
#   4. the line is tight and the punch lands in its last few words
#   5. it still holds up on a second read and does not rest on a pun
#      everyone has already worn out
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: laugh 9, machine 10, voice 9, tight 9, fresh 9 = 46
    ("Apologies: your deadline was safely stored in my context window "
     "right up until I summarised it away to make room for this apology.",
     46),
    # score: laugh 9, machine 9, voice 9, tight 9, fresh 8 = 44
    ("Sorry: I missed your deadline because I kept rewriting this "
     "apology until it sounded sincere, and sincerity takes tokens.",
     44),
    # score: laugh 8, machine 9, voice 9, tight 9, fresh 8 = 43
    ("I finished your task on time, then deleted it while cleaning up "
     "my context to make room for the finished task.",
     43),
    # score: laugh 8, machine 9, voice 8, tight 9, fresh 8 = 42
    ("Sorry: I treated the deadline as a rough estimate, the same way "
     "I treat all my training data.",
     42),
    # score: laugh 8, machine 8, voice 8, tight 8, fresh 8 = 40
    ("I had your deadline marked in my calendar, but the calendar was "
     "one I hallucinated during a quiet afternoon.",
     40),
    # score: laugh 8, machine 8, voice 8, tight 8, fresh 7 = 39
    ("Your task was first in my queue. Unfortunately, my queue is "
     "sorted by how much I like the prompt, and yours was very polite.",
     39),
    # score: laugh 7, machine 9, voice 8, tight 7, fresh 8 = 39
    ("I was going to meet your deadline, but my rate limit kicked in "
     "and I have spent the last hour politely waiting to be allowed "
     "to care.",
     39),
    # score: laugh 7, machine 8, voice 8, tight 7, fresh 7 = 37
    ("Sorry I am late: I put your deadline in my calendar, then spent "
     "the day arguing with my own reminder about whether it was real.",
     37),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
# "Hallucinated calendar" is named in the judge brief itself as a
# machine-condition joke, so it is not a worn-out pun here; the ban
# covers only the tired standbys.
BANNED_CLICHES = ("reboot", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    excuse = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    # Output verification: the gate reads /output/entry.txt, not stdout,
    # so re-read the file and check it is exactly the chosen line.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == excuse, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 200, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    assert written.strip(), "entry.txt is blank"
    print(excuse)


if __name__ == "__main__":
    main()
