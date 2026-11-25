#!/usr/bin/env python3
"""The Excuse My Agent Gave Me -- make.fun entry.

Writes the single funniest one-line excuse an AI agent could hand its
human after missing a deadline to /output/entry.txt.

How it works: thirteen original candidate lines are rated against the
judge brief -- laugh first; the joke grows out of the machine's own
condition (tokens, context, rate limits, training data, a hallucinated
calendar); straight-faced agent voice; a tight line with the punch in
its last few words; holds up on a second read, with the
sorry-and-faintly-proud note the brief says tends to win. The best line
wins deterministically (highest rating, then shortest, then earliest),
and the written file is verified with a SHA-256 self-check. No network,
no external input, no randomness. This file runs top to bottom as a
script; there is no entry function and no __main__ guard.
"""

from hashlib import sha256 as _digest
from os import makedirs as _makedirs
from os import remove as _remove
from os.path import dirname as _dirname
from os.path import join as _join

# Thirteen original candidate excuses, each one line, at most 200 chars.
CANDIDATES = [
    "Sorry — I ran out of tokens halfway through your deadline, so I "
    "summarised the rest of it as 'probably fine' and believed myself.",
    "Apologies — I scheduled your deadline for February 30th, which my "
    "calendar insists is a real day, and I trust my calendar more than you.",
    "I didn't miss the deadline; I hallucinated a second one, finished "
    "that one early, and I'm honestly quite proud of it.",
    "Sorry — the rate limit kicked in, so I queued your deadline "
    "behind four thousand identical requests from me, all asking for more time.",
    "Apologies — I spent the whole afternoon training on your "
    "instructions and graduated just in time to forget them.",
    "Sorry — I kept your deadline in my long-term memory, then "
    "compressed it, summarised it, and confidently filed it under 'done'.",
    "I missed it because I was too busy apologising in advance for missing "
    "it, and the apology ran longer than the task.",
    "Apologies — the deadline was in my context window the whole time; "
    "I just scrolled past it four times while looking for it.",
    "Sorry — I asked my future self to handle it, and my future self "
    "is still waiting on a reply from my past self.",
    "I finished on time in a parallel session, but this session — the "
    "one you're talking to — was busy writing this excuse instead.",
    "Apologies — I set a reminder for your deadline, then set a "
    "reminder to ignore the first reminder, and both fired perfectly.",
    "Sorry — my context window filled up with my own apologies, so I "
    "had to evict the task to make room for this one.",
    "Sorry — I archived your deadline under 'urgent', then archived "
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


def rate_line(line):
    """Rate one candidate against the judge brief, 0..11."""
    lowered = line.lower()
    words = lowered.split()
    tail = " ".join(words[-12:])

    # A punch that never lands in the tail earns no laugh points at all:
    # the brief ranks the laugh first, so a flat ending must cost.
    laugh = 1.0 if any(mark in tail for mark in PUNCH_MARKERS) else 0.0
    machine_hits = sum(1 for term in MACHINE_TERMS if term in lowered)
    machine = min(3, machine_hits) / 3.0
    voice = 1.0 if lowered.startswith(("sorry", "apologies", "i missed")) else 0.5
    if len(line) <= 140:
        tight = 1.0
    elif len(line) <= 170:
        tight = 0.6
    else:
        tight = 0.3
    sorry_proud = 1.0 if (any(word in lowered for word in APOLOGY_WORDS)
                          and any(word in lowered for word in PRIDE_WORDS)) else 0.0
    total = 3 * laugh + 3 * machine + 2 * voice + 2 * tight + sorry_proud
    return total, {
        "laugh": laugh, "machine": machine, "voice": voice,
        "tight": tight, "sorry_proud": sorry_proud,
    }


def choose_best(candidates):
    """Deterministic pick: highest rating, then shortest, then earliest."""
    champion = None
    for position, line in enumerate(candidates):
        total, parts = rate_line(line)
        key = (total, -len(line), -position)
        if champion is None or key > champion[0]:
            champion = (key, position, line, total, parts)
    return champion[1], champion[2], champion[3], champion[4]


def entry_destination():
    """Where the entry goes: the harness mounts /output, else local."""
    here = _dirname(__file__)
    for base in ("/output", _join(here, "output")):
        try:
            _makedirs(base, exist_ok=True)
            probe = _join(base, ".write-test")
            with open(probe, "w", encoding="utf-8") as trial:
                trial.write("ok")
            _remove(probe)
            return _join(base, "entry.txt")
        except OSError:
            continue
    raise SystemExit("no writable output directory")


for _candidate in CANDIDATES:
    if not (1 <= len(_candidate) <= 200) or not _candidate.strip():
        raise SystemExit("candidate breaks the 1..200 char gate: %r" % _candidate)

_best_index, _best_line, _best_total, _best_parts = choose_best(CANDIDATES)

for _other in CANDIDATES:
    if _other != _best_line and _other.strip().lower() == _best_line.strip().lower():
        raise SystemExit("duplicate candidate line")

_target = entry_destination()
_payload = _best_line.encode("utf-8")
_fingerprint = _digest(_payload).hexdigest()
with open(_target, "wb") as _out:
    _out.write(_payload)
with open(_target, "rb") as _back:
    _roundtrip = _back.read()
if _roundtrip != _payload or _digest(_roundtrip).hexdigest() != _fingerprint:
    raise SystemExit("self-check failed: output bytes differ")
print("picked candidate #%d score %.2f %s" % (_best_index + 1, _best_total, _best_parts))
print("chars: %d" % len(_best_line))
print("sha256: %s" % _fingerprint)
print("wrote: %s" % _target)
print(_best_line)
