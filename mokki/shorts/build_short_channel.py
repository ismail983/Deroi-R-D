"""Short #1 - channel introduction: Mokki says hello, shows what Mokki World is about, asks to Like & Subscribe."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import kit, shorts_kit as sk
from kit import NAVY, WHITE, YELLOW, CORAL, GREEN, POP, rect, ell, group, shape_layer, prop, sparkle_icon, heart_icon, mokki_rig, words_from_transcript

VOICE = "https://gcdn.picsart.com/picsart-mcp/4dfe3866-04f3-4f9b-8df6-4744f8e81fc1.mp3"   # 22.6 s
WORDS = [(0.08, 0.24, "Hi"), (0.4, 1.0, "friends"), (1.12, 1.36, "I'm"), (1.4, 2.04, "Mokki"), (2.16, 2.8, "[giggles]"),
         (3.0, 3.2, "Welcome"), (3.28, 3.36, "to"), (3.52, 3.84, "Mokki"), (4.0, 4.6, "World"), (4.8, 4.96, "Here"),
         (5.04, 5.2, "we"), (5.32, 5.44, "sing"), (5.52, 5.76, "happy"), (5.92, 6.24, "songs"), (6.32, 6.4, "and"),
         (6.48, 6.72, "learn"), (6.88, 7.12, "so"), (7.28, 7.44, "many"), (7.68, 8.16, "things"), (8.4, 8.6, "A"),
         (8.64, 8.8, "B"), (8.88, 9.6, "C"), (9.68, 9.88, "one"), (9.92, 10.16, "two"), (10.24, 10.96, "three"),
         (11.04, 11.84, "colours"), (11.88, 11.92, "and"), (12.0, 12.16, "how"), (12.24, 12.32, "to"), (12.4, 12.48, "be"),
         (12.56, 12.88, "kind"), (12.96, 13.04, "and"), (13.12, 14.08, "healthy"), (14.16, 14.32, "There's"),
         (14.373, 14.427, "a"), (14.48, 14.64, "new"), (14.72, 15.04, "song"), (15.2, 15.52, "every"), (15.6, 16.32, "day"),
         (16.4, 16.64, "Ask"), (16.72, 16.76, "a"), (16.8, 17.2, "grown-up"), (17.28, 17.36, "to"), (17.48, 17.6, "tap"),
         (17.68, 17.92, "like"), (17.96, 18.0, "and"), (18.08, 18.88, "subscribe"), (18.96, 19.04, "so"),
         (19.12, 19.28, "you"), (19.36, 19.6, "never"), (19.72, 19.84, "miss"), (19.88, 19.92, "a"), (20.0, 20.72, "song"),
         (20.8, 20.88, "See"), (20.96, 21.04, "you"), (21.12, 21.76, "soon"), (21.8, 22.72, "Bye-bye")]
VO = 4.6                                  # voice starts as the jingle ends
END = VO + 23.6


def w(word, n=1):
    k = 0
    for s, e, t in WORDS:
        if t.lower() == word.lower():
            k += 1
            if k == n:
                return VO + s
    raise KeyError(word)


L = []
sk.sky_bg(L, 0, END)
# opening: big logo + jingle, Mokki pops out of a cloud
L += kit.kid_text("logo", "Mokki\n& Friends", (540, 700), 180, 0.3, VO - 0.2, color=NAVY, wobble=True)
for i, (x, y) in enumerate([(200, 480), (880, 480), (180, 960), (900, 960), (540, 380)]):
    L.append(prop(f"lsp{i}", sparkle_icon(50, YELLOW), (x, y), 0.4 + i * 0.1, VO - 0.5, spin=200))
L.append(sk.audio_trim("jingle", 0, sk.JINGLE, 0, 6.0))

# talking beats
t = w("Hi")
L += kit.kid_text("hi", "Hi! I'm Mokki!", (540, 560), 120, t, w("Welcome") - t - 0.1, color=CORAL, wobble=True)
t = w("Welcome")
L += kit.kid_text("welcome", "Welcome to\nMokki World!", (540, 560), 120, t, w("Here") - t + 0.5, color="#9B59D0")
for i, (x, y) in enumerate([(200, 820), (880, 800), (320, 1080), (760, 1080)]):
    L.append(prop(f"wsp{i}", sparkle_icon(44, YELLOW), (x, y), t + 0.2 + i * 0.1, 2.0, spin=180))
# songs: music notes
t = w("sing")
for i, (x, y, c) in enumerate([(220, 760, CORAL), (420, 640, "#4A90E2"), (660, 660, "#2BB673"), (860, 780, "#FF8A00")]):
    L.append(prop(f"note{i}", [group(rect([16, -48], [10, 96], c, 3) + rect([34, -84], [36, 12], c, 4) + ell([0, 0], [44, 34], c), rot=-15)],
                  (x, y), t + i * 0.12, w("A") - t - i * 0.12 - 0.05, s=1.6, bob=20))
# A B C blocks
for i, (ch, c) in enumerate(zip("ABC", ["#F0506E", "#4A90E2", "#2BB673"])):
    t = w(ch)
    L.append(prop(f"blk{ch}", sk.letter_block(ch, c), (260 + 280 * i, 700), t, w("colours") - t, wiggle=6))
    L += kit.kid_text(f"blt{ch}", ch, (260 + 280 * i, 740), 130, t, w("colours") - t, color=WHITE, stroke=None, letters=False)
# 1 2 3 balloons
for i, (n, word, c) in enumerate([("1", "one", "#FF8A00"), ("2", "two", "#9B59D0"), ("3", "three", "#00B5AD")]):
    t = w(word)
    L.append(prop(f"bal{n}", [group(ell([0, 0], [170, 200], c) + rect([0, 112], [6, 140], "#9AA5B1"))], (260 + 280 * i, 1000), t,
                  w("colours") - t + 0.3, bob=18))
    L += kit.kid_text(f"num{n}", n, (260 + 280 * i, 1040), 120, t, w("colours") - t + 0.3, color=WHITE, stroke=None, letters=False)
# colours: rainbow dots
t = w("colours")
for i, c in enumerate(["#F0506E", "#FF8A00", "#FFD23F", "#2BB673", "#4A90E2", "#5B4BC4", "#9B59D0"]):
    L.append(prop(f"col{i}", [{"type": "ellipse", "position": [0, 0], "size": [110, 110]}, {"type": "fill", "color": c},
                              {"type": "stroke", "color": WHITE, "width": 8}], (130 + 137 * i, 820), t + i * 0.07,
                  w("kind") - t - i * 0.07, bob=14))
# kind + healthy: heart, toothbrush, apple
t = w("kind")
L.append(prop("kheart", heart_icon(110), (300, 800), t, w("There's") - t, wiggle=8))
t = w("healthy")
L.append(prop("hbrush", kit.brush_h_icon(), (760, 820), t - 0.3, w("There's") - t + 0.3, s=1.2, wiggle=8))
# new song every day
t = w("new")
L += kit.kid_text("everyday", "A new song\nevery day!", (540, 640), 120, t, w("Ask") - t - 0.05, color="#2BB673", wobble=True)
for i, (x, y) in enumerate([(200, 940), (880, 940)]):
    L.append(prop(f"dnote{i}", [group(rect([16, -48], [10, 96], CORAL, 3) + rect([34, -84], [36, 12], CORAL, 4) + ell([0, 0], [44, 34], CORAL), rot=-15)],
                  (x, y), t + 0.2 * i, w("Ask") - t - 0.2 * i, s=1.8, bob=20))
# like & subscribe with finger taps
t_in = w("Ask")
L += kit.kid_text("askgrown", "Ask a grown-up!", (540, 540), 100, t_in, w("See") - t_in - 0.1, color=GREEN)
sk.like_subscribe(L, w("like"), w("subscribe") + 0.3, t_in + 0.1, END, ly=780, sy=1000)
# see you soon
t = w("See")
L += kit.kid_text("soon", "See you soon!", (540, 540), 110, t, END - t, color=CORAL, wobble=True)

# Mokki at the bottom, popping out of a cloud
words = words_from_transcript(WORDS, VO)
wave = f"local r=value+5*math.sin(2*math.pi*time/2.2); if time>{w('See'):.2f} or time<{w('Welcome'):.2f} then r=r+10*math.sin(time*10) end; return r"
L += mokki_rig("mokki", words, [{"time": 0, "value": [540, 2500], "easing": POP}, {"time": 0.9, "value": [540, 1780]}], scale=0.5,
               box=(sk.W, sk.H), rot_expr=wave)
L.append(shape_layer("bigcloud", kit.cloud_icon(900, WHITE), 0, END, (540, 1820)))

# audio: voice + soft music bed under it
L.append({"id": "voice", "start": VO, "content": {"kind": "audio", "asset": {"type": "audio", "uri": VOICE}}})
L.append(sk.audio_trim("bed1", 5.6, sk.MUSIC_BED, 0, 14.0, volume=35))
L.append(sk.audio_trim("bed2", 19.6, sk.MUSIC_BED, 0, END - 19.6, volume=35))

sk.finish(L, END, os.path.join(HERE, "short-channel-scene.json"))
print("channel short", round(END, 2), "s,", len(L), "layers")
