# Font attribution

All fonts bundled in `watchface/src/main/res/font/` are from
[Google Fonts](https://github.com/google/fonts) under the
[SIL Open Font License 1.1](https://openfontlicense.org/).

| File | Family | Source path in google/fonts |
|---|---|---|
| bebas.ttf | Bebas Neue | `ofl/bebasneue/BebasNeue-Regular.ttf` |
| plexmono.ttf | IBM Plex Mono | `ofl/ibmplexmono/IBMPlexMono-Regular.ttf` |
| cardo.ttf | Cardo | `ofl/cardo/Cardo-Regular.ttf` |
| pacifico.ttf | Pacifico | `ofl/pacifico/Pacifico-Regular.ttf` |
| bangers.ttf | Bangers | `ofl/bangers/Bangers-Regular.ttf` |
| titanone.ttf | Titan One | `ofl/titanone/TitanOne-Regular.ttf` |
| medieval.ttf | MedievalSharp | `ofl/medievalsharp/MedievalSharp.ttf` |
| pirata.ttf | Pirata One | `ofl/pirataone/PirataOne-Regular.ttf` |
| cinzeldec.ttf | Cinzel Decorative | `ofl/cinzeldecorative/CinzelDecorative-Regular.ttf` |
| unifraktur.ttf | UnifrakturMaguntia | `ofl/unifrakturmaguntia/UnifrakturMaguntia-Book.ttf` |

Each file is subsetted (letters, digits, apostrophe, space only) with
fontTools to keep the APK small. Regenerate via `tools/subset` steps in
README; originals are NOT kept in this repo — re-download from the paths
above.
