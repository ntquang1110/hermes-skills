# Design Critique Checklist

Dùng để phản biện một system design trước khi code.

## 🔴 Mức độ nghiêm trọng

| Label | Ý nghĩa | Hành động |
|-------|---------|-----------|
| 🔴 **Blocking** | Không thể code nếu chưa fix | Bắt buộc giải quyết trước |
| 🟡 **Warning** | Sẽ gây vấn đề về sau | Nên giải quyết ở phase này |
| 🟢 **Nice-to-have** | Có thể cải thiện sau | Ghi nhận, làm sau |

---

## 1. Architecture Checklist

- [ ] 🔴 **Pipeline model**: Linear (sequential) hay Event-driven (parallel)?
  - Linear không real-time được nếu có STT latency >500ms
- [ ] 🔴 **Async xuyên suốt**: Có asyncio/event loop không?
- [ ] 🟡 **Error handling**: Mỗi module có fallback không?
- [ ] 🟡 **Latency budget**: Module A + B + C = ?ms. Có đáp ứng real-time không?
- [ ] 🟡 **Scalability**: Single user? Multi-user? Cần message queue?
- [ ] 🟢 **Monitoring**: Logging, metrics, tracing?

## 2. Real-time Checklist

- [ ] 🔴 **STT latency**: Whisper local ~1-5s. Có streaming/interim results không?
- [ ] 🔴 **Audio buffer**: Có VAD không? Silence tolerance bao nhiêu?
- [ ] 🟡 **Thread safety**: Audio capture ở thread riêng? STT chạy trong thread pool?
- [ ] 🟡 **Backpressure**: Nếu NLP chậm hơn STT thì xử lý thế nào?
- [ ] 🟢 **WebSocket**: Real-time push hay client poll?

## 3. Data & Storage Checklist

- [ ] 🟡 **Vector DB**: Cần semantic search không? ChromaDB đủ không?
- [ ] 🟡 **Relational DB**: Cần transaction không? SQLite đủ không?
- [ ] 🟡 **File storage**: Audio logs? Transcripts? Cần cleanup policy?
- [ ] 🟢 **Backup strategy**: Export/import memory?
- [ ] 🔴 **Data privacy**: Audio data có được local-first không? Encryption?

## 4. Vietnamese-specific Checklist

- [ ] 🔴 **STT quality**: Model có hỗ trợ tiếng Việt tốt không? (faster-whisper: ✅)
- [ ] 🔴 **NLP accuracy**: Thư viện nào dùng cho NER, POS? (spaCy vi model: ⚠ yếu)
- [ ] 🟡 **Code-switching**: User nói tiếng Việt pha tiếng Anh? Cần handle?
- [ ] 🟡 **Critique language**: Critique/suggestion có nên bằng tiếng Việt không?

## 5. Dependency Mapping

Vẽ dependency graph:

```
Module A (không phụ thuộc)
  └── Module B (phụ thuộc A)
       └── Module C (phụ thuộc B)
```

Sau đó xác định P0, P1, P2 dựa trên graph (không phase tùy tiện).

## 6. Interaction Flow Gaps

Với mỗi scenario user đưa ra:
- [ ] Có đủ module để xử lý không?
- [ ] Latency có chấp nhận được không?
- [ ] UX có bị gián đoạn không?
- [ ] Có edge case nào không?

---

## Example output format

```markdown
## 🔴 Vấn đề: Real-time Pipeline không khả thi

**Phát hiện:** STT chạy sequential → NLP → Memory → tổng latency 5-7s

**Impact:** User nghe xong câu, đợi 5s mới thấy critique

**Solution:** 
1. Thread pool cho Whisper
2. Streaming interim results
3. Pipeline: STT chunk N song song với analysis chunk N-1

**Priority:** P0 (blocking)
```
