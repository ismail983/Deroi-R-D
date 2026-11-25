"""Shared building blocks for every Mokki & Friends video (Picsart scene JSON).

- shape helpers and icons
- the Mokki rig: the official picture + lip-synced mouth + blinking eyelids
- the channel intro and outro (with Like & Subscribe), and `wrap_episode` to put them around any episode
"""

NAVY, BODY, GREEN, CORAL, PINK, YELLOW, WHITE = "#14224F", "#8EEBC4", "#1E8F6A", "#FF6B5E", "#FF9FB2", "#FFD23F", "#FFFFFF"
YT_RED, YT_BLUE = "#FF0033", "#065FD4"
POP = {"kind": "cubic_bezier", "control": [0.34, 1.56, 0.64, 1]}
FPS = 30

# Mokki picture without its mouth (the rig draws the mouth). Picsart-hosted copy expires: re-upload
# mokki/character/mokki-nomouth.png with picsart_upload_urls and update this when it does.
MOKKI_URL = "https://gcdn.picsart.com/picsart-mcp/b11868fb-b61c-4d7f-81cf-7a532ef53e52.png"
MW, MH = 1128, 1318
S = 1080 / MH                     # the image is fitted ("contain") into a 1920x1080 layer box
OFFX = (1920 - MW * S) / 2


def m(px, py):
    """Mokki image pixel -> Mokki layer-local pixel."""
    return [round(OFFX + px * S, 2), round(py * S, 2)]


def snap(t):
    return round(round(t * FPS) / FPS, 4)


# ------------------------------------------------------------------ shapes
def rect(pos, size, color, r=0):
    return [{"type": "rect", "position": list(pos), "size": list(size), "roundness": r}, {"type": "fill", "color": color}]


def ell(pos, size, color):
    return [{"type": "ellipse", "position": list(pos), "size": list(size)}, {"type": "fill", "color": color}]


def group(contents, pos=(0, 0), rot=0, scale=None):
    g = {"type": "group", "contents": contents, "position": list(pos)}
    if rot:
        g["rotation"] = rot
    if scale:
        g["scale"] = scale
    return g


def pop_scale(dur, s=1.0):
    t_in = min(0.35, dur / 3)
    return {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": t_in, "value": [s, s]},
                          {"time": max(dur - 0.25, t_in + 0.01), "value": [s, s], "easing": "ease_in"},
                          {"time": dur, "value": [0, 0]}]}


def shape_layer(id_, items, start, dur, pos=(0, 0), anim=None, parent=None, absolute=False):
    d = {"id": id_, "start": snap(start), "duration": snap(dur), "timeMode": "layer",
         "transform": {"position": [0, 0], "anchor": [0, 0]} if absolute else {"position": list(pos)},
         "content": {"kind": "shape", "items": items}}
    if anim:
        d["animations"] = anim
    if parent:
        d["parentId"] = parent
    return d


def prop(id_, items, pos, start, dur, s=1.0, wiggle=0.0, bob=0.0, spin=0.0, extra=None):
    anim = {"scale": pop_scale(dur, s)}
    if wiggle or spin:
        e = f"return value+{wiggle}*math.sin(2*math.pi*time/1.2)" if wiggle else f"return value+{spin}*time"
        anim["rotation"] = {"keyframes": [{"time": 0, "value": 0}], "expression": e}
    if bob:
        anim["position"] = {"keyframes": [{"time": 0, "value": list(pos)}],
                            "expression": f"return value+Vec.v2(0,{bob}*math.sin(2*math.pi*time/1.1))"}
    if extra:
        anim.update(extra)
    return shape_layer(id_, items, start, dur, pos, anim)


def text(id_, t, pos, size, start, dur, color=NAVY, stroke=WHITE, pop=True, wobble=False, weight=800):
    c = {"kind": "text", "text": t, "font": {"size": size, "weight": weight}, "color": color, "alignment": "center"}
    if stroke:
        c["stroke"] = {"width": max(8, size // 7), "color": stroke}
    d = {"id": id_, "start": snap(start), "duration": snap(dur), "timeMode": "layer", "transform": {"position": list(pos)}, "content": c}
    if pop:
        d["animations"] = {"scale": pop_scale(dur)}
        if wobble:
            d["animations"]["rotation"] = {"keyframes": [{"time": 0, "value": 0}],
                                           "expression": "return 4*math.sin(2*math.pi*time/0.8)"}
    return d


def audio(id_, start, uri):
    return {"id": id_, "start": snap(start), "content": {"kind": "audio", "asset": {"type": "audio", "uri": uri}}}


# ------------------------------------------------------------------ icons (centred on 0,0)
def sparkle_icon(r=40, color=WHITE):
    return [{"type": "polystar", "starType": "star", "points": 4, "position": [0, 0], "outerRadius": r, "innerRadius": r * .28},
            {"type": "fill", "color": color}, {"type": "stroke", "color": YELLOW, "width": 4}]


def heart_icon(r=60, color="#FF5C8A"):
    return [group([{"type": "ellipse", "position": [-r * .5, 0], "size": [r * 1.1, r * 1.1]},
                   {"type": "ellipse", "position": [r * .5, 0], "size": [r * 1.1, r * 1.1]},
                   {"type": "polystar", "starType": "polygon", "points": 3, "position": [0, r * .55], "outerRadius": r * 1.05,
                    "rotation": 180, "outerRoundness": 0.1},
                   {"type": "fill", "color": color}])]


def cloud_icon(w=420, color=WHITE):
    h = w * 0.45
    return [group([{"type": "ellipse", "position": [-w * .28, h * .12], "size": [w * .5, h * .75]},
                   {"type": "ellipse", "position": [w * .02, -h * .12], "size": [w * .6, h * .95]},
                   {"type": "ellipse", "position": [w * .3, h * .1], "size": [w * .48, h * .7]},
                   {"type": "rect", "position": [0, h * .3], "size": [w * .9, h * .35], "roundness": h * .17},
                   {"type": "fill", "color": color}])]


def thumb_icon(color):
    """Thumbs-up: fist + thumb + cuff."""
    return [group([{"type": "rect", "position": [-48, 22], "size": [26, 74], "roundness": 8},
                   {"type": "fill", "color": color}]),
            group([{"type": "rect", "position": [8, 26], "size": [78, 70], "roundness": 18},
                   {"type": "rect", "position": [-2, -24], "size": [34, 64], "roundness": 16, },
                   {"type": "fill", "color": color}], rot=-12)]


def bell_icon(color=NAVY):
    return [group([{"type": "ellipse", "position": [0, 44], "size": [22, 22]},
                   {"type": "rect", "position": [0, 30], "size": [90, 14], "roundness": 7},
                   {"type": "rect", "position": [0, 4], "size": [64, 56], "roundness": 26},
                   {"type": "ellipse", "position": [0, -20], "size": [64, 64]},
                   {"type": "fill", "color": color}])]


def finger_icon():
    """A cartoon pointing hand (round fingertip) used to 'tap' buttons."""
    return [group(rect([0, -40], [44, 100], "#FFD7B5", 22) + [{"type": "stroke", "color": "#C98E63", "width": 5}]),
            group(rect([0, 40], [100, 90], "#FFD7B5", 34) + [{"type": "stroke", "color": "#C98E63", "width": 5}])]


# ------------------------------------------------------------------ the Mokki rig
def mouth_table(words):
    """words: list of (start, end, kind) in the timeline the rig lives in.
    kind 0 = talk/sing, 1 = yawn, 2 = giggle, 3 = gasp."""
    w = sorted((s, max(e, s + 0.12), k) for s, e, k in words)
    return "{" + ",".join(f"{s:.2f},{e:.2f},{k}" for s, e, k in w) + "}"


def words_from_transcript(words, offset):
    """[(start, end, text)] from a transcription -> rig word list, dropping delivery tags except yawns/giggles/gasps."""
    out = []
    for s, e, t in words:
        k = 0
        if t.startswith("["):
            k = {"[yawns]": 1, "[giggles]": 2, "[gasps]": 3}.get(t)
            if k is None:
                continue
        out.append((offset + s, offset + e, k))
    return out


def box_map(box=(1920, 1080)):
    """The picture is fitted ("contain") into a layer box the size of the composition.
    Returns (scale, map image px -> layer px, anchor at bottom-centre of the picture)."""
    bw, bh = box
    sc = min(bw / MW, bh / MH)
    ox, oy = (bw - MW * sc) / 2, (bh - MH * sc) / 2
    mp = lambda px, py: [round(ox + px * sc, 2), round(oy + py * sc, 2)]
    return sc, mp, [round(ox + MW * sc / 2, 2), round(oy + MH * sc, 2)]


def hand_pos(box=(1920, 1080)):
    """Where Mokki 'holds' a prop (just right of his mouth), in his layer-local pixels."""
    sc, mp, _ = box_map(box)
    x, y = mp(586, 945)
    return [round(x + 172 * sc / S, 1), round(y + 26 * sc / S, 1)]


def mokki_rig(id_, words, pos_keys, scale=0.5, closed=(), pos_expr=None, rot_expr=None, scale_expr=None, scale_keys=None,
              box=(1920, 1080)):
    """Mokki picture + lip-synced mouth + blinking eyelids. Children are parented to the picture.
    `box` is the composition size the rig lives in."""
    S, m, anchor = box_map(box)
    L = []
    anim = {"position": {"keyframes": pos_keys}}
    if pos_expr:
        anim["position"]["expression"] = pos_expr
    anim["rotation"] = {"keyframes": [{"time": 0, "value": 0}],
                        "expression": rot_expr or "return value+4*math.sin(2*math.pi*time/2.4)"}
    anim["scale"] = {"keyframes": scale_keys or [{"time": 0, "value": [scale, scale]}]}
    if scale_expr:
        anim["scale"]["expression"] = scale_expr
    L.append({"id": id_, "content": {"kind": "media", "asset": {"type": "image", "uri": MOKKI_URL, "width": MW, "height": MH}},
              "transform": {"anchor": anchor, "position": pos_keys[0]["value"], "scale": [scale, scale]}, "animations": anim})
    mouth_o = ("local W=" + mouth_table(words) + "; local o=0; "
               "for i=1,#W,3 do local s=W[i]; if s>time then break end; local e=W[i+1]; "
               "if time<e then local k=W[i+2]; "
               "if k==0 then o=0.3+0.7*math.abs(math.sin(math.pi*(time-s)/0.17)) "
               "elseif k==1 then o=1.4*math.sin(math.pi*(time-s)/(e-s)) "
               "elseif k==2 then o=0.35+0.45*math.abs(math.sin(time*28)) else o=1.1 end; break end end; ")
    mx, my = m(586, 945)
    L.append({"id": id_ + "_smile", "parentId": id_, "transform": {"position": [mx, my], "scale": [S, S]},
              "content": {"kind": "shape", "items": [
                  {"type": "path", "closed": False, "vertices": [
                      {"point": [-127, -40], "outTangent": [30, 45]},
                      {"point": [0, 46], "inTangent": [-70, 0], "outTangent": [70, 0]},
                      {"point": [127, -46], "inTangent": [-30, 45]}]},
                  {"type": "stroke", "color": NAVY, "width": 24, "lineCap": "round", "lineJoin": "round"}]},
              "animations": {"opacity": {"keyframes": [{"time": 0, "value": 1}],
                                         "expression": mouth_o + "if o>0.08 then return 0 end; return 1"}}})
    L.append({"id": id_ + "_mouth", "parentId": id_, "transform": {"position": [mx, my - 8]},
              "content": {"kind": "shape", "items": [group(ell([0, 32], [96, 44], "#FF7A93")),
                                                     group([{"type": "ellipse", "position": [0, 0], "size": [170, 130]},
                                                            {"type": "fill", "color": NAVY}])]},
              "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                       "expression": mouth_o + "if o<0.08 then return Vec.v2(0,0) end; "
                                       f"return Vec.v2({S:.4f}*(0.75+0.25*math.min(o,1.2)), {S:.4f}*(0.25+0.85*o))"}}})
    cl = "{" + ",".join(f"{a:.2f},{b:.2f}" for a, b in closed) + "}" if closed else "{}"
    blink = (f"local b=0; local C={cl}; for i=1,#C,2 do if time>=C[i] and time<C[i+1] then b=1 end end; "
             "local p=(time+0.7)%3.9; local k=0; if p<0.08 then k=p/0.08 elseif p<0.13 then k=1 elseif p<0.21 then k=(0.21-p)/0.08 end; "
             "if b==1 then k=1 end; ")
    for eid, cx, cy, d in [("L", 410, 715.5, 344), ("R", 742.5, 721.5, 228)]:
        L.append({"id": f"{id_}_lid{eid}", "parentId": id_, "transform": {"position": m(cx, cy - d / 2)},
                  "content": {"kind": "shape", "items": ell([0, d / 2], [d, d], BODY)},
                  "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 0]}],
                                           "expression": blink + f"return Vec.v2({S:.4f},{S:.4f}*k)"}}})
        L.append({"id": f"{id_}_lidline{eid}", "parentId": id_, "transform": {"position": m(cx, cy), "scale": [S, S]},
                  "content": {"kind": "shape", "items": [
                      {"type": "path", "closed": False, "vertices": [
                          {"point": [-d * .42, 0], "outTangent": [d * .2, d * .22]},
                          {"point": [d * .42, 0], "inTangent": [-d * .2, d * .22]}]},
                      {"type": "stroke", "color": NAVY, "width": 16, "lineCap": "round"}]},
                  "animations": {"opacity": {"keyframes": [{"time": 0, "value": 0}],
                                             "expression": blink + "if k>0.85 then return 1 end; return 0"}}})
    return L


def wipe(id_, start):
    """Yellow/mint circle wipe, 0.8 s, covering the frame at start+0.4."""
    return shape_layer(id_, ell([0, 0], [900, 900], BODY) + ell([0, 0], [2300, 2300], YELLOW), start, 0.8, (960, 540),
                       {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": "ease_in"},
                                                {"time": 0.4, "value": [1, 1], "easing": "ease_out"},
                                                {"time": 0.8, "value": [0, 0]}]}})


# ------------------------------------------------------------------ kid-friendly text (Fredoka One, letters pop in)
KID_FONT = "https://pastatic.picsart.com/27849958378051772310.ttf"   # Fredoka One (Google Fonts, OFL - free for commercial use)
POP_LETTERS = {"preset": "fade_in_chars", "params": {"duration": 0.5, "stagger": 0.6, "grow": 1, "overshoot": 0.7}}


def kid_text(id_, t, pos, size, start, dur, color=CORAL, stroke=WHITE, letters=True, pop=True, wobble=False, shadow=False, wrap=None):
    """Big round Fredoka One text, thick white outline, soft shadow, letters popping in."""
    out = []
    def content(col, strk):
        c = {"kind": "text", "text": t, "font": {"family": KID_FONT, "size": size}, "color": col, "alignment": "center",
             "lineHeight": round(size * 1.15)}  # pixels between baselines
        if strk:
            c["stroke"] = {"width": max(10, size // 6), "color": strk}
        if wrap:
            c["wrapWidth"] = wrap
        if letters:
            c["animations"] = [POP_LETTERS]
        return c
    anim = {}
    if pop:
        anim["scale"] = {"keyframes": [{"time": 0, "value": [1, 1]}, {"time": max(dur - 0.25, 0.01), "value": [1, 1], "easing": "ease_in"},
                                       {"time": dur, "value": [0, 0]}]}
    if wobble:
        anim["rotation"] = {"keyframes": [{"time": 0, "value": 0}], "expression": "return 4*math.sin(2*math.pi*time/0.8)"}
    if shadow:
        sh = {"id": id_ + "_sh", "start": snap(start), "duration": snap(dur), "timeMode": "layer",
              "transform": {"position": [pos[0] + 6, pos[1] + 8], "opacity": 0.25}, "content": content(NAVY, NAVY)}
        if anim:
            sh["animations"] = dict(anim)
        out.append(sh)
    d = {"id": id_, "start": snap(start), "duration": snap(dur), "timeMode": "layer", "transform": {"position": list(pos)},
         "content": content(color, stroke)}
    if anim:
        d["animations"] = anim
    out.append(d)
    return out


# ------------------------------------------------------------------ close-up demos (big, clear, animated)
BRUSH_BLUE, PASTE, PEA_GREEN = "#4A90E2", "#E8FBFF", "#7BC043"


def brush_h_icon():
    """Horizontal toothbrush, head on the right, bristles on top. Bristle tops at (90,-62)."""
    bristles = []
    for i, x in enumerate(range(48, 140, 16)):
        bristles += [{"type": "rect", "position": [x, -40], "size": [11, 44], "roundness": 5}]
    return [group(bristles + [{"type": "fill", "color": WHITE}, {"type": "stroke", "color": "#8FCDEB", "width": 3}]),
            group(rect([90, -8], [130, 34], BRUSH_BLUE, 14) + rect([-120, 0], [300, 36], BRUSH_BLUE, 18) +
                  rect([-200, 0], [60, 20], "#9CC9F5", 10))]


def paste_blob_icon(r=34):
    return [group(ell([-r * .3, -r * .3], [r * .5, r * .35], WHITE)),
            group([{"type": "ellipse", "position": [0, 0], "size": [r * 2, r * 1.6]}, {"type": "fill", "color": PASTE},
                   {"type": "stroke", "color": "#5BC0EB", "width": 6}])]


def pea_icon(r=34):
    return [group(ell([-r * .3, -r * .35], [r * .45, r * .35], "#D9F2B4")),
            group([{"type": "ellipse", "position": [0, 0], "size": [r * 2, r * 2]}, {"type": "fill", "color": PEA_GREEN},
                   {"type": "stroke", "color": "#4E8A1E", "width": 6}])]


def tube_icon():
    """Toothpaste tube, cap/nozzle at (0,-115)."""
    return [group(rect([0, -108], [44, 30], BRUSH_BLUE, 8) + rect([0, -85], [70, 26], "#DDE7F0", 6) +
                  rect([0, 30], [150, 210], WHITE, 34) + rect([0, 30], [150, 56], CORAL, 0) +
                  [{"type": "stroke", "color": "#8FCDEB", "width": 6}])]


def card_layer(id_, t0, dur, center, size, border=YELLOW):
    w, h = size
    return shape_layer(id_, [group([{"type": "rect", "position": [0, 0], "size": [w, h], "roundness": 60},
                                    {"type": "fill", "color": WHITE}, {"type": "stroke", "color": border, "width": 16}])],
                       t0, dur, center, {"scale": pop_scale(dur)})


def _rot(v, deg):
    import math
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def toothpaste_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """Big brush; the tube squeezes a pea-sized blob onto it; a real pea pops up beside it ('this much!')."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc)))
    bsc = 1.9 * sc
    bpos = (cx - 40 * sc, cy + 190 * sc)
    blob = (bpos[0] + 90 * bsc, bpos[1] - 62 * bsc - 40 * sc)
    L.append(shape_layer(p + "brush", brush_h_icon(), t0 + 0.15, dur - 0.15, bpos, {"scale": pop_scale(dur - 0.15, bsc)}))
    # tube: nozzle points down-left at the blob, squeezes twice
    d = (0.7071, -0.7071)
    tdist = (115 + 50) * 1.3 * sc
    tpos = (blob[0] + d[0] * tdist, blob[1] + d[1] * tdist)
    t_sq = 1.0
    L.append(shape_layer(p + "tube", tube_icon(), t0 + 0.35, 2.6, tpos,
                         {"rotation": {"keyframes": [{"time": 0, "value": -135}]},
                          "scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1.3 * sc, 1.3 * sc]},
                                                  {"time": t_sq - 0.35, "value": [1.3 * sc, 1.3 * sc], "easing": "ease_in_out"},
                                                  {"time": t_sq, "value": [sc * 1.05, sc * 1.4], "easing": "ease_in_out"},
                                                  {"time": t_sq + 0.3, "value": [1.3 * sc, 1.3 * sc], "easing": "ease_in_out"},
                                                  {"time": t_sq + 0.6, "value": [sc * 1.05, sc * 1.4], "easing": "ease_in_out"},
                                                  {"time": t_sq + 0.9, "value": [1.3 * sc, 1.3 * sc]},
                                                  {"time": 2.3, "value": [1.3 * sc, 1.3 * sc], "easing": "ease_in"}, {"time": 2.6, "value": [0, 0]}]}}))
    # blob grows while the tube squeezes
    gb = t0 + 0.35 + t_sq - 0.1
    L.append(shape_layer(p + "blob", paste_blob_icon(46), gb, t0 + dur - gb, blob,
                         {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": "ease_out"}, {"time": 0.9, "value": [sc, sc], "easing": POP},
                                                  {"time": 1.1, "value": [sc * 1.15, sc * 1.15]}, {"time": 1.3, "value": [sc, sc]},
                                                  {"time": t0 + dur - gb - 0.25, "value": [sc, sc], "easing": "ease_in"},
                                                  {"time": t0 + dur - gb, "value": [0, 0]}]}}))
    # the pea pops in next to it, with "="
    tp = gb + 1.3
    if tp < t0 + dur - 0.6:
        pea_pos = (blob[0] + 330 * sc, blob[1])
        L += kid_text(p + "eq", "=", ((blob[0] + pea_pos[0]) / 2, blob[1] + 22 * sc), int(140 * sc), tp, t0 + dur - tp,
                      color=NAVY, letters=False, shadow=False)
        L.append(shape_layer(p + "pea", pea_icon(46), tp + 0.2, t0 + dur - tp - 0.2, pea_pos,
                             {"scale": pop_scale(t0 + dur - tp - 0.2, sc * 1.05),
                              "position": {"keyframes": [{"time": 0, "value": list(pea_pos)}],
                                           "expression": "return value+Vec.v2(0,-12*math.abs(math.sin(time*5)))"}}))
        for i, (dx, dy) in enumerate([(-80, -80), (80, -90), (0, 80)]):
            L.append(prop(p + f"spk{i}", sparkle_icon(34 * sc, YELLOW), (blob[0] + dx * sc, blob[1] + dy * sc), tp + 0.3 + i * 0.12,
                          t0 + dur - tp - 0.3 - i * 0.12, spin=150))
    return L


def mouth_icon():
    teeth = []
    for row, y in ((0, -78), (1, 78)):
        for i, x in enumerate(range(-225, 226, 90)):
            teeth.append({"type": "rect", "position": [x, y], "size": [80, 96], "roundness": 24})
    return [group(teeth + [{"type": "fill", "color": WHITE}, {"type": "stroke", "color": "#D7EEF7", "width": 4}]),
            group(ell([0, 110], [360, 120], "#FF7A93")),
            group(ell([0, 0], [620, 300], "#8B1E3F")),
            group(ell([0, 0], [720, 390], "#FF9FB2") + [{"type": "stroke", "color": "#E86A8A", "width": 10}])]


def mouth_demo(p, t0, dur, mode="updown", center=(1190, 560), sc=1.0, card=True, arrows=True):
    """A big smiling mouth; the brush scrubs up and down (or in little circles) and the teeth start to sparkle."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=PINK))
    ms = 1.3 * sc
    L.append(shape_layer(p + "mouth", mouth_icon(), t0 + 0.1, dur - 0.1, (cx, cy + 10 * sc), {"scale": pop_scale(dur - 0.1, ms)}))
    # sparkles appear tooth by tooth as they get clean
    k = 0
    for row, y in ((0, -78), (1, 78)):
        for i, x in enumerate(range(-225, 226, 180)):
            st = t0 + 0.8 + k * 0.35
            if st < t0 + dur - 0.5:
                L.append(prop(p + f"sh{k}", sparkle_icon(30 * ms, YELLOW), (cx + (x + 20) * ms, cy + 10 * sc + (y - 20) * ms), st, t0 + dur - st, spin=160))
            k += 1
    if mode == "updown":
        motion = f"return value+Vec.v2({230 * ms:.0f}*math.sin(2*math.pi*time/3.2), {75 * ms:.0f}*math.sin(2*math.pi*time*2.0))"
        if arrows:
            for nm, rot, dy in (("up", 0, -1), ("dn", 180, 1)):
                L.append(prop(p + nm, [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -55], "outerRadius": 48},
                                              {"type": "rect", "position": [0, 20], "size": [36, 100], "roundness": 10},
                                              {"type": "fill", "color": CORAL}, {"type": "stroke", "color": WHITE, "width": 6}], rot=rot)],
                              (cx - 500 * sc, cy + dy * 150 * sc), t0 + 0.4, dur - 0.4, s=sc, bob=dy * 20))
    else:
        motion = (f"return value+Vec.v2({200 * ms:.0f}*math.sin(2*math.pi*time/4.5)+{60 * ms:.0f}*math.cos(time*8), "
                  f"{60 * ms:.0f}*math.sin(time*8))")
        if arrows:
            L.append(shape_layer(p + "circ", [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [70, 8],
                                                      "outerRadius": 30, "rotation": 180}, {"type": "fill", "color": CORAL}]),
                                              group([{"type": "ellipse", "position": [0, 0], "size": [140, 140]},
                                                     {"type": "trim", "start": 0, "end": 0.8},
                                                     {"type": "stroke", "color": CORAL, "width": 22, "lineCap": "round"}])],
                                 t0 + 0.4, dur - 0.4, (cx - 500 * sc, cy),
                                 {"scale": pop_scale(dur - 0.4, sc), "rotation": {"keyframes": [{"time": 0, "value": 0}],
                                                                                  "expression": "return value+360*time"}}))
    # brush over the teeth (bristles towards the teeth)
    L.append(shape_layer(p + "brush", brush_h_icon(), t0 + 0.4, dur - 0.4, (cx - 60 * sc, cy + 60 * sc),
                         {"scale": pop_scale(dur - 0.4, 1.35 * sc),
                          "rotation": {"keyframes": [{"time": 0, "value": -12}]},
                          "position": {"keyframes": [{"time": 0, "value": [cx - 60 * sc, cy + 60 * sc]}], "expression": motion}}))
    return L


def swish_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """A cup tips water into Mokki's mouth area -> swish swish -> spit drops into the sink."""
    cx, cy = center
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border="#5BC0EB"))
    L.append(shape_layer(p + "sink", [group(ell([0, -40], [520, 90], "#BFE6F7")),
                                      group(rect([0, 40], [600, 190], WHITE, 90) + [{"type": "stroke", "color": "#8FCDEB", "width": 10}])],
                         t0 + 0.1, dur - 0.1, (cx, cy + 170 * sc), {"scale": pop_scale(dur - 0.1, sc)}))
    L.append(shape_layer(p + "cup", [group(rect([0, -60], [150, 26], "#BFE6F7", 8) + rect([0, 10], [150, 170], PINK, 26) +
                                           [{"type": "stroke", "color": "#E86A8A", "width": 8}])],
                         t0 + 0.2, dur - 0.2, (cx - 260 * sc, cy - 140 * sc),
                         {"scale": pop_scale(dur - 0.2, sc), "rotation": {"keyframes": [{"time": 0, "value": 0, "easing": "ease_in_out"},
                                                                                        {"time": 0.8, "value": 40}]}}))
    for i in range(6):
        off = i * 0.25
        L.append(shape_layer(p + f"drop{i}", [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -22], "outerRadius": 26},
                                                    {"type": "ellipse", "position": [0, 0], "size": [44, 44]},
                                                    {"type": "fill", "color": "#4FB3F6"}])],
                             t0 + 0.6, dur - 0.6, (cx, cy),
                             {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}]},
                              "position": {"keyframes": [{"time": 0, "value": [cx, cy]}],
                                           "expression": f"local t=(time+{off:.2f})%1.5; "
                                                         f"return Vec.v2({cx - 160 * sc:.0f}+{230 * sc:.0f}*t/1.5+{20 * (i % 3 - 1)}, {cy - 120 * sc:.0f}+{300 * sc:.0f}*(t/1.5)^2)"}}))
    return L


# ------------------------------------------------------------------ family rig (Papa, Mama, Pia, Pip, Grandpa, Granny)
import json as _json, os as _os
FAMILY_META = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "character", "family", "family.json")))
# Picsart-hosted copies of mokki/character/family/<id>-nomouth.png (expiring; re-upload when needed)
FAMILY_URLS = {}


def family_rig(cid, words, pos_keys, scale=0.5, closed=(), pos_expr=None, rot_expr=None, scale_keys=None, box=(1920, 1080), prefix=None):
    """Like mokki_rig, for a family member. Same visual scale rule: at scale s, a character appears as big
    relative to Mokki as in the family line-up (pass the same s you give Mokki)."""
    meta = FAMILY_META[cid]
    iw, ih = meta["w"], meta["h"]
    bw, bh = box
    fit = min(bw / iw, bh / ih)
    ox, oy = (bw - iw * fit) / 2, (bh - ih * fit) / 2
    mp = lambda px, py: [round(ox + px * fit, 2), round(oy + py * fit, 2)]
    anchor = [round(ox + iw * fit / 2, 2), round(oy + ih * fit, 2)]
    # keep the line-up proportions: Mokki's picture is MH px tall and fitted with box_map's scale
    mok_fit = box_map(box)[0]
    rel = mok_fit / fit                          # this character's px are drawn at the same size as Mokki's px
    s = scale * rel
    id_ = prefix or cid
    anim = {"position": {"keyframes": pos_keys}, "scale": {"keyframes": scale_keys or [{"time": 0, "value": [s, s]}]},
            "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": rot_expr or "return value+3*math.sin(2*math.pi*time/2.8)"}}
    if scale_keys:
        for k in anim["scale"]["keyframes"]:
            k["value"] = [k["value"][0] * rel, k["value"][1] * rel]
    if pos_expr:
        anim["position"]["expression"] = pos_expr
    L = [{"id": id_, "content": {"kind": "media", "asset": {"type": "image", "uri": FAMILY_URLS[cid], "width": iw, "height": ih}},
          "transform": {"anchor": anchor, "position": pos_keys[0]["value"], "scale": [s, s]}, "animations": anim}]
    mouth_o = ("local W=" + mouth_table(words) + "; local o=0; "
               "for i=1,#W,3 do local s=W[i]; if s>time then break end; local e=W[i+1]; "
               "if time<e then local k=W[i+2]; "
               "if k==0 then o=0.3+0.7*math.abs(math.sin(math.pi*(time-s)/0.17)) "
               "elseif k==1 then o=1.4*math.sin(math.pi*(time-s)/(e-s)) "
               "elseif k==2 then o=0.35+0.45*math.abs(math.sin(time*28)) else o=1.1 end; break end end; ")
    fx, fy, fw = meta["face"]["mouth"]
    mx, my = mp(fx, fy)
    k = fw * fit / 254.0                           # mouth width relative to Mokki's smile path (254 px)
    if cid != "pip":                               # Pip keeps his pacifier drawn on
        L.append({"id": id_ + "_smile", "parentId": id_, "transform": {"position": [mx, my - 6 * k], "scale": [k, k]},
                  "content": {"kind": "shape", "items": [
                      {"type": "path", "closed": False, "vertices": [
                          {"point": [-127, -40], "outTangent": [30, 45]},
                          {"point": [0, 46], "inTangent": [-70, 0], "outTangent": [70, 0]},
                          {"point": [127, -46], "inTangent": [-30, 45]}]},
                      {"type": "stroke", "color": NAVY, "width": 26, "lineCap": "round", "lineJoin": "round"}]},
                  "animations": {"opacity": {"keyframes": [{"time": 0, "value": 1}],
                                             "expression": mouth_o + "if o>0.08 then return 0 end; return 1"}}})
        L.append({"id": id_ + "_mouth", "parentId": id_, "transform": {"position": [mx, my]},
                  "content": {"kind": "shape", "items": [group(ell([0, 32], [96, 44], "#FF7A93")),
                                                         group([{"type": "ellipse", "position": [0, 0], "size": [170, 130]},
                                                                {"type": "fill", "color": NAVY}])]},
                  "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 1]}],
                                           "expression": mouth_o + "if o<0.08 then return Vec.v2(0,0) end; "
                                           f"return Vec.v2({k:.4f}*(0.75+0.25*math.min(o,1.2)), {k:.4f}*(0.25+0.85*o))"}}})
    cl = "{" + ",".join(f"{a:.2f},{b:.2f}" for a, b in closed) + "}" if closed else "{}"
    blink = (f"local b=0; local C={cl}; for i=1,#C,2 do if time>=C[i] and time<C[i+1] then b=1 end end; "
             f"local p=(time+{(sum(map(ord, cid)) % 30) / 10:.1f})%4.3; local k=0; if p<0.08 then k=p/0.08 elseif p<0.13 then k=1 elseif p<0.21 then k=(0.21-p)/0.08 end; "
             "if b==1 then k=1 end; ")
    body = meta["body"]
    for side in ("L", "R"):
        ex, ey, ed = meta["face"]["eye" + side]
        d = ed * 1.04
        L.append({"id": f"{id_}_lid{side}", "parentId": id_, "transform": {"position": mp(ex, ey - d / 2)},
                  "content": {"kind": "shape", "items": ell([0, d / 2], [d, d], body)},
                  "animations": {"scale": {"keyframes": [{"time": 0, "value": [1, 0]}],
                                           "expression": blink + f"return Vec.v2({fit:.4f},{fit:.4f}*k)"}}})
        L.append({"id": f"{id_}_lidline{side}", "parentId": id_, "transform": {"position": mp(ex, ey), "scale": [fit, fit]},
                  "content": {"kind": "shape", "items": [
                      {"type": "path", "closed": False, "vertices": [
                          {"point": [-d * .42, 0], "outTangent": [d * .2, d * .22]},
                          {"point": [d * .42, 0], "inTangent": [-d * .2, d * .22]}]},
                      {"type": "stroke", "color": NAVY, "width": 14, "lineCap": "round"}]},
                  "animations": {"opacity": {"keyframes": [{"time": 0, "value": 0}],
                                             "expression": blink + "if k>0.85 then return 1 end; return 0"}}})
    return L


# ------------------------------------------------------------------ hand-washing demos (cartoon hands, water, soap, germs, towel)
SKIN, SKIN_LINE, WATER, MUD = "#FFD7B5", "#C98E63", "#5BC0EB", "#8B5A2B"


def hand_icon(side=1, color=SKIN, line=SKIN_LINE):
    """A cartoon hand, fingers up, palm facing us. side=1 thumb on the left, -1 thumb on the right. ~260x330 px."""
    fingers = [{"type": "rect", "position": [x, -95 + abs(x) * 0.25], "size": [44, 150], "roundness": 22} for x in (-66, -22, 22, 66)]
    thumb = group([{"type": "rect", "position": [0, 0], "size": [46, 120], "roundness": 23}], pos=(-110 * side, 20), rot=-35 * side)
    return [group(fingers + [{"type": "fill", "color": color}, {"type": "stroke", "color": line, "width": 6}]),
            group([thumb, {"type": "fill", "color": color}, {"type": "stroke", "color": line, "width": 6}]),
            group([{"type": "rect", "position": [0, 40], "size": [190, 170], "roundness": 70},
                   {"type": "fill", "color": color}, {"type": "stroke", "color": line, "width": 6}])]


def germ_icon(color="#7BC043"):
    return [group([{"type": "ellipse", "position": [-13, -4], "size": [16, 16]}, {"type": "ellipse", "position": [13, -4], "size": [16, 16]},
                   {"type": "fill", "color": WHITE}]),
            group([{"type": "ellipse", "position": [-13, -2], "size": [7, 7]}, {"type": "ellipse", "position": [13, -2], "size": [7, 7]},
                   {"type": "fill", "color": NAVY}]),
            group([{"type": "polystar", "starType": "star", "points": 10, "position": [0, 0], "outerRadius": 46, "innerRadius": 34,
                    "outerRoundness": 0.4}, {"type": "fill", "color": color}, {"type": "stroke", "color": "#4E8A1E", "width": 4}])]


def bubble_icon(r=30):
    return [group(ell([-r * .35, -r * .35], [r * .5, r * .35], WHITE)),
            group([{"type": "ellipse", "position": [0, 0], "size": [2 * r, 2 * r]}, {"type": "fill", "color": "#E8F7FF", "opacity": 0.7},
                   {"type": "stroke", "color": "#8FCDEB", "width": 4}])]


def two_hands(p, t0, dur, center, sc, rub=None, mud=False):
    """Two hands side by side. rub: None | 'palms' | 'backs' | 'fingers' | 'thumbs' | 'rub' (rubbing motion)."""
    cx, cy = center
    L = []
    gap = 125 * sc
    for i, side in enumerate((1, -1)):
        x0 = cx - gap * side
        mot = None
        if rub == "palms" or rub == "rub":
            mot = f"return value+Vec.v2({55 * sc:.0f}*math.sin(time*9){'' if side > 0 else '*-1'}, {30 * sc:.0f}*math.cos(time*9))"
        elif rub == "backs":
            mot = f"return value+Vec.v2(0, {60 * sc:.0f}*math.sin(time*8){'' if side > 0 else '*-1'})"
        elif rub == "fingers":
            mot = f"return value+Vec.v2({35 * sc:.0f}*math.sin(time*12){'' if side > 0 else '*-1'}, 0)"
        elif rub == "thumbs":
            mot = f"return value+Vec.v2({20 * sc:.0f}*math.sin(time*14), {20 * sc:.0f}*math.cos(time*14))"
        anim = {"scale": pop_scale(dur, sc)}
        if mot:
            anim["position"] = {"keyframes": [{"time": 0, "value": [x0, cy]}], "expression": mot}
        if rub in ("palms", "rub"):
            anim["rotation"] = {"keyframes": [{"time": 0, "value": 12 * side}]}
        L.append(shape_layer(f"{p}hand{i}", hand_icon(side), t0, dur, (x0, cy), anim))
        if mud:
            spots = [group(ell([dx, dy], [r, r * 0.8], MUD)) for dx, dy, r in ((-40, 30, 50), (35, 70, 40), (10, -40, 34), (-55, -110, 26), (50, -60, 30))]
            L.append(shape_layer(f"{p}mud{i}", spots, t0 + 0.3, dur - 0.3, (x0, cy), {"scale": pop_scale(dur - 0.3, sc),
                                 **({"position": anim["position"]} if mot else {})}))
    return L


def hands_card(p, t0, dur, center=(1190, 560), sc=1.0, card=True, border="#5BC0EB"):
    L = []
    if card:
        L.append(card_layer(p + "card", t0, dur, center, (1180 * sc, 680 * sc), border=border))
    return L


def water_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """A tap pours water on two hands, splash drops."""
    cx, cy = center
    L = hands_card(p, t0, dur, center, sc, card)
    tap = (cx, cy - 250 * sc)
    L.append(shape_layer(p + "tap", [group(rect([0, -40], [60, 50], "#B0B7BF", 10) + rect([-70, -70], [200, 50], "#C9D1D9", 25) +
                                           rect([60, -10], [44, 70], "#C9D1D9", 14) + [{"type": "stroke", "color": "#8A939C", "width": 5}])],
                         t0 + 0.1, dur - 0.1, (tap[0] - 60 * sc, tap[1]), {"scale": pop_scale(dur - 0.1, sc)}))
    L.append(shape_layer(p + "stream", [group(rect([0, 0], [46, 300], WATER, 23)), group(rect([0, 0], [70, 300], "#BFE6F7", 35))],
                         t0 + 0.5, dur - 0.6, (cx, cy - 70 * sc),
                         {"scale": {"keyframes": [{"time": 0, "value": [sc, 0], "easing": "ease_out"}, {"time": 0.4, "value": [sc, sc]}],
                                    "expression": "return Vec.v2(value.x*(1+0.08*math.sin(time*30)), value.y)"}}))
    L += two_hands(p, t0 + 0.3, dur - 0.3, (cx, cy + 120 * sc), sc * 0.85, rub="rub")
    for i in range(6):
        off = i * 0.22
        L.append(shape_layer(f"{p}drop{i}", [group([{"type": "polystar", "starType": "polygon", "points": 3, "position": [0, -16], "outerRadius": 18},
                                                   {"type": "ellipse", "position": [0, 0], "size": [32, 32]}, {"type": "fill", "color": WATER}])],
                             t0 + 0.8, dur - 0.8, (cx, cy),
                             {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}]},
                              "position": {"keyframes": [{"time": 0, "value": [cx, cy]}],
                                           "expression": f"local t=(time+{off:.2f})%1.3; local d={-1 if i % 2 else 1}; "
                                                         f"return Vec.v2({cx:.0f}+d*{(120 + 30 * i) * sc:.0f}*t/1.3, {cy + 60 * sc:.0f}-{150 * sc:.0f}*math.sin(math.pi*t/1.3)+{150 * sc:.0f}*t)"}}))
    return L


def soap_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """Soap pump presses twice, soap drops on the hands, bubbles grow."""
    cx, cy = center
    L = hands_card(p, t0, dur, center, sc, card, border=PINK)
    pump = (cx + 300 * sc, cy - 60 * sc)
    L.append(shape_layer(p + "pump", [group(rect([0, -150], [80, 22], "#9B59D0", 8) + rect([-50, -140], [80, 18], "#9B59D0", 8) +
                                            rect([0, -110], [26, 60], "#B0B7BF", 6)),
                                      group(rect([0, 20], [170, 220], "#F3E6FF", 50) + rect([0, 40], [170, 70], "#C9A2E8", 0) +
                                            [{"type": "stroke", "color": "#9B59D0", "width": 6}])],
                         t0 + 0.1, dur - 0.1, pump, {"scale": pop_scale(dur - 0.1, sc)}))
    # the pump head pressing (a small cap that moves down twice)
    L.append(shape_layer(p + "press", [group(rect([0, 0], [90, 24], "#7B3FB4", 10))], t0 + 0.5, dur - 0.6, (pump[0], pump[1] - 170 * sc),
                         {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}]},
                          "position": {"keyframes": [{"time": 0, "value": [pump[0], pump[1] - 170 * sc], "easing": "ease_in_out"},
                                                     {"time": 0.3, "value": [pump[0], pump[1] - 140 * sc], "easing": "ease_in_out"},
                                                     {"time": 0.6, "value": [pump[0], pump[1] - 170 * sc], "easing": "ease_in_out"},
                                                     {"time": 0.9, "value": [pump[0], pump[1] - 140 * sc], "easing": "ease_in_out"},
                                                     {"time": 1.2, "value": [pump[0], pump[1] - 170 * sc]}]}}))
    L += two_hands(p, t0 + 0.2, dur - 0.2, (cx - 140 * sc, cy + 110 * sc), sc * 0.85)
    # soap blob falls on the hands
    L.append(shape_layer(p + "blob", paste_blob_icon(34), t0 + 0.8, dur - 0.8, (pump[0] - 90 * sc, pump[1] - 140 * sc),
                         {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [sc, sc]}]},
                          "position": {"keyframes": [{"time": 0, "value": [pump[0] - 90 * sc, pump[1] - 140 * sc], "easing": "ease_in"},
                                                     {"time": 0.9, "value": [cx - 140 * sc, cy + 60 * sc]}]}}))
    for i, (dx, dy, r) in enumerate([(-260, -40, 30), (-80, -60, 40), (-180, -150, 26), (20, 20, 34), (-320, 90, 28), (-40, 140, 30), (60, -120, 22)]):
        st = t0 + 1.6 + i * 0.18
        if st < t0 + dur - 0.4:
            L.append(prop(f"{p}bub{i}", bubble_icon(r), (cx + (dx - 60) * sc, cy + dy * sc), st, t0 + dur - st, s=sc * 1.3, bob=10))
    return L


def rub_demo(p, t0, dur, mode="rub", center=(1190, 560), sc=1.0, card=True, germs_at=None, count=False):
    """Hands rubbing with bubbles. germs_at: time the germs run away (germs shown before it). count: 1..20 counter."""
    cx, cy = center
    L = hands_card(p, t0, dur, center, sc, card, border="#2BB673")
    L += two_hands(p, t0 + 0.1, dur - 0.1, (cx, cy + 60 * sc), sc * 0.95, rub=mode)
    for i, (dx, dy, r) in enumerate([(-300, -120, 34), (280, -140, 28), (-250, 160, 30), (300, 120, 36), (0, -230, 26), (-120, 230, 24), (150, 220, 28)]):
        st = t0 + 0.3 + i * 0.12
        L.append(prop(f"{p}bub{i}", bubble_icon(r), (cx + dx * sc, cy + dy * sc), st, t0 + dur - st, s=sc * 1.3, bob=12))
    if germs_at is not None:
        for i, (dx, dy) in enumerate([(-80, -60), (90, 20), (-20, 110), (60, -130)]):
            st = t0 + 0.2 + i * 0.1
            gone = germs_at - st
            L.append(shape_layer(f"{p}germ{i}", germ_icon(), st, min(gone + 1.2, t0 + dur - st), (cx + dx * sc, cy + dy * sc),
                                 {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.3, "value": [0.9 * sc, 0.9 * sc]}]},
                                  "position": {"keyframes": [{"time": 0, "value": [cx + dx * sc, cy + dy * sc]},
                                                             {"time": gone, "value": [cx + dx * sc, cy + dy * sc], "easing": "ease_in"},
                                                             {"time": gone + 1.1, "value": [cx + dx * 6 * sc, cy - 900 * sc]}],
                                               "expression": f"return value+Vec.v2(8*math.sin(time*11+{i}),6*math.cos(time*9+{i}))"},
                                  "rotation": {"keyframes": [{"time": 0, "value": 0}], "expression": "return 15*math.sin(time*8)"}}))
    if count:
        n = 20
        step = (dur - 0.6) / n
        for k in range(1, n + 1):
            L += kid_text(f"{p}cnt{k}", str(k), (cx + 420 * sc, cy - 220 * sc), int(130 * sc), t0 + 0.3 + (k - 1) * step, step,
                          color=["#F0506E", "#4A90E2", "#2BB673", "#FF8A00", "#9B59D0"][k % 5], letters=False, pop=False)
    return L


def rinse_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """Water washes the bubbles away."""
    cx, cy = center
    L = water_demo(p, t0, dur, center, sc, card)
    for i, (dx, dy, r) in enumerate([(-120, 40, 30), (110, 60, 26), (-40, 160, 28), (60, -20, 24)]):
        L.append(shape_layer(f"{p}rb{i}", bubble_icon(r), t0 + 0.3, dur - 0.3, (cx + dx * sc, cy + dy * sc),
                             {"scale": {"keyframes": [{"time": 0, "value": [sc, sc]}, {"time": 0.6 + 0.2 * i, "value": [sc, sc], "easing": "ease_in"},
                                                      {"time": 1.2 + 0.2 * i, "value": [0, 0]}]},
                              "position": {"keyframes": [{"time": 0, "value": [cx + dx * sc, cy + dy * sc], "easing": "ease_in"},
                                                         {"time": 1.2 + 0.2 * i, "value": [cx + dx * sc, cy + (dy + 260) * sc]}]}}))
    return L


def dry_demo(p, t0, dur, center=(1190, 560), sc=1.0, card=True):
    """A striped towel swooshes across the hands; sparkles."""
    cx, cy = center
    L = hands_card(p, t0, dur, center, sc, card, border=YELLOW)
    L += two_hands(p, t0 + 0.1, dur - 0.1, (cx, cy + 60 * sc), sc * 0.95)
    towel = [group(rect([0, -70], [380, 26], "#FFFFFF", 0) + rect([0, 70], [380, 26], "#FFFFFF", 0)),
             group(rect([0, 0], [380, 230], "#FF8A9A", 30) + [{"type": "stroke", "color": "#E05A6E", "width": 8}])]
    L.append(shape_layer(p + "towel", towel, t0 + 0.4, dur - 0.5, (cx, cy + 40 * sc),
                         {"scale": pop_scale(dur - 0.5, sc),
                          "position": {"keyframes": [{"time": 0, "value": [cx, cy + 40 * sc]}],
                                       "expression": f"return value+Vec.v2({230 * sc:.0f}*math.sin(time*5), {25 * sc:.0f}*math.sin(time*10))"}}))
    for i, (dx, dy) in enumerate([(-330, -180), (330, -160), (-300, 200), (320, 190), (0, -250)]):
        st = t0 + 1.0 + i * 0.15
        if st < t0 + dur - 0.3:
            L.append(prop(f"{p}sp{i}", sparkle_icon(34 * sc, YELLOW), (cx + dx * sc, cy + dy * sc), st, t0 + dur - st, spin=160))
    return L
