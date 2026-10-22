# APK Build on Windows (no prior SDK)

## Prerequisites

- Flutter SDK (`git clone --depth 1 --branch stable https://github.com/flutter/flutter.git /c/flutter`)
- JDK 17+ (Temurin: `https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.12%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.12_7.zip`)
- Android SDK (tự động có sau khi chạy `flutter build` lần đầu — Flutter tải về)

## Build steps

```bash
# 1. Set env
export PATH="$PATH:/c/flutter/bin"
export JAVA_HOME="/c/java/jdk-17.0.12+7"
export PATH="$JAVA_HOME/bin:$PATH"

# 2. Clean previous build (nếu có file lock error)
taskkill //F //IM java.exe 2>/dev/null  # kill Gradle daemon
flutter clean

# 3. Get dependencies
flutter pub get

# 4. Build
flutter build apk --debug
# Output: build/app/outputs/flutter-apk/app-debug.apk
```

## Common errors & fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Unable to delete directory ...mergeDebugNativeLibs` | Gradle process locked files | `taskkill //F //IM java.exe` → `flutter clean` → rebuild |
| `JAVA_HOME is not set` | JDK not installed | Install JDK + set JAVA_HOME |
| `No named parameter with name 'path'` | Old `record` package API | Move `path` param: `start(RecordConfig(...), path: path)` |
| `The getter 'tags' isn't defined` | Missing receiver in string interpolation | `$tags` → `${meeting.tags}` |

## Performance

- First build: ~3-5 min (downloads Gradle + Android SDK)
- Subsequent builds: ~1-2 min
- Debug APK size: ~150MB (includes Dart VM + symbols)
- Release APK: use `--release` flag (smaller ~20-40MB, needs signing)
