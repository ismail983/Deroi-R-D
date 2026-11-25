"""Episode 3 Short (1080x1920): channel sting -> Mokki's summary -> verse+chorus -> plug/towel/squeaky clean -> subscribe."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
sys.path.insert(0, os.path.join(HERE, "..", "ep03"))
import kit, shorts_kit as sk
from kit import NAVY, WHITE, YELLOW, CORAL, GREEN, POP, rect, ell, group, shape_layer, prop, sparkle_icon, mokki_rig, snap
# only the data we need from the episode script (without building it): read constants by exec of the header
src = open(os.path.join(HERE, "..", "ep03", "build_scene.py")).read()
hdr = src[: src.index("T = {\"intro\"")]
ns = {"__file__": os.path.join(HERE, "..", "ep03", "build_scene.py")}
exec(hdr, ns)
SONG, SONG_WORDS, LYRICS = ns["SONG"], ns["SONG_WORDS"], ns["LYRICS"]

ABSTRACT = "https://gcdn.picsart.com/picsart-mcp/379d7237-3a16-44e1-98da-a8927de328a8.mp3"   # "Today in Mokki World, it's bath time! Let's go!"
ABS_WORDS = [(0.343, 0.4), (0.48, 0.56), (0.64, 0.96), (1.04, 1.48), (1.6, 1.84), (1.92, 2.16), (2.24, 2.84), (2.96, 3.2), (3.28, 3.84)]
W, H = sk.W, sk.H
B = sk.STING_LEN
T_ABS = B + 0.1
A0, A1 = 4.6, 33.4            # verse 1 + chorus
B0, B1 = 71.8, 79.1           # plug, towel, squeaky clean
TA = T_ABS + 4.0
TB = TA + (A1 - A0)
TEND = TB + (B1 - B0)
END = TEND + 3.2


def song_t(s):
    if A0 <= s < A1:
        return TA + s - A0
    if B0 <= s < B1:
        return TB + s - B0
    return None


L = []
sk.sting(L, 0)
L.append(shape_layer("bg_wall", rect([540, 800], [W, 1600], "#E7F6FF"), B, END - B, absolute=True))
L.append(shape_layer("bg_tiles", rect([540, 1760], [W, 340], "#BFE6F7") + rect([540, 1592], [W, 10], "#8FCDEB"), B, END - B, absolute=True))
L.append(shape_layer("bg_window", ell([170, 200], [220, 220], "#9ED8FF") + ell([170, 200], [250, 250], WHITE), B, END - B, absolute=True))
L += kit.kid_text("hook", "Today:\nBath time!", (540, 470), 120, T_ABS, TA - T_ABS + 0.6, color="#4A90E2", wrap=950, wobble=True)
L.append(prop("hook_duck", kit.duck_icon(), (540, 900), T_ABS + 1.9, TA - T_ABS - 1.6, s=2.2, wiggle=10))
for i, (s, e, line) in enumerate(LYRICS):
    t0 = song_t(s)
    if t0 is not None:
        L += kit.kid_text(f"ly{i}", line, (540, 440), 80, t0, min(e, A1 if s < A1 else B1) - s, color=sk.KID_COLORS[i % 5], pop=False, wrap=960)
C = (540, 860)
L += kit.warm_check_demo("warm_", song_t(4.7), 2.4, C, sc=0.8)
for i in range(8):
    L.append(prop(f"storm{i}", kit.bubble_icon(30 + (i % 4) * 10), (140 + (i * 131) % 820, 650 + (i * 97) % 450), song_t(7.2) + 0.12 * i, 2.2, s=1.4, bob=15))
L.append(prop("bigduck", kit.duck_icon(), C, song_t(9.6), 2.3, s=2.4, wiggle=10))
L += kit.kid_text("splash", "Splash!", C, 150, song_t(12.1), 2.3, color="#4A90E2", wobble=True)
L += kit.scrub_demo("face_", song_t(23.9), 4.8, "face", C, sc=0.8)
L += kit.scrub_demo("feet_", song_t(28.75), A1 - 28.75, "feet", C, sc=0.8)
for i in range(6):
    x = 120 + i * 170
    L.append({"id": f"brk{i}", "start": snap(song_t(14.5)), "duration": snap(9.3), "timeMode": "layer",
              "content": {"kind": "shape", "items": kit.bubble_icon(30 + 6 * i)},
              "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 2000]}],
                                          "expression": f"local t=(time+{i * 0.5})%3.5; return Vec.v2({x}+30*math.sin(t*3), 2000-t/3.5*2100)"}}})
L += kit.kid_text("bubbles", "Splish, splash!", C, 120, song_t(15.0), 4.0, color="#9B59D0", wobble=True)
L += kit.plug_demo("plug_", song_t(71.9), 2.4, C, sc=0.8)
L += kit.dry_demo("towel_", song_t(74.35), 2.3, C, sc=0.8)
for i, (x, y) in enumerate([(220, 650), (860, 640), (200, 1060), (880, 1060), (540, 560)]):
    L.append(prop(f"clean{i}", sparkle_icon(60, YELLOW), (x, y), song_t(76.7) + i * 0.1, TEND - song_t(76.7) - i * 0.1, spin=200))
L += kit.kid_text("cleantxt", "Squeaky clean!", (540, 860), 120, song_t(76.8), TEND - song_t(76.8), color="#2BB673", wobble=True)

words = [(T_ABS + s, T_ABS + e, 0) for s, e in ABS_WORDS]
for s, e in SONG_WORDS:
    t = song_t(s)
    if t is not None:
        words.append((t, t + (e - s), 0))
bounce = f"if time>={TA:.2f} and time<{TEND:.2f} then local b=math.abs(math.sin(math.pi*(time-{TA:.2f})/0.577)); return value+Vec.v2(0,-40*b) end; return value"
L += mokki_rig("mokki", words, [{"time": 0, "value": [540, 2800], "easing": "step"}, {"time": B, "value": [540, 2400], "easing": POP},
                                {"time": B + 0.5, "value": [540, 1760]}], scale=0.5, box=(W, H), pos_expr=bounce,
               scale_keys=[{"time": 0, "value": [0.5, 0.5]}, {"time": TEND, "value": [0.5, 0.5], "easing": "ease_in_out"},
                           {"time": TEND + 0.5, "value": [0.42, 0.42]}])
sk.end_card(L, TEND, END - TEND)
L.append({"id": "a_abs", "start": snap(T_ABS), "content": {"kind": "audio", "asset": {"type": "audio", "uri": ABSTRACT}}})
L.append(sk.audio_trim("a_songA", TA, SONG, A0, A1))
L.append(sk.audio_trim("a_songB", TB, SONG, B0, B1))
sk.finish(L, END, os.path.join(HERE, "short-ep03-scene.json"))
print("short ep03", round(END, 2), "s,", len(L), "layers")
