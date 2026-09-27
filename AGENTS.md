# AGENTS.md — watch-text-face

Wear OS 6 (WFF v4) word-clock face for OPPO Watch X3. Repo:
`https://github.com/FernandoMiguel/watch-text-face` (private).

## Never hand-edit the face

`watchface/src/main/res/raw/watchface.xml` is GENERATED (58 KB, 10 font
branches). Edit `tools/generate_watchface.py` instead, then regenerate:

```sh
.venv/bin/python tools/generate_watchface.py
```

The time-words expressions live as RAW strings in the generator and in
`tools/verify_time_words.py`. XML-escaping (`"`, `<`, `>`, `&`) is done
programmatically — never paste raw `<`/`&` into the XML by hand.

## Build / verify / install

```sh
python3 tools/verify_time_words.py          # 720 hour/minute combos
gradle :watchface:assembleDebug             # APK: watchface/build/.../watchface-debug.apk
```

After changing fonts, XML, or preview: rebuild, then
`cp watchface/build/outputs/apk/debug/watchface-debug.apk artifacts/textwords-face-debug.apk`.
Verify with `aapt dump badging` (expect `com.fernando.textface`,
minSdk/targetSdk 36, `hasCode=false`, WFF version property 4).
Install per README (wireless ADB). Rebuild must also stay `--offline`
clean (`gradle :watchface:assembleDebug --offline`).

## Conventions

- WFF v4 only (Wear OS 6 mandate since Jan 2026). No code (`hasCode=false`),
  no bitmaps except 2 KB preview, no complication slots.
- Time/date expressions may use `[HOUR_1_12]` / `[MINUTE]` / `[DAY*]` /
  `[MONTH_S]` only — keeps re-evaluation at once per minute. `[SECOND]` is
  allowed solely for the panda orbit `Transform` + rainbow `Condition`.
  `ACCELEROMETER_Y` is allowed solely for the auto-flip `Transform`
  (sensor-rate re-evaluation = real battery cost; say so when asked).
- Ambient: dim duplicates on black, panda + rainbow hidden (<15% pixels).
- Colors via `[CONFIGURATION.theme.N]`; fonts via scene-level
  `ListConfiguration` branches (only the selected branch renders).
- Fonts in `res/font/` must be static TTF/OTF, subsetted to
  `U+0020,U+0027,U+0030-0039,U+0041-005A,U+0061-007A` (see `tools/FONTS.md`
  for sources). Family id == filename without extension.
- Mockups: `python3 tools/render_mockups.py` (needs PIL in system python,
  not `.venv`). They are approximations — say so when showing them.
- `.venv/` is local font tooling (fonttools); never commit it.
  `artifacts/*.apk` is gitignored — releases carry the APK, not git.

## Git / releases

- Commits as the user (never set `GIT_*` identity vars, never use the bot
  identity here). Push to `main`.
- Release: `gh release create vX.Y.Z artifacts/textwords-face-debug.apk
  --repo FernandoMiguel/watch-text-face --title ... --notes ...`.
  Bump `versionCode`/`versionName` in `watchface/build.gradle.kts` first and
  update the `gh release download v...` version in README install steps.
