# Text Words — Wear OS 6 watch face for OPPO Watch X3

Minimal, battery-optimized Watch Face Format (WFF v4) face.
Repo: `https://github.com/FernandoMiguel/watch-text-face` (private).

- Time in words, two lines — e.g. `Six` / `Twenty Eight`
  (`O'Clock` on the hour, `Oh Five` style below 10)
- Date line — e.g. `tue 22 sep` (lowercased device-locale short names;
  all-caps faces like Bebas render it `TUE 22 SEP`)
- **Themes**: Dark (light text on black) or Light (dark text on white),
  switchable on the watch / companion editor
- **30 fonts**: Bebas, Plex Mono, Cardo (classic); Pacifico, Bangers,
  Titan One (fun); MedievalSharp, Pirata One, Cinzel Decorative,
  Unifraktur (medieval); plus Lobster, Gochi Hand, Caveat Brush,
  Great Vibes, Shadows Into Light, Bungee, Alfa Slab, Bowlby One, Chicle,
  Rye, Fascinate, Fascinate Inline, Monoton, Ewert, Audiowide, Space Mono,
  Courier Prime, VT323, Creepster, Ribeye Marrow (fun, all readable) —
  switchable the same way
- **Seconds dot** (toggleable, on by default): jumps 6° per second around
  the edge in interactive mode; hidden in ambient. Note: while enabled,
  the face re-renders every second — turn it off for maximum battery life.

Mockups (PIL approximations with the real bundled fonts — metrics and
wrapping can differ slightly on-device):

- `screenshots/shot-dark-bebas.png` — default look
- `screenshots/shot-light-bebas.png` — light theme
- `screenshots/shot-dark-unifraktur.png` — blackletter example
- `screenshots/shot-dark-medieval.png` — medieval example
- `screenshots/shot-ambient.png` — ambient (dim, no dot)

## Can you install 3rd-party faces on the OPPO Watch X3?

Yes. The global X3 runs Wear OS 6, which allows sideloading APKs over
Wi-Fi ADB. No root, no Play Store needed. Two methods:

- **A — Mac/PC + ADB (recommended, used below).** You already have
  `adb 37.x` installed.
- **B — Phone only**, with Bugjaeger / Wear Installer 2 from the Play Store
  (pair to the watch via Wireless debugging, then install the APK from the
  phone). Same watch-side setup as method A, steps 1–4.

OPPO specifics: 1.5" round LTPO AMOLED 466×466, Wear OS 6 + ColorOS Watch.
The 450×450 face scales automatically. Use the watch in **Smart Mode**
(Sideloaded WFF faces live on the Wear OS chip; Power Saver / RTOS mode
will not show them).

## Project layout

```
watch-text-face/
  watchface/src/main/
    res/raw/watchface.xml        # GENERATED — do not hand-edit
    res/font/*.ttf               # 30 subsetted OFL fonts (~750 KB total)
    res/drawable/preview.png     # picker preview
    res/xml/watch_face_info.xml  # Editable=true, multi-instance allowed
    res/values/strings.xml       # face + theme/font option labels
    AndroidManifest.xml          # hasCode=false, WFF version 4, minSdk/targetSdk 36
  tools/
    generate_watchface.py        # single source of truth for watchface.xml
    verify_time_words.py         # expression logic check (720 combos)
    render_mockups.py            # PIL mockups in screenshots/
    FONTS.md                     # font sources / OFL attribution
  artifacts/textwords-face-debug.apk  # built, ~139 KB, debug-signed
```

## Build

```sh
cd /Users/fernando.pereira/tmp/opencode/watch-text-face
.venv/bin/python tools/generate_watchface.py   # regenerate watchface.xml
gradle :watchface:assembleDebug
# output: watchface/build/outputs/apk/debug/watchface-debug.apk
```

APK verified: `com.fernando.textface`, minSdk/targetSdk 36,
`hasCode=false`, WFF v4, 30 fonts + 167 KB face XML, ~445 KB total.

Check the wording logic without a watch:

```sh
python3 tools/verify_time_words.py
```

## Install on the watch (method A)

### Option 1 — download from GitHub Releases (no build needed)

1. Get the APK (repo is private, so sign in first):
   ```sh
   gh release download v1.1.0 --repo FernandoMiguel/watch-text-face --pattern '*.apk'
   # or download textwords-face-debug.apk from the Releases page in a browser
   ```
2. Follow steps 1–5 below to connect to the watch, then:
   ```sh
   adb -s <watch-ip>:<debug-port> install -r textwords-face-debug.apk
   # expect: Performing Streamed Install … Success
   ```
3. Follow steps 7–8 below to apply the face and turn debugging off.

### Option 2 — build from source

```sh
cd /Users/fernando.pereira/tmp/opencode/watch-text-face
.venv/bin/python tools/generate_watchface.py   # regenerate watchface.xml
gradle :watchface:assembleDebug
# output: watchface/build/outputs/apk/debug/watchface-debug.apk
```
then install that APK with the `adb install -r` command from Option 1.

### Watch connection steps

1. Watch and Mac on the **same Wi-Fi**. On the watch: Settings → Connectivity
   → Wi-Fi → connected (disable battery saver if Wi-Fi drops).
2. On the watch: Settings → System → About → tap **Build number 7×**
   until "You are now a developer".
3. Settings → Developer options → **ADB debugging ON** →
   **Wireless debugging ON**. Keep the screen awake (set display timeout long
   or tap it periodically — sleep drops the connection).
4. Tap Wireless debugging → **Pair new device**. Note IP, pairing port,
   and 6-digit code.
5. On the Mac:
   ```sh
   adb pair <watch-ip>:<pairing-port>   # enter the 6-digit code
   adb connect <watch-ip>:<debug-port>  # port shown on the Wireless debugging screen
   adb devices                          # watch must show as "device"
   ```
6. Install:
   ```sh
   adb -s <watch-ip>:<debug-port> install -r artifacts/textwords-face-debug.apk
   # expect: Performing Streamed Install … Success
   ```
7. On the watch: long-press the current face → swipe to **Text Words** →
   tap to apply. Tap the gear / Edit (or the companion phone app) to change
   **Theme**, **Font**, and the **Seconds dot** toggle.
8. Back in Developer options: turn **ADB debugging and Wireless debugging OFF**
   (saves battery).

## How the options work (WFF notes)

- WFF exposes **no system dark-mode data source**, so theme follows the
  face's own toggle, not the watch system setting: a `ColorConfiguration`
  (`theme`: bg / text / sub-text) referenced as `[CONFIGURATION.theme.N]`.
  It appears in the on-watch editor and the phone companion app automatically.
- Fonts work the same way via a scene-level `ListConfiguration` (`font`,
  10 options) — each branch renders the same text in a different bundled
  `res/font` family. Only the selected branch renders, so runtime memory
  is unaffected by the option count.
- Seconds dot: a `Group` pivoted at the face center with
  `<Transform target="angle" value="[SECOND] * 6" />` — integer `[SECOND]`
  gives discrete jumps, and re-evaluates per second only for that tiny node.
  A `Variant` hides it in ambient. Time/date expressions still re-evaluate
  once per minute.

## Optimization notes

- WFF (declarative, no code) — mandatory for Wear OS 6 installs since Jan 2026.
- Fonts subsetted to letters + digits + apostrophe + space
  (1.6 MB → ~210 KB); zero bitmaps (except 2 KB preview), pure black
  background in dark theme / ambient.
- Ambient: dim thin duplicates on black, dot hidden —
  text-on-black stays well under the 15%-pixel guideline; memory far under
  the 10 MB ambient / 100 MB interactive budgets. (Light theme is
  interactive-only by design; ambient always renders on black.)
- Battery: with the seconds dot on, the face redraws every second; with it
  off, everything re-evaluates at most once per minute. If the watch flags
  high battery use, turn the dot off first.

## Customizing

- Month shows the standard 3-letter abbreviation (`sep`, not `sept`).
  For `sept`, edit the date `Template` in `tools/generate_watchface.py`
  and regenerate.
- Add a font: drop `res/font/<name>.ttf`, add a `FONTS` entry + two
  `font_<name>_label` strings, regenerate, rebuild.
- Rebuild + reinstall with `-r` after any edit.

## Troubleshooting

- `adb connect` refused / offline: re-check IP+port (pairing port ≠ debug port),
  same Wi-Fi, screen awake, re-pair.
- `INSTALL_FAILED … signatures do not match`: uninstall first —
  `adb -s <ip>:<port> uninstall com.fernando.textface`, then install.
- Face not in picker: confirm Success message, Smart Mode active, then
  long-press face → swipe to the end of the list.
- Wrong hour (12h/24h): the face uses 12-hour words by design
  (`[HOUR_1_12]`); the date follows the device locale.
