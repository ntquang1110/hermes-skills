# Flutter localhost persistence fix (meTelligent)

## Vấn đề
App lưu URL server vào SimpleStorage. User bấm "💻 Local (8080)" trong Settings → URL `http://10.0.2.2:8080` được lưu.
Lần sau mở app, `ServerService.init()` đọc storage → override URL tunnel → app không kết nối được.

## Fix code (dài hạn) — `server_service.dart`

```dart
// === TRONG class ServerService ===

static const String defaultUrl = 'https://metelligent-123.loca.lt';
String serverUrl = defaultUrl;

/// Returns true if the URL is a local-only address (emulator/dev).
static bool _isLocalhost(String url) {
  final lower = url.toLowerCase();
  return lower.contains('localhost') ||
      lower.contains('10.0.2.2') ||
      lower.contains('127.0.0.1') ||
      lower == 'http://0.0.0.0' ||
      lower.startsWith('http://0.0.0.0:');
}

Future<void> init() async {
  final stored = await simpleStorage.getString('server_url');
  if (stored != null && stored.isNotEmpty && !_isLocalhost(stored)) {
    serverUrl = stored;  // only accept non-localhost URLs
  } else if (stored != null && _isLocalhost(stored)) {
    // Clean up stale localhost/emulator URLs from previous dev builds
    await simpleStorage.remove('server_url');
  }
}
```

## Quick fix (không rebuild APK)
1. User mở app → tab **Cài đặt**
2. Bấm nút **🌐 Tunnel** (quick switch)
3. Bấm **Lưu**
4. Bấm **Kiểm tra** — nếu 🟢 Đã kết nối là OK

## Kiểm tra
- `serverUrl` default = tunnel URL
- Nếu storage có URL valid (non-localhost) → dùng storage
- Nếu storage có URL localhost → xoá khỏi storage, dùng default
- Các method `checkConnection`, `getInfo`, `dispose` không đổi
