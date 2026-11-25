"""Mokki & Friends - Episode 4: Yummy Vegetables. Builds ep04-scene.json (episode) and ep04-full-scene.json (with intro/outro)."""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import kit, text_check, branding, veggies as vg
from kit import (NAVY, WHITE, YELLOW, CORAL, GREEN, PINK, BODY, POP, snap, rect, ell, group, shape_layer, prop, audio,
                 sparkle_icon, heart_icon, cloud_icon, mokki_rig, family_rig, words_from_transcript, wipe, kid_text)

A = "https://gcdn.picsart.com/picsart-mcp/"
SONG = A + "03c821bd-e0b5-4716-8b34-8be0ba1d6752.mp3"
V = {"intro": A + "6e66538c-06c6-4fa1-b60a-30ebc0338182.mp3", "granny1": A + "05df3839-588f-4f5e-a420-7b7d738ab20b.mp3",
     "mokki1": A + "ffc6cb48-276f-4d19-af4b-538b1fee46ff.mp3", "granny2": A + "de6355ef-dc36-44d0-b425-28d064d06016.mp3",
     "mokki2": A + "2250c6cd-8251-47db-90a0-7b68d2a73525.mp3", "granny3": A + "b14cc713-a5d8-4685-bee7-a9be8ace236d.mp3",
     "lesson": A + "ecfdcf6f-e90c-499f-882d-51ef2559264c.mp3", "bye": A + "016d15ea-4dfc-4afc-a312-45831f6a7488.mp3"}
ABSTRACT = A + "6a99cc0e-bddd-476f-a14e-f72e128b7a84.mp3"
kit.FAMILY_URLS.update({"papa": A + "5516daa6-d600-4b6f-a122-3abc2539f009.png", "mama": A + "01131a7b-4f78-493a-a350-6618e929c06e.png",
                        "pia": A + "3ddbe55c-ed46-4d5c-a19f-b6a70cba4911.png", "pip": A + "2a573c49-2923-41de-a8ff-90e5deb37f64.png",
                        "grandpa": A + "a61529f1-96eb-4251-a7c3-0c0c77f0435a.png", "grandma": A + "5abb3d82-2b1d-4d45-a169-de98b8c0cb78.png"})

W = {
 "intro": [(0.08,0.24,"Hi"),(0.4,0.92,"friends"),(1.04,1.28,"It's"),(1.4,1.64,"me"),(1.76,2.36,"Mokki"),(2.48,3.16,"[giggles]"),
           (3.2,3.52,"Today"),(3.68,3.84,"I'm"),(3.92,4.24,"visiting"),(4.32,4.56,"Granny"),(4.64,4.88,"Mo"),(4.96,5.12,"and"),
           (5.24,5.52,"Grandpa"),(5.6,6.48,"Moss"),(6.64,6.8,"Look"),(6.88,6.96,"at"),(7.12,7.28,"their"),(7.36,7.68,"big"),
           (7.72,8.72,"garden"),(8.84,8.96,"So"),(9.04,9.36,"many"),(9.44,10.36,"colors"),(10.4,11.2,"orange"),(11.4,11.92,"green"),
           (12.04,12.4,"red"),(12.52,12.64,"and"),(12.92,13.44,"purple")],
 "granny1": [(0.16,0.4,"Lunch"),(0.48,0.56,"is"),(0.64,0.96,"ready"),(1.04,1.12,"my"),(1.2,1.36,"little"),(1.44,2.16,"sprout"),
             (2.4,2.8,"Yummy"),(2.96,3.44,"vegetable"),(3.6,3.92,"soup"),(4.0,4.08,"and"),(4.16,4.24,"a"),(4.48,4.96,"rainbow"),(5.04,5.76,"plate")],
 "mokki1": [(0.16,0.96,"Hmm"),(1.2,2.28,"vegetables"),(2.48,2.64,"I"),(2.76,2.88,"only"),(2.96,3.2,"like"),(3.28,4.24,"cookies")],
 "granny2": [(0.24,0.56,"Try"),(0.8,1.04,"one"),(1.28,1.68,"tiny"),(1.76,2.56,"bite"),(2.88,3.44,"Vegetables"),(3.52,3.68,"make"),
             (3.76,3.92,"you"),(4.2,4.72,"strong"),(4.8,5.04,"help"),(5.12,5.2,"you"),(5.4,5.84,"grow"),(6.0,6.16,"and"),(6.32,6.48,"keep"),
             (6.56,6.72,"your"),(6.8,7.04,"tummy"),(7.12,7.76,"happy")],
 "mokki2": [(0.16,1.2,"Okay"),(1.52,1.84,"one"),(1.92,2.32,"tiny"),(2.56,3.28,"bite"),(3.44,4.0,"[crunch]"),(4.24,4.92,"Mmm"),
            (5.04,5.36,"It's"),(5.44,6.24,"yummy")],
 "granny3": [(0.08,1.04,"Hooray"),(1.2,1.44,"Let's"),(1.56,1.68,"sing"),(1.76,1.84,"the"),(2.0,2.32,"veggie"),(2.4,3.2,"song")],
 "lesson": [(0.16,0.4,"My"),(0.56,0.96,"tummy"),(1.04,1.2,"is"),(1.28,1.88,"happy"),(2.0,2.72,"[giggles]"),(2.76,3.12,"Veggie"),
            (3.28,4.12,"secrets"),(4.32,4.56,"Number"),(4.72,5.36,"one"),(5.44,5.52,"eat"),(5.6,5.64,"a"),(5.68,6.48,"rainbow"),
            (6.64,6.88,"lots"),(6.96,7.04,"of"),(7.12,7.6,"colors"),(7.68,8.0,"every"),(8.08,8.72,"day"),(8.96,9.2,"Number"),
            (9.36,10.0,"two"),(10.2,10.4,"always"),(10.48,10.72,"try"),(10.96,11.12,"one"),(11.28,11.68,"tiny"),(11.76,12.4,"bite"),
            (12.52,12.64,"even"),(12.72,12.8,"if"),(12.84,12.88,"it"),(12.96,13.2,"looks"),(13.28,13.6,"new"),(14.0,14.24,"Number"),
            (14.4,15.12,"three"),(15.2,15.44,"wash"),(15.52,16.08,"vegetables"),(16.16,16.64,"before"),(16.72,16.8,"we"),(16.88,17.04,"eat"),
            (17.12,17.56,"them"),(17.76,18.0,"Number"),(18.16,18.8,"four"),(18.88,19.04,"say"),(19.2,19.44,"thank"),(19.52,19.6,"you"),
            (19.68,19.76,"to"),(19.8,19.84,"the"),(20.0,20.48,"cook"),(20.72,20.88,"Now"),(20.96,21.12,"it's"),(21.2,21.36,"your"),
            (21.44,21.92,"turn"),(22.08,22.32,"Find"),(22.36,22.4,"a"),(22.48,22.8,"veggie"),(22.88,22.96,"and"),(23.12,23.28,"sing"),
            (23.36,23.44,"with"),(23.52,23.76,"me"),(24.08,24.64,"Ready"),(24.88,25.36,"One"),(25.44,25.92,"two"),(26.12,26.64,"three")],
 "bye": [(0.08,0.32,"Thank"),(0.4,0.56,"you"),(0.64,1.24,"Granny"),(1.44,1.68,"Thank"),(1.76,1.88,"you"),(1.92,2.6,"Grandpa"),
         (2.72,3.36,"[giggles]"),(3.44,3.52,"I"),(3.76,4.0,"love"),(4.08,4.64,"vegetables"),(4.72,5.28,"now"),(5.52,5.6,"What"),
         (5.68,5.84,"is"),(5.96,6.08,"your"),(6.16,6.48,"favorite"),(6.56,7.32,"vegetable"),(7.68,8.04,"Bye-bye"),(8.08,8.76,"friends"),
         (8.96,9.04,"See"),(9.12,9.2,"you"),(9.32,9.68,"tomorrow"),(9.76,9.92,"in"),(10.0,10.32,"Mokki"),(10.4,11.04,"World")],
}
SONG_WORDS = [(9.52,10.02),(10.12,10.68),(10.76,11.04),(11.08,11.24),(11.3,11.68),(11.88,12.12),(12.18,12.38),(12.46,12.72),(12.8,12.98),
 (13.08,13.36),(13.42,13.62),(13.68,14.02),(14.24,14.72),(14.8,15.3),(15.42,15.88),(16.0,16.34),(16.62,17.12),(17.26,17.64),(17.8,18.06),
 (18.16,18.62),(19.0,19.2),(19.3,19.5),(19.58,20.14),(20.24,20.62),(20.74,20.98),(21.3,21.56),(21.64,21.76),(21.84,22.12),(22.18,22.42),
 (22.46,22.72),(22.76,23.4),(23.7,23.88),(23.96,24.18),(24.26,24.46),(24.56,24.84),(24.9,25.14),(25.18,25.28),(25.38,25.78),(26.02,26.52),
 (26.6,27.14),(27.2,27.46),(27.52,27.64),(27.74,28.16),(37.78,38.02),(38.1,38.88),(38.96,39.26),(39.28,39.42),(39.52,39.8),(40.16,40.6),
 (40.72,41.0),(41.08,41.16),(41.28,41.76),(41.86,42.22),(42.48,42.7),(42.78,43.04),(43.12,43.58),(43.7,43.86),(43.96,44.1),(44.22,44.54),
 (44.84,45.34),(45.46,45.96),(46.04,46.3),(46.36,46.56),(46.64,46.88),(56.64,56.88),(56.94,57.14),(57.22,57.78),(57.9,58.26),(58.38,58.7),
 (58.94,59.2),(59.28,59.42),(59.48,59.74),(59.82,60.06),(60.1,60.36),(60.4,61.0),(61.34,61.52),(61.6,61.82),(61.9,62.1),(62.22,62.48),
 (62.56,62.78),(62.82,62.92),(63.04,63.36),(63.7,64.16),(64.24,64.8),(64.86,65.1),(65.16,65.28),(65.4,65.78),(77.54,77.66),(77.76,78.28),
 (78.42,78.58),(78.64,78.8),(78.9,79.16),(79.22,79.82),(80.06,80.38),(80.46,80.64),(80.72,81.2),(81.3,81.52),(81.62,82.28),(84.88,85.34),
 (85.46,85.92),(86.06,86.38)]
LYRICS = [(9.4, 11.8, "Crunchy carrots, orange and bright,"), (11.85, 14.15, "Help my eyes see day and night!"),
          (14.2, 16.5, "Green broccoli, little trees,"), (16.55, 18.9, "Yummy, yummy, more please!"),
          (18.95, 21.2, "Eat your veggies every day,"), (21.25, 23.6, "Grow up strong, hip hip hooray!"),
          (23.65, 25.9, "One more bite, give it a try,"), (25.95, 28.4, "Yummy veggies, reach the sky!"),
          (37.7, 40.0, "Red tomatoes, round and sweet,"), (40.05, 42.4, "Yellow corn, a crunchy treat!"),
          (42.45, 44.7, "Green peas rolling, one, two, three,"), (44.75, 47.2, "Purple eggplant, look at me!"),
          (56.55, 58.85, "Eat your veggies every day,"), (58.9, 61.2, "Grow up strong, hip hip hooray!"),
          (61.25, 63.6, "One more bite, give it a try,"), (63.65, 66.1, "Yummy veggies, reach the sky!"),
          (77.45, 79.95, "A rainbow on my plate today,"), (80.0, 82.6, "Strong and healthy, hip hooray!"),
          (84.8, 87.2, "Yummy, yummy, yay!")]

T = {"intro": 0.8, "granny1": 15.3, "mokki1": 21.6, "granny2": 26.4, "mokki2": 34.7, "granny3": 41.4, "lesson": 135.8, "bye": 253.8}
T_SONG1, T_SONG2, SONG_LEN = 45.0, 163.0, 90.0
CUT_KITCHEN, CUT_SONG1, CUT_LESSON, CUT_SONG2, CUT_BYE = 14.8, 44.6, 135.4, 162.6, 253.4
END = 267.5
SONGS = [(T_SONG1, T_SONG1 + SONG_LEN), (T_SONG2, T_SONG2 + SONG_LEN)]
KID_COLORS = ["#F0506E", "#2BB673", "#4A90E2", "#FF8A00", "#9B59D0"]
VEG_ORDER = ["carrot", "broccoli", "tomato", "corn", "peas", "eggplant"]


def wt(clip, word, n=1):
    k = 0
    for s, e, w in W[clip]:
        if w.lower() == word.lower():
            k += 1
            if k == n:
                return T[clip] + s
    raise KeyError((clip, word, n))


def we(clip, word, n=1):
    k = 0
    for s, e, w in W[clip]:
        if w.lower() == word.lower():
            k += 1
            if k == n:
                return T[clip] + e
    raise KeyError((clip, word, n))


def text(id_, t, pos, size, start, dur, color=None, stroke=WHITE, pop=True, wobble=False, wrap=None):
    if color is None:
        color = KID_COLORS[sum(map(ord, id_)) % len(KID_COLORS)]
    L.extend(kid_text(id_, t, pos, size, start, dur, color=color, stroke=stroke, pop=pop, wobble=wobble, wrap=wrap))


def bg(id_, items, start, end):
    L.append(shape_layer(id_, items, start, end - start, absolute=True))


def place(layers, start, dur):
    for l in layers:
        l["start"], l["duration"], l["timeMode"] = snap(start), snap(dur), "layer"
    return layers


def cookie_icon():
    chips = [{"type": "ellipse", "position": [x, y], "size": [26, 22]} for x, y in ((-40, -30), (30, -45), (0, 10), (45, 25), (-35, 40))]
    return [group(chips + [{"type": "fill", "color": "#6B3E1E"}]),
            group(ell([0, 0], [200, 200], "#E8B46A") + [{"type": "stroke", "color": "#B57A35", "width": 8}])]


L = []
# ================================================================ SETS
def garden(sfx, s, e, sunset=False):
    sky, sky2 = ("#FFC59A", "#FFB0A0") if sunset else ("#9ED8FF", "#BDE6FF")
    bg("g_sky" + sfx, rect([960, 400], [1920, 800], sky), s, e)
    bg("g_sky2" + sfx, rect([960, 120], [1920, 240], sky2), s, e)
    L.append(shape_layer("g_sun" + sfx, ell([0, 0], [200, 200], "#FFD23F") + ell([0, 0], [260, 260], "#FFE58A"), s, e - s,
                         (1700, 160) if not sunset else (1600, 520)))
    if not sunset:
        for i, (x, y) in enumerate([(300, 150), (1000, 110)]):
            L.append(shape_layer(f"g_cloud{sfx}{i}", cloud_icon(300), s, e - s, (x, y),
                                 {"position": {"keyframes": [{"time": 0, "value": [x, y]}], "expression": "return value+Vec.v2(15*time%300,0)"}}))
    bg("g_hill" + sfx, ell([500, 700], [1500, 300], "#6BB84E") + ell([1500, 720], [1300, 260], "#7BC85E"), s, e)
    bg("g_grass" + sfx, rect([960, 900], [1920, 360], "#8BD36B"), s, e)
    # fence
    bg("g_fence" + sfx, [group([{"type": "rect", "position": [x, 640], "size": [36, 150], "roundness": 10} for x in range(30, 1920, 90)] +
                               [{"type": "rect", "position": [960, 610], "size": [1920, 20]}, {"type": "rect", "position": [960, 670], "size": [1920, 20]},
                                {"type": "fill", "color": WHITE}, {"type": "stroke", "color": "#D8D2C4", "width": 4}])], s, e)
    # vegetable beds: soil rows with carrot tops, cabbages, tomato plants
    bg("g_soil" + sfx, rect([960, 790], [1920, 70], "#8A5A3C", 35), s, e)
    tops = []
    for x in range(80, 1920, 150):
        tops += [vg.leaf([x, 770], -25, (24, 70)), vg.leaf([x, 770], 0, (24, 80)), vg.leaf([x, 770], 25, (24, 70))]
    bg("g_tops" + sfx, tops, s, e)
    bg("g_carrots" + sfx, [group([{"type": "ellipse", "position": [x, 778], "size": [40, 26]} for x in range(80, 1920, 150)] +
                                 [{"type": "fill", "color": vg.ORANGE}])], s, e)


def kitchen(s, e):
    bg("k_wall", rect([960, 440], [1920, 880], "#FFF1C9"), s, e)
    bg("k_stripe", [group([{"type": "rect", "position": [x, 440], "size": [40, 880]} for x in range(40, 1920, 160)] + [{"type": "fill", "color": "#FFE7A8"}])], s, e)
    bg("k_floor", [group([{"type": "rect", "position": [x + (60 if (y // 60) % 2 else 0), y], "size": [60, 60]}
                          for x in range(0, 1980, 120) for y in range(910, 1080, 60)] + [{"type": "fill", "color": "#F6D0A0"}])] +
       rect([960, 980], [1920, 200], "#FFE3BF") + rect([960, 882], [1920, 8], "#E5B47E"), s, e)
    bg("k_window", rect([960, 250], [420, 300], "#9ED8FF", 20) + rect([960, 250], [460, 340], WHITE, 30), s, e)
    bg("k_winsill", rect([960, 250], [12, 300], WHITE) + rect([960, 250], [420, 12], WHITE) + ell([900, 330], [260, 120], "#8BD36B"), s, e)
    bg("k_shelf", rect([300, 300], [300, 20], "#B5835A", 8) + ell([230, 260], [60, 60], vg.RED) + ell([300, 262], [56, 56], vg.CORN) +
       ell([370, 262], [58, 58], vg.LEAF), s, e)
    bg("k_table", rect([960, 700], [760, 40], "#C98E63", 20) + rect([960, 722], [720, 24], "#8A5A3C", 10) +
       rect([680, 820], [36, 220], "#8A5A3C", 12) + rect([1240, 820], [36, 220], "#8A5A3C", 12), s, e)
    L.append(shape_layer("k_pot", vg.soup_pot_icon(), s, e - s, (840, 590), {"scale": {"keyframes": [{"time": 0, "value": [0.6, 0.6]}]}}))
    L.extend(vg.steam_layers("k_", (840, 520), s, e - s))
    L.append(shape_layer("k_plate", vg.plate_icon(300), s, e - s, (1100, 676)))
    for i, (v, dx) in enumerate(zip(["tomato", "carrot", "broccoli", "corn"], (-90, -30, 30, 90))):
        L.append(shape_layer(f"k_pv{i}", vg.VEG[v](False), s, e - s, (1100 + dx, 640), {"scale": {"keyframes": [{"time": 0, "value": [0.3, 0.3]}]}}))


garden("1", 0, CUT_KITCHEN)
kitchen(CUT_KITCHEN, CUT_SONG1)
garden("2", CUT_SONG1, CUT_LESSON)
bg("les_wall", rect([960, 440], [1920, 880], "#FFF6D8"), CUT_LESSON, CUT_SONG2)
bg("les_floor", rect([960, 980], [1920, 200], "#CDEBC0") + rect([960, 882], [1920, 8], "#9ED39A"), CUT_LESSON, CUT_SONG2)
bg("les_board", rect([1230, 440], [1140, 640], "#2F6B57", 24) + rect([1230, 440], [1190, 690], "#B5835A", 36), CUT_LESSON, CUT_SONG2)
garden("3", CUT_SONG2, CUT_BYE)
garden("4", CUT_BYE, END, sunset=True)

# ================================================================ INTRO (garden)
text("t_hi", "Hi! I'm Mokki!", (960, 130), 100, wt("intro", "Hi"), wt("intro", "Today") - wt("intro", "Hi"))
text("t_grand", "Granny Mo & Grandpa Moss!", (960, 130), 84, wt("intro", "Granny"), wt("intro", "Look") - wt("intro", "Granny"), color="#C9733A")
text("t_garden", "A big garden!", (960, 130), 100, wt("intro", "garden"), wt("intro", "orange") - wt("intro", "garden"), color="#2BB673")
for k, (word, v, nxt) in enumerate([("orange", "carrot", "green"), ("green", "broccoli", "red"), ("red", "tomato", "purple"), ("purple", "eggplant", None)]):
    t0 = wt("intro", word)
    t1 = wt("intro", nxt) if nxt else CUT_KITCHEN
    text(f"t_col{k}", word.capitalize() + "!", (960, 130), 110, t0, t1 - t0, color=vg.VEG_COLOR[v], wobble=True)
    L.append(vg.veg_layer(f"i_veg{k}", v, (790, 400), t0, t1 - t0, s=1.3, wiggle=10))

# ================================================================ STORY (kitchen)
text("t_lunch", "Lunch time!", (960, 110), 100, wt("granny1", "Lunch"), wt("granny1", "Yummy") - wt("granny1", "Lunch"), color="#C9733A")
text("t_soup", "Yummy soup!", (960, 110), 100, wt("granny1", "Yummy"), wt("granny1", "rainbow") - wt("granny1", "Yummy"), color=vg.RED)
r0 = wt("granny1", "rainbow")
L.extend(vg.rainbow_plate_demo("st_plate_", r0, T["mokki1"] - r0, (960, 390), sc=0.5))
text("t_rainbow", "Rainbow plate!", (960, 110), 100, r0, T["mokki1"] - r0, color="#9B59D0")
text("t_hmm", "Hmm...", (960, 110), 110, wt("mokki1", "Hmm"), wt("mokki1", "I") - wt("mokki1", "Hmm"), color="#4A90E2")
c0 = wt("mokki1", "like")
text("t_cookies", "Only cookies?", (960, 110), 100, c0, T["granny2"] - c0, color="#B57A35", wobble=True)
L.append(prop("st_cookie", cookie_icon(), (760, 380), c0, T["granny2"] - c0, s=0.9, wiggle=12))
b0 = wt("granny2", "Try")
text("t_bite", "One tiny bite!", (960, 110), 100, b0, wt("granny2", "Vegetables") - b0, color=vg.ORANGE)
L.extend(vg.bite_demo("st_bite_", b0, wt("granny2", "Vegetables") - b0, "carrot", (960, 390), sc=0.5, crunch=False, bites=(1.5,)))
s0 = wt("granny2", "strong")
text("t_strong", "Strong!", (960, 110), 110, s0, wt("granny2", "grow") - s0, color="#2BB673", wobble=True)
L.extend(vg.grow_demo("st_grow_", s0, wt("granny2", "and") - s0, (960, 390), sc=0.5))
text("t_grow", "Grow!", (960, 110), 110, wt("granny2", "grow"), wt("granny2", "and") - wt("granny2", "grow"), color="#2BB673", wobble=True)
h0 = wt("granny2", "and")
text("t_tummy", "Happy tummy!", (960, 110), 100, h0, T["mokki2"] - h0, color="#E84393")
L.extend(vg.tummy_demo("st_tum_", h0, T["mokki2"] - h0, (960, 390), sc=0.5))
text("t_okay", "Okay...", (960, 110), 100, wt("mokki2", "Okay"), wt("mokki2", "one") - wt("mokki2", "Okay"), color="#4A90E2")
text("t_onebite", "One tiny bite...", (960, 110), 100, wt("mokki2", "one"), wt("mokki2", "[crunch]") - wt("mokki2", "one"), color=vg.ORANGE)
cr = wt("mokki2", "[crunch]")
text("t_crunch", "CRUNCH!", (960, 300), 150, cr, 1.0, color=vg.ORANGE, wobble=True)
text("t_yummy", "Mmm! Yummy!", (960, 110), 110, wt("mokki2", "Mmm"), T["granny3"] - wt("mokki2", "Mmm"), color="#E84393", wobble=True)
for i, (x, y) in enumerate([(220, 420), (650, 380), (300, 250), (600, 230)]):
    L.append(prop(f"st_heart{i}", heart_icon(40), (x, y), wt("mokki2", "Mmm") + 0.12 * i, T["granny3"] - wt("mokki2", "Mmm") - 0.12 * i, bob=14))
text("t_hooray", "Hooray!", (960, 110), 120, wt("granny3", "Hooray"), wt("granny3", "Let's") - wt("granny3", "Hooray"), color=CORAL, wobble=True)
text("t_sing", "The Veggie Song!", (960, 110), 100, wt("granny3", "Let's"), T_SONG1 + 3 - wt("granny3", "Let's"), color="#2BB673")
for i in range(12):
    x = 120 + i * 150
    L.append(prop(f"st_conf{i}", [group(rect([0, 0], [22, 34], KID_COLORS[i % 5], 6))], (x, 260 + (i % 3) * 60),
                  wt("granny3", "Hooray") + 0.05 * i, 1.6, spin=300))
# the carrot: Granny offers it, Mokki holds it and bites
L.append(vg.veg_layer("st_offer", "carrot", (1240, 560), b0, T["mokki2"] - b0, s=0.45, wiggle=10))
# ================================================================ SONG (garden)
C = (1230, 520)


def veg_row(p, t0, dur, y=600, xs=(760, 960, 1160, 1360, 1560, 1760), s=0.7, dance=True):
    for i, (v, x) in enumerate(zip(VEG_ORDER, xs)):
        ex = {"position": {"keyframes": [{"time": 0, "value": [x, y]}],
                           "expression": f"return value+Vec.v2(0,-40*math.abs(math.sin(math.pi*(time+{i * 0.1:.1f})/0.59)))"}} if dance else None
        L.append(vg.veg_layer(f"{p}{i}", v, (x, y), t0 + 0.08 * i, dur - 0.08 * i, s=s, wiggle=12, extra=ex))


def sky_demo(p, t0, dur):
    text(p + "txt", "Reach the sky!", (C[0], C[1]), 110, t0 + 0.2, dur - 0.2, color="#4A90E2", wobble=True)
    for i, v in enumerate(VEG_ORDER):
        x = 760 + i * 190
        L.append({"id": f"{p}up{i}", "start": snap(t0 + 0.1 * i), "duration": snap(dur - 0.1 * i), "timeMode": "layer",
                  "content": {"kind": "shape", "items": vg.VEG[v]()},
                  "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 1000], "easing": "ease_out"}, {"time": dur - 0.1 * i, "value": [x, 280]}]},
                                 "scale": {"keyframes": [{"time": 0, "value": [0.6, 0.6]}]},
                                 "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 15*math.sin(time*6)"}}})
    for i, (x, y) in enumerate([(780, 200), (1680, 220), (1230, 150)]):
        L.append(prop(f"{p}st{i}", sparkle_icon(50, YELLOW), (x, y), t0 + 0.4 + 0.15 * i, dur - 0.4 - 0.15 * i, spin=200))


def peas_demo(p, t0, dur, nums):
    cx, cy = C
    L.append(kit.card_layer(p + "card", t0, dur, C, (1062, 612), border=vg.LEAF_D))
    L.append(prop(p + "pod", vg.peapod_icon(True, peas=0), (cx, cy - 60), t0 + 0.1, dur - 0.1, s=1.6, wiggle=5))
    for k, tn in enumerate(nums):
        x = cx - 260 + 260 * k
        L.append({"id": f"{p}pea{k}", "start": snap(tn), "duration": snap(t0 + dur - tn), "timeMode": "layer",
                  "content": {"kind": "shape", "items": vg.pea_icon(50)},
                  "animations": {"position": {"keyframes": [{"time": 0, "value": [cx, cy - 60], "easing": "ease_out"}, {"time": 0.35, "value": [x, cy + 120]}]},
                                 "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 360*time"},
                                 "scale": {"keyframes": [{"time": 0, "value": [0.3, 0.3], "easing": POP}, {"time": 0.3, "value": [1, 1]}]}}})
        text(f"{p}n{k}", str(k + 1), (x, cy + 240), 90, tn + 0.1, t0 + dur - tn - 0.1, color=vg.LEAF_D)


def song_pass(si, a):
    p = f"s{si}_"
    text(p + "head", "The Veggie Song!" if si == 0 else "Now YOU sing with Mokki!", (1150, 120), 90, a + 0.3, 8.9)
    veg_row(p + "intro", a + 0.6, 8.6)
    for li, (s, e, line) in enumerate(LYRICS):
        text(f"{p}ly{li}", line, (1150, 110), 70, a + s, e - s, pop=False)
    L.extend(vg.veg_card_demo(p + "carrot_", a + 9.45, 2.35, "carrot", C, sc=0.9))
    L.extend(vg.eye_demo(p + "eye_", a + 11.85, 2.3, C, sc=0.9))
    L.extend(vg.veg_card_demo(p + "broc_", a + 14.2, 2.35, "broccoli", C, sc=0.9))
    L.extend(vg.bite_demo(p + "more_", a + 16.55, 2.35, "broccoli", C, sc=0.9, bites=(0.5, 1.2)))
    for c0, sub in [(18.95, "a"), (56.55, "b")]:
        L.extend(vg.rainbow_plate_demo(f"{p}{sub}plate_", a + c0, 2.3, C, sc=0.9))
        L.extend(vg.grow_demo(f"{p}{sub}grow_", a + c0 + 2.3, 2.4, C, sc=0.9))
        L.extend(vg.bite_demo(f"{p}{sub}bite_", a + c0 + 4.7, 2.3, "carrot", C, sc=0.9, bites=(0.6,)))
        sky_demo(f"{p}{sub}sky_", a + c0 + 7.0, 2.45)
    L.extend(vg.veg_card_demo(p + "tom_", a + 37.7, 2.35, "tomato", C, sc=0.9))
    L.extend(vg.veg_card_demo(p + "corn_", a + 40.05, 2.4, "corn", C, sc=0.9))
    peas_demo(p + "peas_", a + 42.45, 2.3, [a + 43.7, a + 43.96, a + 44.22])
    L.extend(vg.veg_card_demo(p + "egg_", a + 44.75, 2.45, "eggplant", C, sc=0.9))
    L.extend(vg.rainbow_plate_demo(p + "oplate_", a + 77.45, 2.55, C, sc=0.9))
    L.extend(vg.grow_demo(p + "ogrow_", a + 80.0, 2.6, C, sc=0.9))
    text(p + "yay", "Yummy, yummy, yay!", (C[0], C[1]), 110, a + 84.8, 5.0, color="#E84393", wobble=True)
    for i, (x, y) in enumerate([(760, 320), (1700, 300), (800, 760), (1660, 760), (1230, 260), (1230, 820)]):
        L.append(prop(f"{p}yay{i}", sparkle_icon(55, YELLOW), (x, y), a + 82.7 + 0.1 * i, 7.0, spin=200))
    for i, v in enumerate(VEG_ORDER):
        L.append(vg.veg_layer(f"{p}yv{i}", v, (760 + i * 190, 800), a + 82.7 + 0.1 * i, 7.0 - 0.1 * i, s=0.6, wiggle=12))
    # instrumental breaks: dancing veggies + a cheer
    for brk, (b0, b1, cheer, col) in enumerate([(28.4, 37.6, "Crunch, crunch!", vg.ORANGE), (47.2, 56.5, "Yum, yum!", "#E84393"),
                                               (66.1, 77.4, "Eat a rainbow!", "#9B59D0")]):
        text(f"{p}cheer{brk}", cheer, (1230, 280), 110, a + b0 + 0.2, b1 - b0 - 0.3, color=col, wobble=True)
        veg_row(f"{p}brk{brk}_", a + b0 + 0.1, b1 - b0 - 0.2, y=620)


for si, (a, b) in enumerate(SONGS):
    song_pass(si, a)

# ================================================================ LESSON (board)
o = T["lesson"]
BOARD = (1250, 480)
LS = 0.75
L.extend(vg.tummy_demo("le_tum_", wt("lesson", "My"), wt("lesson", "Veggie") - wt("lesson", "My"), BOARD, sc=LS))
text("le_title", "Veggie Secrets", (1230, 175), 64, wt("lesson", "Veggie"), wt("lesson", "Now") - wt("lesson", "Veggie"), color=WHITE, stroke=None)
nums = [wt("lesson", "Number", k) for k in range(1, 5)] + [wt("lesson", "Now")]
demos = [lambda p, s, d: vg.rainbow_plate_demo(p, s, d, BOARD, sc=LS),
         lambda p, s, d: vg.bite_demo(p, s, d, "carrot", BOARD, sc=LS, bites=(1.6, 2.6)),
         lambda p, s, d: vg.wash_veg_demo(p, s, d, BOARD, sc=LS),
         lambda p, s, d: vg.thanks_demo(p, s, d, BOARD, sc=LS)]
for k in range(4):
    s, e = nums[k] + 0.2, nums[k + 1] - 0.1
    text(f"le_num{k}", str(k + 1), (720, 470), 150, nums[k], e - nums[k], color=YELLOW, stroke=None)
    L.extend(demos[k](f"le_d{k}_", s, e - s))
t1 = wt("lesson", "thank")
text("le_thx", "Thank you!", (1250, 700), 60, t1, nums[4] - 0.1 - t1, color=PINK, stroke=None)
a1 = wt("lesson", "Now")
c1 = wt("lesson", "One", 3)
text("le_turn", "Your turn!", (1230, 260), 90, a1, c1 - a1 - 0.1, color=YELLOW, stroke=None)
veg_row("le_vrow", wt("lesson", "Find"), c1 - wt("lesson", "Find") - 0.1, y=560, xs=(800, 970, 1140, 1310, 1480, 1650), s=0.6)
for n, (k, c) in enumerate([("One", CORAL), ("two", "#4A90E2"), ("three", "#2BB673")], 1):
    t0 = wt("lesson", k, {"One": 3, "two": 2, "three": 2}[k])
    text(f"le_cnt{n}", str(n), (930 + 300 * (n - 1), 480), 240, t0, CUT_SONG2 + 0.1 - t0, color=c)

# ================================================================ BYE (garden at sunset)
text("by_thx1", "Thank you, Granny!", (960, 130), 96, wt("bye", "Thank"), wt("bye", "Thank", 2) - wt("bye", "Thank"), color="#B9705E")
text("by_thx2", "Thank you, Grandpa!", (960, 130), 96, wt("bye", "Thank", 2), wt("bye", "I") - wt("bye", "Thank", 2), color="#C9733A")
text("by_love", "I love veggies!", (960, 130), 100, wt("bye", "I"), wt("bye", "What") - wt("bye", "I"), color="#E84393", wobble=True)
for i, (x, y) in enumerate([(700, 330), (1000, 280), (1250, 340)]):
    L.append(prop(f"by_h{i}", heart_icon(50), (x, y), wt("bye", "love") + 0.12 * i, wt("bye", "What") - wt("bye", "love") - 0.12 * i, bob=12))
f0 = wt("bye", "What")
text("by_fav", "What's your favorite?", (960, 130), 90, f0, wt("bye", "Bye-bye") - f0, color="#4A90E2")
for i, v in enumerate(VEG_ORDER):
    L.append(vg.veg_layer(f"by_v{i}", v, (620 + i * 130, 300), f0 + 0.15 * i, wt("bye", "Bye-bye") - f0 - 0.15 * i, s=0.5, wiggle=12))
text("bye", "Bye-bye, friends!\nSee you tomorrow!", (960, 150), 90, wt("bye", "Bye-bye"), END - wt("bye", "Bye-bye"), color=CORAL)

# ================================================================ CHARACTERS
MX = 420
pos_keys = [{"time": 0, "value": [MX, 905], "easing": "step"},
            {"time": CUT_LESSON, "value": [MX + 10, 890], "easing": "step"},
            {"time": CUT_SONG2, "value": [MX, 905], "easing": "step"}]
songs_cond = " or ".join(f"(time>={a:.2f} and time<{b:.2f})" for a, b in SONGS)
songs_start = " ".join(f"if time>={a:.2f} and time<{b:.2f} then s={a:.2f} end;" for a, b in SONGS)
g0 = wt("intro", "garden")
yum0 = wt("mokki2", "Mmm")
bounce = (f"if time>={g0:.2f} and time<{g0 + 0.8:.2f} then return value+Vec.v2(0,-120*math.sin(math.pi*(time-{g0:.2f})/0.8)) end; "
          f"if time>={yum0:.2f} and time<{yum0 + 1.6:.2f} then return value+Vec.v2(0,-60*math.abs(math.sin(math.pi*(time-{yum0:.2f})/0.8))) end; "
          f"local s=0; {songs_start} if {songs_cond} then local b=math.abs(math.sin(math.pi*(time-s)/0.59)); return value+Vec.v2(0,-30*b) "
          f"else return value+Vec.v2(0,-10*math.sin(2*math.pi*time/1.6)) end")
h1 = wt("mokki1", "Hmm")
wave0 = wt("bye", "Bye-bye")
rot = (f"local r=value+4*math.sin(2*math.pi*time/2.4); if time>={h1:.2f} and time<{T['granny2']:.2f} then r=r+10 end; "
       f"if time>={wave0:.2f} then r=r+12*math.sin(time*10) end; return r")
mwords = []
for clip in ("intro", "mokki1", "mokki2", "lesson", "bye"):
    mwords += words_from_transcript(W[clip], T[clip])
for a, _ in SONGS:
    mwords += [(a + s, a + e, 0) for s, e in SONG_WORDS]
mwords.append((cr, cr + 0.5, 3))    # big open mouth for the crunch
L += mokki_rig("mokki", mwords, pos_keys, scale=0.5, pos_expr=bounce, rot_expr=rot,
               scale_keys=[{"time": 0, "value": [0.5, 0.5]}, {"time": END - 0.8, "value": [0.5, 0.5], "easing": "ease_in"}, {"time": END, "value": [0, 0]}],
               closed=[(yum0, yum0 + 0.7)])
HOLD = []
hp = kit.hand_pos()
HOLD.append({"id": "st_hold", "parentId": "mokki", "start": snap(T["mokki2"]), "duration": snap(T["granny3"] + 1.5 - T["mokki2"]), "timeMode": "layer",
          "transform": {"position": [hp[0] + 40, hp[1] - 60], "rotation": -35},
          "content": {"kind": "shape", "items": vg.carrot_icon(False)},
          "animations": {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [1.1, 1.1]},
                                                 {"time": cr - T["mokki2"], "value": [1.1, 1.1], "easing": "ease_out"},
                                                 {"time": cr - T["mokki2"] + 0.2, "value": [1.1, 0.75]}]},
                         "position": {"keyframes": [{"time": 0, "value": [hp[0] + 40, hp[1] - 60]},
                                                    {"time": cr - T["mokki2"] - 0.5, "value": [hp[0] + 40, hp[1] - 60], "easing": "ease_in"},
                                                    {"time": cr - T["mokki2"], "value": [hp[0] - 40, hp[1] - 30], "easing": "ease_out"},
                                                    {"time": cr - T["mokki2"] + 0.5, "value": [hp[0] + 60, hp[1] - 40]}]}}})
for i, (dx, dy) in enumerate([(120, -60), (160, 20), (90, 60)]):
    HOLD.append({"id": f"st_crumb{i}", "parentId": "mokki", "start": snap(cr), "duration": 0.8, "timeMode": "layer",
              "content": {"kind": "shape", "items": [group(ell([0, 0], [40, 32], vg.ORANGE))]},
              "animations": {"position": {"keyframes": [{"time": 0, "value": [hp[0] - 40, hp[1] - 30], "easing": "ease_out"},
                                                        {"time": 0.8, "value": [hp[0] - 40 + dx * 2, hp[1] - 30 + dy * 2]}]},
                             "scale": {"keyframes": [{"time": 0, "value": [1, 1]}, {"time": 0.8, "value": [0, 0]}]}}})

L += HOLD
# Granny Mo (talks in the kitchen) and Grandpa Moss (silent, waves)
GR, GP = (1200, 905), (1640, 905)
wave_rot = lambda t: f"local r=value+3*math.sin(time*2); if time>{t:.2f} then r=r+10*math.sin(time*9) end; return r"
L += place(family_rig("grandma", [], [{"time": 0, "value": list(GR)}], scale=0.5, prefix="gma_i", rot_expr=wave_rot(wt("intro", "Granny") - 0.0)),
           0, CUT_KITCHEN)
L += place(family_rig("grandpa", [], [{"time": 0, "value": list(GP)}], scale=0.5, prefix="gpa_i", rot_expr=wave_rot(wt("intro", "Grandpa"))),
           0, CUT_KITCHEN)
gw = []
for clip in ("granny1", "granny2", "granny3"):
    gw += words_from_transcript(W[clip], T[clip] - CUT_KITCHEN)
L += place(family_rig("grandma", gw, [{"time": 0, "value": [1500, 905]}], scale=0.5, prefix="gma_k",
                      rot_expr=wave_rot(wt("granny3", "Hooray") - CUT_KITCHEN)), CUT_KITCHEN, CUT_SONG1 - CUT_KITCHEN)
L += place(family_rig("grandma", [], [{"time": 0, "value": [1180, 905]}], scale=0.5, prefix="gma_b", rot_expr=wave_rot(wave0 - CUT_BYE)),
           CUT_BYE, END - CUT_BYE)
L += place(family_rig("grandpa", [], [{"time": 0, "value": [1620, 905]}], scale=0.5, prefix="gpa_b", rot_expr=wave_rot(wave0 - CUT_BYE)),
           CUT_BYE, END - CUT_BYE)

# ================================================================ wipes + audio
for i, cut in enumerate([CUT_KITCHEN, CUT_SONG1, CUT_LESSON, CUT_SONG2, CUT_BYE]):
    L.append(wipe(f"wipe{i}", cut - 0.4))
for k, uri in V.items():
    L.append(audio("a_" + k, T[k], uri))
L.append(audio("a_song1", T_SONG1, SONG))
L.append(audio("a_song2", T_SONG2, SONG))

for l in L:
    for k in ("start", "duration"):
        if k in l:
            l[k] = snap(l[k])
text_check.resolve(L)
ids = [l["id"] for l in L]
dup = {i for i in ids if ids.count(i) > 1}
assert not dup, dup
scene = {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": END, "background": "#9ED8FF"}, "layers": L}
json.dump(scene, open(os.path.join(HERE, "ep04-scene.json"), "w"), separators=(",", ":"))
full = branding.wrap_episode(L, END)
json.dump(full, open(os.path.join(HERE, "ep04-full-scene.json"), "w"), separators=(",", ":"))
print("episode", END, "s; full", full["composition"]["duration"], "s;", len(L), "layers")
