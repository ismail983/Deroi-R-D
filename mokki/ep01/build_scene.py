"""Builds the Picsart scene for Mokki & Friends Episode 1 (Brush Your Teeth), ~4:41.

v2: lip-synced mouth, blinking eyes, four sets (bedroom day, bathroom, lesson board, bedroom night)
and props timed to the spoken words and lyrics.
"""
import json, random
from word_timings import INTRO, STORY, LESSON, BYE, SONG_WORDS, word_time as wt

MOKKI = "https://gcdn.picsart.com/picsart-mcp/b11868fb-b61c-4d7f-81cf-7a532ef53e52.png"   # mouthless cutout
SONG = "https://gcdn.picsart.com/picsart-mcp/f2d69eec-3e2a-493c-8ad1-ef2c3cbc3e81.mp3"
V_INTRO = "https://gcdn.picsart.com/picsart-mcp/e79c0ab1-5ab7-4a1d-a2dc-9f504e287b97.mp3"
V_STORY = "https://gcdn.picsart.com/picsart-mcp/0759fc9a-f8c3-404d-ac9f-f4d5ce8e0057.mp3"
V_LESSON = "https://gcdn.picsart.com/picsart-mcp/273d020b-8f6a-454b-b66f-91a80aebe288.mp3"
V_BYE = "https://gcdn.picsart.com/picsart-mcp/489a0ae2-f87e-4d71-9c57-deb54f235954.mp3"

T_INTRO, T_STORY, T_SONG1, T_LESSON, T_SONG2, T_BYE = 0.8, 18.5, 45.5, 136.5, 172.5, 263.5
SONG_LEN, END = 90.0, 281.0
SONGS = [(T_SONG1, T_SONG1 + SONG_LEN), (T_SONG2, T_SONG2 + SONG_LEN)]
# set changes happen at the peak of a wipe
CUT_BATH1, CUT_LESSON, CUT_BATH2, CUT_NIGHT = 16.25, 136.25, 172.25, 263.25

NAVY, BODY, GREEN, CORAL, PINK, YELLOW, WHITE = "#14224F", "#8EEBC4", "#1E8F6A", "#FF6B5E", "#FF9FB2", "#FFD23F", "#FFFFFF"
POP = {"kind": "cubic_bezier", "control": [0.34, 1.56, 0.64, 1]}

LYRICS = [
    (9.2, 11.9, "Wake up, wake up, the sun says hi!"), (11.95, 14.25, "Mokki stretches to the sky!"),
    (14.3, 16.65, "Grab your brush and toothpaste too,"), (16.7, 19.05, "Tiny pea, just like I do!"),
    (19.1, 21.45, "Brush, brush, brush your teeth,"), (21.5, 23.9, "Top and bottom, up and down!"),
    (23.95, 26.3, "Brush, brush, brush your teeth,"), (26.35, 29.8, "Round and round and round and round!"),
    (47.9, 50.3, "Little circles, front and back,"), (50.35, 52.65, "Bye-bye, bye-bye, sugar snack!"),
    (52.7, 55.05, "Count with Mokki: one, two, three,"), (55.1, 58.2, "Shiny teeth for you and me!"),
    (67.1, 69.45, "Brush, brush, brush your teeth,"), (69.5, 71.9, "Top and bottom, up and down!"),
    (71.95, 74.3, "Brush, brush, brush your teeth,"), (74.35, 77.8, "Round and round and round and round!"),
    (81.4, 83.9, "Swish and spit, and smile so bright,"), (83.95, 86.3, "Morning teeth and teeth at night!"),
    (86.35, 89.6, "Ding! Sparkle!"),
]

L = []


# ---------------------------------------------------------------- helpers
def rect(pos, size, color, r=0):
    return [{"type": "rect", "position": pos, "size": size, "roundness": r}, {"type": "fill", "color": color}]


def ell(pos, size, color):
    return [{"type": "ellipse", "position": pos, "size": size}, {"type": "fill", "color": color}]


def group(contents, pos=(0, 0), rot=0, scale=None):
    g = {"type": "group", "contents": contents, "position": list(pos)}
    if rot:
        g["rotation"] = rot
    if scale:
        g["scale"] = scale
    return g


def bg(id_, items, start, end):
    """Static background shape drawn in composition pixels, visible from start to end."""
    L.append({"id": id_, "start": start, "duration": end - start, "timeMode": "layer",
              "transform": {"position": [0, 0], "anchor": [0, 0]}, "content": {"kind": "shape", "items": items}})


def pop_scale(dur, s=1.0):
    t_in = min(0.35, dur / 3)
    return {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": t_in, "value": [s, s]},
                          {"time": max(dur - 0.25, t_in + 0.01), "value": [s, s], "easing": "ease_in"},
                          {"time": dur, "value": [0, 0]}]}


def prop(id_, items, pos, start, dur, s=1.0, wiggle=0.0, bob=0.0, spin=0.0, extra=None, parent=None):
    """A prop that pops in, optionally wiggles/bobs/spins, and pops out."""
    anim = {"scale": pop_scale(dur, s)}
    if wiggle or spin:
        e = f"return value+{wiggle}*math.sin(2*math.pi*time/1.2)" if wiggle else f"return value+{spin}*time"
        anim["rotation"] = {"keyframes": [{"time": 0, "value": 0}], "expression": e}
    if bob:
        anim["position"] = {"keyframes": [{"time": 0, "value": list(pos)}],
                            "expression": f"return value+Vec.v2(0,{bob}*math.sin(2*math.pi*time/1.1))"}
    if extra:
        anim.update(extra)
    d = {"id": id_, "start": start, "duration": dur, "timeMode": "layer", "transform": {"position": list(pos)},
         "content": {"kind": "shape", "items": items}, "animations": anim}
    if parent:
        d["parentId"] = parent
    L.append(d)


def text(id_, t, pos, size, start, dur, color=NAVY, stroke=WHITE, pop=True, wobble=False):
    c = {"kind": "text", "text": t, "font": {"size": size, "weight": 800}, "color": color, "alignment": "center"}
    if stroke:
        c["stroke"] = {"width": 14, "color": stroke}
    d = {"id": id_, "start": start, "duration": dur, "timeMode": "layer", "transform": {"position": list(pos)}, "content": c}
    if pop:
        d["animations"] = {"scale": pop_scale(dur)}
    if wobble:
        d["animations"]["rotation"] = {"keyframes": [{"time": 0, "value": 0}], "expression": "return 4*math.sin(2*math.pi*time/0.8)"}
    L.append(d)


# ---------------------------------------------------------------- icon library (centered on 0,0)
def sun_icon(r=70, face=True):
    items = []
    if face:
        items += ell([-r * .3, -r * .1], [r * .18, r * .18], NAVY)[:1] + ell([r * .3, -r * .1], [r * .18, r * .18], NAVY)[:1] + \
                 [{"type": "fill", "color": NAVY}]
    items += [{"type": "ellipse", "position": [0, 0], "size": [2 * r, 2 * r]}, {"type": "fill", "color": YELLOW},
              {"type": "polystar", "starType": "star", "points": 12, "position": [0, 0], "outerRadius": r * 1.45,
               "innerRadius": r * 1.05, "outerRoundness": 0.2}, {"type": "fill", "color": "#FFB23F"}]
    return items


def moon_icon(r=70, sky="#2B3A6B"):
    return [group(ell([r * .45, -r * .2], [r * 1.7, r * 1.7], sky)), group(ell([0, 0], [2 * r, 2 * r], "#FFE58A"))]


def sparkle_icon(r=40, color=WHITE):
    return [{"type": "polystar", "starType": "star", "points": 4, "position": [0, 0], "outerRadius": r, "innerRadius": r * .28},
            {"type": "fill", "color": color}, {"type": "stroke", "color": YELLOW, "width": 4}]


def heart_icon(r=60, color="#FF5C8A"):
    return [group([{"type": "ellipse", "position": [-r * .5, 0], "size": [r * 1.1, r * 1.1]},
                   {"type": "ellipse", "position": [r * .5, 0], "size": [r * 1.1, r * 1.1]},
                   {"type": "polystar", "starType": "polygon", "points": 3, "position": [0, r * .55], "outerRadius": r * 1.05,
                    "rotation": 180, "outerRoundness": 0.1},
                   {"type": "fill", "color": color}])]


def toothbrush_icon(paste=True):
    items = []
    if paste:
        items += ell([0, -118], [44, 34], "#E8FBFF") + [{"type": "stroke", "color": "#8FCDEB", "width": 3}]
    items += rect([0, -70], [46, 60], WHITE, 10) + rect([0, -28], [70, 26], "#4A90E2", 10) + rect([0, 90], [38, 240], "#4A90E2", 19)
    return [group(items)]


def toothpaste_icon():
    return [group(rect([0, -105], [60, 50], "#4A90E2", 10) + rect([0, 20], [130, 220], WHITE, 30) +
                  rect([0, 20], [130, 50], CORAL, 0) + [{"type": "stroke", "color": "#8FCDEB", "width": 5}])]


def candy_icon():
    return [group(rect([0, 0], [120, 120], "#FF6B9A", 60) +
                  [{"type": "polystar", "starType": "polygon", "points": 3, "position": [-95, 0], "outerRadius": 45, "rotation": 90},
                   {"type": "fill", "color": "#FFB3CC"},
                   {"type": "polystar", "starType": "polygon", "points": 3, "position": [95, 0], "outerRadius": 45, "rotation": -90},
                   {"type": "fill", "color": "#FFB3CC"}])]


def bug_icon():
    return [group(ell([-14, -6], [18, 18], WHITE) + ell([14, -6], [18, 18], WHITE) +
                  [{"type": "ellipse", "position": [-14, -6], "size": [8, 8]}, {"type": "ellipse", "position": [14, -6], "size": [8, 8]},
                   {"type": "fill", "color": NAVY}] +
                  [{"type": "rect", "position": [-22, 32], "size": [8, 18], "roundness": 4},
                   {"type": "rect", "position": [22, 32], "size": [8, 18], "roundness": 4}, {"type": "fill", "color": "#7A5FCC"}] +
                  ell([0, 0], [80, 64], "#A98BEB"))]


def tooth_icon(happy=False):
    face = [{"type": "ellipse", "position": [-38, -20], "size": [18, 18]}, {"type": "ellipse", "position": [38, -20], "size": [18, 18]},
            {"type": "fill", "color": NAVY}]
    mouth = [{"type": "path", "closed": False, "vertices": [
        {"point": [-30, 25 if happy else 40], "outTangent": [15, 18 if happy else -14]},
        {"point": [30, 25 if happy else 40], "inTangent": [-15, 18 if happy else -14]}]},
        {"type": "stroke", "color": NAVY, "width": 8, "lineCap": "round"}]
    body = [{"type": "rect", "position": [0, -10], "size": [280, 230], "roundness": 100},
            {"type": "ellipse", "position": [-72, 120], "size": [110, 200]},
            {"type": "ellipse", "position": [72, 120], "size": [110, 200]},
            {"type": "merge", "mode": "add"},
            {"type": "stroke", "color": "#8FCDEB", "width": 10}, {"type": "fill", "color": WHITE}]
    return [group(face + mouth), group(body)]


def arrow_icon(rot=0, color=CORAL):
    return [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -70], "outerRadius": 55},
                   {"type": "rect", "position": [0, 20], "size": [40, 120], "roundness": 10},
                   {"type": "fill", "color": color}], rot=rot)]


def circle_arrow_icon(r=90, color=CORAL):
    return [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [r, 10], "outerRadius": 36, "rotation": 180},
                   {"type": "fill", "color": color}]),
            group([{"type": "ellipse", "position": [0, 0], "size": [2 * r, 2 * r]}, {"type": "trim", "start": 0, "end": 0.8},
                   {"type": "stroke", "color": color, "width": 26, "lineCap": "round"}])]


def bulb_icon():
    rays = []
    for a in range(0, 360, 45):
        rays.append(group(rect([0, -120], [14, 40], YELLOW, 7), rot=a))
    return rays + [group(rect([0, 75], [70, 50], "#9AA5B1", 12) + ell([0, 0], [150, 150], "#FFE58A") +
                         [{"type": "stroke", "color": "#FFB23F", "width": 6}])]


def thought_icon(inner):
    return inner + [group(ell([-150, 150], [40, 40], WHITE) + ell([-110, 110], [60, 60], WHITE) +
                          [{"type": "ellipse", "position": [0, 0], "size": [300, 230]}, {"type": "fill", "color": WHITE},
                           {"type": "stroke", "color": "#8FCDEB", "width": 6}])]


def drop_icon(color="#4FB3F6"):
    return [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -22], "outerRadius": 26},
                   {"type": "ellipse", "position": [0, 0], "size": [44, 44]}, {"type": "fill", "color": color}])]


def note_icon(color=NAVY):
    return [group(rect([14, -40], [8, 80], color, 2) + rect([28, -70], [30, 10], color, 4) + ell([0, 0], [36, 28], color), rot=-15)]


def zigzag_icon():
    return [{"type": "path", "closed": False,
             "vertices": [{"point": [x, (-12 if i % 2 else 12)]} for i, x in enumerate(range(-50, 60, 20))]},
            {"type": "stroke", "color": "#9AA5B1", "width": 8, "lineCap": "round", "lineJoin": "round"}]


# ---------------------------------------------------------------- sets
def set_bedroom(start, end, night=False):
    wall = "#2B3A6B" if night else "#E9E4FF"
    bg("bed_wall%d" % night, rect([960, 440], [1920, 880], wall), start, end)
    bg("bed_floor%d" % night, rect([960, 980], [1920, 200], "#7A5C46" if night else "#E8C49A"), start, end)
    bg("bed_window%d" % night, rect([1500, 330], [420, 360], WHITE, 40) + rect([1500, 330], [380, 320], "#1B2550" if night else "#9ED8FF", 30),
       start, end)
    if night:
        L.append({"id": "night_moon", "start": start, "duration": end - start, "timeMode": "layer", "transform": {"position": [1560, 290]},
                  "content": {"kind": "shape", "items": moon_icon(55, "#1B2550")}})
        for i, (x, y) in enumerate([(1360, 230), (1420, 420), (1640, 420), (1380, 330)]):
            L.append({"id": f"night_star{i}", "start": start, "duration": end - start, "timeMode": "layer",
                      "transform": {"position": [x, y]}, "content": {"kind": "shape", "items": sparkle_icon(18, "#FFE58A")},
                      "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                               "expression": f"local k=0.6+0.4*math.abs(math.sin(time*2+{i})); return Vec.v2(k,k)"}}})
    else:
        # morning sun rising in the window
        L.append({"id": "bed_sun", "start": start, "duration": end - start, "timeMode": "layer", "transform": {"position": [1500, 430]},
                  "content": {"kind": "shape", "items": sun_icon(55)},
                  "animations": {"position": {"keyframes": [{"time": 0, "value": [1500, 430], "easing": "ease_out"},
                                                            {"time": 4.0, "value": [1500, 300]}]},
                                 "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 8*time"}}})
    # bed (left side)
    bg("bed_frame%d" % night, rect([520, 850], [700, 120], "#B5835A", 30) + rect([200, 760], [60, 300], "#B5835A", 25), start, end)
    bg("bed_mattress%d" % night, rect([540, 780], [640, 70], WHITE, 30), start, end)
    bg("bed_pillow%d" % night, ell([330, 735], [200, 90], "#FFF6D8"), start, end)


def set_bathroom(start, end):
    bg("bath_wall", rect([960, 440], [1920, 880], "#FFF1C1"), start, end)
    bg("bath_tiles", rect([960, 980], [1920, 200], "#BFE6F7") + rect([960, 882], [1920, 8], "#8FCDEB"), start, end)
    bg("bath_window", ell([330, 330], [380, 380], WHITE), start, end)
    bg("bath_sky", ell([330, 330], [340, 340], "#9ED8FF"), start, end)
    L.append({"id": "bath_sun", "start": start, "duration": end - start, "timeMode": "layer", "transform": {"position": [380, 290]},
              "content": {"kind": "shape", "items": ell([0, 0], [120, 120], YELLOW)},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                       "expression": "return value*(1+0.06*math.sin(2*math.pi*time/3))"}}})
    bg("bath_mirror", rect([1560, 380], [330, 400], "#DFF4FF", 60) + rect([1560, 380], [360, 430], GREEN, 70), start, end)
    bg("bath_sink", rect([1560, 700], [420, 60], WHITE, 30) + rect([1560, 800], [300, 180], "#F4F9FF", 30), start, end)
    bg("bath_cup", rect([1430, 630], [60, 90], PINK, 14), start, end)
    bg("bath_duck", ell([1730, 600], [50, 50], YELLOW) + ell([1700, 640], [90, 70], YELLOW), start, end)
    bg("bath_stool", rect([900, 935], [420, 70], "#E2A86B", 25), start, end)


def set_lesson(start, end):
    bg("les_wall", rect([960, 440], [1920, 880], "#FFF6D8"), start, end)
    bg("les_floor", rect([960, 980], [1920, 200], "#CDEBC0") + rect([960, 882], [1920, 8], "#9ED39A"), start, end)
    bg("les_board", rect([1230, 440], [1140, 640], "#2F6B57", 24) + rect([1230, 440], [1190, 690], "#B5835A", 36), start, end)
    bg("les_chalk", rect([1230, 790], [1190, 26], "#B5835A", 8), start, end)


set_bedroom(0, CUT_BATH1)
set_bathroom(CUT_BATH1, CUT_LESSON)
set_lesson(CUT_LESSON, CUT_BATH2)
# second bathroom pass: duplicate ids need suffixes
_n = len(L)
set_bathroom(CUT_BATH2, CUT_NIGHT)
for l in L[_n:]:
    l["id"] += "_2"
set_bedroom(CUT_NIGHT, END, night=True)

# ---------------------------------------------------------------- floating bubbles + notes during songs
random.seed(3)
for si, (a, b) in enumerate(SONGS):
    for i in range(10):
        x = random.randint(150, 1800); p = random.uniform(3.5, 6.5); off = random.uniform(0, p)
        items = note_icon(random.choice([NAVY, CORAL, "#4A90E2"])) if i % 3 == 0 else \
            [{"type": "ellipse", "position": [0, 0], "size": [s := random.randint(40, 90), s]},
             {"type": "fill", "color": WHITE, "opacity": 0.6}, {"type": "stroke", "color": "#8FCDEB", "width": 4}]
        L.append({"id": f"float{si}_{i}", "start": a, "duration": b - a, "timeMode": "layer", "content": {"kind": "shape", "items": items},
                  "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 1100]}],
                                              "expression": f"local t=(time+{off:.2f})%{p:.2f}; return Vec.v2({x}+25*math.sin(t*3), 1100-t/{p:.2f}*1250)"}}})

# ---------------------------------------------------------------- INTRO props (bedroom)
o = T_INTRO
prop("in_fuzzy1", zigzag_icon(), (1250, 780), o + wt(INTRO, "teeth") - 0.1, 3.6, wiggle=10)
prop("in_fuzzy2", zigzag_icon(), (1270, 850), o + wt(INTRO, "teeth") + 0.1, 3.4, wiggle=-10)
text("in_fuzzytxt", "Fuzzy teeth?", (960, 140), 92, o + wt(INTRO, "fuzzy"), 3.2, wobble=True)
prop("in_brush", toothbrush_icon(), (1330, 560), o + wt(INTRO, "toothbrush"), 2.9, s=1.3, wiggle=15)
text("title1", "Brush Your Teeth\nwith Mokki!", (960, 150), 100, 0.4, 3.0)

# ---------------------------------------------------------------- STORY props (bathroom)
o = T_STORY
candy_in, candy_out = o + wt(STORY, "Ooh"), o + wt(STORY, "Mama") + 0.2
prop("st_candy", candy_icon(), (480, 600), candy_in, candy_out - candy_in, s=1.4, wiggle=10,
     extra={"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1.0, 1.0]},
                                    {"time": wt(STORY, "big") - wt(STORY, "Ooh"), "value": [1.0, 1.0], "easing": POP},
                                    {"time": wt(STORY, "big") - wt(STORY, "Ooh") + 0.4, "value": [1.6, 1.6]},
                                    {"time": candy_out - candy_in - 0.25, "value": [1.6, 1.6], "easing": "ease_in"},
                                    {"time": candy_out - candy_in, "value": [0, 0]}]}})
text("st_q", "?", (1150, 380), 160, candy_in + 0.3, 1.6, color=CORAL)
for i, (x, y) in enumerate([(420, 420), (560, 440), (500, 760)]):
    prop(f"st_heart{i}", heart_icon(30), (x, y), o + wt(STORY, "yummy") + i * 0.2, 2.2, bob=12)
think_in = o + wt(STORY, "Hmm")
prop("st_think", thought_icon([group([{"type": "ellipse", "position": [0, 0], "size": [0.1, 0.1]}])]), (1260, 330), think_in, 1.5, s=0.8)
text("st_think_q", "?", (1260, 300), 110, think_in + 0.2, 1.2, color=NAVY, stroke=None)
moon_in = o + wt(STORY, "Mama")
prop("st_moonthought", thought_icon([group(moon_icon(60, WHITE), pos=(0, -10))]), (1260, 330), moon_in, 2.7, s=0.9)
tooth_in, tooth_out = o + wt(STORY, "candy", 2), o + wt(STORY, "Are")
prop("st_tooth", tooth_icon(happy=False), (470, 560), tooth_in, tooth_out - tooth_in, s=1.0, wiggle=3)
bugs_in, bugs_gone = o + wt(STORY, "sugar"), o + wt(STORY, "bye-bye")
for i, (dx, dy) in enumerate([(-90, -60), (80, -90), (10, 60), (-60, 110)]):
    st = bugs_in + i * 0.25
    prop(f"st_bug{i}", bug_icon(), (470 + dx, 560 + dy), st, bugs_gone + 0.9 - st, s=1.1,
         extra={"position": {"keyframes": [{"time": 0, "value": [470 + dx, 560 + dy]},
                                            {"time": bugs_gone - st, "value": [470 + dx, 560 + dy], "easing": "ease_in"},
                                            {"time": bugs_gone - st + 0.9, "value": [470 + dx * 3, -200]}],
                             "expression": f"return value+Vec.v2(10*math.sin(time*6+{i}),8*math.cos(time*5+{i}))"}})
text("st_bugs_txt", "Sugar bugs!", (960, 140), 100, o + wt(STORY, "Sugar", 2) - 0.05, 1.5, color="#7A5FCC", wobble=True)
text("st_eww", "Eww!", (960, 140), 130, o + wt(STORY, "Eww"), 1.5, color="#7A5FCC", wobble=True)
prop("st_bulb", bulb_icon(), (1200, 330), o + wt(STORY, "know"), 1.6, s=0.8)
brush_in = o + wt(STORY, "brush")
prop("st_brush", toothbrush_icon(), (620, 560), brush_in, tooth_out - brush_in, s=1.1,
     extra={"rotation": {"keyframes": [{"time": 0, "value": -70}], "expression": "return value+12*math.sin(time*18)"},
            "position": {"keyframes": [{"time": 0, "value": [640, 560]}], "expression": "return value+Vec.v2(70*math.sin(time*9),0)"}})
for i, (x, y) in enumerate([(380, 420), (580, 470), (470, 700), (330, 610)]):
    prop(f"st_spark{i}", sparkle_icon(36), (x, y), bugs_gone + 0.5 + i * 0.15, tooth_out - bugs_gone - 0.4, spin=90)
text("st_sing", "Let's sing!", (960, 140), 100, o + wt(STORY, "Let's"), 2.0)

# ---------------------------------------------------------------- SONG props (both passes)
def song_props(si, a):
    p = f"sg{si}_"
    text(p + "head", "Let's sing!" if si == 0 else "Now YOU sing with Mokki!", (960, 140), 96, a + 0.5, 7.5)
    for li, (s, e, line) in enumerate(LYRICS):
        text(f"{p}ly{li}", line, (960, 130), 80, a + s, e - s, pop=False)
    prop(p + "sun", sun_icon(80), (330, 330), a + 9.2, 2.8, wiggle=12)
    prop(p + "paste", toothpaste_icon(), (1250, 560), a + 14.3, 2.4, s=0.8, wiggle=8)
    prop(p + "pea", [group(ell([0, -40], [40, 40], "#E8FBFF") + [{"type": "stroke", "color": "#4A90E2", "width": 5}]),
                     group(toothbrush_icon(False), pos=(80, 0), rot=90, scale=[0.9, 0.9]),
                     group(ell([0, 0], [260, 260], WHITE) + [{"type": "stroke", "color": "#8FCDEB", "width": 8}])], (1220, 480), a + 16.7, 2.4)
    for c0, c1 in [(21.5, 23.9), (69.5, 71.9)]:
        prop(f"{p}up{c0}", arrow_icon(0), (1240, 430), a + c0, c1 - c0, bob=25)
        prop(f"{p}dn{c0}", arrow_icon(180), (1240, 700), a + c0, c1 - c0, bob=-25)
    for c0, c1 in [(26.35, 29.8), (47.9, 50.3), (74.35, 77.8)]:
        prop(f"{p}circ{c0}", circle_arrow_icon(), (1240, 560), a + c0, c1 - c0, spin=300)
    candy_t = 50.35
    prop(p + "candy", candy_icon(), (470, 600), a + candy_t, 2.3,
         extra={"position": {"keyframes": [{"time": 0, "value": [470, 600]}, {"time": 1.0, "value": [470, 600], "easing": "ease_in"},
                                           {"time": 2.3, "value": [-300, 100]}]}})
    prop(p + "candybug", bug_icon(), (560, 520), a + candy_t + 0.2, 2.1, s=1.3,
         extra={"position": {"keyframes": [{"time": 0, "value": [560, 520]}, {"time": 0.9, "value": [560, 520], "easing": "ease_in"},
                                           {"time": 2.1, "value": [-200, 60]}]},
                "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 20*math.sin(time*10)"}})
    for n, t in zip("123", [54.04, 54.28, 54.56]):
        text(f"{p}num{n}", n, (330 + 150 * int(n) - 150, 600), 220, a + t, 57.0 - t, color=[CORAL, "#4A90E2", "#2BB673"][int(n) - 1])
    for i, (x, y) in enumerate([(700, 420), (1150, 380), (650, 760), (1200, 760), (420, 560)]):
        prop(f"{p}sh{i}", sparkle_icon(40), (x, y), a + 55.1 + i * 0.12, 3.0, spin=120)
    for i, x in enumerate([380, 470, 560]):
        prop(f"{p}drop{i}", drop_icon(), (x, 520), a + 81.4 + i * 0.25, 2.3, s=1.6, bob=20)
    prop(p + "msun", sun_icon(80), (420, 560), a + 84.0, 1.3)
    prop(p + "mmoon", moon_icon(80, "#FFF1C1"), (420, 560), a + 85.2, 1.2)
    for i, (x, y) in enumerate([(600, 380), (1250, 420), (520, 720), (1300, 700), (960, 300), (380, 480)]):
        prop(f"{p}ding{i}", sparkle_icon(55), (x, y), a + 86.4 + i * 0.1, 3.0, spin=200)
    # toothbrush in Mokki's hand while singing
    b = a + SONG_LEN
    L.append({"id": p + "hbrush", "parentId": "mokki", "start": a, "duration": b - a, "timeMode": "layer",
              "transform": {"position": [1150, 980], "scale": [1.6, 1.6], "rotation": -60},
              "content": {"kind": "shape", "items": toothbrush_icon(False)},
              "animations": {"rotation": {"keyframes": [{"time": 0, "value": -60}], "expression": "return value+15*math.sin(2*math.pi*time/0.3)"},
                             "opacity": {"keyframes": [{"time": 0, "value": 0}, {"time": 0.3, "value": 1}]}}})


for si, (a, b) in enumerate(SONGS):
    song_props(si, a)

# ---------------------------------------------------------------- LESSON props (on the board)
o = T_LESSON
for i, (x, y) in enumerate([(300, 500), (560, 470), (250, 760), (620, 760)]):
    prop(f"le_spark{i}", sparkle_icon(40), (x, y), o + wt(LESSON, "Ding") + i * 0.12, 2.6, spin=150)
text("le_title", "Mokki's Brushing Secrets", (1230, 200), 72, o + wt(LESSON, "brushing"), 34.7 - wt(LESSON, "brushing") - 0.3,
     color=WHITE, stroke=None)
n1, n2, n3, n4 = (o + wt(LESSON, "Number", k) for k in (1, 2, 3, 4))
nturn = o + wt(LESSON, "Now")
steps = [(n1, n2, "1"), (n2, n3, "2"), (n3, n4, "3"), (n4, nturn, "4")]
for s, e, n in steps:
    text(f"le_num{n}", n, (790, 330), 160, s, e - s - 0.1, color=YELLOW, stroke=None)
# 1: toothpaste + pea
prop("le_paste", toothpaste_icon(), (1080, 470), n1 + 0.4, n2 - n1 - 0.5, s=0.9, wiggle=6)
pea_t = o + wt(LESSON, "pea")
prop("le_brushpea", toothbrush_icon(True), (1420, 470), o + wt(LESSON, "tiny"), n2 - o - wt(LESSON, "tiny") - 0.1, s=1.2,
     extra={"rotation": {"keyframes": [{"time": 0, "value": 90}]}})
text("le_t1", "as small as a pea!", (1230, 690), 64, o + wt(LESSON, "small"), n2 - o - wt(LESSON, "small") - 0.1, color=WHITE, stroke=None)
# 2: up and down
prop("le_up", arrow_icon(0, YELLOW), (1080, 420), n2 + 0.5, n3 - n2 - 0.6, bob=25)
prop("le_dn", arrow_icon(180, YELLOW), (1080, 650), n2 + 0.5, n3 - n2 - 0.6, bob=-25)
prop("le_brushud", toothbrush_icon(False), (1380, 520), o + wt(LESSON, "brush"), n3 - o - wt(LESSON, "brush") - 0.1, s=1.1,
     extra={"position": {"keyframes": [{"time": 0, "value": [1380, 520]}], "expression": "return value+Vec.v2(0,90*math.sin(time*7))"}})
text("le_t2", "up and down!", (1230, 700), 64, o + wt(LESSON, "up"), n3 - o - wt(LESSON, "up") - 0.1, color=WHITE, stroke=None)
# 3: circles
prop("le_circ", circle_arrow_icon(120, YELLOW), (1250, 480), n3 + 0.5, n4 - n3 - 0.6, spin=280)
prop("le_brushc", toothbrush_icon(False), (1250, 480), o + wt(LESSON, "round"), n4 - o - wt(LESSON, "round") - 0.1, s=0.8,
     extra={"position": {"keyframes": [{"time": 0, "value": [1250, 480]}],
                         "expression": "return value+Vec.v2(110*math.cos(time*6),110*math.sin(time*6))"}})
text("le_t3", "round and round!", (1230, 700), 64, o + wt(LESSON, "round"), n4 - o - wt(LESSON, "round") - 0.1, color=WHITE, stroke=None)
# 4: two times a day, morning + night
text("le_t4", "2 times every day", (1230, 360), 80, o + wt(LESSON, "two", 2), nturn - o - wt(LESSON, "two", 2) - 0.1, color=WHITE, stroke=None)
prop("le_sun", sun_icon(85), (1050, 560), o + wt(LESSON, "morning"), nturn - o - wt(LESSON, "morning") - 0.1, wiggle=8)
text("le_morning", "morning", (1050, 720), 56, o + wt(LESSON, "morning"), nturn - o - wt(LESSON, "morning") - 0.1, color=WHITE, stroke=None)
prop("le_moon", moon_icon(85, "#2F6B57"), (1420, 560), o + wt(LESSON, "night"), nturn - o - wt(LESSON, "night") - 0.1, wiggle=-8)
text("le_night", "night", (1420, 720), 56, o + wt(LESSON, "night"), nturn - o - wt(LESSON, "night") - 0.1, color=WHITE, stroke=None)
# your turn + 1 2 3
prop("le_turnbrush", toothbrush_icon(True), (1230, 500), nturn, o + wt(LESSON, "One", 2) - nturn - 0.1, s=1.3, wiggle=15)
text("le_turn", "Your turn!", (1230, 700), 80, nturn, o + wt(LESSON, "One", 2) - nturn - 0.1, color=YELLOW, stroke=None)
for n, (k, c) in enumerate([("One", CORAL), ("two", "#4A90E2"), ("three", "#2BB673")], 1):
    t0 = o + wt(LESSON, k, {"One": 2, "two": 3, "three": 2}[k])
    text(f"le_cnt{n}", str(n), (930 + 300 * (n - 1), 480), 240, t0, o + 35.6 - t0, color=c)

# ---------------------------------------------------------------- BYE props (night bedroom)
o = T_BYE
for i in range(14):
    x = 200 + i * 120; c = [CORAL, YELLOW, "#4A90E2", "#2BB673", PINK][i % 5]
    prop(f"by_conf{i}", [group(rect([0, 0], [26, 40], c, 6))], (x, -50), o + 0.1 + (i % 4) * 0.1, 4.0, spin=200,
         extra={"position": {"keyframes": [{"time": 0, "value": [x, -50]}, {"time": 4.0, "value": [x + 60 * ((i % 3) - 1), 1150]}]}})
text("by_yay", "Yay! You did it!", (960, 150), 100, o + wt(BYE, "Yay"), 3.3, color=CORAL)
for i, (x, y) in enumerate([(700, 420), (1150, 420), (650, 760), (1200, 760)]):
    prop(f"by_sh{i}", sparkle_icon(42), (x, y), o + wt(BYE, "shiny") + i * 0.12, 2.8, spin=140)
prop("by_sun", sun_icon(70), (400, 450), o + wt(BYE, "morning"), 1.4)
prop("by_moon", moon_icon(70, "#2B3A6B"), (400, 450), o + wt(BYE, "night"), 1.2)
prop("by_brush", toothbrush_icon(True), (400, 450), o + wt(BYE, "brush"), 1.6, s=1.1,
     extra={"rotation": {"keyframes": [{"time": 0, "value": -40}], "expression": "return value+15*math.sin(time*20)"}})
text("bye", "Bye-bye, friends!\nSee you tomorrow!", (960, 150), 90, o + wt(BYE, "Bye-bye"), END - o - wt(BYE, "Bye-bye"))
mwah = o + wt(BYE, "Mwah")
for i, (x, y) in enumerate([(1250, 520), (1350, 420), (1180, 380)]):
    prop(f"by_heart{i}", heart_icon(40 + 10 * i), (x, y), mwah + i * 0.15, END - mwah - i * 0.15,
         extra={"position": {"keyframes": [{"time": 0, "value": [x, y]}, {"time": END - mwah, "value": [x + 40, y - 300]}]}})

# ---------------------------------------------------------------- MOKKI
W, H = 1128, 1318
POS = {"bed": [1050, 1000], "bath": [900, 1025], "lesson": [430, 1000]}
pos_keys = [{"time": 0, "value": [880, 690], "easing": "step"},
            {"time": 3.9, "value": [880, 690], "easing": "ease_out"},
            {"time": 4.3, "value": [980, 600], "easing": "ease_in"},
            {"time": 4.7, "value": POS["bed"], "easing": "step"},
            {"time": CUT_BATH1, "value": POS["bath"], "easing": "step"},
            {"time": CUT_LESSON, "value": POS["lesson"], "easing": "step"},
            {"time": CUT_BATH2, "value": POS["bath"], "easing": "step"},
            {"time": CUT_NIGHT, "value": POS["bed"], "easing": "step"}]
songs_cond = " or ".join(f"(time>={a:.2f} and time<{b:.2f})" for a, b in SONGS)
songs_start = " ".join(f"if time>={a:.2f} and time<{b:.2f} then s={a:.2f} end;" for a, b in SONGS)
bounce = (f"if time<4.7 then return value end; local s=0; {songs_start} "
          f"if {songs_cond} then local b=math.abs(math.sin(math.pi*(time-s)/0.6)); return value+Vec.v2(0,-45*b) "
          f"else return value+Vec.v2(0,-10*math.sin(2*math.pi*time/1.6)) end")
# stretch moments: yawns + "stretches to the sky"
yawns = [(T_INTRO + 4.32, T_INTRO + 5.2), (T_LESSON + 24.84, T_LESSON + 25.76)]
stretches = yawns + [(a + 11.95, a + 14.25) for a, _ in SONGS]
st_lua = "{" + ",".join(f"{a:.2f},{b:.2f}" for a, b in stretches) + "}"
squash = (f"local S={st_lua}; for i=1,#S,2 do if time>=S[i] and time<S[i+1] then "
          f"local k=math.sin(math.pi*(time-S[i])/(S[i+1]-S[i])); return Vec.v2(value.x*(1-0.06*k), value.y*(1+0.14*k)) end end; "
          f"local s=0; {songs_start} if {songs_cond} then local b=math.abs(math.sin(math.pi*(time-s)/0.6)); "
          f"return Vec.v2(value.x*(1+0.04*(1-b)), value.y*(1-0.04*(1-b))) end; return value")
eww0, eww1 = T_STORY + wt(STORY, "Eww"), T_STORY + wt(STORY, "Eww") + 0.8
lean0, lean1 = T_STORY + wt(STORY, "Mmm"), T_STORY + wt(STORY, "Hmm")
wave0, wave1 = T_BYE + wt(BYE, "Bye-bye"), T_BYE + wt(BYE, "World") + 0.8
rot_expr = (f"if time<4.5 then return value end; local r=value+4*math.sin(2*math.pi*time/2.4); "
            f"if time>={eww0:.2f} and time<{eww1:.2f} then r=r+10*math.sin(time*45) end; "
            f"if time>={lean0:.2f} and time<{lean1:.2f} then r=r-9*math.sin(math.pi*(time-{lean0:.2f})/{lean1 - lean0:.2f}) end; "
            f"if time>={wave0:.2f} and time<{wave1:.2f} then r=r+12*math.sin(time*10) end; return r")
L.append({"id": "mokki", "content": {"kind": "media", "asset": {"type": "image", "uri": MOKKI, "width": W, "height": H}},
          "transform": {"anchor": [W / 2, H], "position": [880, 690], "scale": [0.5, 0.5]},
          "animations": {
              "scale": {"keyframes": [{"time": 0, "value": [0.5, 0.5]}, {"time": END - 1.0, "value": [0.5, 0.5], "easing": "ease_in"},
                                      {"time": END, "value": [0, 0]}], "expression": squash},
              "position": {"keyframes": pos_keys, "expression": bounce},
              "rotation": {"keyframes": [{"time": 0, "value": -80, "easing": "step"}, {"time": 3.9, "value": -80, "easing": "ease_in_out"},
                                         {"time": 4.5, "value": 0}], "expression": rot_expr}}})

# ---- mouth (lip-sync from word timings)
def mouth_table():
    out = []
    def add(words, off, tagged=True):
        for w in words:
            s, e = w[0], w[1]
            word = w[2] if tagged else ""
            if word.startswith("["):
                if word == "[yawns]":
                    k = 1
                elif word == "[giggles]":
                    k = 2
                elif word == "[gasps]":
                    k = 3
                else:
                    continue
            else:
                k = 0
            out.append((off + s, off + max(e, s + 0.12), k))
    add(INTRO, T_INTRO); add(STORY, T_STORY); add(LESSON, T_LESSON); add(BYE, T_BYE)
    for a, _ in SONGS:
        add([(s, e, "x") for s, e in SONG_WORDS], a)
    out.sort()
    return "{" + ",".join(f"{s:.2f},{e:.2f},{k}" for s, e, k in out) + "}"


MOUTH_O = ("local W=" + mouth_table() + "; local o=0; "
           "for i=1,#W,3 do local s=W[i]; if s>time then break end; local e=W[i+1]; "
           "if time<e then local k=W[i+2]; "
           "if k==0 then o=0.3+0.7*math.abs(math.sin(math.pi*(time-s)/0.17)) "
           "elseif k==1 then o=1.4*math.sin(math.pi*(time-s)/(e-s)) "
           "elseif k==2 then o=0.35+0.45*math.abs(math.sin(time*28)) else o=1.1 end; break end end; ")
MX, MY = 586, 945
# closed smile, hidden while the mouth is open
L.append({"id": "mouth_smile", "parentId": "mokki", "transform": {"position": [MX, MY]},
          "content": {"kind": "shape", "items": [
              {"type": "path", "closed": False, "vertices": [
                  {"point": [-127, -40], "outTangent": [30, 45]},
                  {"point": [0, 46], "inTangent": [-70, 0], "outTangent": [70, 0]},
                  {"point": [127, -46], "inTangent": [-30, 45]}]},
              {"type": "stroke", "color": NAVY, "width": 24, "lineCap": "round", "lineJoin": "round"}]},
          "animations": {"opacity": {"keyframes": [{"time": 0, "value": 1}], "expression": MOUTH_O + "if o>0.08 then return 0 end; return 1"}}})
# open mouth: navy oval + pink tongue, scaled by openness
L.append({"id": "mouth_open", "parentId": "mokki", "transform": {"position": [MX, MY - 10]},
          "content": {"kind": "shape", "items": [
              group(ell([0, 32], [96, 44], "#FF7A93")),
              group([{"type": "ellipse", "position": [0, 0], "size": [170, 130]}, {"type": "fill", "color": NAVY}])]},
          "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                   "expression": MOUTH_O + "if o<0.08 then return Vec.v2(0,0) end; return Vec.v2(0.75+0.25*math.min(o,1.2), 0.25+0.85*o)"}}})

# ---- eyelids (blink every ~3.9 s, closed during yawns and "Mwah")
closed = yawns + [(T_BYE + wt(BYE, "Mwah"), T_BYE + wt(BYE, "Mwah") + 0.6), (0, 0.9)]
cl_lua = "{" + ",".join(f"{a:.2f},{b:.2f}" for a, b in closed) + "}"
BLINK = (f"local C={cl_lua}; for i=1,#C,2 do if time>=C[i] and time<C[i+1] then b=1 end end; "
         "local p=(time+0.7)%3.9; local k=0; if p<0.08 then k=p/0.08 elseif p<0.13 then k=1 elseif p<0.21 then k=(0.21-p)/0.08 end; "
         "if b==1 then k=1 end; ")
for eid, cx, cy, d in [("L", 410, 715.5, 344), ("R", 742.5, 721.5, 228)]:
    L.append({"id": f"lid{eid}", "parentId": "mokki", "transform": {"position": [cx, cy - d / 2]},
              "content": {"kind": "shape", "items": ell([0, d / 2], [d, d], BODY)},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 0]}],
                                       "expression": "local b=0; " + BLINK + "return Vec.v2(1,k)"}}})
    L.append({"id": f"lidline{eid}", "parentId": "mokki", "transform": {"position": [cx, cy]},
              "content": {"kind": "shape", "items": [
                  {"type": "path", "closed": False, "vertices": [
                      {"point": [-d * .42, 0], "outTangent": [d * .2, d * .22]},
                      {"point": [d * .42, 0], "inTangent": [-d * .2, d * .22]}]},
                  {"type": "stroke", "color": NAVY, "width": 16, "lineCap": "round"}]},
              "animations": {"opacity": {"keyframes": [{"time": 0, "value": 0}],
                                         "expression": "local b=0; " + BLINK + "if k>0.85 then return 1 end; return 0"}}})

# bedroom blanket over Mokki while he is in bed
L.append({"id": "blanket", "start": 0, "duration": 4.1, "timeMode": "layer", "transform": {"position": [0, 0], "anchor": [0, 0]},
          "content": {"kind": "shape", "items": rect([800, 760], [440, 220], "#6CC79A", 60) +
                      [{"type": "stroke", "color": GREEN, "width": 8}]},
          "animations": {"opacity": {"keyframes": [{"time": 3.8, "value": 1}, {"time": 4.1, "value": 0}]}}})

# ---------------------------------------------------------------- wipes between sets (on top)
for i, cut in enumerate([CUT_BATH1, CUT_LESSON, CUT_BATH2, CUT_NIGHT]):
    L.append({"id": f"wipe{i}", "start": cut - 0.4, "duration": 0.8, "timeMode": "layer", "transform": {"position": [960, 540]},
              "content": {"kind": "shape", "items": ell([0, 0], [900, 900], BODY) + ell([0, 0], [2300, 2300], YELLOW)},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": "ease_in"}, {"time": 0.4, "value": [1, 1], "easing": "ease_out"},
                                                     {"time": 0.8, "value": [0, 0]}]}}})

# ---------------------------------------------------------------- audio
for id_, start, uri in [("v_intro", T_INTRO, V_INTRO), ("v_story", T_STORY, V_STORY), ("song1", T_SONG1, SONG),
                        ("v_lesson", T_LESSON, V_LESSON), ("song2", T_SONG2, SONG), ("v_bye", T_BYE, V_BYE)]:
    L.append({"id": id_, "start": start, "content": {"kind": "audio", "asset": {"type": "audio", "uri": uri}}})

scene = {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": END, "background": "#FFF1C1"},
         "layers": L}
ids = [l["id"] for l in L]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
json.dump(scene, open("ep01-scene.json", "w"), separators=(",", ":"))
print("layers", len(L), "bytes", len(json.dumps(scene)), "duration", END)
