"""YouTube Short (1080x1920, ~35 s) cut from Episode 1: hook + song verse/chorus + outro line + subscribe end card."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
sys.path.insert(0, os.path.join(HERE, "..", "ep01"))
import kit, text_check
from kit import (NAVY, WHITE, YELLOW, CORAL, GREEN, PINK, YT_RED, POP, rect, ell, group, shape_layer, prop, audio, snap,
                 sparkle_icon, bell_icon, mokki_rig, pop_scale)
from word_timings import INTRO, SONG_WORDS

SONG = "https://gcdn.picsart.com/picsart-mcp/f2d69eec-3e2a-493c-8ad1-ef2c3cbc3e81.mp3"
V_INTRO = "https://gcdn.picsart.com/picsart-mcp/e79c0ab1-5ab7-4a1d-a2dc-9f504e287b97.mp3"
W, H = 1080, 1920

HOOK = 2.45                                  # "Hi friends! It's me, Mokki!"
A0, A1 = 9.0, 30.0                           # song: verse 1 + chorus
B0, B1 = 81.2, 89.8                          # song: swish & spit ... Ding! Sparkle!
TA = HOOK                                    # short time where segment A starts
TB = TA + (A1 - A0)
TEND = TB + (B1 - B0)
END = TEND + 3.2


def song_t(s):
    """song time -> short time (None when the moment is cut out)."""
    if A0 <= s < A1:
        return TA + s - A0
    if B0 <= s < B1:
        return TB + s - B0
    return None


L = []
# ---- background (vertical bathroom)
L.append(shape_layer("bg_wall", rect([540, 800], [1080, 1600], "#FFF1C1"), 0, END, absolute=True))
L.append(shape_layer("bg_tiles", rect([540, 1760], [1080, 340], "#BFE6F7") + rect([540, 1592], [1080, 10], "#8FCDEB"), 0, END, absolute=True))
L.append(shape_layer("bg_window", ell([170, 200], [220, 220], "#9ED8FF") + ell([170, 200], [250, 250], WHITE), 0, END, absolute=True))
L.append(shape_layer("bg_sun", ell([0, 0], [80, 80], YELLOW), 0, END, (195, 180)))
L.append(shape_layer("bg_mirror", rect([900, 230], [200, 250], "#DFF4FF", 40) + rect([900, 230], [230, 280], GREEN, 50), 0, END, absolute=True))

# ---- floating bubbles
for i, (x, p, off) in enumerate([(120, 4.2, 0.3), (330, 5.1, 2.0), (760, 4.6, 1.1), (960, 5.6, 3.2), (560, 3.9, 2.6)]):
    L.append({"id": f"bub{i}", "start": TA, "duration": snap(TEND - TA), "timeMode": "layer",
              "content": {"kind": "shape", "items": [{"type": "ellipse", "position": [0, 0], "size": [60, 60]},
                                                     {"type": "fill", "color": WHITE, "opacity": 0.6},
                                                     {"type": "stroke", "color": "#8FCDEB", "width": 4}]},
              "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 2000]}],
                                          "expression": f"local t=(time+{off})%{p}; return Vec.v2({x}+25*math.sin(t*3), 2000-t/{p}*2100)"}}})

# ---- hook text
L += kit.kid_text("hook", "Brush with Mokki!", (540, 330), 110, 0.1, HOOK + 1.2, color=CORAL, wrap=950, wobble=True)

# ---- lyrics (only the lines that are in the cut)
LYRICS = [(9.2, 11.9, "Wake up, wake up, the sun says hi!"), (11.95, 14.25, "Mokki stretches to the sky!"),
          (14.3, 16.65, "Grab your brush and toothpaste too,"), (16.7, 19.05, "Tiny pea, just like I do!"),
          (19.1, 21.45, "Brush, brush, brush your teeth,"), (21.5, 23.9, "Top and bottom, up and down!"),
          (23.95, 26.3, "Brush, brush, brush your teeth,"), (26.35, 29.8, "Round and round and round and round!"),
          (81.4, 83.9, "Swish and spit, and smile so bright,"), (83.95, 86.3, "Morning teeth and teeth at night!"),
          (86.35, 89.6, "Ding! Sparkle!")]
COLORS = ["#F0506E", "#2BB673", "#4A90E2", "#FF8A00", "#9B59D0"]
for i, (s, e, line) in enumerate(LYRICS):
    t0 = song_t(s)
    L += kit.kid_text(f"ly{i}", line, (540, 330), 84, t0, e - s, color=COLORS[i % 5], pop=False, wrap=960)

# ---- demos in the upper middle, Mokki below
C = (540, 860)
L.append(prop("sun", [{"type": "polystar", "starType": "star", "points": 12, "position": [0, 0], "outerRadius": 120, "innerRadius": 85},
                     {"type": "fill", "color": "#FFB23F"}], (540, 860), song_t(9.2), 2.7, wiggle=12))
L.append(shape_layer("sunface", ell([0, 0], [160, 160], YELLOW), song_t(9.2), 2.7, (540, 860), {"scale": pop_scale(2.7)}))
L += kit.toothpaste_demo("tp_", song_t(14.3), 4.75, center=C, sc=0.8)
L += kit.mouth_demo("ud_", song_t(19.1), 7.2, "updown", center=C, sc=0.8)
L += kit.mouth_demo("rr_", song_t(26.35), A1 - 26.35, "circles", center=C, sc=0.8)
L += kit.swish_demo("sw_", song_t(81.4), 2.5, center=C, sc=0.8)
L.append(prop("msun", [{"type": "ellipse", "position": [0, 0], "size": [200, 200]}, {"type": "fill", "color": YELLOW}], (360, 860), song_t(84.0), 2.4))
L.append(prop("mmoon", [group(ell([45, -20], [170, 170], "#FFF1C1")), group(ell([0, 0], [200, 200], "#FFE58A"))], (720, 860), song_t(85.2), 1.2))
for i, (x, y) in enumerate([(250, 650), (830, 640), (200, 1050), (880, 1060), (540, 560), (540, 1150)]):
    L.append(prop(f"ding{i}", sparkle_icon(60, YELLOW), (x, y), song_t(86.4) + i * 0.1, TEND - song_t(86.4) - i * 0.1, spin=200))

# ---- Mokki (bottom), lip-synced to the hook line and the song
words = [(s, e, 0) for s, e, w in INTRO if s < HOOK and not w.startswith("[")]
for s, e in SONG_WORDS:
    t = song_t(s)
    if t is not None:
        words.append((t, t + (e - s), 0))
songs_cond = f"(time>={TA:.2f} and time<{TEND:.2f})"
bounce = f"if {songs_cond} then local b=math.abs(math.sin(math.pi*(time-{TA:.2f})/0.6)); return value+Vec.v2(0,-40*b) end; return value"
L += mokki_rig("mokki", words, [{"time": 0, "value": [540, 2400], "easing": POP}, {"time": 0.5, "value": [540, 1760]}], scale=0.5, box=(W, H),
               pos_expr=bounce,
               scale_keys=[{"time": 0, "value": [0.5, 0.5]}, {"time": TEND, "value": [0.5, 0.5], "easing": "ease_in_out"},
                           {"time": TEND + 0.5, "value": [0.42, 0.42]}])
L.append({"id": "hbrush", "parentId": "mokki", "start": TA, "duration": snap(TEND - TA), "timeMode": "layer",
          "transform": {"position": kit.hand_pos((W, H)), "scale": [1.3 * kit.box_map((W, H))[0] / kit.S, 1.3 * kit.box_map((W, H))[0] / kit.S], "rotation": -60},
          "content": {"kind": "shape", "items": [group(rect([0, -70], [46, 60], WHITE, 10) + rect([0, -28], [70, 26], "#4A90E2", 10) +
                                                       rect([0, 90], [38, 240], "#4A90E2", 19))]},
          "animations": {"rotation": {"keyframes": [{"time": 0, "value": -60}], "expression": "return value+15*math.sin(2*math.pi*time/0.3)"}}})

# ---- end card: subscribe
L += kit.kid_text("end1", "More songs\nwith Mokki!", (540, 420), 110, TEND, END - TEND, color=CORAL)
L.append(shape_layer("sub_btn", [{"type": "rect", "position": [0, 0], "size": [640, 170], "roundness": 85},
                                 {"type": "fill", "color": YT_RED}], TEND + 0.3, END - TEND - 0.3, (500, 820),
                     {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1, 1]}],
                                "expression": "return value*(1+0.05*math.sin(time*8))"}}))
L += kit.kid_text("sub_txt", "SUBSCRIBE", (500, 850), 80, TEND + 0.4, END - TEND - 0.4, color=WHITE, stroke=None, letters=False)
L.append(shape_layer("bell", bell_icon(NAVY), TEND + 0.6, END - TEND - 0.6, (900, 820),
                     {"scale": pop_scale(END - TEND - 0.6, 1.3),
                      "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 25*math.sin(time*20)*math.max(0,1-time/2)"}}))

# ---- audio: hook line + two cuts of the song
L.append({"id": "a_hook", "start": 0, "duration": HOOK,
          "content": {"kind": "audio", "asset": {"type": "audio", "uri": V_INTRO}, "trim": {"in": 0, "out": HOOK}}})
L.append({"id": "a_songA", "start": snap(TA), "duration": snap(A1 - A0),
          "content": {"kind": "audio", "asset": {"type": "audio", "uri": SONG}, "trim": {"in": A0, "out": A1}}})
L.append({"id": "a_songB", "start": snap(TB), "duration": snap(B1 - B0),
          "content": {"kind": "audio", "asset": {"type": "audio", "uri": SONG}, "trim": {"in": B0, "out": B1}}})

for l in L:
    for k in ("start", "duration"):
        if k in l:
            l[k] = snap(l[k])
text_check.resolve(L)
scene = {"version": "1.0", "composition": {"width": W, "height": H, "fps": 30, "duration": snap(END), "background": "#FFF1C1"}, "layers": L}
json.dump(scene, open(os.path.join(HERE, "short-ep01-scene.json"), "w"), separators=(",", ":"))
print("short", snap(END), "s,", len(L), "layers")
