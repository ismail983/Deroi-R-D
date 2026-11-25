"""Vegetables & food demos for Mokki (Episode 4 and later food episodes).
Icons are drawn around (0,0), about 200-260 px tall at scale 1. Item 0 is drawn on top."""
from kit import (NAVY, WHITE, YELLOW, CORAL, PINK, snap, rect, ell, group, shape_layer, prop, pop_scale, card_layer,
                 sparkle_icon, heart_icon, kid_text, hand_icon, bubble_icon, body_part_icon)

ORANGE, ORANGE_D = "#FF8A00", "#D9650A"
LEAF, LEAF_D = "#5BBF3A", "#2E8A1E"
RED, RED_D = "#F0453A", "#B8261E"
PURPLE, PURPLE_D = "#8E5AD0", "#5E3496"
CORN, CORN_D = "#FFD23F", "#D19A12"


def face(dx=0, dy=0, s=1.0):
    """Cute eyes + smile for a vegetable."""
    e = 16 * s
    return [group(ell([dx - 22 * s - 3 * s, dy - 4 * s], [e * .4, e * .4], WHITE) + ell([dx + 22 * s - 3 * s, dy - 4 * s], [e * .4, e * .4], WHITE)),
            group(ell([dx - 22 * s, dy], [e, e * 1.2], NAVY) + ell([dx + 22 * s, dy], [e, e * 1.2], NAVY)),
            group([{"type": "path", "closed": False, "vertices": [{"point": [dx - 16 * s, dy + 22 * s], "outTangent": [8 * s, 12 * s]},
                                                                  {"point": [dx + 16 * s, dy + 22 * s], "inTangent": [-8 * s, 12 * s]}]},
                   {"type": "stroke", "color": NAVY, "width": 6 * s, "lineCap": "round"}]),
            group(ell([dx - 44 * s, dy + 18 * s], [20 * s, 12 * s], PINK) + ell([dx + 44 * s, dy + 18 * s], [20 * s, 12 * s], PINK))]


def leaf(pos, rot, size=(40, 110), color=LEAF, line=LEAF_D):
    return group([{"type": "ellipse", "position": [0, -size[1] / 2], "size": list(size)}, {"type": "fill", "color": color},
                  {"type": "stroke", "color": line, "width": 5}], pos=pos, rot=rot)


def carrot_icon(cute=True):
    body = group([{"type": "path", "closed": True, "vertices": [
        {"point": [-62, -70], "inTangent": [0, -20], "outTangent": [0, 0]},
        {"point": [-6, 130], "inTangent": [-20, -10], "outTangent": [4, 4]},
        {"point": [6, 130], "inTangent": [-4, 4], "outTangent": [20, -10]},
        {"point": [62, -70], "inTangent": [0, 0], "outTangent": [0, -20]},
        {"point": [0, -96], "inTangent": [40, 0], "outTangent": [-40, 0]}]},
        {"type": "fill", "color": ORANGE}, {"type": "stroke", "color": ORANGE_D, "width": 6}])
    ridges = group([{"type": "path", "closed": False, "vertices": [{"point": [x, y]}, {"point": [x + w, y + 4]}]}
                    for x, y, w in ((-50, -20, 26), (24, 20, 26), (-34, 60, 20), (14, 92, 14))] +
                   [{"type": "stroke", "color": ORANGE_D, "width": 6, "lineCap": "round"}])
    leaves = [leaf([0, -86], 0), leaf([-10, -86], -30), leaf([10, -86], 30)]
    return (face(0, -30, 0.9) if cute else []) + [ridges, body] + leaves


def broccoli_icon(cute=True):
    florets = [{"type": "ellipse", "position": [x, y], "size": [r, r]} for x, y, r in
               ((-70, -40, 100), (70, -40, 100), (0, -80, 120), (-40, 10, 100), (40, 10, 100), (0, -10, 110))]
    return (face(0, -20, 0.9) if cute else []) + [
        group([{"type": "ellipse", "position": [x, y], "size": [22, 22]} for x, y in ((-60, -70), (50, -90), (-20, -110), (75, -10))] +
              [{"type": "fill", "color": "#1F7A34"}]),
        group(florets + [{"type": "fill", "color": "#2E9E4A"}, {"type": "stroke", "color": "#1F7A34", "width": 6}]),
        group(rect([0, 90], [70, 130], "#A8DC7A", 26) + [{"type": "stroke", "color": "#6FAE45", "width": 6}])]


def tomato_icon(cute=True):
    star = group([{"type": "polystar", "starType": "star", "points": 5, "position": [0, -84], "outerRadius": 46, "innerRadius": 16,
                   "outerRoundness": 0.3}, {"type": "fill", "color": LEAF}, {"type": "stroke", "color": LEAF_D, "width": 4}])
    return [star, group(rect([0, -106], [12, 30], LEAF_D, 6))] + (face(0, 10, 0.9) if cute else []) + [
        group(ell([-40, -40], [40, 26], "#FF8E85")),
        group(ell([0, 10], [220, 190], RED) + [{"type": "stroke", "color": RED_D, "width": 6}])]


def corn_icon(cute=True):
    kern = [{"type": "ellipse", "position": [x, y], "size": [22, 20]} for y in range(-100, 100, 26) for x in (-30, 0, 30)
            if abs(x) < 50 - abs(y) * 0.12]
    husk = [group([{"type": "path", "closed": True, "vertices": [
        {"point": [0, 120]}, {"point": [s * 70, -20], "inTangent": [0, 60]}, {"point": [s * 20, 80]}]},
        {"type": "fill", "color": LEAF}, {"type": "stroke", "color": LEAF_D, "width": 5}]) for s in (-1, 1)]
    return husk + (face(0, -10, 0.85) if cute else []) + [
        group(kern + [{"type": "fill", "color": "#FFE58A"}, {"type": "stroke", "color": CORN_D, "width": 3}]),
        group(ell([0, 0], [120, 260], CORN) + [{"type": "stroke", "color": CORN_D, "width": 6}])]


def peapod_icon(cute=True, peas=3):
    ps = [{"type": "ellipse", "position": [x, 0], "size": [60, 60]} for x in (-70, 0, 70)[:peas]]
    return (face(0, -4, 0.55) if cute else []) + [
        group(ps + [{"type": "fill", "color": "#9EE06A"}, {"type": "stroke", "color": LEAF_D, "width": 5}]),
        group(ell([0, -6], [250, 60], "#BFF08C")),
        group([{"type": "ellipse", "position": [0, 0], "size": [270, 110]}, {"type": "fill", "color": LEAF},
               {"type": "stroke", "color": LEAF_D, "width": 6}]),
        group(rect([150, -30], [40, 12], LEAF_D, 6), rot=-20)]


def pea_icon(r=30):
    return [group(ell([-r * .3, -r * .3], [r * .5, r * .4], "#DDF7C4")),
            group(ell([0, 0], [2 * r, 2 * r], "#7BC043") + [{"type": "stroke", "color": LEAF_D, "width": 4}])]


def eggplant_icon(cute=True):
    cap = group([{"type": "polystar", "starType": "star", "points": 4, "position": [0, -86], "outerRadius": 54, "innerRadius": 22,
                  "outerRoundness": 0.3}, {"type": "fill", "color": LEAF}, {"type": "stroke", "color": LEAF_D, "width": 4}])
    return [cap, group(rect([0, -116], [16, 40], LEAF_D, 8))] + (face(0, 10, 0.9) if cute else []) + [
        group(ell([-36, -30], [26, 60], "#B18AE8")),
        group([{"type": "path", "closed": True, "vertices": [
            {"point": [0, -100], "inTangent": [-40, 0], "outTangent": [40, 0]},
            {"point": [80, 40], "inTangent": [0, -80], "outTangent": [0, 60]},
            {"point": [0, 130], "inTangent": [60, 0], "outTangent": [-60, 0]},
            {"point": [-80, 40], "inTangent": [0, 60], "outTangent": [0, -80]}]},
            {"type": "fill", "color": PURPLE}, {"type": "stroke", "color": PURPLE_D, "width": 6}])]


VEG = {"carrot": carrot_icon, "broccoli": broccoli_icon, "tomato": tomato_icon, "corn": corn_icon, "peas": peapod_icon,
       "eggplant": eggplant_icon}
VEG_COLOR = {"carrot": ORANGE, "broccoli": "#2E9E4A", "tomato": RED, "corn": CORN_D, "peas": LEAF_D, "eggplant": PURPLE}
VEG_NAME = {"carrot": "Carrot", "broccoli": "Broccoli", "tomato": "Tomato", "corn": "Corn", "peas": "Peas", "eggplant": "Eggplant"}


def plate_icon(w=520):
    return [group(ell([0, 0], [w * .78, w * .78 * .42], "#F4F7FA")),
            group(ell([0, 0], [w, w * .45], WHITE) + [{"type": "stroke", "color": "#B8C7D6", "width": 8}])]


def rainbow_icon(w=520, bg=WHITE):
    """Rainbow arc (upper half). bg must match what is behind it."""
    cols = [RED, ORANGE, CORN, LEAF, "#4A90E2", PURPLE]
    band = w / 2 / (len(cols) + 2)
    items = [group(rect([0, w / 4 + 2], [w + 20, w / 2], bg)), group(ell([0, 0], [w - 2 * band * len(cols), w - 2 * band * len(cols)], bg))]
    for i in range(len(cols) - 1, -1, -1):
        d = w - 2 * band * i
        items.append(group(ell([0, 0], [d, d], cols[i])))
    # order: cover & inner hole first (drawn on top), then inner bands ... outer red last
    return items[:2] + items[2:]


def cloud_puff(w=140):
    return [group([{"type": "ellipse", "position": [x, y], "size": [r, r]} for x, y, r in
                   ((-w * .3, 0, w * .55), (w * .3, 0, w * .55), (0, -w * .18, w * .7))] + [{"type": "fill", "color": WHITE}])]


def veg_layer(id_, veg, pos, start, dur, s=1.0, wiggle=8.0, bob=0.0, extra=None, cute=True):
    return prop(id_, VEG[veg](cute), pos, start, dur, s=s, wiggle=wiggle, bob=bob, extra=extra)


# ------------------------------------------------------------------ big close-up demos
def veg_card_demo(p, t0, dur, veg, center=(1190, 560), sc=1.0, card=True, label=True):
    """A big vegetable with its name, dancing, sparkles."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=VEG_COLOR[veg]))
    L.append(veg_layer(p + "veg", veg, (cx, cy - 30 * sc), t0 + 0.1, dur - 0.1, s=1.7 * sc, wiggle=10))
    if label:
        L += kid_text(p + "name", VEG_NAME[veg] + "!", (cx, cy + 250 * sc), int(84 * sc), t0 + 0.4, dur - 0.4, color=VEG_COLOR[veg])
    for i, (dx, dy) in enumerate([(-380, -200), (380, -180), (-400, 150), (390, 140)]):
        st = t0 + 0.5 + 0.12 * i
        if st < t0 + dur - 0.3:
            L.append(prop(f"{p}sp{i}", sparkle_icon(34 * sc, YELLOW), (cx + dx * sc, cy + dy * sc), st, t0 + dur - st, spin=160))
    return L


def eye_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """Carrot + a big friendly eye that looks around, sun & moon (day and night)."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=ORANGE))
    ex, ey = cx + 150 * sc, cy - 10 * sc
    L.append(shape_layer(p + "eye", [group(ell([0, 0], [340, 250], WHITE) + [{"type": "stroke", "color": NAVY, "width": 12}])],
                         t0 + 0.2, dur - 0.2, (ex, ey), {"scale": pop_scale(dur - 0.2, sc)}))
    L.append(shape_layer(p + "pupil", [group(ell([-14, -14], [26, 26], WHITE)), group(ell([0, 0], [90, 90], NAVY)),
                                       group(ell([0, 0], [150, 150], "#4A90E2"))],
                         t0 + 0.3, dur - 0.3, (ex, ey), {"scale": pop_scale(dur - 0.3, sc),
                                                         "position": {"keyframes": [{"time": 0, "value": [ex, ey]}],
                                                                      "expression": f"return value+Vec.v2({50 * sc:.0f}*math.sin(time*2.2),{18 * sc:.0f}*math.sin(time*3.1))"}}))
    L.append(veg_layer(p + "carrot", "carrot", (cx - 300 * sc, cy + 20 * sc), t0 + 0.1, dur - 0.1, s=1.2 * sc, wiggle=10))
    L.append(prop(p + "sun", [group(ell([0, 0], [90, 90], YELLOW) + [{"type": "stroke", "color": "#FFB300", "width": 6}])],
                  (cx + 420 * sc, cy - 220 * sc), t0 + 0.6, dur - 0.6, s=sc, spin=60))
    L.append(prop(p + "moon", [group(ell([22, -12], [80, 80], WHITE)), group(ell([0, 0], [90, 90], "#FFE58A"))],
                  (cx + 420 * sc, cy + 200 * sc), t0 + 1.0, dur - 1.0, s=sc, wiggle=10))
    return L


def bite_demo(p, t0, dur, veg="carrot", center=(1190, 560), sc=1.0, card=True, crunch=True, bites=(0.9,)):
    """A big vegetable gets a bite taken out of it (white bite marks pop on), 'Crunch!'."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=LEAF))
    vx, vy = cx - 40 * sc, cy
    # bite marks: three circles in card white over the bottom-right edge of the veggie
    spots = {"carrot": (40, 90), "broccoli": (90, -60), "tomato": (100, 40), "corn": (50, -100), "peas": (130, 0), "eggplant": (70, 80)}
    bx, by = spots[veg]
    L.append(veg_layer(p + "veg", veg, (vx, vy), t0 + 0.1, dur - 0.1, s=1.6 * sc, wiggle=6))
    for k, bt in enumerate(bites):
        if bt < dur - 0.2:
            L.append(shape_layer(f"{p}bite{k}", [group([{"type": "ellipse", "position": [dx, dy], "size": [70, 70]} for dx, dy in ((0, 0), (-26, 40), (26, -40))] +
                                                       [{"type": "fill", "color": WHITE}])],
                                 t0 + bt, dur - bt, (vx + (bx - 20 * k) * 1.6 * sc, vy + (by + 30 * k) * 1.6 * sc),
                                 {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": "ease_out"}, {"time": 0.15, "value": [sc, sc]}]}}))
    if crunch:
        bt = bites[0]
        if bt < dur - 0.4:
            L += kid_text(p + "crunch", "Crunch!", (cx + 300 * sc, cy - 200 * sc), int(90 * sc), t0 + bt, dur - bt, color=ORANGE, wobble=True)
            for i, (dx, dy) in enumerate([(160, -40), (200, 40), (130, 90)]):
                L.append(shape_layer(f"{p}crumb{i}", [group(ell([0, 0], [24, 20], VEG_COLOR[veg]))], t0 + bt, min(0.8, dur - bt),
                                     (vx + dx * sc, vy + dy * sc),
                                     {"position": {"keyframes": [{"time": 0, "value": [vx + dx * sc, vy + dy * sc], "easing": "ease_out"},
                                                                 {"time": 0.8, "value": [vx + (dx + 120) * sc, vy + (dy - 60 + 40 * i) * sc]}]},
                                      "scale": {"keyframes": [{"time": 0, "value": [sc, sc]}, {"time": 0.8, "value": [0, 0]}]}}))
    return L


def rainbow_plate_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True, rainbow=True):
    """A plate fills with colourful veggies one by one, a rainbow appears over it."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border="#9B59D0"))
    order = ["tomato", "carrot", "corn", "broccoli", "peas", "eggplant"]
    step = min(0.35, max(0.12, (dur - 1.0) / 7))
    if rainbow:
        rt = t0 + 0.3 + step * 6  # rainbow pops after the veggies
        if rt < t0 + dur - 0.3:
            L.append(shape_layer(p + "rainbow", rainbow_icon(560), rt, t0 + dur - rt, (cx, cy + 10 * sc),
                                 {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": {"kind": "cubic_bezier", "control": [0.34, 1.56, 0.64, 1]}},
                                                          {"time": 0.4, "value": [sc, sc]}]}}))
            for i, dx in enumerate((-330, 330)):
                L.append(prop(f"{p}cl{i}", cloud_puff(150), (cx + dx * sc, cy + 10 * sc), rt + 0.1, t0 + dur - rt - 0.1, s=sc, bob=6))
    L.append(shape_layer(p + "plate", plate_icon(560), t0 + 0.15, dur - 0.15, (cx, cy + 170 * sc), {"scale": pop_scale(dur - 0.15, sc)}))
    order = ["tomato", "carrot", "corn", "broccoli", "peas", "eggplant"]
    spots = [(-160, 150), (-60, 120), (40, 150), (140, 120), (-110, 185), (90, 190)]
    step = min(0.35, max(0.12, (dur - 1.0) / 7))
    for i, (v, (dx, dy)) in enumerate(zip(order, spots)):
        st = t0 + 0.3 + step * i
        L.append(veg_layer(f"{p}v{i}", v, (cx + dx * sc, cy + dy * sc), st, t0 + dur - st, s=0.55 * sc, wiggle=6, cute=False))
    return L


def grow_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """'Grow up strong': a sprout grows tall next to a height chart, a strong arm flexes."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=LEAF))
    gx, gy = cx - 260 * sc, cy + 230 * sc
    L.append(shape_layer(p + "chart", [group(rect([0, -220], [70, 440], "#FFE58A", 14) + [{"type": "stroke", "color": CORN_D, "width": 6}]),
                                       group([{"type": "rect", "position": [-18, -40 - 80 * k], "size": [36, 8]} for k in range(5)] +
                                             [{"type": "fill", "color": CORN_D}])],
                         t0 + 0.1, dur - 0.1, (gx - 130 * sc, gy), {"scale": pop_scale(dur - 0.1, sc)}))
    sprout = [leaf([0, -380], -45, (60, 120)), leaf([0, -380], 45, (60, 120)), leaf([0, -230], -60, (50, 100)),
              group(rect([0, -190], [18, 380], LEAF_D, 9))]
    L.append(shape_layer(p + "sprout", sprout, t0 + 0.2, dur - 0.2, (gx, gy),
                         {"scale": {"keyframes": [{"time": 0, "value": [sc, 0.15 * sc], "easing": "ease_out"},
                                                  {"time": min(1.6, dur - 0.3), "value": [sc, sc]}]}}))
    L.append(shape_layer(p + "pot", [group(rect([0, 30], [150, 90], "#C9733A", 16) + [{"type": "stroke", "color": "#8A4A1E", "width": 6}])],
                         t0 + 0.1, dur - 0.1, (gx, gy), {"scale": pop_scale(dur - 0.1, sc)}))
    # strong arm (flexing): upper arm + forearm with a bicep bump
    ax, ay = cx + 230 * sc, cy + 60 * sc
    arm = [group(ell([0, -30], [120, 90], "#FFD7B5") + [{"type": "stroke", "color": "#C98E63", "width": 6}]),
           group(rect([110, -100], [80, 200], "#FFD7B5", 40) + [{"type": "stroke", "color": "#C98E63", "width": 6}], rot=0),
           group(ell([110, -210], [110, 110], "#FFD7B5") + [{"type": "stroke", "color": "#C98E63", "width": 6}]),
           group(rect([0, 0], [260, 90], "#FFD7B5", 45) + [{"type": "stroke", "color": "#C98E63", "width": 6}])]
    L.append(shape_layer(p + "arm", arm, t0 + 0.4, dur - 0.4, (ax, ay),
                         {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}], "expression": "local k=1+0.08*math.abs(math.sin(time*5)); return Vec.v2(value.x*k,value.y*k)"},
                          "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return -6*math.abs(math.sin(time*5))"}}))
    L.append(prop(p + "star", sparkle_icon(50 * sc, YELLOW), (ax + 40 * sc, ay - 200 * sc), t0 + 0.8, max(0.3, dur - 0.8), spin=180))
    return L


def tummy_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """A happy tummy with a smile and a pulsing heart."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=PINK))
    L.append(shape_layer(p + "tum", body_part_icon("tummy"), t0 + 0.1, dur - 0.1, (cx, cy + 20 * sc),
                         {"scale": {"keyframes": [{"time": 0, "value": [1.4 * sc, 1.4 * sc]}],
                                    "expression": "local k=1+0.05*math.sin(time*6); return Vec.v2(value.x*k,value.y/k)"}}))
    L.append(shape_layer(p + "smile", face(0, -30, 1.6), t0 + 0.3, dur - 0.3, (cx, cy + 20 * sc), {"scale": pop_scale(dur - 0.3, sc)}))
    L.append(prop(p + "heart", heart_icon(70), (cx + 280 * sc, cy - 170 * sc), t0 + 0.6, max(0.3, dur - 0.6), s=sc, bob=12))
    return L


def wash_veg_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """Water from a tap washes a carrot and a tomato in a bowl; drops and sparkles."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border="#5BC0EB"))
    L.append(shape_layer(p + "tap", [group(rect([0, -40], [60, 50], "#B0B7BF", 10) + rect([-70, -70], [200, 50], "#C9D1D9", 25) +
                                           rect([60, -10], [44, 70], "#C9D1D9", 14) + [{"type": "stroke", "color": "#8A939C", "width": 5}])],
                         t0 + 0.1, dur - 0.1, (cx - 60 * sc, cy - 220 * sc), {"scale": pop_scale(dur - 0.1, sc)}))
    L.append(shape_layer(p + "stream", [group(rect([0, 0], [40, 240], "#5BC0EB", 20)), group(rect([0, 0], [64, 240], "#BFE6F7", 32))],
                         t0 + 0.4, dur - 0.5, (cx, cy - 60 * sc),
                         {"scale": {"keyframes": [{"time": 0, "value": [sc, 0], "easing": "ease_out"}, {"time": 0.4, "value": [sc, sc]}],
                                    "expression": "return Vec.v2(value.x*(1+0.08*math.sin(time*30)), value.y)"}}))
    L.append(veg_layer(p + "carrot", "carrot", (cx - 70 * sc, cy + 110 * sc), t0 + 0.3, dur - 0.3, s=0.8 * sc, wiggle=10,
                       extra={"rotation": {"keyframes": [{"time": 0, "value": -30}], "expression": "return value+10*math.sin(time*6)"}}))
    L.append(veg_layer(p + "tomato", "tomato", (cx + 90 * sc, cy + 130 * sc), t0 + 0.4, dur - 0.4, s=0.7 * sc, wiggle=10))
    L.append(shape_layer(p + "water", [group(ell([0, 0], [440, 90], "#BFE6F7") + [{"type": "stroke", "color": "#8FCDEB", "width": 6}])],
                         t0 + 0.1, dur - 0.1, (cx, cy + 190 * sc), {"scale": pop_scale(dur - 0.1, sc)}))
    L.append(shape_layer(p + "bowlfront", [group(rect([0, 40], [460, 130], "#4A90E2", 60) + [{"type": "stroke", "color": "#2A6FB0", "width": 8}])],
                         t0 + 0.1, dur - 0.1, (cx, cy + 190 * sc), {"scale": pop_scale(dur - 0.1, sc)}))
    for i in range(6):
        off = i * 0.22
        dx = (-1) ** i * (90 + 30 * (i % 3))
        L.append(shape_layer(f"{p}drop{i}", [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -16], "outerRadius": 18},
                                                    {"type": "ellipse", "position": [0, 0], "size": [30, 30]}, {"type": "fill", "color": "#5BC0EB"}])],
                             t0 + 0.6, dur - 0.7, (cx, cy + 90 * sc),
                             {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}]},
                              "position": {"keyframes": [{"time": 0, "value": [cx, cy + 90 * sc]}],
                                           "expression": f"local t=(time+{off:.2f})%1.3; return value+Vec.v2({dx * sc:.0f}*t/1.3, {-140 * sc:.0f}*math.sin(math.pi*t/1.3))"}}))
    for i, (dx, dy) in enumerate([(-300, -100), (300, -80), (-280, 160), (300, 150)]):
        st = t0 + 1.0 + i * 0.15
        if st < t0 + dur - 0.3:
            L.append(prop(f"{p}sp{i}", sparkle_icon(34 * sc, YELLOW), (cx + dx * sc, cy + dy * sc), st, t0 + dur - st, spin=160))
    return L


def thanks_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """'Thank you!': two hands together, a big pulsing heart, a soup bowl."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=PINK))
    L.append(shape_layer(p + "heart", heart_icon(130), t0 + 0.2, dur - 0.2, (cx + 230 * sc, cy - 40 * sc),
                         {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}], "expression": "local k=1+0.12*math.abs(math.sin(time*4)); return Vec.v2(value.x*k,value.y*k)"}}))
    for i, side in enumerate((1, -1)):
        L.append(shape_layer(f"{p}hand{i}", hand_icon(side), t0 + 0.1, dur - 0.1, (cx - 260 * sc + side * 60 * sc, cy + 20 * sc),
                             {"scale": pop_scale(dur - 0.1, sc * 0.8), "rotation": {"keyframes": [{"time": 0, "value": -12 * side}]}}))
    return L


def soup_pot_icon():
    return [group(rect([0, -110], [60, 20], "#5A6470", 10)),
            group(rect([0, -86], [300, 30], "#E05A3C", 14)),
            group(rect([-170, -30], [60, 26], "#B8261E", 13) + rect([170, -30], [60, 26], "#B8261E", 13)),
            group(rect([0, 0], [300, 170], "#F0453A", 40) + [{"type": "stroke", "color": "#B8261E", "width": 8}])]


def steam_layers(p, pos, start, dur):
    L = []
    for i, dx in enumerate((-50, 0, 50)):
        L.append({"id": f"{p}steam{i}", "start": snap(start), "duration": snap(dur), "timeMode": "layer",
                  "transform": {"opacity": 0.8},
                  "content": {"kind": "shape", "items": [group([{"type": "path", "closed": False, "vertices": [
                      {"point": [0, 0], "outTangent": [20, -20]}, {"point": [0, -60], "inTangent": [20, 20], "outTangent": [-20, -20]},
                      {"point": [0, -120], "inTangent": [-20, 20]}]}, {"type": "stroke", "color": WHITE, "width": 12, "lineCap": "round"}])]},
                  "animations": {"position": {"keyframes": [{"time": 0, "value": [pos[0] + dx, pos[1]]}],
                                              "expression": f"local t=(time+{i * 0.6})%1.8; return value+Vec.v2(0,-50*t)"},
                                 "scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                           "expression": f"local t=(time+{i * 0.6})%1.8; local k=math.sin(math.pi*t/1.8); return Vec.v2(k,k)"}}})
    return L
