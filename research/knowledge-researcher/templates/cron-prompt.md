# Cron Prompt Template — Research Queue Processor

Use this as the prompt for the `knowledge-researcher` cron job.

## Cron job config

```yaml
job_id: d43697af1322
name: knowledge-researcher
schedule: every 120m
skills: ["web-research"]
deliver: origin
```

## Prompt (latest — with quality gates)

```
## Cron: Research sau, 2 tieng/lan

Tap trung: HEO (chan nuoi lon), SINH HOC, Y HOC

### QUY TAC CHAT LUONG NGHIEM NGAT (BAT BUOC)

1. TIENG VIET CO DAU DAY DU — "co che tac dung" KHONG phai "co che tac dung"
2. EMOJI THAT — dung 🧬🐷🔬 KHONG dung :dna: :warning: (se hien text tho)
3. source_url BAT BUOC — moi card phai co link den nguon goc
4. DI SAU BAN CHAT — giai thich pathway, protein, gene, co che, KHONG chi liet ke

### Format card:
## Ten co che / pathway

**Mo ta ban chat:** [giai thich cot loi, 3-4 cau]
- **Protein A** -> vai tro
- **Gene B** -> dieu hoa

Buoc 1 -> Buoc 2 -> Buoc 3

> **Ban chat:** [insight chinh]

Nguon: [URL tham khao]

### Steps:
1. GET /api/research-queue -> pending? xu ly
2. Queue rong? -> chon HEO/SINH HOC/Y HOC (luan phien, khong lap)
3. Research sau 3-4 nguon
4. Viet card: co dau, emoji that, source_url, sau
5. POST /api/knowledge (Authorization: Bearer hermes-knowledge-secret)
6. Queue item? -> PATCH done

KIEM TRA: co dau? emoji that? co source_url? du sau?
```

## Update command

Use `cronjob(action='update', job_id='d43697af1322', schedule='every 120m', skills=['web-research'], prompt='...')`.
