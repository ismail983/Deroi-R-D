"""Episode 2 Short (1080x1920): channel sting -> Mokki's summary -> verse+chorus -> rinse/dry/sparkly clean -> subscribe."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
sys.path.insert(0, os.path.join(HERE, "..", "ep02"))
import kit, shorts_kit as sk
from kit import NAVY, WHITE, YELLOW, CORAL, GREEN, POP, rect, ell, group, shape_layer, prop, sparkle_icon, mokki_rig, snap
# only the data we need from the episode script (without building it): read constants by exec of the header
src = open(os.path.join(HERE, "..", "ep02", "build_scene.py")).read()
hdr = src[: src.index("# ---------------------------------------------------------------- timeline")]
ns = {"__file__": os.path.join(HERE, "..", "ep02", "build_scene.py")}
exec(hdr, ns)
SONG, SONG_WORDS, LYRICS = ns["SONG"], ns["SONG_WORDS"], ns["LYRICS"]

ABSTRACT = "https://gcdn.picsart.com/picsart-mcp/fe5eaae4-2169-44b0-a33e-979afd662c63.mp3"   # "Today in Mokki World, we learn to wash our hands! Let's go!"
ABS_WORDS = [(0.08, 0.48), (0.56, 0.64), (0.68, 1.04), (1.2, 1.52), (1.68, 1.84), (1.96, 2.08), (2.16, 2.24), (2.36, 2.48), (2.56, 2.72), (2.96, 3.36), (3.52, 3.76), (3.84, 4.48)]
W, H = sk.W, sk.H
B = sk.STING_LEN
T_ABS = B + 0.1
A0, A1 = 9.0, 27.5            # verse 1 + chorus
B0, B1 = 73.6, 83.2           # rinse, dry, sparkly clean
TA = T_ABS + 4.6
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
L.append(shape_layer("bg_wall", rect([540, 800], [W, 1600], "#FFF1C1"), B, END - B, absolute=True))
L.append(shape_layer("bg_tiles", rect([540, 1760], [W, 340], "#BFE6F7") + rect([540, 1592], [W, 10], "#8FCDEB"), B, END - B, absolute=True))
L.append(shape_layer("bg_window", ell([170, 200], [220, 220], "#9ED8FF") + ell([170, 200], [250, 250], WHITE), B, END - B, absolute=True))
L += kit.kid_text("hook", "Today:\nWash our hands!", (540, 470), 110, T_ABS, TA - T_ABS + 0.6, color=CORAL, wrap=950, wobble=True)
L += kit.two_hands("hook_h_", T_ABS + 2.3, TA - T_ABS - 2.0, (540, 900), 0.9, rub="rub")
for i, (s, e, line) in enumerate(LYRICS):
    t0 = song_t(s)
    if t0 is not None:
        L += kit.kid_text(f"ly{i}", line, (540, 440), 80, t0, min(e, A1 if s < A1 else B1) - s, color=sk.KID_COLORS[i % 5], pop=False, wrap=960)
C = (540, 860)
L += kit.water_demo("wat_", song_t(9.2), 4.55, C, sc=0.8)
L += kit.soap_demo("soap_", song_t(13.8), 4.5, C, sc=0.8)
L += kit.rub_demo("rub_", song_t(18.4), A1 - 18.4, "rub", C, sc=0.8, germs_at=song_t(23.3))
L += kit.rinse_demo("rin_", song_t(73.75), 2.35, C, sc=0.8)
L += kit.dry_demo("dry_", song_t(76.1), 4.5, C, sc=0.8)
for i, (x, y) in enumerate([(220, 650), (860, 640), (200, 1060), (880, 1060), (540, 560)]):
    L.append(prop(f"clean{i}", sparkle_icon(60, YELLOW), (x, y), song_t(80.7) + i * 0.1, TEND - song_t(80.7) - i * 0.1, spin=200))
L += kit.kid_text("cleantxt", "Sparkly clean!", (540, 860), 120, song_t(80.9), TEND - song_t(80.9), color="#2BB673", wobble=True)

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
sk.finish(L, END, os.path.join(HERE, "short-ep02-scene.json"))
print("short ep02", round(END, 2), "s,", len(L), "layers")
