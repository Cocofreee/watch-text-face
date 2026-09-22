"""Generate res/raw/watchface.xml from verified expression strings.

Single source of truth for the time-words expressions (also verified by
tools/verify_time_words.py). Run:  .venv/bin/python tools/generate_watchface.py
"""
import xml.etree.ElementTree as ET

HOUR_RAW = '[HOUR_1_12] == 1 ? "One" : ([HOUR_1_12] == 2 ? "Two" : ([HOUR_1_12] == 3 ? "Three" : ([HOUR_1_12] == 4 ? "Four" : ([HOUR_1_12] == 5 ? "Five" : ([HOUR_1_12] == 6 ? "Six" : ([HOUR_1_12] == 7 ? "Seven" : ([HOUR_1_12] == 8 ? "Eight" : ([HOUR_1_12] == 9 ? "Nine" : ([HOUR_1_12] == 10 ? "Ten" : ([HOUR_1_12] == 11 ? "Eleven" : "Twelve"))))))))))'
TENS_RAW = '[MINUTE] == 0 ? "O\'Clock" : ([MINUTE] < 10 ? "Oh" : ([MINUTE] < 20 ? ([MINUTE] == 10 ? "Ten" : ([MINUTE] == 11 ? "Eleven" : ([MINUTE] == 12 ? "Twelve" : ([MINUTE] == 13 ? "Thirteen" : ([MINUTE] == 14 ? "Fourteen" : ([MINUTE] == 15 ? "Fifteen" : ([MINUTE] == 16 ? "Sixteen" : ([MINUTE] == 17 ? "Seventeen" : ([MINUTE] == 18 ? "Eighteen" : "Nineteen"))))))))) : ([MINUTE] < 30 ? "Twenty" : ([MINUTE] < 40 ? "Thirty" : ([MINUTE] < 50 ? "Forty" : "Fifty")))))'
ONES_RAW = '[MINUTE] == 0 ? "" : ([MINUTE] >= 10 && [MINUTE] < 20 ? "" : ([MINUTE] % 10 == 0 ? "" : ([MINUTE] % 10 == 1 ? " One" : ([MINUTE] % 10 == 2 ? " Two" : ([MINUTE] % 10 == 3 ? " Three" : ([MINUTE] % 10 == 4 ? " Four" : ([MINUTE] % 10 == 5 ? " Five" : ([MINUTE] % 10 == 6 ? " Six" : ([MINUTE] % 10 == 7 ? " Seven" : ([MINUTE] % 10 == 8 ? " Eight" : " Nine"))))))))))'

# (option id, font family, label) — order defines the on-watch picker order.
FONTS = [
    ("0", "bebas", "Bebas (classic)"),
    ("1", "plexmono", "Plex Mono (classic)"),
    ("2", "cardo", "Cardo (classic serif)"),
    ("3", "pacifico", "Pacifico (fun script)"),
    ("4", "bangers", "Bangers (fun comic)"),
    ("5", "titanone", "Titan One (fun chunky)"),
    ("6", "medieval", "Medieval Sharp"),
    ("7", "pirata", "Pirata One (blackletter)"),
    ("8", "cinzeldec", "Cinzel (roman caps)"),
    ("9", "unifraktur", "Unifraktur (blackletter)"),
    ("10", "lobster", "Lobster (fun script)"),
    ("11", "gochihand", "Gochi Hand (fun handwritten)"),
    ("12", "caveatbrush", "Caveat Brush (fun brush)"),
    ("13", "greatvibes", "Great Vibes (fun script)"),
    ("14", "shadows", "Shadows Into Light (fun handwritten)"),
    ("15", "bungee", "Bungee (fun chunky)"),
    ("16", "alfaslabone", "Alfa Slab (fun chunky)"),
    ("17", "bowlbyone", "Bowlby One (fun chunky)"),
    ("18", "chicle", "Chicle (fun rounded)"),
    ("19", "rye", "Rye (fun western)"),
    ("20", "fascinate", "Fascinate (fun deco)"),
    ("21", "fascinateinline", "Fascinate Inline (fun deco)"),
    ("22", "monoton", "Monoton (fun deco)"),
    ("23", "ewert", "Ewert (fun woodtype)"),
    ("24", "audiowide", "Audiowide (fun techy)"),
    ("25", "spacemono", "Space Mono (fun mono)"),
    ("26", "courierprime", "Courier Prime (fun typewriter)"),
    ("27", "vt323", "VT323 (fun pixel)"),
    ("28", "creepster", "Creepster (fun spooky)"),
    ("29", "ribeyemarrow", "Ribeye Marrow (fun quirky)"),
]


def esc(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


HOUR = esc(HOUR_RAW)
TENS = esc(TENS_RAW)
ONES = esc(ONES_RAW)


def part_text(x, y, w, h, family, size, weight, color, template_inner,
              ambient_hide=False, ambient_show=False, max_lines=None):
    ml = f' maxLines="{max_lines}"' if max_lines else ""
    if ambient_hide:
        variant = '\n      <Variant mode="AMBIENT" target="alpha" value="0" />'
        open_tag = f'<PartText x="{x}" y="{y}" width="{w}" height="{h}">'
    else:
        variant = '\n      <Variant mode="AMBIENT" target="alpha" value="255" />'
        open_tag = (f'<PartText x="{x}" y="{y}" width="{w}" height="{h}" '
                    f'alpha="0">')
    return (f"""    {open_tag}{variant}
      <Text align="CENTER"{ml}>
        <Font family="{family}" size="{size}" weight="{weight}" color="{color}">
          {template_inner}
        </Font>
      </Text>
    </PartText>""")


def hour_block(family, color, weight, ambient_hide):
    t = (f'<Template>%s<Parameter expression="{HOUR}" />'
         f"</Template>")
    return part_text(0, 96, 450, 96, family, 66, weight, color, t,
                     ambient_hide=ambient_hide,
                     ambient_show=not ambient_hide)


def minute_block(family, color, weight, ambient_hide):
    t = (f'<Template>%s%s<Parameter expression="{TENS}" />'
         f'<Parameter expression="{ONES}" /></Template>')
    return part_text(0, 188, 450, 128, family, 48, weight, color, t,
                     ambient_hide=ambient_hide,
                     ambient_show=not ambient_hide, max_lines=2)


def date_block(family, color, weight, ambient_hide):
    t = ("<Lower>\n            <Template>%s %d %s"
         '<Parameter expression="[DAY_OF_WEEK_S]" />'
         '<Parameter expression="[DAY]" />'
         '<Parameter expression="[MONTH_S]" />'
         "</Template>\n          </Lower>")
    return part_text(0, 312, 450, 46, family, 32, weight, color, t,
                     ambient_hide=ambient_hide,
                     ambient_show=not ambient_hide)


def main():
    for e in (HOUR_RAW, TENS_RAW, ONES_RAW):
        assert e.count("(") == e.count(")"), e[:60]
    assert len(FONTS) == 30

    theme_cfg = """    <ColorConfiguration id="theme" displayName="theme_label" defaultValue="0">
      <ColorOption id="0" displayName="theme_dark_label" colors="#ff000000 #ffffffff #ffbbbbbb" />
      <ColorOption id="1" displayName="theme_light_label" colors="#ffffffff #ff000000 #ff555555" />
    </ColorConfiguration>"""
    font_opts = "\n".join(
        f'      <ListOption id="{i}" displayName="font_{fam}_label" />'
        for i, fam, _ in FONTS)
    font_cfg = (f'    <ListConfiguration id="font" displayName="font_label"\n'
                f'        screenReaderText="font_label" defaultValue="0">\n'
                f'{font_opts}\n    </ListConfiguration>')
    seconds_cfg = ('    <BooleanConfiguration id="seconds_dot"\n'
                   '        displayName="seconds_dot_label"\n'
                   '        screenReaderText="seconds_dot_label"\n'
                   '        defaultValue="TRUE" />')

    branches = []
    for i, fam, _ in FONTS:
        branches.append(f"""    <ListOption id="{i}">
{hour_block(fam, "[CONFIGURATION.theme.1]", "BOLD", True)}
{minute_block(fam, "[CONFIGURATION.theme.1]", "NORMAL", True)}
{date_block(fam, "[CONFIGURATION.theme.2]", "NORMAL", True)}
{hour_block(fam, "#ff999999", "THIN", False)}
{minute_block(fam, "#ff888888", "THIN", False)}
{date_block(fam, "#ff666666", "THIN", False)}
    </ListOption>""")
    font_switch = "<ListConfiguration id=\"font\">\n" + "\n".join(branches) + "\n  </ListConfiguration>"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
  Text Words — WFF v4 / Wear OS 6. Time in words, single date line,
  mono-chrome themes (ColorConfiguration), 10 bundled fonts (ListConfiguration),
  toggleable seconds dot (interactive only). Generated by tools/generate_watchface.py —
  do not hand-edit; edit the generator instead.
-->
<WatchFace width="450" height="450">
  <Metadata key="CLOCK_TYPE" value="DIGITAL" />
  <Metadata key="PREVIEW_TIME" value="06:28" />
  <UserConfigurations>
{theme_cfg}
{font_cfg}
{seconds_cfg}
  </UserConfigurations>
  <Scene backgroundColor="#ff000000">
    <!-- Theme background (interactive). Ambient uses plain black. -->
    <PartDraw x="0" y="0" width="450" height="450">
      <Variant mode="AMBIENT" target="alpha" value="0" />
      <Rectangle x="0" y="0" width="450" height="450">
        <Fill color="[CONFIGURATION.theme.0]" />
      </Rectangle>
    </PartDraw>
    <PartDraw x="0" y="0" width="450" height="450" alpha="0">
      <Variant mode="AMBIENT" target="alpha" value="255" />
      <Rectangle x="0" y="0" width="450" height="450">
        <Fill color="#ff000000" />
      </Rectangle>
    </PartDraw>

    <!-- Seconds dot: jumps 6 degrees per second around the edge.
         Interactive only, toggleable via the "Seconds dot" setting. -->
    <BooleanConfiguration id="seconds_dot">
      <BooleanOption id="TRUE">
        <Group name="seconds_dot" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
          <Variant mode="AMBIENT" target="alpha" value="0" />
          <Transform target="angle" value="[SECOND] * 6" />
          <PartDraw x="220" y="10" width="10" height="10">
            <Ellipse x="0" y="0" width="10" height="10">
              <Fill color="[CONFIGURATION.theme.1]" />
            </Ellipse>
          </PartDraw>
        </Group>
      </BooleanOption>
      <BooleanOption id="FALSE" />
    </BooleanConfiguration>

{font_switch}
  </Scene>
</WatchFace>
"""
    out = "watchface/src/main/res/raw/watchface.xml"
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    # Validate: well-formed + expected structure.
    tree = ET.parse(out)
    root = tree.getroot()
    assert root.tag == "WatchFace"
    params = [p.attrib["expression"] for p in root.iter("Parameter")]
    assert len([p for p in params if "HOUR_1_12" in p]) == 60, len(params)
    assert len(list(root.iter("ListOption"))) == 60  # 30 config + 30 scene font
    assert len(list(root.iter("BooleanOption"))) == 2  # seconds-dot TRUE/FALSE
    assert not any("COMPLICATION" in p for p in params), "no complication refs"
    assert len(list(root.iter("ComplicationSlot"))) == 0
    fams = {fo.attrib.get("family") for fo in root.iter("Font")}
    for _, fam, _ in FONTS:
        assert fam in fams, fam
    print(f"wrote {out} ({len(xml)//1024} KB), "
          f"{len(params)} Parameters, fonts: {sorted(fams)}")


if __name__ == "__main__":
    main()
