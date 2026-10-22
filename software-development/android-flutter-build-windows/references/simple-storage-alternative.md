# SimpleStorage — shared_preferences alternative

When `shared_preferences` triggers the Kotlin incremental cache bug on
Windows, use this pure-Dart file-based storage instead.

## Code

```dart
import 'dart:io';
import 'dart:convert';

class SimpleStorage {
  static final SimpleStorage _instance = SimpleStorage._internal();
  factory SimpleStorage() => _instance;
  SimpleStorage._internal();

  final Map<String, String> _cache = {};
  bool _initialized = false;

  Future<void> init() async {
    if (_initialized) return;
    _initialized = true;
    try {
      final file = _getFile();
      if (await file.exists()) {
        final content = await file.readAsString();
        final data = jsonDecode(content) as Map<String, dynamic>;
        data.forEach((k, v) => _cache[k] = v.toString());
      }
    } catch (_) {}
  }

  Future<void> _save() async {
    try {
      final file = _getFile();
      await file.parent.create(recursive: true);
      await file.writeAsString(jsonEncode(_cache));
    } catch (_) {}
  }

  File _getFile() {
    // Android app-specific directory
    final dir = Directory('/data/data/com.metelligent.metelligent/files');
    return File('${dir.path}/metelligent_config.json');
  }

  Future<String?> getString(String key) async {
    if (!_initialized) await init();
    return _cache[key];
  }

  Future<void> setString(String key, String value) async {
    _cache[key] = value;
    await _save();
  }
}

final simpleStorage = SimpleStorage();
```

## Usage

```dart
// Initialize once
await simpleStorage.init();

// Store
await simpleStorage.setString('server_url', 'http://192.168.1.2:8080');

// Retrieve
final url = await simpleStorage.getString('server_url');
```

## Limitations

- NOT suitable for large data (JSON file grows)
- NOT encrypted
- Data persists until app data is cleared
- Path is hardcoded per app package name — change for your project
