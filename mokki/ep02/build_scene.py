"""Mokki & Friends - Episode 2: Wash Your Hands. Builds ep02-scene.json (episode only) and ep02-full-scene.json (with intro/outro)."""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import kit, text_check, branding
from kit import (NAVY, WHITE, YELLOW, CORAL, GREEN, PINK, BODY, POP, snap, rect, ell, group, shape_layer, prop, audio,
                 sparkle_icon, heart_icon, mokki_rig, family_rig, words_from_transcript, wipe, kid_text)

A = "https://gcdn.picsart.com/picsart-mcp/"
SONG = A + "8374e555-f940-4a05-bccb-e1dd2bca6640.mp3"
V = {"intro": A + "698efdaf-1b2b-4ce4-bb5b-6c26efa63bd1.mp3", "mama1": A + "72d2879f-b13d-4f3b-b06f-1baddef2420f.mp3",
     "mokki1": A + "498b6e5a-1f8e-48e7-b17a-c3e3b5fe4bae.mp3", "mama2": A + "52a103eb-971e-4fc6-afb8-dc18ce6e3f47.mp3",
     "mokki2": A + "220d5f27-290e-465c-a6ac-8f26660405b8.mp3", "mama3": A + "85efc561-c06b-4295-ad57-1afd9307eae8.mp3",
     "lesson": A + "170294cd-68e0-453c-bf05-7248f661da19.mp3", "bye": A + "a7e11304-5229-402b-adb4-ee1416ecfe19.mp3"}
kit.FAMILY_URLS.update({"papa": A + "5516daa6-d600-4b6f-a122-3abc2539f009.png", "mama": A + "01131a7b-4f78-493a-a350-6618e929c06e.png",
                        "pia": A + "3ddbe55c-ed46-4d5c-a19f-b6a70cba4911.png", "pip": A + "2a573c49-2923-41de-a8ff-90e5deb37f64.png",
                        "grandpa": A + "a61529f1-96eb-4251-a7c3-0c0c77f0435a.png", "grandma": A + "5abb3d82-2b1d-4d45-a169-de98b8c0cb78.png"})

# ---------------------------------------------------------------- word timings (seconds from clip start)
W = {
 "intro": [(0.08,0.24,"Hi"),(0.4,0.92,"friends"),(1.04,1.36,"It's"),(1.48,1.72,"me"),(1.84,2.44,"Mokki"),(2.56,3.16,"[giggles]"),
           (3.2,3.68,"Look"),(3.84,4.0,"I'm"),(4.16,4.32,"playing"),(4.36,4.4,"in"),(4.48,4.56,"the"),(4.6,4.88,"garden"),(4.96,5.04,"with"),
           (5.12,5.2,"my"),(5.28,5.44,"little"),(5.52,5.84,"sister"),(5.92,6.56,"Pia"),(6.8,6.96,"We"),(7.04,7.12,"made"),(7.36,7.44,"a"),
           (7.52,7.84,"big"),(8.0,8.24,"mud"),(8.32,8.8,"cake"),(8.88,9.52,"[giggles]"),(9.6,10.2,"Ooh"),(10.32,10.48,"but"),(10.64,10.8,"now"),
           (10.88,11.04,"my"),(11.12,11.36,"hands"),(11.44,11.52,"are"),(11.68,11.84,"all"),(11.92,12.16,"muddy"),(12.28,12.4,"and"),(12.56,13.28,"sticky")],
 "mama1": [(0.08,0.84,"Mokki"),(1.04,1.76,"Pia"),(2.0,2.24,"Dinner"),(2.32,3.12,"time")],
 "mokki1": [(0.16,0.84,"Yay"),(0.96,1.52,"Dinner"),(1.68,2.0,"I'm"),(2.08,2.4,"so"),(2.48,3.36,"hungry")],
 "mama2": [(0.16,0.64,"Wait"),(0.72,0.96,"little"),(1.04,1.52,"one"),(1.76,1.92,"Look"),(1.96,2.0,"at"),(2.08,2.24,"your"),(2.52,3.08,"hands"),
           (3.36,3.68,"Tiny"),(3.76,4.16,"germs"),(4.24,4.32,"are"),(4.427,4.64,"hiding"),(4.8,5.2,"there"),(5.52,5.84,"Germs"),(5.92,6.0,"can"),
           (6.08,6.24,"make"),(6.32,6.72,"tummies"),(6.8,7.44,"hurt")],
 "mokki2": [(0.0,0.64,"[gasps]"),(0.84,1.48,"Germs"),(1.76,2.44,"Eww"),(2.64,2.8,"Go"),(2.88,3.28,"away"),(3.36,4.08,"germs")],
 "mama3": [(0.16,0.4,"Let's"),(0.48,0.64,"wash"),(0.72,0.8,"our"),(0.88,1.12,"hands"),(1.2,1.28,"with"),(1.36,1.52,"soap"),(1.6,1.68,"and"),
           (1.76,2.36,"water"),(2.56,3.12,"Ready"),(3.36,3.6,"Let's"),(3.84,4.4,"sing")],
 "lesson": [(0.16,0.64,"Look"),(0.8,0.96,"My"),(1.04,1.28,"hands"),(1.4,1.52,"are"),(1.72,2.08,"sparkly"),(2.16,2.72,"clean"),(2.8,3.6,"[giggles]"),
            (3.68,3.76,"When"),(3.84,3.92,"do"),(4.0,4.08,"we"),(4.2,4.32,"wash"),(4.4,4.48,"our"),(4.56,5.28,"hands"),(5.52,5.92,"Before"),
            (6.04,6.16,"we"),(6.24,7.04,"eat"),(7.2,7.36,"after"),(7.44,7.52,"we"),(7.6,7.76,"use"),(7.84,7.92,"the"),(7.96,8.8,"potty"),
            (8.96,9.12,"after"),(9.2,9.36,"we"),(9.44,9.52,"play"),(9.84,10.48,"outside"),(10.64,10.8,"and"),(11.04,11.28,"after"),(11.36,11.52,"we"),
            (11.56,11.84,"sneeze"),(11.92,12.0,"or"),(12.08,12.56,"cough"),(13.04,13.28,"Number"),(13.44,14.16,"one"),(14.24,14.72,"water"),
            (15.2,15.44,"Number"),(15.6,16.24,"two"),(16.32,17.2,"soap"),(17.32,17.44,"Number"),(17.6,18.32,"three"),(18.48,18.76,"rub"),
            (18.8,19.08,"rub"),(19.12,19.52,"rub"),(19.64,19.76,"while"),(19.84,19.92,"we"),(20.04,20.16,"count"),(20.24,20.32,"to"),(20.4,21.28,"twenty"),
            (21.4,21.52,"Number"),(21.68,22.4,"four"),(22.56,23.28,"rinse"),(23.52,23.76,"Number"),(23.84,24.56,"five"),(24.64,24.88,"dry"),
            (24.96,25.04,"with"),(25.08,25.12,"a"),(25.2,25.68,"towel"),(26.16,26.32,"Now"),(26.4,26.56,"it's"),(26.64,26.8,"your"),(26.88,27.28,"turn"),
            (27.6,27.84,"Wash"),(27.92,28.0,"your"),(28.16,28.32,"hands"),(28.4,28.48,"and"),(28.64,28.8,"sing"),(28.88,28.96,"with"),(29.04,29.28,"me"),
            (29.6,30.0,"Ready"),(30.48,31.04,"One"),(31.16,31.6,"two"),(31.76,32.24,"three")],
 "bye": [(0.16,0.84,"Yay"),(0.96,1.28,"Clean"),(1.36,2.12,"hands"),(2.32,2.48,"Now"),(2.56,2.64,"we"),(2.72,2.8,"can"),(2.88,2.96,"eat"),
         (3.04,3.28,"dinner"),(3.4,3.52,"with"),(3.56,4.08,"Papa"),(4.12,4.64,"Mama"),(4.68,5.04,"Pia"),(5.12,5.2,"and"),(5.28,5.52,"baby"),
         (5.6,6.08,"Pip"),(6.16,6.96,"[giggles]"),(7.2,7.84,"Remember"),(8.0,8.16,"wash"),(8.24,8.32,"your"),(8.44,8.56,"hands"),(8.64,8.8,"with"),
         (8.88,9.04,"soap"),(9.12,9.2,"and"),(9.28,9.68,"water"),(10.227,10.56,"Bye-bye"),(10.8,11.36,"friends"),(11.44,11.52,"See"),(11.6,11.68,"you"),
         (11.8,12.16,"tomorrow"),(12.24,12.4,"in"),(12.44,12.72,"Mokki"),(12.8,13.44,"World")],
}
SONG_WORDS = [(9.22,9.52),(9.56,9.66),(9.7,9.76),(9.84,10.22),(10.3,10.58),(10.88,11.26),(11.28,11.5),(11.56,11.8),(11.86,12.04),(12.12,12.62),
 (12.7,12.96),(13.0,13.14),(13.26,13.62),(13.86,14.1),(14.16,14.28),(14.4,14.64),(14.76,14.9),(15.02,15.26),(15.58,16.06),(16.16,16.64),(16.74,16.96),
 (17.04,17.22),(17.36,17.56),(18.48,18.76),(19.06,19.3),(19.64,19.86),(19.94,20.1),(20.2,20.58),(20.72,21.06),(21.28,21.62),(21.84,22.18),(22.26,22.4),
 (22.5,22.84),(23.12,23.44),(23.52,23.6),(23.66,23.98),(24.02,24.56),(24.68,25.12),(25.36,25.64),(25.7,26.0),(26.1,26.46),(26.58,27.06),
 (36.92,37.3),(37.36,37.98),(38.12,38.4),(38.42,38.58),(38.68,39.02),(39.24,39.54),(39.62,39.74),(39.82,40.26),(40.44,40.66),(40.7,40.88),(40.98,41.28),
 (41.4,41.82),(41.88,42.02),(42.12,42.62),(42.72,43.16),(43.26,43.7),(43.82,44.14),(44.18,44.34),(44.44,44.92),(45.04,45.46),(45.6,46.14),
 (55.38,55.68),(55.98,56.26),(56.54,56.8),(56.86,57.02),(57.12,57.5),(57.64,58.06),(58.2,58.64),(58.76,59.1),(59.16,59.3),(59.4,59.76),(60.02,60.36),
 (60.44,60.52),(60.58,60.88),(60.94,61.46),(61.6,62.0),(62.28,62.56),(62.62,62.9),(63.02,63.38),(63.5,63.98),
 (73.82,74.2),(74.26,74.34),(74.42,74.94),(75.02,75.22),(75.26,75.5),(75.56,75.84),(76.14,76.4),(76.46,76.58),(76.62,76.68),(76.74,77.16),(77.28,77.7),
 (78.4,78.8),(78.9,78.98),(79.04,79.48),(79.58,79.84),(79.9,80.12),(80.2,80.44),(80.7,81.2),(81.3,81.52),(81.62,82.6)]
LYRICS = [(9.2, 11.5, "Turn on the water, splish, splash, splash,"), (11.55, 13.75, "Wet your hands, nice and fast!"),
          (13.8, 15.5, "Pump the soap, one, two,"), (15.55, 18.3, "Bubbles, bubbles, just for you!"),
          (18.4, 20.65, "Rub, rub, rub your hands,"), (20.7, 23.0, "Scrub, scrub, scrub your hands!"),
          (23.05, 25.3, "Wash the germs away, hooray!"), (25.35, 27.6, "Clean hands every day!"),
          (36.85, 39.15, "Palms together, round and round,"), (39.2, 41.35, "Backs of hands, up and down,"),
          (41.4, 43.75, "Between your fingers, wiggle, wiggle,"), (43.8, 46.5, "Thumbs and nails, giggle, giggle!"),
          (55.3, 57.6, "Rub, rub, rub your hands,"), (57.62, 59.95, "Scrub, scrub, scrub your hands!"),
          (59.98, 62.2, "Wash the germs away, hooray!"), (62.25, 64.6, "Clean hands every day!"),
          (73.75, 76.05, "Rinse the bubbles, whoosh, whoosh, whoosh,"), (76.1, 80.6, "Dry with a towel, swoosh, swoosh, swoosh!"),
          (80.65, 83.6, "Sparkly clean, hooray!")]

# ---------------------------------------------------------------- timeline
T = {"intro": 0.8, "mama1": 15.2, "mokki1": 18.6, "mama2": 22.3, "mokki2": 30.1, "mama3": 34.5, "lesson": 130.6, "bye": 254.6}
T_SONG1, T_SONG2, SONG_LEN = 39.8, 163.7, 90.0
CUT_KITCHEN, CUT_BATH1, CUT_LESSON, CUT_BATH2, CUT_DINNER = 14.6, 39.4, 130.3, 163.3, 254.2
END = 270.0
SONGS = [(T_SONG1, T_SONG1 + SONG_LEN), (T_SONG2, T_SONG2 + SONG_LEN)]
KID_COLORS = ["#F0506E", "#2BB673", "#4A90E2", "#FF8A00", "#9B59D0"]


def wt(clip, word, n=1):
    k = 0
    for s, e, w in W[clip]:
        if w.lower() == word.lower():
            k += 1
            if k == n:
                return T[clip] + s
    raise KeyError((clip, word, n))


def text(id_, t, pos, size, start, dur, color=None, stroke=WHITE, pop=True, wobble=False):
    if color is None:
        color = KID_COLORS[sum(map(ord, id_)) % len(KID_COLORS)]
    L.extend(kid_text(id_, t, pos, size, start, dur, color=color, stroke=stroke, pop=pop, wobble=wobble))


def bg(id_, items, start, end):
    L.append(shape_layer(id_, items, start, end - start, absolute=True))


def place(layers, start, dur):
    """Show a rig only from start for dur (its keys, words and expressions are relative to start)."""
    for l in layers:
        l["start"], l["duration"], l["timeMode"] = snap(start), snap(dur), "layer"
    return layers


L = []
# ================================================================ SETS
def set_garden(s, e):
    bg("g_sky", rect([960, 400], [1920, 800], "#9ED8FF"), s, e)
    bg("g_grass", rect([960, 940], [1920, 280], "#8BD36B") + rect([960, 802], [1920, 10], "#6BB84E"), s, e)
    L.append(shape_layer("g_sun", kit.sun_icon(80) if hasattr(kit, "sun_icon") else ell([0, 0], [160, 160], YELLOW), s, e - s, (1700, 170),
                         {"rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 6*time"}}))
    for i, (x, y, w) in enumerate([(300, 180, 300), (1150, 130, 360)]):
        L.append(shape_layer(f"g_cloud{i}", kit.cloud_icon(w), s, e - s, (x, y),
                             {"position": {"keyframes": [{"time": 0, "value": [x, y]}], "expression": "return value+Vec.v2(10*time,0)"}}))
    for i, (x, c) in enumerate([(120, "#FF6B9A"), (260, YELLOW), (1600, "#9B59D0"), (1760, "#FF8A00"), (1860, "#FF6B9A")]):
        bg(f"g_flower{i}", [group([{"type": "polystar", "starType": "star", "points": 6, "position": [x, 860], "outerRadius": 34, "innerRadius": 20,
                                    "outerRoundness": 0.6}, {"type": "fill", "color": c}]),
                            group(rect([x, 910], [8, 90], "#4E8A1E", 4))], s, e)
    bg("g_puddle", ell([930, 900], [420, 90], "#A0703F") + ell([930, 895], [460, 110], "#7A5230"), s, e)


def set_kitchen(s, e, night=False):
    bg("k_wall", rect([960, 440], [1920, 880], "#3E4C7A" if night else "#FFE9C7"), s, e)
    bg("k_floor", rect([960, 980], [1920, 200], "#D9A878") + rect([960, 882], [1920, 8], "#B9875A"), s, e)
    bg("k_window", rect([350, 300], [300, 260], "#1B2550" if night else "#9ED8FF", 20) + rect([350, 300], [340, 300], WHITE, 30), s, e)
    if night:
        L.append(shape_layer("k_moon", kit.moon_icon(45, "#1B2550") if hasattr(kit, "moon_icon") else ell([0, 0], [90, 90], "#FFE58A"),
                             s, e - s, (380, 280)))
        bg("k_lamp", ell([960, 160], [260, 120], "#FFE58A") + rect([960, 60], [10, 120], "#8A939C"), s, e)
    bg("k_shelf", rect([1500, 260], [420, 20], "#B5835A", 8) + ell([1380, 220], [70, 70], CORAL) + rect([1500, 215], [70, 70], "#4A90E2", 14) +
       ell([1620, 220], [70, 70], "#2BB673"), s, e)


def table(id_, s, e, x=1000, w=900, food=True):
    items = []
    if food:
        for i, dx in enumerate([-300, -100, 100, 300]):
            items += [group(ell([x + dx, 760], [130, 40], ["#FF8A00", "#2BB673", CORAL, YELLOW][i]))]
            items += [group(ell([x + dx, 770], [170, 50], WHITE) + [{"type": "stroke", "color": "#D0D7DE", "width": 4}])]
    items += [group(rect([x, 800], [w, 40], "#C98E63", 16) + rect([x - w / 2 + 40, 900], [30, 200], "#A86F45", 10) +
                    rect([x + w / 2 - 40, 900], [30, 200], "#A86F45", 10) + rect([x, 850], [w - 60, 70], "#E8B98A", 10))]
    bg(id_, items, s, e)


set_garden(0, CUT_KITCHEN)
set_kitchen(CUT_KITCHEN, CUT_BATH1)
table("k_table", CUT_KITCHEN, CUT_BATH1, x=1000, w=520, food=False)
L.append(prop("k_plate", [group(ell([0, 0], [120, 40], "#FF8A00")), group(ell([0, 10], [170, 50], WHITE) + [{"type": "stroke", "color": "#D0D7DE", "width": 4}])],
              (1000, 760), T["mama1"] + 1.9, CUT_BATH1 - T["mama1"] - 1.9))
for i in range(3):
    L.append(prop(f"k_steam{i}", [group(rect([0, 0], [10, 60], WHITE, 5))], (970 + 30 * i, 690), T["mama1"] + 2.2 + 0.2 * i,
                  CUT_BATH1 - T["mama1"] - 2.4, bob=12))


def set_bathroom(sfx, s, e):
    bg("b_wall" + sfx, rect([960, 440], [1920, 880], "#FFF1C1"), s, e)
    bg("b_tiles" + sfx, rect([960, 980], [1920, 200], "#BFE6F7") + rect([960, 882], [1920, 8], "#8FCDEB"), s, e)
    bg("b_window" + sfx, ell([330, 300], [340, 340], "#9ED8FF") + ell([330, 300], [380, 380], WHITE), s, e)
    bg("b_stool" + sfx, rect([330, 935], [380, 70], "#E2A86B", 25), s, e)


set_bathroom("1", CUT_BATH1, CUT_LESSON)
bg("les_wall", rect([960, 440], [1920, 880], "#FFF6D8"), CUT_LESSON, CUT_BATH2)
bg("les_floor", rect([960, 980], [1920, 200], "#CDEBC0") + rect([960, 882], [1920, 8], "#9ED39A"), CUT_LESSON, CUT_BATH2)
bg("les_board", rect([1230, 440], [1140, 640], "#2F6B57", 24) + rect([1230, 440], [1190, 690], "#B5835A", 36), CUT_LESSON, CUT_BATH2)
set_bathroom("2", CUT_BATH2, CUT_DINNER)
set_kitchen(CUT_DINNER, END, night=True)
for l in L[-6:]:
    l["id"] += "_n"

# ================================================================ INTRO (garden) props
mud_t = wt("intro", "mud")
L.append(prop("mudcake", [group(rect([0, -95], [8, 60], "#FFE58A", 4) + ell([0, -135], [22, 30], "#FF8A00")),
                          group(rect([0, -30], [220, 70], "#9B6A3C", 20) + rect([0, 20], [260, 80], "#7A5230", 24) +
                                [{"type": "stroke", "color": "#5A3A1E", "width": 6}])], (930, 860), 0.3, CUT_KITCHEN - 0.3, wiggle=3))
for i, (x, y) in enumerate([(820, 700), (1040, 690), (930, 640)]):
    L.append(prop(f"mudspark{i}", sparkle_icon(34, YELLOW), (x, y), mud_t + 0.1 * i, 2.2, spin=150))
text("t_pia", "Pia", (1330, 470), 80, wt("intro", "Pia"), 2.0, color="#7B55C7")
hands_t = wt("intro", "hands")
L += kit.two_hands("in_hands_", hands_t - 0.3, CUT_KITCHEN - hands_t + 0.2, (960, 380), 0.75, mud=True)
text("t_muddy", "Muddy hands!", (960, 130), 100, wt("intro", "muddy") - 0.2, CUT_KITCHEN - wt("intro", "muddy"), color="#8B5A2B", wobble=True)
text("t_hi", "Hi! I'm Mokki!", (960, 130), 100, wt("intro", "Hi"), wt("intro", "Look") - wt("intro", "Hi"))

# ================================================================ STORY (kitchen)
text("t_dinner", "Dinner time!", (960, 130), 100, wt("mama1", "Dinner") - 0.3, 2.0, color=CORAL)
text("t_wait", "Wait!", (960, 130), 120, wt("mama2", "Wait"), 1.5, color="#9B59D0", wobble=True)
card_c = (1000, 420)
c0 = wt("mama2", "Look")
c1 = T["mama3"] - 0.2
L.append(kit.card_layer("st_card", c0, c1 - c0, card_c, (720, 420), border="#7BC043"))
L += kit.two_hands("st_hands_", c0 + 0.2, c1 - c0 - 0.2, (card_c[0], card_c[1] + 40), 0.8, mud=True)
g0 = wt("mama2", "Tiny")
gone = wt("mokki2", "away")
for i, (dx, dy) in enumerate([(-150, -40), (120, 10), (-40, 100), (170, -100), (-200, 90)]):
    st = g0 + 0.15 * i
    L.append(shape_layer(f"st_germ{i}", kit.germ_icon(), st, c1 - st, (card_c[0] + dx, card_c[1] + dy),
                         {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [0.8, 0.8]}]},
                          "position": {"keyframes": [{"time": 0, "value": [card_c[0] + dx, card_c[1] + dy]}],
                                       "expression": f"return value+Vec.v2(10*math.sin(time*9+{i}),8*math.cos(time*7+{i}))"},
                          "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 15*math.sin(time*6)"}}))
text("t_germs", "Germs!", (960, 130), 110, wt("mama2", "germs"), 1.6, color="#4E8A1E", wobble=True)
text("t_eww", "Eww!", (960, 130), 130, wt("mokki2", "Eww"), 1.3, color="#4E8A1E", wobble=True)
text("t_goaway", "Go away, germs!", (960, 130), 100, wt("mokki2", "Go"), T["mama3"] - wt("mokki2", "Go"), color=CORAL)
s0 = wt("mama3", "soap")
L.append(prop("st_soap", [group(rect([0, 20], [120, 150], "#F3E6FF", 36) + rect([0, -80], [60, 16], "#9B59D0", 6) +
                                [{"type": "stroke", "color": "#9B59D0", "width": 6}])], (860, 420), s0, CUT_BATH1 - s0 - 0.2, wiggle=8))
L.append(prop("st_water", [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -40], "outerRadius": 46},
                                  {"type": "ellipse", "position": [0, 0], "size": [80, 80]}, {"type": "fill", "color": "#5BC0EB"}])],
              (1140, 420), wt("mama3", "water"), CUT_BATH1 - wt("mama3", "water") - 0.2, wiggle=-8))
text("t_sing1", "Let's sing!", (960, 130), 110, wt("mama3", "Let's", 2), CUT_BATH1 - wt("mama3", "Let's", 2))

# ================================================================ SONG (both passes)
C = (1190, 560)
def song_pass(si, a):
    p = f"s{si}_"
    text(p + "head", "Let's wash our hands!" if si == 0 else "Now YOU wash with Mokki!", (960, 130), 90, a + 0.4, 8.0)
    for li, (s, e, line) in enumerate(LYRICS):
        text(f"{p}ly{li}", line, (960, 120), 74, a + s, e - s, pop=False)
    L.extend(kit.water_demo(p + "wat_", a + 9.2, 4.55, C))
    L.extend(kit.soap_demo(p + "soap_", a + 13.8, 4.5, C))
    L.extend(kit.rub_demo(p + "rub1_", a + 18.4, 9.0, "rub", C, germs_at=a + 23.3))
    for k, (s, e, mode) in enumerate([(36.85, 39.15, "palms"), (39.2, 41.35, "backs"), (41.4, 43.75, "fingers"), (43.8, 46.5, "thumbs")]):
        L.extend(kit.rub_demo(f"{p}v2_{k}_", a + s, e - s, mode, C))
    L.extend(kit.rub_demo(p + "rub2_", a + 55.3, 9.0, "rub", C, germs_at=a + 60.2))
    L.extend(kit.rinse_demo(p + "rin_", a + 73.75, 2.35, C))
    L.extend(kit.dry_demo(p + "dry_", a + 76.1, 4.5, C))
    for i, (x, y) in enumerate([(700, 380), (1650, 360), (760, 760), (1600, 760), (1190, 280), (1190, 860)]):
        L.append(prop(f"{p}clean{i}", sparkle_icon(55, YELLOW), (x, y), a + 80.7 + 0.1 * i, 3.3, spin=200))
    text(p + "clean", "Sparkly clean!", (1190, 560), 130, a + 80.9, 3.0, color="#2BB673", wobble=True)
    # dancing bubbles during the instrumental breaks
    random.seed(si)
    for brk, (b0, b1) in enumerate([(27.7, 36.7), (46.6, 55.2), (64.7, 73.6)]):
        for i in range(7):
            x = random.randint(650, 1800); per = random.uniform(2.5, 4.0)
            L.append({"id": f"{p}brk{brk}_{i}", "start": snap(a + b0), "duration": snap(b1 - b0), "timeMode": "layer",
                      "content": {"kind": "shape", "items": kit.bubble_icon(random.randint(26, 50))},
                      "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 1100]}],
                                                  "expression": f"local t=(time+{i * 0.5})%{per:.2f}; return Vec.v2({x}+30*math.sin(t*3), 1100-t/{per:.2f}*1200)"}}})
    text(p + "dance", "Dance with Mokki!", (1190, 560), 110, a + 28.0, 4.0, color="#9B59D0", wobble=True)

for si, (a, b) in enumerate(SONGS):
    song_pass(si, a)

# ================================================================ LESSON (board)
o = T["lesson"]
for i, (x, y) in enumerate([(250, 450), (600, 420), (230, 760), (640, 760)]):
    L.append(prop(f"le_sp{i}", sparkle_icon(40, YELLOW), (x, y), wt("lesson", "sparkly") + 0.1 * i, 2.2, spin=150))
text("le_when", "When do we wash?", (1230, 175), 64, wt("lesson", "When"), wt("lesson", "Number") - wt("lesson", "When") - 0.2, color=WHITE, stroke=None)
BOARD = (1250, 480)
when = [("eat", (960, 420), [group(ell([0, 0], [120, 40], "#FF8A00")), group(ell([0, 10], [170, 50], WHITE) + [{"type": "stroke", "color": "#D0D7DE", "width": 4}]),
                              group(rect([-120, 0], [14, 120], "#C9D1D9", 6) + rect([120, 0], [14, 120], "#C9D1D9", 6))], "before eating"),
        ("potty", (1520, 420), [group(rect([0, -50], [90, 70], WHITE, 14) + [{"type": "stroke", "color": "#8FCDEB", "width": 6}]),
                                group(ell([0, 30], [160, 90], WHITE) + [{"type": "stroke", "color": "#8FCDEB", "width": 6}]),
                                group(rect([0, 80], [80, 70], WHITE, 10) + [{"type": "stroke", "color": "#8FCDEB", "width": 6}])], "after the potty"),
        ("outside", (960, 660), [group(ell([0, 0], [120, 120], CORAL) + rect([0, 0], [120, 16], WHITE, 0)),
                                 group(ell([0, 0], [124, 124], "#B9875A"))], "after playing"),
        ("sneeze", (1520, 660), [group(rect([0, 20], [150, 100], WHITE, 20) + [{"type": "stroke", "color": "#8FCDEB", "width": 6}]),
                                 group(rect([0, -40], [80, 50], WHITE, 14) + [{"type": "stroke", "color": "#8FCDEB", "width": 6}])], "after a sneeze")]
w_end = wt("lesson", "Number") - 0.2
for k, (word, pos, items, label) in enumerate(when):
    t0 = wt("lesson", word)
    L.append(prop(f"le_w{k}", items, pos, t0, w_end - t0, s=0.8, wiggle=6))
    text(f"le_wl{k}", label, (pos[0], pos[1] + 100), 40, t0 + 0.1, w_end - t0 - 0.1, color=WHITE, stroke=None)
text("le_achoo", "Achoo!", (1700, 560), 56, wt("lesson", "sneeze"), w_end - wt("lesson", "sneeze"), color=YELLOW, stroke=None)
nums = [wt("lesson", "Number", k) for k in range(1, 6)] + [wt("lesson", "Now")]
demos = [kit.water_demo, kit.soap_demo, None, kit.rinse_demo, kit.dry_demo]
for k in range(5):
    s, e = nums[k] + 0.2, nums[k + 1] - 0.1
    text(f"le_num{k}", str(k + 1), (735, 470), 150, nums[k], e - nums[k], color=YELLOW, stroke=None)
    if k == 2:
        L.extend(kit.rub_demo("le_rub_", s, e - s, "rub", BOARD, sc=0.85, card=False, count=True))
    else:
        L.extend(demos[k](f"le_d{k}_", s, e - s, BOARD, sc=0.85, card=False))
L.extend(kid_text("le_turn", "Your turn!", (1230, 300), 90, nums[5], wt("lesson", "One") - nums[5] - 0.1,
                                                      color=YELLOW, stroke=None))
L += kit.two_hands("le_turnh_", nums[5] + 0.3, wt("lesson", "One") - nums[5] - 0.4, (1230, 560), 0.75, rub="rub")
for n, (k, c) in enumerate([("One", CORAL), ("two", "#4A90E2"), ("three", "#2BB673")], 1):
    t0 = wt("lesson", k)
    text(f"le_cnt{n}", str(n), (930 + 300 * (n - 1), 480), 240, t0, o + 33.0 - t0, color=c)

# ================================================================ BYE (family dinner)
o = T["bye"]
for i in range(14):
    x = 200 + i * 120; c = [CORAL, YELLOW, "#4A90E2", "#2BB673", PINK][i % 5]
    L.append(prop(f"by_conf{i}", [group(rect([0, 0], [26, 40], c, 6))], (x, -50), o + 0.1 + (i % 4) * 0.1, 4.0, spin=200,
                  extra={"position": {"keyframes": [{"time": 0, "value": [x, -50]}, {"time": 4.0, "value": [x + 60 * ((i % 3) - 1), 1150]}]}}))
text("by_yay", "Clean hands!", (960, 130), 110, wt("bye", "Yay"), wt("bye", "Papa") - wt("bye", "Yay") - 0.1, color="#2BB673")
SEATS = {"papa": 330, "mama": 640, "mokki": 960, "pia": 1260, "pip": 1530}
for k, (cid, word, name, col) in enumerate([("papa", "Papa", "Papa", "#2A6FB0"), ("mama", "Mama", "Mama", "#D65A86"),
                                            ("pia", "Pia", "Pia", "#7B55C7"), ("pip", "Pip", "baby Pip", "#D19A12")]):
    t0 = wt("bye", word)
    text(f"by_name{k}", name, (SEATS[cid], 330), 64, t0, END - t0, color=col)
L.append(prop("by_soap", [group(rect([0, 20], [120, 150], "#F3E6FF", 36) + rect([0, -80], [60, 16], "#9B59D0", 6) +
                                [{"type": "stroke", "color": "#9B59D0", "width": 6}])], (1760, 600), wt("bye", "soap"), 2.0, wiggle=8))
text("bye", "Bye-bye, friends!\nSee you tomorrow!", (960, 150), 90, wt("bye", "Bye-bye"), END - wt("bye", "Bye-bye"), color=CORAL)

# ================================================================ CHARACTERS
# Mokki: one rig for the whole episode (positions per set)
POS = {"garden": [620, 905], "kitchen": [380, 905], "bath": [330, 905], "lesson": [430, 890], "dinner": [SEATS["mokki"], 860]}
pos_keys = [{"time": 0, "value": POS["garden"], "easing": "step"},
            {"time": CUT_KITCHEN, "value": POS["kitchen"], "easing": "step"},
            {"time": T["mokki1"], "value": POS["kitchen"], "easing": "ease_in_out"},
            {"time": T["mokki1"] + 0.6, "value": [600, 905]},
            {"time": T["mama2"] + 0.3, "value": [600, 905], "easing": "ease_in_out"},
            {"time": T["mama2"] + 1.0, "value": POS["kitchen"], "easing": "step"},
            {"time": CUT_BATH1, "value": POS["bath"], "easing": "step"},
            {"time": CUT_LESSON, "value": POS["lesson"], "easing": "step"},
            {"time": CUT_BATH2, "value": POS["bath"], "easing": "step"},
            {"time": CUT_DINNER, "value": POS["dinner"], "easing": "step"}]
songs_cond = " or ".join(f"(time>={a:.2f} and time<{b:.2f})" for a, b in SONGS)
songs_start = " ".join(f"if time>={a:.2f} and time<{b:.2f} then s={a:.2f} end;" for a, b in SONGS)
bounce = (f"local s=0; {songs_start} if {songs_cond} then local b=math.abs(math.sin(math.pi*(time-s)/0.577)); return value+Vec.v2(0,-40*b) "
          f"else return value+Vec.v2(0,-10*math.sin(2*math.pi*time/1.6)) end")
eww0 = wt("mokki2", "Eww")
wave0 = wt("bye", "Bye-bye")
rot = (f"local r=value+4*math.sin(2*math.pi*time/2.4); if time>={eww0:.2f} and time<{eww0 + 0.8:.2f} then r=r+10*math.sin(time*45) end; "
       f"if time>={wave0:.2f} then r=r+12*math.sin(time*10) end; return r")
mwords = []
for clip in ("intro", "mokki1", "mokki2", "lesson", "bye"):
    mwords += words_from_transcript(W[clip], T[clip])
for a, _ in SONGS:
    mwords += [(a + s, a + e, 0) for s, e in SONG_WORDS]
L += mokki_rig("mokki", mwords, pos_keys, scale=0.5, pos_expr=bounce, rot_expr=rot,
               scale_keys=[{"time": 0, "value": [0.5, 0.5], "easing": "step"}, {"time": CUT_DINNER, "value": [0.42, 0.42], "easing": "step"},
                           {"time": END - 0.8, "value": [0.42, 0.42], "easing": "ease_in"}, {"time": END, "value": [0, 0]}],
               closed=[(T["lesson"] + 2.8, T["lesson"] + 3.6)])

# Pia in the garden (giggling, bouncing)
L += place(family_rig("pia", [], [{"time": 0, "value": [1330, 905]}], scale=0.5, prefix="pia_g",
                      pos_expr="return value+Vec.v2(0,-18*math.abs(math.sin(time*3)))",
                      rot_expr=f"local r=value+5*math.sin(time*2); if time>{wt('intro','Pia') - 0.8:.2f} and time<{wt('intro','Pia') + 1.2:.2f} then r=r+12*math.sin(time*12) end; return r"),
           0, CUT_KITCHEN)
# Mama in the kitchen (talks)
ks = CUT_KITCHEN
mama_words = []
for clip in ("mama1", "mama2", "mama3"):
    mama_words += words_from_transcript(W[clip], T[clip] - ks)
L += place(family_rig("mama", mama_words, [{"time": 0, "value": [1620, 905]}], scale=0.5, prefix="mama_k"), ks, CUT_BATH1 - ks)
# family at the dinner table (behind the table)
ds = CUT_DINNER
for cid, sc in [("papa", 0.42), ("mama", 0.42), ("pia", 0.42), ("pip", 0.42)]:
    rot_wave = f"local r=value+4*math.sin(time*2+{len(cid)}); if time>{wave0 - ds:.2f} then r=r+10*math.sin(time*9+{len(cid)}) end; return r"
    L += place(family_rig(cid, [], [{"time": 0, "value": [SEATS[cid], 860]}], scale=sc, prefix=cid + "_d", rot_expr=rot_wave), ds, END - ds)
table("d_table", CUT_DINNER, END, x=950, w=1600)

# ================================================================ wipes + audio
for i, cut in enumerate([CUT_KITCHEN, CUT_BATH1, CUT_LESSON, CUT_BATH2, CUT_DINNER]):
    L.append(wipe(f"wipe{i}", cut - 0.4))
for k, uri in V.items():
    L.append(audio("a_" + k, T[k], uri))
L.append(audio("a_song1", T_SONG1, SONG))
L.append(audio("a_song2", T_SONG2, SONG))

# ================================================================ write
for l in L:
    for k in ("start", "duration"):
        if k in l:
            l[k] = snap(l[k])
text_check.resolve(L)
ids = [l["id"] for l in L]
dup = {i for i in ids if ids.count(i) > 1}
assert not dup, dup
scene = {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": END, "background": "#FFF1C1"}, "layers": L}
json.dump(scene, open(os.path.join(HERE, "ep02-scene.json"), "w"), separators=(",", ":"))
full = branding.wrap_episode(L, END)
json.dump(full, open(os.path.join(HERE, "ep02-full-scene.json"), "w"), separators=(",", ":"))
print("episode", END, "s; full", full["composition"]["duration"], "s;", len(L), "layers")
