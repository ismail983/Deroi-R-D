"""Builds the Picsart scene for Mokki & Friends Episode 1 (Brush Your Teeth), ~4:40."""
import json, random

MOKKI = "https://gcdn.picsart.com/picsart-mcp/5a88349b-de7a-4dd7-8ee9-e2385f0ef217.png"
SONG = "https://gcdn.picsart.com/picsart-mcp/f2d69eec-3e2a-493c-8ad1-ef2c3cbc3e81.mp3"        # 90 s
V_INTRO = "https://gcdn.picsart.com/picsart-mcp/e79c0ab1-5ab7-4a1d-a2dc-9f504e287b97.mp3"     # 17.0 s
V_STORY = "https://gcdn.picsart.com/picsart-mcp/0759fc9a-f8c3-404d-ac9f-f4d5ce8e0057.mp3"     # 26.0 s
V_LESSON = "https://gcdn.picsart.com/picsart-mcp/273d020b-8f6a-454b-b66f-91a80aebe288.mp3"    # 34.6 s
V_BYE = "https://gcdn.picsart.com/picsart-mcp/489a0ae2-f87e-4d71-9c57-deb54f235954.mp3"       # 15.4 s

# timeline (seconds)
T_INTRO, T_STORY, T_SONG1, T_LESSON, T_SONG2, T_BYE = 0.8, 18.5, 45.5, 136.5, 172.5, 263.5
SONG_LEN = 90.0
END = 281.0
SONGS = [(T_SONG1, T_SONG1 + SONG_LEN), (T_SONG2, T_SONG2 + SONG_LEN)]

# lyric lines, times relative to song start (from transcription)
LYRICS = [
    (9.2, 11.9, "Wake up, wake up, the sun says hi!"),
    (11.95, 14.25, "Mokki stretches to the sky!"),
    (14.3, 16.65, "Grab your brush and toothpaste too,"),
    (16.7, 19.05, "Tiny pea, just like I do!"),
    (19.1, 21.45, "Brush, brush, brush your teeth,"),
    (21.5, 23.9, "Top and bottom, up and down!"),
    (23.95, 26.3, "Brush, brush, brush your teeth,"),
    (26.35, 29.8, "Round and round and round and round!"),
    (47.9, 50.3, "Little circles, front and back,"),
    (50.35, 52.65, "Bye-bye, bye-bye, sugar snack!"),
    (52.7, 55.05, "Count with Mokki: one, two, three,"),
    (55.1, 58.2, "Shiny teeth for you and me!"),
    (67.1, 69.45, "Brush, brush, brush your teeth,"),
    (69.5, 71.9, "Top and bottom, up and down!"),
    (71.95, 74.3, "Brush, brush, brush your teeth,"),
    (74.35, 77.8, "Round and round and round and round!"),
    (81.4, 83.9, "Swish and spit, and smile so bright,"),
    (83.95, 86.3, "Morning teeth and teeth at night!"),
    (86.35, 89.6, "Ding! Sparkle!"),
]

POP = {"kind": "cubic_bezier", "control": [0.34, 1.56, 0.64, 1]}
NAVY = "#14224F"


def shape(id_, items, **kw):
    d = {"id": id_, "content": {"kind": "shape", "items": items}}
    if "transform" not in kw and "animations" not in kw or kw.get("abs"):
        d["transform"] = {"position": [0, 0], "anchor": [0, 0]}
    kw.pop("abs", None)
    d.update(kw)
    if "start" in d:
        d["timeMode"] = "layer"
    return d


def rect(pos, size, color, r=0):
    return [{"type": "rect", "position": pos, "size": size, "roundness": r}, {"type": "fill", "color": color}]


def ell(pos, size, color):
    return [{"type": "ellipse", "position": pos, "size": size}, {"type": "fill", "color": color}]


def pop_scale(dur, s=1.0):
    return {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": min(0.4, dur / 3), "value": [s, s]},
                          {"time": max(dur - 0.25, 0.5), "value": [s, s], "easing": "ease_in"}, {"time": dur, "value": [0, 0]}]}


def text(id_, t, pos, size, start, dur, color=NAVY, stroke=True, anim=True):
    c = {"kind": "text", "text": t, "font": {"size": size, "weight": 800}, "color": color, "alignment": "center"}
    if stroke:
        c["stroke"] = {"width": 14, "color": "#FFFFFF"}
    d = {"id": id_, "start": start, "duration": dur, "timeMode": "layer", "transform": {"position": pos}, "content": c}
    if anim:
        d["animations"] = {"scale": pop_scale(dur)}
    return d


L = []
# ---------- background: bathroom ----------
L.append(shape("wall", rect([960, 440], [1920, 880], "#FFF1C1")))
L.append(shape("tiles", rect([960, 980], [1920, 200], "#BFE6F7")))
L.append(shape("tileline", rect([960, 882], [1920, 8], "#8FCDEB")))
L.append(shape("window", ell([330, 330], [380, 380], "#FFFFFF")))
L.append(shape("sky", ell([330, 330], [340, 340], "#9ED8FF")))
L.append(shape("sun", ell([380, 290], [120, 120], "#FFD23F"), transform={"position": [0, 0], "anchor": [0, 0]},
               animations={"scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                     "expression": "return value*(1+0.06*math.sin(2*math.pi*time/3))"}}))
L.append(shape("mirrorframe", rect([1560, 380], [360, 430], "#1E8F6A", 70)))
L.append(shape("mirror", rect([1560, 380], [330, 400], "#DFF4FF", 60)))
L.append(shape("sinktop", rect([1560, 700], [420, 60], "#FFFFFF", 30)))
L.append(shape("sinkbase", rect([1560, 800], [300, 180], "#F4F9FF", 30)))
L.append(shape("cup", rect([1430, 630], [60, 90], "#FF9FB2", 14)))
L.append(shape("duck", ell([1700, 640], [90, 70], "#FFD23F")))
L.append(shape("duckhead", ell([1730, 600], [50, 50], "#FFD23F")))
L.append(shape("stool", rect([900, 935], [420, 70], "#E2A86B", 25)))

# ---------- bubbles during both songs ----------
random.seed(3)
for si, (a, b) in enumerate(SONGS):
    for i in range(8):
        x = random.randint(150, 1800); p = random.uniform(3, 6); off = random.uniform(0, p); s = random.randint(40, 90)
        L.append(shape(f"bubble{si}_{i}", ell([0, 0], [s, s], "#FFFFFF")[:1] +
                       [{"type": "fill", "color": "#FFFFFF", "opacity": 0.6}, {"type": "stroke", "color": "#8FCDEB", "width": 4}],
                       start=a, duration=b - a,
                       animations={"position": {"keyframes": [{"time": 0, "value": [x, 1100]}],
                                                "expression": f"local t=(time+{off:.2f})%{p:.2f}; return Vec.v2({x}+25*math.sin(t*3), 1100-t/{p:.2f}*1250)"}}))

# ---------- story props: candy + sugar bugs ----------
CANDY_IN, CANDY_OUT = T_STORY + 0.5, T_STORY + 18.5
L.append(shape("candy", [
    {"type": "group", "contents": rect([0, 0], [120, 120], "#FF6B9A", 60) +
     [{"type": "polystar", "starType": "polygon", "points": 3, "position": [-95, 0], "outerRadius": 45, "rotation": 90},
      {"type": "fill", "color": "#FFB3CC"},
      {"type": "polystar", "starType": "polygon", "points": 3, "position": [95, 0], "outerRadius": 45, "rotation": -90},
      {"type": "fill", "color": "#FFB3CC"}]}],
    start=CANDY_IN, duration=CANDY_OUT - CANDY_IN, transform={"position": [480, 560], "scale": [1.3, 1.3]},
    animations={"scale": pop_scale(CANDY_OUT - CANDY_IN, 1.3),
                "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 10*math.sin(2*math.pi*time/1.5)"}}))
BUGS_IN, BUGS_OUT = T_STORY + 9.5, T_STORY + 21.0
for i, (x, y) in enumerate([(470, 330), (1260, 330), (650, 560)]):
    L.append(shape(f"sugarbug{i}", [
        {"type": "group", "contents":
            ell([-14, -6], [16, 16], "#FFFFFF") + ell([14, -6], [16, 16], "#FFFFFF") +
            ell([-14, -6], [8, 8], NAVY)[:1] + [{"type": "fill", "color": NAVY}] +
            ell([0, 0], [80, 64], "#A98BEB")}],
        start=BUGS_IN + i * 0.4, duration=BUGS_OUT - BUGS_IN - i * 0.4, transform={"position": [x, y], "scale": [1.8, 1.8]},
        animations={"scale": pop_scale(BUGS_OUT - BUGS_IN - i * 0.4, 1.8),
                    "position": {"keyframes": [{"time": 0, "value": [x, y]}],
                                 "expression": f"return value+Vec.v2(18*math.sin(time*5+{i}), 12*math.cos(time*4+{i}))"}}))
L.append(text("storytitle", "Oh no! Sugar bugs!", [960, 130], 90, BUGS_IN + 2, 7))

# ---------- Mokki ----------
W, H = 1128, 1318
def in_songs(expr_song, expr_else):
    cond = " or ".join(f"(time>={a:.2f} and time<{b:.2f})" for a, b in SONGS)
    starts = " ".join(f"if time>={a:.2f} and time<{b:.2f} then s={a:.2f} end;" for a, b in SONGS)
    return f"local s=0; {starts} if {cond} then {expr_song} else {expr_else} end"
bounce = in_songs("local b=math.abs(math.sin(math.pi*(time-s)/0.6)); return value+Vec.v2(0,-45*b)",
                  "return value+Vec.v2(0,-10*math.sin(2*math.pi*time/1.6))")
squash = in_songs("local b=math.abs(math.sin(math.pi*(time-s)/0.6)); return Vec.v2(value.x*(1+0.04*(1-b)), value.y*(1-0.04*(1-b)))",
                  "return value")
L.append({"id": "mokki", "content": {"kind": "media", "asset": {"type": "image", "uri": MOKKI, "width": W, "height": H}},
          "transform": {"anchor": [W / 2, H], "position": [900, 1025], "scale": [0.5, 0.5]},
          "animations": {
              "scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.7, "value": [0.5, 0.5]},
                                      {"time": END - 1.0, "value": [0.5, 0.5], "easing": "ease_in"}, {"time": END, "value": [0, 0]}],
                        "expression": squash},
              "position": {"keyframes": [{"time": 0, "value": [900, 1025]}], "expression": bounce},
              "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 4*math.sin(2*math.pi*time/2.4)"}}})

# toothbrush in Mokki's hand during both songs
for si, (a, b) in enumerate(SONGS):
    L.append(shape(f"toothbrush{si}",
                   [{"type": "group", "contents": rect([0, -70], [46, 60], "#FFFFFF", 10) + rect([0, -28], [70, 26], "#4A90E2", 10) +
                     rect([0, 90], [38, 240], "#4A90E2", 19), "position": [0, 0]}],
                   parentId="mokki", start=a, duration=b - a, transform={"position": [1150, 980], "scale": [1.6, 1.6], "rotation": -60},
                   animations={"rotation": {"keyframes": [{"time": 0, "value": -60}], "expression": "return value+15*math.sin(2*math.pi*time/0.3)"},
                               "opacity": {"keyframes": [{"time": 0, "value": 0}, {"time": 0.3, "value": 1}]}}))

# ---------- titles ----------
L.append(text("title1", "Brush Your Teeth\nwith Mokki!", [960, 150], 100, 0.6, 5.0))
L.append(text("song1title", "Let's sing!", [960, 130], 96, T_SONG1 + 0.5, 6.5))
L.append(text("song2title", "Now YOU sing with Mokki!", [960, 130], 90, T_SONG2 + 0.5, 6.5))
for si, (a, b) in enumerate(SONGS):
    for li, (s, e, line) in enumerate(LYRICS):
        L.append(text(f"lyric{si}_{li}", line, [960, 140], 78, a + s, e - s, anim=False))

# lesson cards
CARDS = [(4.5, 10.5, "1. A tiny bit of toothpaste,\nas small as a pea!"),
         (10.5, 15.5, "2. Brush up and down!"),
         (15.5, 20.5, "3. Little circles, round and round!"),
         (20.5, 29.5, "4. Brush 2 times a day:\nmorning and night!"),
         (29.5, 34.6, "Get your toothbrush!")]
for i, (s, e, t) in enumerate(CARDS):
    L.append(text(f"card{i}", t, [960, 170], 84, T_LESSON + s, e - s))
L.append(text("bye", "Bye-bye, friends!\nSee you tomorrow!", [960, 150], 90, T_BYE + 7.5, END - T_BYE - 7.5))

# ---------- audio ----------
for id_, start, uri in [("v_intro", T_INTRO, V_INTRO), ("v_story", T_STORY, V_STORY), ("song1", T_SONG1, SONG),
                        ("v_lesson", T_LESSON, V_LESSON), ("song2", T_SONG2, SONG), ("v_bye", T_BYE, V_BYE)]:
    L.append({"id": id_, "start": start, "content": {"kind": "audio", "asset": {"type": "audio", "uri": uri}}})

scene = {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": END, "background": "#FFF1C1"},
         "layers": L}
json.dump(scene, open("ep01-scene.json", "w"), indent=1)
print("layers", len(L), "bytes", len(json.dumps(scene)), "duration", END)
