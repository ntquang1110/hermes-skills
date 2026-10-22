# Leadership Canvas — 9 Blocks

A one-page visual framework for defining a leader's identity, inspired by the Business Model Canvas.

## Layout

```
┌──────────────────────┬──────────────────────┐
│ 🎯 Mission           │ 🧭 Vision            │
│──────────────────────┴──────────────────────│
│ 💎 Values  │ ⚡ Strengths │ 🌱 Growth │ 🎭 Style  │
│────────────┴─────────────┴──────────┴─────────│
│ 🤝 Key Relationships (2 cols)                  │
├──────────────────────┬───────────────────────│
│ 📊 Success Metrics   │ 🌟 Legacy             │
└──────────────────────┴───────────────────────┘
```

## Each Block

| Block | Prompts |
|-------|---------|
| **Mission** | Why do I lead? Why should people follow me? |
| **Vision** | Where am I taking the team? 1-3 year picture |
| **Values** | 3-5 non-negotiable values (e.g. efficiency, speed, autonomy) |
| **Strengths** | What I'm naturally good at as a leader |
| **Growth Areas** | What's holding me back? What needs improvement? |
| **Style** | How do I lead? (Visionary/Coach/Democratic/Servant/Transformational) |
| **Key Relationships** | Who I need to lead/influence/learn from |
| **Success Metrics** | How do I know I'm on the right track? |
| **Legacy** | What will people remember about me? 5 years from now |

## HTML Implementation

- 9 editable `<textarea>` blocks in a CSS grid
- Auto-saves to localStorage on every keystroke (key = `lc_b1`, `lc_b2`, ...)
- Restores on page load
- Ctrl+S triggers save with toast notification
- Clear button with confirm dialog
- Responsive: 4-col → 2-col → 1-col on mobile
- Dark theme matching user's design preferences

## When to Use

Use the Leadership Canvas:
- After Module 1 (Self-Mastery) as the first action task
- When the user needs to crystallize their leadership identity
- As a periodic review tool (every quarter)

## Local Save via Server

The reusable script at `scripts/canvas-server.py` turns the canvas into a Save-to-file tool:

```bash
cd ~/AppData/Local/hermes/skills/coaching/leadership-coaching
python scripts/canvas-server.py
# → http://localhost:2345
```

When user clicks "Save":
1. Browser POSTs JSON body to `http://localhost:2345/save`
2. Server writes `canvas-data.json` (raw) + `canvas-data.md` (pretty markdown)
3. Both files land in the same directory as the script

**Critical:** The user MUST open `http://localhost:2345` directly — Gist preview (htmlpreview.github.io) is cross-origin and cannot POST to localhost. If they're on the Gist version, add a "Download JSON" or "Copy text" fallback.
