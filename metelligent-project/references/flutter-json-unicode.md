# Flutter/Dart: Proper JSON Construction for Unicode Safety

## Problem
Manual JSON string interpolation in Dart corrupts Unicode characters (Vietnamese `ừ` → `?`):

```dart
// ❌ WRONG — breaks Unicode
body: '{"text": "${text.replaceAll('"', '\\"')}", "language": "vi"}',
```

The `replaceAll` + string interpolation pattern:
1. Doesn't escape backslashes (`\`)
2. Doesn't handle newlines/control characters
3. Can mangle multi-byte UTF-8 sequences in edge cases
4. Fails with Unicode characters like `ừ` (U+1EEB)

## Solution: Always use jsonEncode
```dart
import 'dart:convert';

// ✅ CORRECT — handles all Unicode properly
body: jsonEncode({'text': text, 'language': 'vi'}),
```

## Rule of Thumb
**Never build JSON by hand** — always use the language's native serialization:
| Language | Function |
|----------|----------|
| Dart/Flutter | `jsonEncode()` from `dart:convert` |
| Python | `json.dumps()` from `json` |
| JavaScript | `JSON.stringify()` |
| Java | `new JSONObject()` or Gson |
| Swift | `JSONEncoder()` |

## Why this matters for Vietnamese
Vietnamese characters use multi-byte Unicode:
- `ừ` = U+1EEB (2 bytes in UTF-8: `1B EB`)
- `ả` = U+1EA3 (2 bytes)
- `á` = U+00E1 (2 bytes)

Manual string operations that split on byte boundaries can corrupt these. `jsonEncode` always produces correct UTF-8 JSON output.
