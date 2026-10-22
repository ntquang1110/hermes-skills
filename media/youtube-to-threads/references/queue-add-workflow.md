# Queue Addition Workflow (Verified 2026-09-27)

When user says "ok" after reading a draft inline, treat it as approval.

## Steps

1. Read `youtube-schedule.json` to find the latest date among ALL items (pending + posted).
2. Next date = latest + 1 day.
3. Read the draft file from disk (NOT from context — context may truncate).
4. Append to queue with `status: "pending"`, full content, url, title, scheduled_date.
5. Add video ID to `youtube-processed.json` `video_ids` array and URL to `urls` array.
6. Cross-check: if video ID already in `video_ids`, reject — "Video này đã có trong queue rồi".
7. Report the date and title back to user.

## Critical Rules

- Always read the draft file from disk before adding to queue. Context may not contain full draft content.
- Always verify video ID is not already processed — check `youtube-processed.json` NOT just the queue.
- For batch approval: user sends multiple links, keep all unapproved drafts as pending files, present all by video id, then add all approved sequentially from queue tail.
- Date uniqueness: check both schedule queue AND processed.json for existing dates before assigning.

## Files

- Queue: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-schedule.json`
- Processed: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-processed.json`
- Drafts: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\draft_<video_id>.txt`
