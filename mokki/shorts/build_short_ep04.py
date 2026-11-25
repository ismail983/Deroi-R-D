"""Episode 4 Short (1080x1920): channel sting -> Mokki's summary -> verse 1 + chorus -> rainbow plate outro -> subscribe."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import kit, shorts_kit as sk, veggies as vg
from kit import NAVY, WHITE, YELLOW, CORAL, POP, rect, ell, group, shape_layer, prop, sparkle_icon, heart_icon, mokki_rig, snap
src = open(os.path.join(HERE, "..", "ep04", "build_scene.py")).read()
hdr = src[: src.index("T = {\"intro\"")]
ns = {"__file__": os.path.join(HERE, "..", "ep04", "build_scene.py")}
exec(hdr, ns)
SONG, SONG_WORDS, LYRICS, ABSTRACT = ns["SONG"], ns["SONG_WORDS"], ns["LYRICS"], ns["ABSTRACT"]
# "Today in Mokki World, we eat yummy vegetables! Let's go!"
ABS_WORDS = [(0.343, 0.4), (0.48, 0.56), (0.64, 0.96), (1.04, 1.48), (1.6, 1.76), (1.84, 2.08), (2.24, 2.56), (2.64, 3.52), (3.68, 3.92), (4.12, 4.64)]
W, H = sk.W, sk.H
B = sk.STING_LEN
T_ABS = B + 0.1
A0, A1 = 9.3, 28.4            # verse 1 + chorus
B0, B1 = 77.4, 87.2           # rainbow plate, strong & healthy, yummy yummy yay
TA = T_ABS + 4.9
TB = TA + (A1 - A0)
TEND = TB + (B1 - B0)
END = TEND + 3.2
VEG_ORDER = ["carrot", "broccoli", "tomato", "corn", "peas", "eggplant"]


def song_t(s):
    if A0 <= s < A1:
        return TA + s - A0
    if B0 <= s < B1:
        return TB + s - B0
    return None


L = []
sk.sting(L, 0)
L.append(shape_layer("bg_sky", rect([540, 700], [W, 1400], "#9ED8FF"), B, END - B, absolute=True))
L.append(shape_layer("bg_sun", ell([900, 200], [200, 200], "#FFD23F") + ell([900, 200], [260, 260], "#FFE58A"), B, END - B, absolute=True))
L.append(shape_layer("bg_grass", rect([540, 1660], [W, 520], "#8BD36B") + ell([540, 1420], [1600, 200], "#7BC85E"), B, END - B, absolute=True))
L.append(shape_layer("bg_soil", rect([540, 1500], [W, 60], "#8A5A3C", 30), B, END - B, absolute=True))
tops = []
for x in range(60, 1080, 140):
    tops += [vg.leaf([x, 1480], -25, (24, 70)), vg.leaf([x, 1480], 0, (24, 80)), vg.leaf([x, 1480], 25, (24, 70))]
L.append(shape_layer("bg_tops", tops, B, END - B, absolute=True))
L += kit.kid_text("hook", "Today:\nYummy veggies!", (540, 430), 110, T_ABS, TA - T_ABS + 0.3, color=vg.ORANGE, wrap=950, wobble=True)
for i, v in enumerate(VEG_ORDER):
    x, y = 200 + (i % 3) * 340, 820 + (i // 3) * 300
    L.append(vg.veg_layer(f"hook_v{i}", v, (x, y), T_ABS + 1.6 + 0.2 * i, TA - T_ABS - 1.8 - 0.2 * i, s=0.9, wiggle=12))
for i, (s, e, line) in enumerate(LYRICS):
    t0 = song_t(s)
    if t0 is not None:
        L += kit.kid_text(f"ly{i}", line, (540, 400), 80, t0, min(e, A1 if s < A1 else B1) - s, color=sk.KID_COLORS[i % 5], pop=False, wrap=960)
C = (540, 860)
L += vg.veg_card_demo("carrot_", song_t(9.45), 2.35, "carrot", C, sc=0.8)
L += vg.eye_demo("eye_", song_t(11.85), 2.3, C, sc=0.8)
L += vg.veg_card_demo("broc_", song_t(14.2), 2.35, "broccoli", C, sc=0.8)
L += vg.bite_demo("more_", song_t(16.55), 2.35, "broccoli", C, sc=0.8, bites=(0.5, 1.2))
L += vg.rainbow_plate_demo("plate_", song_t(18.95), 2.3, C, sc=0.8)
L += vg.grow_demo("grow_", song_t(21.25), 2.4, C, sc=0.8)
L += vg.bite_demo("bite_", song_t(23.65), 2.3, "carrot", C, sc=0.8, bites=(0.6,))
t_sky = song_t(25.95)
L += kit.kid_text("skytxt", "Reach the sky!", C, 110, t_sky + 0.2, TB - t_sky - 0.2, color="#4A90E2", wobble=True)
for i, v in enumerate(VEG_ORDER):
    x = 120 + i * 168
    L.append({"id": f"up{i}", "start": snap(t_sky + 0.1 * i), "duration": snap(TB - t_sky - 0.1 * i), "timeMode": "layer",
              "content": {"kind": "shape", "items": vg.VEG[v]()},
              "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 1400], "easing": "ease_out"}, {"time": TB - t_sky - 0.1 * i, "value": [x, 600]}]},
                             "scale": {"keyframes": [{"time": 0, "value": [0.55, 0.55]}]},
                             "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 15*math.sin(time*6)"}}})
L += vg.rainbow_plate_demo("oplate_", song_t(77.45), 2.55, C, sc=0.8)
L += vg.grow_demo("ogrow_", song_t(80.0), 2.6, C, sc=0.8)
L += kit.kid_text("yay", "Yummy, yummy, yay!", C, 110, song_t(82.7), TEND - song_t(82.7), color="#E84393", wobble=True, wrap=900)
for i, (x, y) in enumerate([(220, 650), (860, 640), (200, 1060), (880, 1060), (540, 560)]):
    L.append(prop(f"yaysp{i}", sparkle_icon(60, YELLOW), (x, y), song_t(82.7) + i * 0.1, TEND - song_t(82.7) - i * 0.1, spin=200))

words = [(T_ABS + s, T_ABS + e, 0) for s, e in ABS_WORDS]
for s, e in SONG_WORDS:
    t = song_t(s)
    if t is not None:
        words.append((t, t + (e - s), 0))
bounce = f"if time>={TA:.2f} and time<{TEND:.2f} then local b=math.abs(math.sin(math.pi*(time-{TA:.2f})/0.59)); return value+Vec.v2(0,-40*b) end; return value"
L += mokki_rig("mokki", words, [{"time": 0, "value": [540, 2800], "easing": "step"}, {"time": B, "value": [540, 2400], "easing": POP},
                                {"time": B + 0.5, "value": [540, 1760]}], scale=0.5, box=(W, H), pos_expr=bounce,
               scale_keys=[{"time": 0, "value": [0.5, 0.5]}, {"time": TEND, "value": [0.5, 0.5], "easing": "ease_in_out"},
                           {"time": TEND + 0.5, "value": [0.42, 0.42]}])
sk.end_card(L, TEND, END - TEND)
L.append({"id": "a_abs", "start": snap(T_ABS), "content": {"kind": "audio", "asset": {"type": "audio", "uri": ABSTRACT}}})
L.append(sk.audio_trim("a_songA", TA, SONG, A0, A1))
L.append(sk.audio_trim("a_songB", TB, SONG, B0, B1))
sk.finish(L, END, os.path.join(HERE, "short-ep04-scene.json"))
print("short ep04", round(END, 2), "s,", len(L), "layers")
