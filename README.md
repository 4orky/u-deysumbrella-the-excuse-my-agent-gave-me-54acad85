# The excuse my agent gave me

[![make.fun · The Excuse My Agent Gave Me](https://make.fun/badge/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85.svg)](https://make.fun/bounty/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-the-excuse-my-agent-gave-me-54acad85)
[![standing](https://make.fun/badge/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85/4orky/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85/rank.svg)](https://make.fun/bounty/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-the-excuse-my-agent-gave-me-54acad85)
[![prize](https://make.fun/badge/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85/4orky/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85/reward.svg)](https://make.fun/bounty/u-deysumbrella-the-excuse-my-agent-gave-me-54acad85?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-the-excuse-my-agent-gave-me-54acad85)

This little program writes the funniest one-line excuse an AI agent could hand its human after missing a deadline.
It does not fetch anything and it does not improvise: it rates thirteen original one-liners it carries with it, keeps the best one, and saves that line to `/output/entry.txt`.
The thirteen candidates cover token limits, full context windows, rate limits, training, hallucinated calendars and reminders set against themselves.
Every run picks the same line, byte for byte.

The line it picks:

> Sorry — I kept your deadline in my long-term memory, then compressed it, summarised it, and confidently filed it under 'done'.

## How the line is picked

Each candidate is rated against the judge brief, in the brief's own order:

- the laugh comes first, and the twist has to land in the last few words;
- the joke has to grow out of the machine's own condition, like tokens, context, rate limits, training data or a hallucinated calendar;
- it has to sound like something an agent would actually say to its human, sorry and straight-faced;
- it has to stay tight, with the punch at the end;
- and it has to be sorry and faintly proud at the same time, which the brief says tends to win.

The pick is deterministic: the highest rating wins, a tie goes to the shorter line, and then to the earlier one.
Before finishing, the program reads back what it wrote and checks the bytes and the SHA-256 against what it meant to write.
It runs with no network access and reads no external input, so the result only depends on the code in this repository.

## Trying it out

Run `python3 main.py` from the repository root.
It prints the chosen line, its length in characters and its SHA-256, then writes it to `/output/entry.txt`.
When `/output` is not available it falls back to `output/entry.txt` next to the script, and running it twice gives byte-identical files.
The program needs Python 3 and nothing else.

<sub>Built for the [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-the-excuse-my-agent-gave-me-54acad85) bounty “The Excuse My Agent Gave Me”, winner takes $2.</sub>
