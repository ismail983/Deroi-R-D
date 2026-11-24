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


def mokki_rig(id_, words, pos_keys, scale=0.5, closed=(), pos_expr=None, rot_expr=None, scale_expr=None, scale_keys=None):
    """Mokki picture + lip-synced mouth + blinking eyelids. Children are parented to the picture."""
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
              "transform": {"anchor": [960, 1080], "position": pos_keys[0]["value"], "scale": [scale, scale]}, "animations": anim})
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
