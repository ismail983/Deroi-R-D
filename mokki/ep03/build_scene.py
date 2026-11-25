"""Mokki & Friends - Episode 3: Bath Time. Builds ep03-scene.json (episode) and ep03-full-scene.json (with intro/outro)."""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import kit, text_check, branding
from kit import (NAVY, WHITE, YELLOW, CORAL, GREEN, PINK, BODY, POP, snap, rect, ell, group, shape_layer, prop, audio,
                 sparkle_icon, heart_icon, mokki_rig, family_rig, words_from_transcript, wipe, kid_text)

A = "https://gcdn.picsart.com/picsart-mcp/"
SONG = A + "04e6ea0b-5a1d-4e79-aabd-5cc798f8a8c7.mp3"
V = {"intro": A + "ce4a4303-de87-444a-bd27-a7cdba77f6ae.mp3", "papa1": A + "3f203f4d-42f7-41fb-aa59-20957eaca8ff.mp3",
     "mokki1": A + "17410118-4b80-4a7b-a162-b7a7258ed37a.mp3", "papa2": A + "a3037dda-b938-4d33-9ff4-33231465ba84.mp3",
     "mokki2": A + "6ffab9ce-f886-4c1c-a2a2-83de5905736b.mp3", "papa3": A + "d5a4e58b-4044-40ed-957f-371325f8d591.mp3",
     "lesson": A + "3a5594d1-4ecf-484f-afc0-4ecb1fdd8f60.mp3", "bye": A + "9a67f082-83d6-462a-8e6f-e12e85118746.mp3"}
ABSTRACT = A + "379d7237-3a16-44e1-98da-a8927de328a8.mp3"
kit.FAMILY_URLS.update({"papa": A + "5516daa6-d600-4b6f-a122-3abc2539f009.png", "mama": A + "01131a7b-4f78-493a-a350-6618e929c06e.png",
                        "pia": A + "3ddbe55c-ed46-4d5c-a19f-b6a70cba4911.png", "pip": A + "2a573c49-2923-41de-a8ff-90e5deb37f64.png",
                        "grandpa": A + "a61529f1-96eb-4251-a7c3-0c0c77f0435a.png", "grandma": A + "5abb3d82-2b1d-4d45-a169-de98b8c0cb78.png"})

W = {
 "intro": [(0.08,0.24,"Hi"),(0.4,0.92,"friends"),(1.04,1.28,"It's"),(1.44,1.68,"me"),(1.76,2.36,"Mokki"),(2.48,3.16,"[giggles]"),
           (3.2,3.6,"Today"),(3.76,3.84,"I"),(3.92,4.32,"played"),(4.4,4.64,"all"),(4.8,5.04,"day"),(5.08,5.12,"in"),(5.2,5.28,"the"),
           (5.36,6.2,"park"),(6.32,6.4,"I"),(6.48,7.08,"jumped"),(7.2,7.24,"I"),(7.28,7.787,"ran"),(7.813,7.84,"and"),(8.08,8.12,"I"),
           (8.16,8.4,"rolled"),(8.44,8.48,"in"),(8.56,8.64,"the"),(8.72,9.28,"grass"),(9.36,10.2,"[giggles]"),(10.32,11.16,"Phew"),
           (11.2,11.36,"now"),(11.44,11.6,"I'm"),(11.68,11.92,"all"),(12.0,12.32,"dirty"),(12.44,12.56,"and"),(12.64,13.52,"sleepy")],
 "papa1": [(0.649,0.76,"Hello"),(0.8,0.96,"little"),(1.04,1.88,"explorer"),(2.08,2.24,"Look"),(2.32,2.48,"at"),(2.56,3.04,"you"),
           (3.12,3.76,"[giggles]"),(3.84,4.08,"Grass"),(4.16,4.24,"on"),(4.32,4.4,"your"),(4.48,4.96,"antenna"),(5.08,5.2,"and"),
           (5.28,5.52,"dust"),(5.6,5.68,"on"),(5.76,5.84,"your"),(5.92,6.56,"cheeks")],
 "mokki1": [(0.0,0.4,"[giggles]"),(0.72,0.92,"Hee"),(0.96,1.44,"hee"),(1.68,2.48,"Oops")],
 "papa2": [(0.08,0.32,"It's"),(0.4,0.64,"bath"),(0.72,1.32,"time"),(1.52,1.76,"Warm"),(1.84,2.4,"water"),(2.48,2.72,"lots"),
           (2.76,2.8,"of"),(2.88,3.44,"bubbles"),(3.52,3.76,"and"),(3.84,4.0,"your"),(4.08,4.32,"rubber"),(4.4,5.04,"duck")],
 "mokki2": [(0.16,0.84,"Yay"),(0.96,1.28,"Bath"),(1.36,1.92,"time"),(2.08,2.24,"Can"),(2.32,2.56,"baby"),(2.64,2.88,"Pip"),
            (3.0,3.12,"come"),(3.2,3.76,"too")],
 "papa3": [(0.272,0.32,"Of"),(0.64,1.12,"course"),(1.28,1.52,"Let's"),(1.6,1.68,"sing"),(1.76,1.84,"the"),(1.92,2.16,"bath"),(2.24,2.96,"song")],
 "lesson": [(0.08,0.56,"Look"),(0.72,0.88,"I'm"),(0.96,1.44,"squeaky"),(1.52,2.12,"clean"),(2.24,2.96,"[giggles]"),(3.04,3.28,"Bath"),
            (3.36,3.68,"time"),(3.84,4.76,"secrets"),(5.04,5.28,"Number"),(5.44,6.08,"one"),(6.12,6.16,"a"),(6.24,6.64,"grown-up"),
            (6.72,6.96,"checks"),(7.04,7.08,"the"),(7.12,7.36,"water"),(7.44,7.6,"is"),(7.68,8.32,"warm"),(8.4,8.64,"not"),(8.72,8.8,"too"),
            (8.88,9.28,"hot"),(9.76,10.0,"Number"),(10.16,10.8,"two"),(10.88,11.12,"wash"),(11.2,11.36,"with"),(11.44,11.92,"soap"),
            (12.04,12.16,"from"),(12.24,12.48,"head"),(12.56,12.64,"to"),(12.8,13.2,"toe"),(13.6,13.84,"Number"),(14.0,14.72,"three"),
            (14.8,15.2,"rinse"),(15.28,15.52,"all"),(15.6,15.68,"the"),(15.76,16.08,"bubbles"),(16.16,16.56,"away"),(17.04,17.28,"Number"),
            (17.44,18.16,"four"),(18.36,18.56,"dry"),(18.64,18.72,"with"),(18.8,18.92,"a"),(19.04,19.28,"soft"),(19.36,19.84,"towel"),
            (20.24,20.32,"And"),(20.6,21.28,"remember"),(21.44,21.68,"never"),(21.84,22.0,"play"),(22.04,22.08,"in"),(22.16,22.2,"the"),
            (22.24,22.48,"bath"),(22.56,23.04,"alone"),(23.36,23.84,"Always"),(23.92,24.0,"with"),(24.04,24.08,"a"),(24.16,24.72,"grown-up"),
            (25.12,25.28,"Now"),(25.32,25.44,"it's"),(25.52,25.68,"your"),(25.76,26.24,"turn"),(26.4,26.8,"Splash"),(26.88,26.96,"and"),
            (27.04,27.2,"sing"),(27.28,27.44,"with"),(27.52,27.84,"me"),(28.0,28.56,"Ready"),(28.8,29.28,"One"),(29.44,29.76,"two"),(29.84,30.48,"three")],
 "bye": [(0.16,0.96,"Ahh"),(1.12,1.6,"clean"),(1.68,1.92,"and"),(2.08,2.64,"cozy"),(3.04,3.28,"Thank"),(3.36,3.52,"you"),(3.56,4.08,"Papa"),
         (4.56,5.44,"[yawns]"),(5.84,6.0,"Now"),(6.08,6.24,"it's"),(6.32,6.48,"time"),(6.56,6.64,"for"),(6.72,7.36,"pajamas"),(7.52,7.6,"and"),
         (7.68,7.76,"a"),(7.84,8.32,"bedtime"),(8.4,8.88,"story"),(9.347,9.68,"Bye-bye"),(9.92,10.36,"friends"),(10.56,10.64,"See"),
         (10.72,10.8,"you"),(10.92,11.28,"tomorrow"),(11.36,11.52,"in"),(11.6,11.92,"Mokki"),(12.0,12.64,"World")],
}
SONG_WORDS = [(4.8,5.2),(5.26,5.34),(5.4,5.62),(5.72,5.86),(6.02,6.54),(6.66,6.88),(7.22,7.58),(7.64,7.72),(7.8,8.0),(8.16,8.24),(8.4,8.84),
 (8.96,9.28),(9.66,10.14),(10.2,10.62),(10.78,10.98),(11.08,11.3),(11.4,11.66),(12.02,12.48),(12.6,13.02),(13.12,13.4),(13.48,13.7),(13.78,14.18),
 (23.98,24.24),(24.32,24.54),(24.6,24.82),(24.9,25.08),(25.14,26.06),(26.4,26.7),(26.74,26.86),(26.96,27.56),(27.68,27.84),(27.92,28.04),(28.18,28.48),
 (28.82,29.04),(29.12,29.32),(29.42,29.64),(29.7,29.92),(29.98,30.24),(30.32,30.44),(30.58,30.82),(31.14,31.66),(31.78,32.1),(32.14,32.28),(32.38,32.54),
 (32.58,32.66),(32.74,32.94),(33.62,33.88),(33.94,34.06),(34.18,34.48),(34.54,34.7),(34.82,35.06),(35.14,35.32),(35.48,35.76),(36.02,36.28),(36.34,36.46),
 (36.62,37.04),(37.22,37.64),(37.76,38.12),(38.42,38.66),(38.74,38.88),(39.04,39.3),(39.34,39.46),(39.6,39.86),(39.92,40.06),(40.18,40.46),(40.82,41.28),
 (41.38,41.62),(41.7,41.86),(41.96,42.3),(42.36,42.52),(42.62,42.88),(52.8,53.04),(53.12,53.32),(53.4,53.62),(53.7,53.86),(53.96,54.86),(55.2,55.5),
 (55.54,55.66),(55.76,56.36),(56.5,56.64),(56.72,56.86),(56.98,57.26),(57.62,57.84),(57.92,58.12),(58.22,58.44),(58.5,58.72),(58.82,59.04),(59.12,59.24),
 (59.38,59.62),(59.94,60.46),(60.58,60.9),(60.96,61.1),(61.24,61.44),(61.54,61.66),(61.82,62.08),(71.98,72.26),(72.32,72.44),(72.58,73.08),(73.22,73.46),
 (73.52,73.64),(73.74,74.08),(74.38,74.64),(74.72,74.86),(75.0,75.38),(75.48,75.54),(75.62,76.06),(76.18,76.44),(76.72,77.24),(77.36,77.64),(77.72,78.4),
 (79.18,79.42),(79.52,79.74),(79.82,80.02),(80.12,80.32),(80.38,80.88),(81.52,82.04),(82.16,82.44),(82.52,83.2),(83.98,84.24),(84.32,84.54),(84.62,84.84),
 (84.92,85.12),(85.22,85.68)]
LYRICS = [(4.7, 7.1, "Turn the tap, the water's warm,"), (7.15, 9.5, "Fill the tub, a bubble storm!"),
          (9.55, 11.9, "Rubber ducky, quack, quack, quack,"), (11.95, 14.5, "Hop in, Mokki, splash, splash, splash!"),
          (23.9, 26.3, "Bath time, bath time, scrub-a-dub-dub,"), (26.35, 28.7, "Bubbles and splashes in the tub!"),
          (28.75, 31.05, "Wash, wash, wash from head to toe,"), (31.1, 33.4, "Squeaky clean, and here we go!"),
          (33.55, 35.95, "Wash your face and wash your ears,"), (36.0, 38.35, "Wash your tummy, giggle, cheers!"),
          (38.4, 40.7, "Wash your arms and wash your feet,"), (40.75, 43.3, "Wiggle toes so clean and neat!"),
          (52.7, 55.1, "Bath time, bath time, scrub-a-dub-dub,"), (55.15, 57.5, "Bubbles and splashes in the tub!"),
          (57.55, 59.85, "Wash, wash, wash from head to toe,"), (59.9, 62.4, "Squeaky clean, and here we go!"),
          (71.9, 74.3, "Rinse the bubbles, pull the plug,"), (74.35, 76.65, "Wrap the towel, a cozy hug!"),
          (76.7, 79.1, "Squeaky clean, hooray!"), (79.15, 81.4, "Bath time, bath time, hooray!"),
          (81.45, 83.8, "Squeaky clean, hooray!"), (83.9, 86.3, "Bath time, bath time, hooray!")]

T = {"intro": 0.8, "papa1": 15.3, "mokki1": 22.2, "papa2": 25.0, "mokki2": 30.3, "papa3": 34.4, "lesson": 128.8, "bye": 251.0}
T_SONG1, T_SONG2, SONG_LEN = 37.9, 160.1, 90.0
CUT_BATH, CUT_LESSON, CUT_BATH2, CUT_NIGHT = 14.8, 128.4, 159.7, 250.6
END = 265.5
SONGS = [(T_SONG1, T_SONG1 + SONG_LEN), (T_SONG2, T_SONG2 + SONG_LEN)]
KID_COLORS = ["#F0506E", "#2BB673", "#4A90E2", "#FF8A00", "#9B59D0"]
TUB = (390, 905)
MOKKI_TUB_X, PIP_TUB_X = 440, 170


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
    for l in layers:
        l["start"], l["duration"], l["timeMode"] = snap(start), snap(dur), "layer"
    return layers


L = []
# ================================================================ SETS
# park at sunset
bg("p_sky", rect([960, 400], [1920, 800], "#FFC59A"), 0, CUT_BATH)
bg("p_sky2", rect([960, 170], [1920, 340], "#FFB0A0"), 0, CUT_BATH)
L.append(shape_layer("p_sun", ell([0, 0], [220, 220], "#FFD23F"), 0, CUT_BATH, (1600, 560)))
bg("p_hill", ell([500, 860], [1500, 300], "#6BB84E") + ell([1500, 880], [1300, 260], "#7BC85E"), 0, CUT_BATH)
bg("p_grass", rect([960, 960], [1920, 240], "#8BD36B"), 0, CUT_BATH)
bg("p_tree", ell([200, 470], [300, 280], "#4E9A2E") + rect([200, 680], [60, 260], "#8A5A3C", 20), 0, CUT_BATH)
bg("p_slide", rect([1350, 760], [30, 240], "#4A90E2", 10) + rect([1520, 700], [30, 360], "#4A90E2", 10), 0, CUT_BATH)


def bathroom(sfx, s, e, water_t=None):
    bg("b_wall" + sfx, rect([960, 440], [1920, 880], "#E7F6FF"), s, e)
    bg("b_tile" + sfx, [group([{"type": "rect", "position": [x, y], "size": [118, 118], "roundness": 10} for x in range(60, 1920, 120)
                               for y in range(60, 760, 120)] + [{"type": "fill", "color": "#D3EEFB"}])], s, e)
    bg("b_floor" + sfx, rect([960, 980], [1920, 200], "#9ED8FF") + rect([960, 882], [1920, 8], "#7EC8F5"), s, e)
    bg("b_tap" + sfx, rect([140, 640], [90, 40], "#C9D1D9", 16) + rect([110, 680], [36, 60], "#C9D1D9", 12), s, e)
    bg("b_tubback" + sfx, [group([tb], pos=TUB) for tb in kit.tub_back_icon(720)], s, e)


bathroom("1", CUT_BATH, CUT_LESSON)
bg("les_wall", rect([960, 440], [1920, 880], "#FFF6D8"), CUT_LESSON, CUT_BATH2)
bg("les_floor", rect([960, 980], [1920, 200], "#CDEBC0") + rect([960, 882], [1920, 8], "#9ED39A"), CUT_LESSON, CUT_BATH2)
bg("les_board", rect([1230, 440], [1140, 640], "#2F6B57", 24) + rect([1230, 440], [1190, 690], "#B5835A", 36), CUT_LESSON, CUT_BATH2)
bathroom("2", CUT_BATH2, CUT_NIGHT)
# night bedroom
bg("n_wall", rect([960, 440], [1920, 880], "#2B3A6B"), CUT_NIGHT, END)
bg("n_floor", rect([960, 980], [1920, 200], "#7A5C46"), CUT_NIGHT, END)
bg("n_window", rect([1600, 300], [380, 320], "#1B2550", 30) + rect([1600, 300], [420, 360], WHITE, 40), CUT_NIGHT, END)
L.append(shape_layer("n_moon", ell([0, 0], [110, 110], "#FFE58A"), CUT_NIGHT, END - CUT_NIGHT, (1650, 260)))
for i, (x, y) in enumerate([(1480, 220), (1540, 400), (1720, 390)]):
    L.append(shape_layer(f"n_star{i}", sparkle_icon(18, "#FFE58A"), CUT_NIGHT, END - CUT_NIGHT, (x, y),
                         {"scale": {"keyframes": [{"time": 0, "value": [1, 1]}], "expression": f"local k=0.6+0.4*math.abs(math.sin(time*2+{i})); return Vec.v2(k,k)"}}))
bg("n_bed", rect([560, 850], [760, 120], "#B5835A", 30) + rect([560, 790], [700, 70], WHITE, 30) + rect([230, 760], [60, 300], "#B5835A", 25), CUT_NIGHT, END)

# ================================================================ INTRO (park) props
text("t_hi", "Hi! I'm Mokki!", (960, 130), 100, wt("intro", "Hi"), wt("intro", "Today") - wt("intro", "Hi"))
text("t_park", "The park!", (960, 130), 100, wt("intro", "park"), 1.3, color="#2BB673")
text("t_jump", "Jump!", (960, 130), 120, wt("intro", "jumped"), 0.75, color=CORAL, wobble=True)
text("t_run", "Run!", (960, 130), 120, wt("intro", "ran"), 0.75, color="#4A90E2", wobble=True)
text("t_roll", "Roll!", (960, 130), 120, wt("intro", "rolled"), 1.3, color="#9B59D0", wobble=True)
text("t_dirty", "Dirty and sleepy!", (960, 130), 96, wt("intro", "dirty"), CUT_BATH - wt("intro", "dirty"), color="#8B5A2B")

# ================================================================ STORY (bathroom)
text("t_explorer", "Little explorer!", (1150, 130), 96, wt("papa1", "Hello"), wt("papa1", "Grass") - wt("papa1", "Hello") - 0.1, color="#2A6FB0")
text("t_oops", "Oops!", (960, 130), 130, wt("mokki1", "Oops"), 1.5, color=CORAL, wobble=True)
text("t_bath", "Bath time!", (1150, 130), 120, wt("papa2", "bath"), 2.0, color="#4A90E2", wobble=True)
water_t = wt("papa2", "Warm")
L.append(shape_layer("tubwater", [group(ell([0, 0], [600, 110], "#9ED8FF"))], water_t, CUT_LESSON - water_t, (TUB[0], TUB[1] - 70),
                     {"scale": {"keyframes": [{"time": 0, "value": [1, 0], "easing": "ease_out"}, {"time": 1.0, "value": [1, 1]}]}}))
L.append(shape_layer("tapstream", [group(rect([0, 0], [26, 160], "#5BC0EB", 13))], water_t, 1.6, (120, 780),
                     {"scale": {"keyframes": [{"time": 0, "value": [1, 0], "easing": "ease_out"}, {"time": 0.3, "value": [1, 1]},
                                              {"time": 1.3, "value": [1, 1], "easing": "ease_in"}, {"time": 1.6, "value": [1, 0]}]}}))
bub_t = wt("papa2", "bubbles")
for i, (dx, dy, r) in enumerate([(-200, -170, 40), (-60, -210, 34), (90, -190, 44), (210, -160, 30), (-130, -260, 26), (160, -260, 28)]):
    L.append(prop(f"st_bub{i}", kit.bubble_icon(r), (TUB[0] + dx, TUB[1] + dy), bub_t + 0.1 * i, CUT_LESSON - bub_t - 0.1 * i, s=1.3, bob=10))
duck_t = wt("papa2", "duck")
L.append(prop("duck1", kit.duck_icon(), (TUB[0] + 200, TUB[1] - 150), duck_t, CUT_LESSON - duck_t, s=0.8,
              extra={"position": {"keyframes": [{"time": 0, "value": [TUB[0] + 200, TUB[1] - 150]}],
                                  "expression": "return value+Vec.v2(25*math.sin(time*1.5),8*math.sin(time*4))"},
                     "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 8*math.sin(time*3)"}}))
text("t_quack", "Quack!", (TUB[0] + 330, TUB[1] - 330), 70, duck_t + 0.2, 1.3, color="#D19A12", wobble=True)
text("t_pip", "Baby Pip!", (960, 130), 110, wt("mokki2", "Pip"), 2.0, color="#D19A12")
text("t_sing", "Let's sing!", (1150, 130), 110, wt("papa3", "Let's"), T_SONG1 + 3 - wt("papa3", "Let's"))
# grass & dust on Mokki (parented): appear when Papa says them, washed away when Mokki hops in the tub
g_t, d_t = wt("papa1", "Grass"), wt("papa1", "dust")
hop = T_SONG1 + 12.0
cheek = [kit.m(250, 895), kit.m(877, 882)]
for i, (x, y) in enumerate([(300, 260), (420, 210), (560, 230)]):
    pos = kit.m(x, y)
    L.append({"id": f"grass{i}", "parentId": "mokki", "start": snap(g_t), "duration": snap(hop - g_t), "timeMode": "layer",
              "transform": {"position": pos, "rotation": -20 + 20 * i},
              "content": {"kind": "shape", "items": [group(rect([0, 0], [14, 70], "#4E9A2E", 7))]},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [1, 1]}]}}})
for i, (cx, cy) in enumerate(cheek):
    L.append({"id": f"dust{i}", "parentId": "mokki", "start": snap(d_t), "duration": snap(hop - d_t), "timeMode": "layer",
              "transform": {"position": [cx, cy]},
              "content": {"kind": "shape", "items": [group([{"type": "ellipse", "position": [dx, dy], "size": [26, 22]} for dx, dy in ((-20, 0), (15, -12), (5, 18))] +
                                                           [{"type": "fill", "color": "#A0703F"}])]},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [1.4, 1.4]}]}}})
# dirt spots from the intro "dirty" until the bath
dirt_t = wt("intro", "dirty")
for i, (x, y) in enumerate([(330, 600), (800, 560), (640, 1050), (420, 980)]):
    L.append({"id": f"dirt{i}", "parentId": "mokki", "start": snap(dirt_t), "duration": snap(hop - dirt_t), "timeMode": "layer",
              "transform": {"position": kit.m(x, y)},
              "content": {"kind": "shape", "items": [group(ell([0, 0], [70, 54], "#8B5A2B"))]},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [1, 1]}]}}})

# ================================================================ SONG
C = (1230, 520)


def song_pass(si, a):
    p = f"s{si}_"
    text(p + "head", "Bath time with Mokki!" if si == 0 else "Now YOU splash with Mokki!", (960, 120), 90, a + 0.3, 4.2)
    for li, (s, e, line) in enumerate(LYRICS):
        text(f"{p}ly{li}", line, (1100, 110), 70, a + s, e - s, pop=False)
    L.extend(kit.warm_check_demo(p + "warm_", a + 4.7, 2.4, C, sc=0.9))
    for i in range(10):
        x, y = 650 + (i * 137) % 1200, 300 + (i * 97) % 500
        L.append(prop(f"{p}storm{i}", kit.bubble_icon(30 + (i % 4) * 10), (x, y), a + 7.2 + 0.12 * i, 2.2, s=1.4, bob=15))
    L.append(prop(p + "bigduck", kit.duck_icon(), (1190, 520), a + 9.6, 2.3, s=2.2, wiggle=10))
    for k, qt in enumerate([10.78, 11.08, 11.4]):
        text(f"{p}quack{k}", "Quack!", (900 + 280 * k, 280), 80, a + qt, 0.9, color="#D19A12")
    for k in range(8):
        L.append(prop(f"{p}splash{k}", [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -18], "outerRadius": 20},
                                               {"type": "ellipse", "position": [0, 0], "size": [36, 36]}, {"type": "fill", "color": "#5BC0EB"}])],
                      (TUB[0] - 250 + 70 * k, TUB[1] - 230 - 40 * (k % 3)), a + 12.4 + 0.08 * k, 1.6, s=1.2, bob=-30))
    text(p + "splashtxt", "Splash!", (1190, 520), 150, a + 13.1, 1.4, color="#4A90E2", wobble=True)
    for c0, sub in [(23.9, ""), (52.7, "b")]:
        L.extend(kit.scrub_demo(f"{p}ch{sub}face_", a + c0, 4.8, "face", C, sc=0.9))
        L.extend(kit.scrub_demo(f"{p}ch{sub}feet_", a + c0 + 4.85, 4.6, "feet", C, sc=0.9))
    for k, (s, e, part) in enumerate([(33.55, 34.8, "face"), (34.8, 35.95, "ears"), (36.0, 38.35, "tummy"), (38.4, 39.55, "arms"), (39.55, 43.3, "feet")]):
        L.extend(kit.scrub_demo(f"{p}v2_{k}_", a + s, e - s, part, C, sc=0.9))
    L.extend(kit.plug_demo(p + "plug_", a + 71.9, 2.4, C, sc=0.9))
    L.extend(kit.dry_demo(p + "towel_", a + 74.35, 2.3, C, sc=0.9))
    text(p + "squeaky", "Squeaky clean!", (1190, 520), 130, a + 76.8, 9.4, color="#2BB673", wobble=True)
    for i, (x, y) in enumerate([(760, 320), (1640, 300), (800, 760), (1600, 760), (1190, 260), (1190, 820)]):
        L.append(prop(f"{p}sq{i}", sparkle_icon(55, YELLOW), (x, y), a + 76.8 + 0.1 * i, 9.2, spin=200))
    # instrumental breaks: rising bubbles + duck swimming across
    random.seed(si + 3)
    for brk, (b0, b1) in enumerate([(14.6, 23.8), (43.4, 52.6), (62.5, 71.8)]):
        text(f"{p}splashwith{brk}", ["Splish, splash!", "Bubbles!", "Scrub-a-dub-dub!"][brk], (1190, 520), 120, a + b0 + 0.3, 3.5,
             color=["#4A90E2", "#9B59D0", "#2BB673"][brk], wobble=True)
        L.append(prop(f"{p}swimduck{brk}", kit.duck_icon(), (700, 760), a + b0, b1 - b0, s=1.0,
                      extra={"position": {"keyframes": [{"time": 0, "value": [700, 760]}, {"time": b1 - b0, "value": [1800, 760]}],
                                          "expression": "return value+Vec.v2(0,10*math.sin(time*4))"}}))
        for i in range(8):
            x = random.randint(650, 1850); per = random.uniform(2.5, 4.0)
            L.append({"id": f"{p}brk{brk}_{i}", "start": snap(a + b0), "duration": snap(b1 - b0), "timeMode": "layer",
                      "content": {"kind": "shape", "items": kit.bubble_icon(random.randint(26, 50))},
                      "animations": {"position": {"keyframes": [{"time": 0, "value": [x, 1100]}],
                                                  "expression": f"local t=(time+{i * 0.45})%{per:.2f}; return Vec.v2({x}+30*math.sin(t*3), 1100-t/{per:.2f}*1200)"}}})


for si, (a, b) in enumerate(SONGS):
    song_pass(si, a)

# ================================================================ LESSON
o = T["lesson"]
for i, (x, y) in enumerate([(250, 450), (600, 420), (230, 760), (640, 760)]):
    L.append(prop(f"le_sp{i}", sparkle_icon(40, YELLOW), (x, y), wt("lesson", "squeaky") + 0.1 * i, 2.2, spin=150))
text("le_title", "Bath Time Secrets", (1230, 175), 64, wt("lesson", "secrets"), wt("lesson", "remember") - wt("lesson", "secrets"), color=WHITE, stroke=None)
BOARD = (1250, 480)
nums = [wt("lesson", "Number", k) for k in range(1, 5)] + [wt("lesson", "And")]
demos = [kit.warm_check_demo, None, None, kit.dry_demo]
for k in range(4):
    s, e = nums[k] + 0.2, nums[k + 1] - 0.1
    text(f"le_num{k}", str(k + 1), (735, 470), 150, nums[k], e - nums[k], color=YELLOW, stroke=None)
    if k == 1:
        L.extend(kit.scrub_demo("le_scrub_", s, e - s, "tummy", BOARD, sc=0.85, card=False))
    elif k == 2:
        L.extend(kit.plug_demo("le_plug_", s, e - s, BOARD, sc=0.85, card=False))
    else:
        L.extend(demos[k](f"le_d{k}_", s, e - s, BOARD, sc=0.85, card=False))
a0, a1 = wt("lesson", "remember"), wt("lesson", "Now")
text("le_never", "Never alone in the bath!", (1230, 260), 64, a0, wt("lesson", "Always") - a0, color=YELLOW, stroke=None)
text("le_always", "Always with a grown-up!", (1230, 260), 64, wt("lesson", "Always"), a1 - wt("lesson", "Always") - 0.1, color="#9EF07A", stroke=None)
L.append(prop("le_tub", kit.duck_icon(), (1060, 540), a0 + 0.3, a1 - a0 - 0.4, s=1.4, wiggle=8))
L.append(prop("le_heart", heart_icon(60), (1430, 520), wt("lesson", "Always"), a1 - wt("lesson", "Always") - 0.1, bob=12))
L.append(prop("le_hand", kit.hand_icon(-1), (1430, 680), wt("lesson", "Always") + 0.2, a1 - wt("lesson", "Always") - 0.3, s=0.6, wiggle=10))
text("le_turn", "Your turn!", (1230, 300), 90, a1, wt("lesson", "One", 2) - a1 - 0.1, color=YELLOW, stroke=None)
L.append(prop("le_duck", kit.duck_icon(), (1230, 560), a1 + 0.2, wt("lesson", "One", 2) - a1 - 0.3, s=1.4, wiggle=10))
for n, (k, c) in enumerate([("One", CORAL), ("two", "#4A90E2"), ("three", "#2BB673")], 1):
    t0 = wt("lesson", k, 2)
    text(f"le_cnt{n}", str(n), (930 + 300 * (n - 1), 480), 240, t0, o + 31.3 - t0, color=c)

# ================================================================ BYE (night bedroom)
o = T["bye"]
text("by_cozy", "Clean and cozy!", (960, 130), 100, wt("bye", "clean"), wt("bye", "Thank") - wt("bye", "clean"), color="#9B59D0")
text("by_thanks", "Thank you, Papa!", (960, 130), 100, wt("bye", "Thank"), 1.6, color="#2A6FB0")
L.append(prop("by_pj", [group(rect([0, 0], [70, 80], "#C9E7FF", 16) + rect([-60, -20], [60, 40], "#C9E7FF", 16) + rect([60, -20], [60, 40], "#C9E7FF", 16)),
                        group([{"type": "polystar", "starType": "star", "points": 5, "position": [x, y], "outerRadius": 10, "innerRadius": 5}
                               for x, y in ((-15, -10), (18, 15), (-10, 25))] + [{"type": "fill", "color": YELLOW}])],
              (1200, 520), wt("bye", "pajamas"), 2.2, s=2.2, wiggle=8))
L.append(prop("by_book", [group(rect([-55, 0], [110, 150], CORAL, 12) + rect([55, 0], [110, 150], "#4A90E2", 12)),
                          group(rect([0, 0], [10, 150], "#5A3A1E", 4))], (1200, 520), wt("bye", "bedtime"), 1.9, s=2.0, wiggle=6))
text("bye", "Bye-bye, friends!\nSee you tomorrow!", (960, 150), 90, wt("bye", "Bye-bye"), END - wt("bye", "Bye-bye"), color=CORAL)
# towel wrapped around Mokki at bedtime
L.append({"id": "towelwrap", "parentId": "mokki", "start": snap(CUT_NIGHT), "duration": snap(END - CUT_NIGHT), "timeMode": "layer",
          "transform": {"position": kit.m(564, 1150)},
          "content": {"kind": "shape", "items": [group(rect([0, -60], [1000, 24], WHITE, 10)), group(rect([0, 40], [1060, 260], "#FF8A9A", 120) +
                                                                                                    [{"type": "stroke", "color": "#E05A6E", "width": 14}])]}})

# ================================================================ CHARACTERS
POS = {"park": [520, 905], "bath_stand": [820, 905], "tub": [MOKKI_TUB_X, 905], "lesson": [430, 890], "night": [820, 905]}
roll0 = wt("intro", "rolled")
pos_keys = [{"time": 0, "value": POS["park"], "easing": "step"},
            {"time": wt("intro", "ran"), "value": POS["park"], "easing": "ease_in_out"},
            {"time": wt("intro", "ran") + 0.9, "value": [1150, 905], "easing": "step"},
            {"time": CUT_BATH, "value": POS["bath_stand"], "easing": "step"},
            {"time": hop, "value": POS["bath_stand"], "easing": "ease_out"},
            {"time": hop + 0.35, "value": [600, 600], "easing": "ease_in"},
            {"time": hop + 0.7, "value": POS["tub"], "easing": "step"},
            {"time": CUT_LESSON, "value": POS["lesson"], "easing": "step"},
            {"time": CUT_BATH2, "value": POS["tub"], "easing": "step"},
            {"time": CUT_NIGHT, "value": POS["night"], "easing": "step"}]
songs_cond = " or ".join(f"(time>={a:.2f} and time<{b:.2f})" for a, b in SONGS)
songs_start = " ".join(f"if time>={a:.2f} and time<{b:.2f} then s={a:.2f} end;" for a, b in SONGS)
j0 = wt("intro", "jumped")
bounce = (f"if time>={j0:.2f} and time<{j0 + 0.8:.2f} then return value+Vec.v2(0,-160*math.sin(math.pi*(time-{j0:.2f})/0.8)) end; "
          f"local s=0; {songs_start} if {songs_cond} then local b=math.abs(math.sin(math.pi*(time-s)/0.6)); return value+Vec.v2(0,-30*b) "
          f"else return value+Vec.v2(0,-10*math.sin(2*math.pi*time/1.6)) end")
wave0 = wt("bye", "Bye-bye")
rot = (f"local r=value+4*math.sin(2*math.pi*time/2.4); if time>={roll0:.2f} and time<{roll0 + 0.8:.2f} then r=r+360*(time-{roll0:.2f})/0.8 end; "
       f"if time>={wave0:.2f} then r=r+12*math.sin(time*10) end; return r")
mwords = []
for clip in ("intro", "mokki1", "mokki2", "lesson", "bye"):
    mwords += words_from_transcript(W[clip], T[clip])
for a, _ in SONGS:
    mwords += [(a + s, a + e, 0) for s, e in SONG_WORDS]
yawn = (wt("bye", "pajamas") - 1.3, wt("bye", "pajamas") - 0.45)
L += mokki_rig("mokki", mwords, pos_keys, scale=0.5, pos_expr=bounce, rot_expr=rot,
               scale_keys=[{"time": 0, "value": [0.5, 0.5]}, {"time": END - 0.8, "value": [0.5, 0.5], "easing": "ease_in"}, {"time": END, "value": [0, 0]}],
               closed=[(T["intro"] + 10.3, T["intro"] + 11.2), yawn])
# Papa: bathroom story + bedtime
bs = CUT_BATH
pw = []
for clip in ("papa1", "papa2", "papa3"):
    pw += words_from_transcript(W[clip], T[clip] - bs)
L += place(family_rig("papa", pw, [{"time": 0, "value": [1560, 905]}], scale=0.5, prefix="papa_b"), bs, T_SONG1 + 0.5 - bs)
L += place(family_rig("papa", [], [{"time": 0, "value": [1420, 905]}], scale=0.5, prefix="papa_n",
                      rot_expr=f"local r=value+3*math.sin(time*2); if time>{wave0 - CUT_NIGHT:.2f} then r=r+10*math.sin(time*9) end; return r"),
           CUT_NIGHT, END - CUT_NIGHT)
# Pip in the tub (from when Mokki asks for him)
pip0 = wt("mokki2", "Pip")
pipbob = "return value+Vec.v2(0,-14*math.abs(math.sin(time*2.6)))"
L += place(family_rig("pip", [], [{"time": 0, "value": [PIP_TUB_X, 905]}], scale=0.5, prefix="pip_b1", pos_expr=pipbob), pip0, CUT_LESSON - pip0)
L += place(family_rig("pip", [], [{"time": 0, "value": [PIP_TUB_X, 905]}], scale=0.5, prefix="pip_b2", pos_expr=pipbob), CUT_BATH2, CUT_NIGHT - CUT_BATH2)
# tub front (over Mokki & Pip)
for sfx, s, e in (("1", CUT_BATH, CUT_LESSON), ("2", CUT_BATH2, CUT_NIGHT)):
    bg("tubfront" + sfx, [group([tb], pos=(TUB[0], TUB[1] + 20)) for tb in kit.tub_front_icon(720, 250)], s, e)

# ================================================================ wipes + audio
for i, cut in enumerate([CUT_BATH, CUT_LESSON, CUT_BATH2, CUT_NIGHT]):
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
scene = {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": END, "background": "#E7F6FF"}, "layers": L}
json.dump(scene, open(os.path.join(HERE, "ep03-scene.json"), "w"), separators=(",", ":"))
full = branding.wrap_episode(L, END)
json.dump(full, open(os.path.join(HERE, "ep03-full-scene.json"), "w"), separators=(",", ":"))
print("episode", END, "s; full", full["composition"]["duration"], "s;", len(L), "layers")
