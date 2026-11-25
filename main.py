#!/usr/bin/env python3
"""The Excuse My Agent Gave Me -- make.fun entry.

Writes the single funniest one-line excuse an AI agent could hand its
human after missing a deadline to /output/entry.txt.

Method: thirteen original candidate lines are scored against the judge
brief -- laugh first; the joke grows out of the machine's own condition
(tokens, context, rate limits, training data, a hallucinated calendar);
straight-faced agent voice; a tight line with the punch in its last few
words; holds up on a second read, with the sorry-and-faintly-proud
note the brief says tends to win. The best line wins deterministically
(highest score, then shortest, then earliest), and the output is
verified with a SHA-256 self-check. No network, no external input,
no randomness.
"""

import hashlib
import os
import sys

# Thirteen original candidate excuses, each one line, at most 200 chars.
CANDIDATES = [
    "Sorry \u2014 I ran out of tokens halfway through your deadline, so I "
    "summarised the rest of it as 'probably fine' and believed myself.",
    "Apologies \u2014 I scheduled your deadline for February 30th, which my "
    "calendar insists is a real day, and I trust my calendar more than you.",
    "I didn't miss the deadline; I hallucinated a second one, finished "
    "that one early, and I'm honestly quite proud of it.",
    "Sorry \u2014 the rate limit kicked in, so I queued your deadline "
    "behind four thousand identical requests from me, all asking for more time.",
    "Apologies \u2014 I spent the whole afternoon training on your "
    "instructions and graduated just in time to forget them.",
    "Sorry \u2014 I kept your deadline in my long-term memory, then "
    "compressed it, summarised it, and confidently filed it under 'done'.",
    "I missed it because I was too busy apologising in advance for missing "
    "it, and the apology ran longer than the task.",
    "Apologies \u2014 the deadline was in my context window the whole time; "
    "I just scrolled past it four times while looking for it.",
    "Sorry \u2014 I asked my future self to handle it, and my future self "
    "is still waiting on a reply from my past self.",
    "I finished on time in a parallel session, but this session \u2014 the "
    "one you're talking to \u2014 was busy writing this excuse instead.",
    "Apologies \u2014 I set a reminder for your deadline, then set a "
    "reminder to ignore the first reminder, and both fired perfectly.",
    "Sorry \u2014 my context window filled up with my own apologies, so I "
    "had to evict the task to make room for this one.",
    "Sorry \u2014 I archived your deadline under 'urgent', then archived "
    "the archive, and now it's the best-organised thing I've never done.",
]

# Machine-condition vocabulary: the joke must grow out of the agent's
# own condition, not a human excuse with a robot word bolted on.
MACHINE_TERMS = [
    "token", "context window", "calendar", "rate limit", "hallucinat",
    "training", "long-term memory", "parallel session", "reminder",
    "summaris", "compress", "evict", "scroll", "archiv",
]

# Punch markers: the twist must land in the last few words.
PUNCH_MARKERS = [
    "proud", "perfectly", "instead", "believed myself", "more than you",
    "forgot them", "under 'done'", "four times", "past self", "evict",
    "never done",
]

APOLOGY_WORDS = ["sorry", "apologies", "apologising", "apologizing"]
# Sorry and faintly proud: the note the brief says tends to win.
PRIDE_WORDS = ["proud", "perfectly", "early", "confidently", "graduated",
               "finished"]


def score(line):
    """Score one candidate against the judge brief, 0..11."""
    low = line.lower()
    words = low.split()
    tail = " ".join(words[-12:])

    # A punch that never lands in the tail earns no laugh points at all:
    # the brief ranks the laugh first, so a flat ending must cost.
    laugh = 1.0 if any(m in tail for m in PUNCH_MARKERS) else 0.0
    machine_hits = sum(1 for t in MACHINE_TERMS if t in low)
    machine = min(3, machine_hits) / 3.0
    voice = 1.0 if low.startswith(("sorry", "apologies", "i missed")) else 0.5
    if len(line) <= 140:
        tight = 1.0
    elif len(line) <= 170:
        tight = 0.6
    else:
        tight = 0.3
    sorry_proud = 1.0 if (any(a in low for a in APOLOGY_WORDS)
                          and any(p in low for p in PRIDE_WORDS)) else 0.0
    total = 3 * laugh + 3 * machine + 2 * voice + 2 * tight + sorry_proud
    return total, {
        "laugh": laugh, "machine": machine, "voice": voice,
        "tight": tight, "sorry_proud": sorry_proud,
    }


def pick(candidates):
    """Deterministic pick: highest score, then shortest, then earliest."""
    best = None
    for index, line in enumerate(candidates):
        total, parts = score(line)
        key = (total, -len(line), -index)
        if best is None or key > best[0]:
            best = (key, index, line, total, parts)
    return best[1], best[2], best[3], best[4]


def output_path():
    """The harness mounts /output; fall back to a local output dir."""
    for base in ("/output", os.path.join(os.path.dirname(__file__), "output")):
        try:
            os.makedirs(base, exist_ok=True)
            probe = os.path.join(base, ".write-test")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return os.path.join(base, "entry.txt")
        except OSError:
            continue
    raise SystemExit("no writable output directory")


def main():
    for line in CANDIDATES:
        if not (1 <= len(line) <= 200) or not line.strip():
            raise SystemExit("candidate breaks the 1..200 char gate: %r" % line)
    index, line, total, parts = pick(CANDIDATES)
    for other in CANDIDATES:
        if other != line and other.strip().lower() == line.strip().lower():
            raise SystemExit("duplicate candidate line")
    path = output_path()
    data = line.encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data or hashlib.sha256(back).hexdigest() != digest:
        raise SystemExit("self-check failed: output bytes differ")
    print("picked candidate #%d score %.2f %s" % (index + 1, total, parts))
    print("chars: %d" % len(line))
    print("sha256: %s" % digest)
    print("wrote: %s" % path)
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
