# How we work with Bob (daily routine + prompts)

Judging gives **30% to depth of Bob usage**, so most of the work is done inside Bob. Bob's own
history plus `docs/bob-log.md` are the evidence for that. Another tool (Claude, ChatGPT, etc.)
can help draft prompts or review work, but the build itself runs through Bob's
**Ask → Plan → Code** modes.

---

## ☀️ START-OF-DAY prompt (paste into Bob, Ask mode)
```
Start of session. Read AGENTS.md, then docs/plan/scope.md, prd.md, spec.md,
decisions.md, checklist.md, and the last entry of docs/bob-log.md.
Then tell me:
1. What's done (checked items) and today's day on the checklist.
2. The next unchecked item, and your plan for it in 3–5 bullets.
3. Any question you need answered before starting (numbered).
Do not write code yet.
```
→ Answer the questions **by voice** (speech-to-text), then switch to **Plan** mode.

## 🧭 PLAN prompt (Plan mode)
```
Plan checklist item: "<paste item>". List the files you'll create or change, the tests
you'll add, and how I'll check it in the browser. Keep it to one item. Wait for my OK.
```

## 🔨 BUILD prompt (Code mode)
```
Go. Build only that item, follow AGENTS.md rules, run pytest -q, check the item off in
docs/plan/checklist.md, then stop and tell me exactly what to click to test it.
```
Test it yourself. If something is wrong, describe it out loud and paste that in.
Repeat Plan → Build for the next item.

## 🌙 END-OF-DAY prompt (Ask or Code mode)
```
End of session. Do these steps:
1. Run pytest -q and report the result.
2. Append an entry to docs/bob-log.md using the template there: date, items finished,
   Bob modes used, key prompts, problems + fixes, decisions changed, next item.
3. Update any plan doc that is no longer true.
4. Show me the git commands to commit with a clear message (e.g. "Day 3: login + lockout").
5. Tell me tomorrow's first item and anything that is at risk for the Oct 18 deadline.
```
Then commit and push. Take 1–2 screenshots of Bob doing the work (for the deck and video).

---

## Using another tool to draft prompts (optional, the 10%)
1. In the other tool: "Here is my checklist item and spec section. Write a precise
   engineering prompt for IBM Bob to plan and build it in one step, with acceptance tests."
2. Paste that prompt into Bob **Ask** mode first: "Does this prompt fit our docs? What's
   missing?" Then Plan, then Code.
3. Note in `bob-log.md` that the prompt was drafted outside Bob. Bob always does the
   planning and the code.

## Catch-up interview (run once, now, since docs were drafted from your notes)
```
Read AGENTS.md and everything in docs/. Interview me with a numbered list of questions
covering anything in scope/prd/spec/decisions that is unclear, risky, or that you'd do
differently: style, features, roles, data, security, deploy. I'll answer by voice. Then
update the docs and mark decisions CONFIRMED.
```
