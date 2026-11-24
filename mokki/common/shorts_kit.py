"""Shared pieces for vertical YouTube Shorts (1080x1920)."""
import kit
from kit import (NAVY, WHITE, YELLOW, CORAL, GREEN, PINK, YT_RED, YT_BLUE, POP, snap, rect, ell, group, shape_layer, prop,
                 sparkle_icon, bell_icon, heart_icon, cloud_icon, thumb_icon, finger_icon, pop_scale)

W, H = 1080, 1920
SKY = "#7EC8F5"
JINGLE = "https://gcdn.picsart.com/picsart-mcp/b8057fc5-8457-47e6-978e-18c691e5bea0.mp3"     # 6 s sung "Mokki and Friends!"
MUSIC_BED = "https://gcdn.picsart.com/picsart-mcp/c8d8c768-6ea7-4cd7-a2a3-80669be04f82.mp3"  # 14 s instrumental
STING_LEN = 2.5
KID_COLORS = ["#F0506E", "#2BB673", "#4A90E2", "#FF8A00", "#9B59D0", "#00B5AD", "#E84393"]


def sky_bg(L, start, dur, clouds=True):
    L.append(shape_layer("sky", rect([540, 960], [W, H], SKY), start, dur, absolute=True))
    if clouds:
        for i, (x, y, w, sp) in enumerate([(200, 260, 300, 18), (880, 160, 340, -15), (900, 1150, 360, -12), (160, 1280, 320, 14)]):
            L.append(shape_layer(f"cloud{i}", cloud_icon(w, "#EAF7FF" if i % 2 else WHITE), start, dur, (x, y),
                                 {"position": {"keyframes": [{"time": 0, "value": [x, y]}],
                                               "expression": f"return value+Vec.v2({sp}*time,0)"}}))


def sting(L, t0=0.0):
    """2.5 s channel sting: sky, logo pops, sparkles, first notes of the jingle. Returns the end time."""
    d = STING_LEN
    sky_bg(L, t0, d)
    L += kit.kid_text("st_logo", "Mokki\n& Friends", (540, 820), 170, t0 + 0.1, d - 0.1, color=NAVY, wobble=True)
    for i, (x, y) in enumerate([(220, 560), (860, 560), (200, 1080), (880, 1080), (540, 470)]):
        L.append(prop(f"st_sp{i}", sparkle_icon(50, YELLOW), (x, y), t0 + 0.2 + i * 0.08, d - 0.2 - i * 0.08, spin=200))
    L.append(audio_trim("st_jingle", t0, JINGLE, 0.0, d))
    return t0 + d


def audio_trim(id_, start, uri, t_in, t_out, volume=None):
    c = {"kind": "audio", "asset": {"type": "audio", "uri": uri}, "trim": {"in": t_in, "out": t_out}}
    if volume is not None:
        c["volume"] = volume
    return {"id": id_, "start": snap(start), "duration": snap(t_out - t_in), "content": c}


def end_card(L, t0, dur, line="More songs\nwith Mokki!"):
    L += kit.kid_text("end_txt", line, (540, 430), 110, t0, dur, color=CORAL)
    L.append(shape_layer("end_sub", [{"type": "rect", "position": [0, 0], "size": [640, 170], "roundness": 85},
                                     {"type": "fill", "color": YT_RED}], t0 + 0.3, dur - 0.3, (500, 830),
                         {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1, 1]}],
                                    "expression": "return value*(1+0.05*math.sin(time*8))"}}))
    L += kit.kid_text("end_subtxt", "SUBSCRIBE", (500, 860), 80, t0 + 0.4, dur - 0.4, color=WHITE, stroke=None, letters=False)
    L.append(shape_layer("end_bell", bell_icon(NAVY), t0 + 0.6, dur - 0.6, (900, 830),
                         {"scale": pop_scale(dur - 0.6, 1.3),
                          "rotation": {"keyframes": [{"time": 0, "value": 0}],
                                       "expression": "return 25*math.sin(time*20)*math.max(0,1-time/2)"}}))


def letter_block(ch, color):
    """A toy block with a big letter/number drawn as a shape-free text-friendly square (text goes on top)."""
    return [group(rect([0, 0], [170, 170], color, 34) + [{"type": "stroke", "color": WHITE, "width": 10}])]


def like_subscribe(L, t_like, t_sub, t_in, t_out, lx=540, ly=760, sy=980):
    """LIKE (grey->blue) and SUBSCRIBE (red->grey 'SUBSCRIBED' + bell) with a tapping finger."""
    dur = t_out - t_in
    L.append(shape_layer("ls_like", [{"type": "rect", "position": [0, 0], "size": [560, 160], "roundness": 80},
                                     {"type": "fill", "color": {"keyframes": [{"time": 0, "value": "#F1F1F1", "easing": "step"},
                                                                             {"time": t_like + 0.15 - t_in, "value": YT_BLUE}]}},
                                     {"type": "stroke", "color": "#D0D0D0", "width": 4}], t_in, dur, (lx, ly),
                         {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1, 1]},
                                                  {"time": t_like + 0.05 - t_in, "value": [1, 1]},
                                                  {"time": t_like + 0.15 - t_in, "value": [0.9, 0.9], "easing": POP},
                                                  {"time": t_like + 0.45 - t_in, "value": [1, 1]}]}}))
    L.append(shape_layer("ls_thumb_g", thumb_icon(NAVY), t_in + 0.2, t_like + 0.15 - t_in - 0.2, (lx - 160, ly)))
    L.append(shape_layer("ls_thumb_w", thumb_icon(WHITE), t_like + 0.15, t_out - t_like - 0.15, (lx - 160, ly),
                         {"scale": {"keyframes": [{"time": 0, "value": [1.5, 1.5], "easing": POP}, {"time": 0.4, "value": [1, 1]}]}}))
    L += kit.kid_text("ls_liketxt", "LIKE", (lx + 60, ly + 26), 80, t_in + 0.2, t_like + 0.15 - t_in - 0.2, color=NAVY, stroke=None, letters=False, pop=False)
    L += kit.kid_text("ls_likedtxt", "LIKE", (lx + 60, ly + 26), 80, t_like + 0.15, t_out - t_like - 0.15, color=WHITE, stroke=None, letters=False, pop=False)
    for i, (dx, dy) in enumerate([(-200, -100), (-40, -130), (140, -110), (240, -50)]):
        L.append(prop(f"ls_h{i}", heart_icon(28), (lx + dx, ly + dy), t_like + 0.2 + i * 0.08, 1.5,
                      extra={"position": {"keyframes": [{"time": 0, "value": [lx + dx, ly + dy]},
                                                        {"time": 1.5, "value": [lx + dx * 1.2, ly + dy - 180]}]}}))
    L.append(shape_layer("ls_sub", [{"type": "rect", "position": [0, 0], "size": [600, 160], "roundness": 80},
                                    {"type": "fill", "color": {"keyframes": [{"time": 0, "value": YT_RED, "easing": "step"},
                                                                            {"time": t_sub + 0.2 - t_in, "value": "#E6E6E6"}]}}],
                         t_in + 0.3, dur - 0.3, (lx, sy),
                         {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1, 1]},
                                                  {"time": t_sub + 0.1 - t_in - 0.3, "value": [1, 1]},
                                                  {"time": t_sub + 0.2 - t_in - 0.3, "value": [0.9, 0.9], "easing": POP},
                                                  {"time": t_sub + 0.5 - t_in - 0.3, "value": [1, 1]}]}}))
    L += kit.kid_text("ls_subtxt", "SUBSCRIBE", (lx, sy + 24), 72, t_in + 0.5, t_sub + 0.2 - t_in - 0.5, color=WHITE, stroke=None, letters=False, pop=False)
    L += kit.kid_text("ls_subdtxt", "SUBSCRIBED", (lx, sy + 24), 64, t_sub + 0.2, t_out - t_sub - 0.2, color="#606060", stroke=None, letters=False, pop=False)
    L.append(shape_layer("ls_bell", bell_icon(NAVY), t_sub + 0.4, t_out - t_sub - 0.4, (lx + 380, sy),
                         {"scale": pop_scale(t_out - t_sub - 0.4, 1.2),
                          "rotation": {"keyframes": [{"time": 0, "value": 0}],
                                       "expression": "if time<1.6 then return 25*math.sin(time*25)*(1-time/1.6) end; return 0"}}))
    f0 = t_like - 0.6
    L.append(shape_layer("ls_finger", finger_icon(), f0, t_sub + 1.2 - f0, (1150, 2050),
                         {"position": {"keyframes": [
                             {"time": 0, "value": [1150, 2050], "easing": "ease_out"},
                             {"time": t_like - f0, "value": [lx + 40, ly + 95], "easing": "ease_in_out"},
                             {"time": t_like + 0.25 - f0, "value": [lx + 40, ly + 95], "easing": "ease_in_out"},
                             {"time": t_sub - f0, "value": [lx + 40, sy + 95], "easing": "ease_in_out"},
                             {"time": t_sub + 0.5 - f0, "value": [lx + 40, sy + 95], "easing": "ease_in"},
                             {"time": t_sub + 1.2 - f0, "value": [1150, 2050]}]},
                          "scale": {"keyframes": [
                              {"time": 0, "value": [1, 1]}, {"time": t_like + 0.05 - f0, "value": [1, 1]},
                              {"time": t_like + 0.15 - f0, "value": [0.85, 0.85]}, {"time": t_like + 0.3 - f0, "value": [1, 1]},
                              {"time": t_sub + 0.1 - f0, "value": [1, 1]}, {"time": t_sub + 0.2 - f0, "value": [0.85, 0.85]},
                              {"time": t_sub + 0.35 - f0, "value": [1, 1]}]}}))


def finish(L, end, path):
    import json, text_check
    for l in L:
        for k in ("start", "duration"):
            if k in l:
                l[k] = snap(l[k])
    text_check.resolve(L)
    scene = {"version": "1.0", "composition": {"width": W, "height": H, "fps": 30, "duration": snap(end), "background": SKY}, "layers": L}
    json.dump(scene, open(path, "w"), separators=(",", ":"))
    return scene
