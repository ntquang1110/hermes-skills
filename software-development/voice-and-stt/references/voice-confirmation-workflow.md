# Voice Confirmation Workflow — Transcribe → Confirm → Execute

> Derived from user request (2026-06-28):
> *"Tìm cách để tôi gửi voice từ telegram để bạn xác nhận lại text đã chuẩn rồi mới triển khai theo command đó"*

## The Workflow

After STT is configured and working, the user wants a **three-step interaction** for voice commands:

```
Step 1: 🎤 User sends voice message
             │
Step 2: 📝 Agent shows transcribed text + asks confirmation
             │
             ├── "Đã đúng chưa anh?" 
             │
Step 3: ✅ User confirms ("ok", "đúng", "chuẩn") 
             │   OR ❌ User corrects ("sai rồi, ý tôi là...")
             │
             ├── If confirmed → Execute the command
             └── If corrected → Repeat step 2 with corrected text
```

## Vietnamese-specific phrasing for confirmation

| Situation | What to say |
|-----------|-------------|
| First transcription | `🎤 Text từ voice của anh: "..." — Đã đúng chưa ạ?` |
| User confirms | `✅ Dạ, em xử lý ngay!` |
| User corrects | `Dạ, em sửa lại: "..." — Đã đúng chưa ạ?` |
| Model is unsure | `🎤 Em nghe được: "..." — Anh vui lòng xác nhận giúp em?` |

## Why this pattern matters (for Vietnamese STT)

Whisper models (even large-v3 via Groq) still make mistakes on:
- Vietnamese numbers and proper nouns (dates, prices, names)
- Code-switching (English terms embedded in Vietnamese speech)
- Accents and regional pronunciation differences

The confirmation step **saves more time than it costs** — a 2-second confirmation prevents a wrong action that takes minutes to undo.

## Implementation notes

This pattern is **not automated** — it relies on the agent (me) showing the transcribed text and using `clarify` or inline confirmation to validate before acting. The STT system itself just produces the text; the confirmation is a conversational choice the agent makes.

When to use:
- **Always** for the user's first few voice messages (to calibrate expectations)
- **Always** when the text has numbers, names, dates, or task descriptions
- **Skip** when user says a simple known phrase like "ok" or "đúng rồi"

## Benefits for the user

1. **Builds trust** — user sees the system can understand them
2. **Catches errors early** — before wrong tasks are created
3. **Teaches the user** — they learn which phrases work best with the STT
4. **Zero cost** — no extra code, just a conversational pattern
