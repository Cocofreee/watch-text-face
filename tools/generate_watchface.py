"""Generate res/raw/watchface.xml from verified expression strings.

Single source of truth for the time-words expressions (also verified by
tools/verify_time_words.py). Run:  .venv/bin/python tools/generate_watchface.py
"""
import xml.etree.ElementTree as ET

HOUR_RAW = '[HOUR_1_12] == 1 ? "One" : ([HOUR_1_12] == 2 ? "Two" : ([HOUR_1_12] == 3 ? "Three" : ([HOUR_1_12] == 4 ? "Four" : ([HOUR_1_12] == 5 ? "Five" : ([HOUR_1_12] == 6 ? "Six" : ([HOUR_1_12] == 7 ? "Seven" : ([HOUR_1_12] == 8 ? "Eight" : ([HOUR_1_12] == 9 ? "Nine" : ([HOUR_1_12] == 10 ? "Ten" : ([HOUR_1_12] == 11 ? "Eleven" : "Twelve"))))))))))'
TENS_RAW = '[MINUTE] == 0 ? "O\'Clock" : ([MINUTE] < 10 ? "O" : ([MINUTE] < 20 ? ([MINUTE] == 10 ? "Ten" : ([MINUTE] == 11 ? "Eleven" : ([MINUTE] == 12 ? "Twelve" : ([MINUTE] == 13 ? "Thirteen" : ([MINUTE] == 14 ? "Fourteen" : ([MINUTE] == 15 ? "Fifteen" : ([MINUTE] == 16 ? "Sixteen" : ([MINUTE] == 17 ? "Seventeen" : ([MINUTE] == 18 ? "Eighteen" : "Nineteen"))))))))) : ([MINUTE] < 30 ? "Twenty" : ([MINUTE] < 40 ? "Thirty" : ([MINUTE] < 50 ? "Forty" : "Fifty")))))'
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
    ("30", "mogra", "Mogra (fun display)"),
    ("31", "rubikmarkerhatch", "Rubik Marker (fun marker)"),
    ("32", "gorditas", "Gorditas (fun rounded)"),
    ("33", "sonsieone", "Sonsie One (fun chunky)"),
    ("34", "berkshireswash", "Berkshire Swash (fun swash)"),
    ("35", "racingsansone", "Racing Sans (fun speedy)"),
    ("36", "cutivemono", "Cutive Mono (fun mono)"),
    ("37", "arvo", "Arvo (classic slab)"),
    ("38", "newrocker", "New Rocker (fun rock)"),
    ("39", "metalmania", "Metal Mania (fun metal)"),
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
    assert len(FONTS) == 40

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
    flip_cfg = ('    <BooleanConfiguration id="autoflip"\n'
                '        displayName="autoflip_label"\n'
                '        screenReaderText="autoflip_label"\n'
                '        defaultValue="TRUE" />')

    white, black, grey = "#ffffffff", "#ff000000", "#ffbbbbbb"

    def el(x, y, w, h, style):
        return f'<Ellipse x="{x}" y="{y}" width="{w}" height="{h}">{style}</Ellipse>'

    # Climb-test panda: single black-ears design (~108x120 in a 120x130
    # PartDraw). Stride frames differ only in limb offsets + bob.
    def panda_stride(frame):
        lo = 10 if frame == 0 else -10
        ao = 9 if frame == 0 else -9
        bob = 0 if frame == 0 else -4
        e = []
        for lx in (24 + lo, 68 - lo):
            e.append(el(lx, 93 + bob, 28, 30, f'<Fill color="{black}" />'))
            e.append(el(lx, 93 + bob, 28, 30, f'<Stroke thickness="2" color="{white}" />'))
        for ax, ay in ((6, 61 + ao), (90, 61 - ao)):
            e.append(el(ax, ay + bob, 24, 32, f'<Fill color="{black}" />'))
            e.append(el(ax, ay + bob, 24, 32, f'<Stroke thickness="2" color="{white}" />'))
        e.append(el(22, 53 + bob, 76, 56, f'<Fill color="{white}" />'))
        e.append(el(22, 53 + bob, 76, 56, f'<Stroke thickness="3" color="{black}" />'))
        for ex in (14, 84):
            e.append(el(ex, 3 + bob, 22, 22, f'<Fill color="{black}" />'))
        e.append(el(22, 17 + bob, 76, 58, f'<Fill color="{white}" />'))
        e.append(el(22, 17 + bob, 76, 58, f'<Stroke thickness="3" color="{black}" />'))
        for px in (33, 69):
            e.append(el(px, 29 + bob, 18, 22, f'<Fill color="{black}" />'))
        for gx in (38, 74):
            e.append(el(gx, 32 + bob, 5, 5, f'<Fill color="{white}" />'))
        e.append(el(54, 55 + bob, 12, 8, f'<Fill color="{black}" />'))
        e.append(f'<Arc centerX="60" centerY="{60 + bob}" width="24" height="16" startAngle="120" endAngle="240"><Stroke thickness="2" color="{black}" /></Arc>')
        shapes = "\n".join(f"          {s}" for s in e)
        return (f'        <PartDraw x="0" y="0" width="120" height="130">\n'
                f'{shapes}\n'
                f'        </PartDraw>')

    # 15s climb loop expressions (escaped for XML attributes on use).
    cyc = "([SECOND] % 15)"
    cyc7 = f"(({cyc}) - 7)"
    dx_raw = (f"({cyc} <= 7 ? (({cyc} <= 3) ? (({cyc}) * 6.0) : ((7 - ({cyc})) * 6.0)) : "
              f"(({cyc7} <= 3) ? (({cyc7}) * 6.0) : ((7 - ({cyc7})) * 6.0)))")
    dy_raw = (f"({cyc} <= 7 ? (0 - (({cyc}) * 245.0 / 7.0)) : "
              f"((({cyc7}) * 245.0 / 7.0) - 245.0))")
    ang_raw = f"({cyc} <= 7 ? 0 : (0 - (({cyc7}) * 360.0 / 7.0)))"
    dx, dy, ang = esc(dx_raw), esc(dy_raw), esc(ang_raw)

    panda_block = f"""    <!-- Panda climb (TEST): 15s loop on the right edge — walks up
         sec 0-7 with alternating stride, tumbles down sec 8-14.
         Interactive only, toggleable via "Panda seconds". -->
    <BooleanConfiguration id="seconds_dot">
      <BooleanOption id="TRUE">
        <Group name="panda_climb" x="0" y="0" width="450" height="450">
          <Variant mode="AMBIENT" target="alpha" value="0" />
          <Transform target="x" value="{dx}" />
          <Transform target="y" value="{dy}" />
          <Group name="panda_tumble" x="283" y="319" width="120" height="130" pivotX="0.5" pivotY="0.5">
            <Transform target="angle" value="{ang}" />
          <Condition>
            <Expressions>
              <Expression name="stride_even"><![CDATA[[SECOND] % 2 == 0]]></Expression>
            </Expressions>
            <Compare expression="stride_even">
{panda_stride(0)}
            </Compare>
            <Default>
{panda_stride(1)}
            </Default>
          </Condition>
          </Group>
        </Group>
      </BooleanOption>
      <BooleanOption id="FALSE" />
    </BooleanConfiguration>"""

    rainbow_block = """    <!-- Rainbow hour: vivid sweep arc over the top half during the first
         30 seconds of each hour. Interactive only. -->
    <Condition>
      <Expressions>
        <Expression name="rainbow_on"><![CDATA[[MINUTE] == 0 && [SECOND] < 30]]></Expression>
      </Expressions>
      <Compare expression="rainbow_on">
        <PartDraw x="10" y="10" width="430" height="430">
          <Variant mode="AMBIENT" target="alpha" value="0" />
          <Arc centerX="215" centerY="215" width="430" height="430" startAngle="270" endAngle="90">
            <Stroke thickness="14" cap="ROUND">
              <SweepGradient centerX="215" centerY="215" startAngle="270" endAngle="90" direction="CLOCKWISE" colors="#ffff0000 #ffff8000 #ffffff00 #ff00ff00 #ff00ffff #ff0000ff #ffff00ff" positions="" />
            </Stroke>
          </Arc>
        </PartDraw>
      </Compare>
    </Condition>"""

    flip_expr = esc('(([CONFIGURATION.autoflip] == "TRUE") && ([ACCELEROMETER_Y] > 5)) ? 180 : 0')

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
  mono-chrome themes (ColorConfiguration), 40 bundled fonts (ListConfiguration),
  panda seconds marker, rainbow hour, flip-for-others. Generated by
  tools/generate_watchface.py — do not hand-edit; edit the generator instead.
-->
<WatchFace width="450" height="450">
  <Metadata key="CLOCK_TYPE" value="DIGITAL" />
  <Metadata key="PREVIEW_TIME" value="06:28" />
  <UserConfigurations>
{theme_cfg}
{font_cfg}
{seconds_cfg}
{flip_cfg}
  </UserConfigurations>
  <Scene backgroundColor="#ff000000">
  <Group name="root" x="0" y="0" width="450" height="450" pivotX="0.5" pivotY="0.5">
    <Transform target="angle" value="{flip_expr}" />
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

{rainbow_block}

{panda_block}

{font_switch}
  </Group>
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
    assert len([p for p in params if "HOUR_1_12" in p]) == 80, len(params)
    assert len(list(root.iter("ListOption"))) == 80  # 40 config + 40 scene font
    assert len(list(root.iter("BooleanOption"))) == 2  # seconds-dot TRUE/FALSE
    assert not any("COMPLICATION" in p for p in params), "no complication refs"
    assert len(list(root.iter("ComplicationSlot"))) == 0
    assert root.find(".//SweepGradient") is not None, "rainbow gradient"
    assert root.find(".//Group[@name='panda_climb']") is not None, "panda climb"
    assert root.find(".//Group[@name='panda_tumble']") is not None, "panda tumble"
    assert root.find(".//Group[@name='root']") is not None, "flip root"
    fams = {fo.attrib.get("family") for fo in root.iter("Font")}
    for _, fam, _ in FONTS:
        assert fam in fams, fam
    print(f"wrote {out} ({len(xml)//1024} KB), "
          f"{len(params)} Parameters, fonts: {sorted(fams)}")


if __name__ == "__main__":
    main()
