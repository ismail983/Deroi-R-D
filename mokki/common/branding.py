"""Channel intro (6 s) and outro with Like & Subscribe (14 s), reused around every episode."""
import random
from kit import (NAVY, BODY, GREEN, CORAL, PINK, YELLOW, WHITE, YT_RED, YT_BLUE, POP, snap, rect, ell, group, pop_scale,
                 shape_layer, prop, text, audio, sparkle_icon, heart_icon, cloud_icon, thumb_icon, bell_icon, finger_icon,
                 mokki_rig, words_from_transcript, wipe)

# Picsart-hosted audio (expiring copies; masters live in ElevenLabs flow "Mokki & Friends – Channel intro & outro")
INTRO_JINGLE = "https://gcdn.picsart.com/picsart-mcp/b8057fc5-8457-47e6-978e-18c691e5bea0.mp3"   # 6.0 s, sung
OUTRO_MUSIC = "https://gcdn.picsart.com/picsart-mcp/c8d8c768-6ea7-4cd7-a2a3-80669be04f82.mp3"    # 14.0 s, instrumental
OUTRO_VOICE = "https://gcdn.picsart.com/picsart-mcp/2c73ed91-3bc4-487c-aa1d-388eafe0f862.mp3"    # 9.8 s, Mokki

INTRO_LEN, OUTRO_LEN = 6.0, 14.0

OUTRO_WORDS = [(0.08, 0.24, "Did"), (0.32, 0.4, "you"), (0.52, 0.64, "like"), (0.72, 1.08, "it"), (1.28, 2.0, "Yay"),
               (2.16, 2.68, "[giggles]"), (2.72, 2.96, "Ask"), (3.0, 3.04, "a"), (3.12, 3.44, "grown-up"), (3.52, 3.6, "to"),
               (3.68, 3.84, "tap"), (3.92, 4.0, "the"), (4.08, 4.32, "like"), (4.6, 4.92, "button"), (4.96, 5.12, "and"),
               (5.44, 6.0, "subscribe"), (6.24, 6.4, "Then"), (6.48, 6.56, "we"), (6.68, 6.8, "can"), (6.88, 6.96, "sing"),
               (7.04, 7.12, "and"), (7.2, 7.36, "play"), (7.44, 7.84, "together"), (7.92, 8.56, "again"),
               (8.64, 9.04, "Bye-bye"), (9.28, 9.84, "friends")]
SKY = "#7EC8F5"


def intro_layers():
    L = [shape_layer("in_sky", rect([960, 540], [1920, 1080], SKY), 0, INTRO_LEN, absolute=True)]
    # drifting clouds
    for i, (x, y, w, sp) in enumerate([(300, 180, 300, 25), (1500, 140, 360, -20), (1750, 900, 420, -15), (900, 980, 380, 18)]):
        L.append(shape_layer(f"in_cloud{i}", cloud_icon(w, "#EAF7FF" if i % 2 else WHITE), 0, INTRO_LEN, (x, y),
                             {"position": {"keyframes": [{"time": 0, "value": [x, y]}],
                                           "expression": f"return value+Vec.v2({sp}*time,0)"}}))
    # Mokki pops up from behind the big cloud, waving
    L += mokki_rig("in_mokki", [], [{"time": 0, "value": [380, 1250], "easing": POP}, {"time": 0.8, "value": [380, 860]}],
                   scale=0.55, rot_expr="return value+8*math.sin(2*math.pi*time/1.0)")
    L.append(shape_layer("in_bigcloud", cloud_icon(720, WHITE), 0, INTRO_LEN, (380, 900), {"scale": pop_scale(INTRO_LEN + 1)}))
    # title + subtitle
    L.append(text("in_title", "Mokki & Friends", (1270, 430), 150, 0.9, INTRO_LEN - 0.9, wobble=True))
    L.append(text("in_sub", "Songs and stories for little ones", (1270, 590), 58, 1.7, INTRO_LEN - 1.7, color=GREEN))
    random.seed(7)
    for i, (x, y) in enumerate([(760, 300), (1800, 300), (760, 640), (1800, 680), (1270, 230), (1270, 740)]):
        L.append(prop(f"in_spark{i}", sparkle_icon(34 + 6 * (i % 3)), (x, y), 1.0 + i * 0.15, INTRO_LEN - 1.0 - i * 0.15, spin=120))
    L.append(audio("in_jingle", 0, INTRO_JINGLE))
    return L


def outro_layers():
    VO = 0.8
    w = {t: s for s, e, t in reversed(OUTRO_WORDS)}           # first occurrence of each word
    like_t = VO + OUTRO_WORDS[12][0]                            # "like" (button)
    sub_t = VO + w["subscribe"]
    bye_t = VO + w["Bye-bye"]
    L = [shape_layer("out_bg", rect([960, 540], [1920, 1080], "#FFF1C1"), 0, OUTRO_LEN, absolute=True),
         shape_layer("out_circle", ell([0, 0], [900, 900], "#FFE48A"), 0, OUTRO_LEN, (500, 560),
                     {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.5, "value": [1, 1]}]}})]
    words = words_from_transcript(OUTRO_WORDS, VO)
    wave = f"local r=value+4*math.sin(2*math.pi*time/2.4); if time>{bye_t:.2f} then r=r+12*math.sin(time*10) end; return r"
    L += mokki_rig("out_mokki", words, [{"time": 0, "value": [500, 1250], "easing": POP}, {"time": 0.6, "value": [500, 900]}],
                   scale=0.6, rot_expr=wave,
                   scale_keys=[{"time": 0, "value": [0.6, 0.6]}, {"time": OUTRO_LEN - 0.6, "value": [0.6, 0.6], "easing": "ease_in"},
                               {"time": OUTRO_LEN, "value": [0, 0]}])
    L.append(text("out_yay", "Did you like it?", (1300, 170), 96, VO, w["Ask"] - 0.1, color=CORAL))
    for i, (x, y) in enumerate([(240, 330), (780, 300), (220, 760), (800, 760)]):
        L.append(prop(f"out_sp{i}", sparkle_icon(40), (x, y), VO + w["Yay"] + i * 0.1, 2.0, spin=150))

    # ---- LIKE button: grey -> blue when tapped
    lx, ly, sx, sy = 1300, 420, 1300, 650
    like_in = VO + w["like"]
    L.append(shape_layer("out_like_btn", [
        {"type": "rect", "position": [0, 0], "size": [520, 150], "roundness": 75},
        {"type": "fill", "color": {"keyframes": [{"time": 0, "value": "#F1F1F1", "easing": "step"},
                                                 {"time": like_t + 0.15 - like_in, "value": YT_BLUE}]}},
        {"type": "stroke", "color": "#D0D0D0", "width": 4}], like_in, OUTRO_LEN - like_in, (lx, ly),
        {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1, 1]},
                                 {"time": like_t + 0.05 - like_in, "value": [1, 1]}, {"time": like_t + 0.15 - like_in, "value": [0.9, 0.9], "easing": POP},
                                 {"time": like_t + 0.45 - like_in, "value": [1, 1]}]}}))
    L.append(shape_layer("out_like_thumb_g", thumb_icon(NAVY), like_in + 0.2, like_t + 0.15 - like_in - 0.2, (lx - 150, ly)))
    L.append(shape_layer("out_like_thumb_w", thumb_icon(WHITE), like_t + 0.15, OUTRO_LEN - like_t - 0.15, (lx - 150, ly),
                         {"scale": {"keyframes": [{"time": 0, "value": [1.5, 1.5], "easing": POP}, {"time": 0.4, "value": [1, 1]}]},
                          "rotation": {"keyframes": [{"time": 0, "value": -20, "easing": POP}, {"time": 0.4, "value": 0}]}}))
    L.append(text("out_like_txt", "LIKE", (lx + 60, ly + 25), 76, like_in + 0.2, like_t + 0.15 - like_in - 0.2, stroke=None, pop=False))
    L.append(text("out_liked_txt", "LIKE", (lx + 60, ly + 25), 76, like_t + 0.15, OUTRO_LEN - like_t - 0.15, color=WHITE, stroke=None, pop=False))
    for i, (dx, dy) in enumerate([(-200, -90), (-60, -120), (120, -100), (230, -40)]):
        L.append(prop(f"out_like_h{i}", heart_icon(26), (lx + dx, ly + dy), like_t + 0.2 + i * 0.08, 1.5,
                      extra={"position": {"keyframes": [{"time": 0, "value": [lx + dx, ly + dy]},
                                                        {"time": 1.5, "value": [lx + dx * 1.2, ly + dy - 160]}]}}))

    # ---- SUBSCRIBE button: red -> grey "SUBSCRIBED" + ringing bell
    sub_in = VO + w["grown-up"]
    L.append(shape_layer("out_sub_btn", [
        {"type": "rect", "position": [0, 0], "size": [560, 150], "roundness": 75},
        {"type": "fill", "color": {"keyframes": [{"time": 0, "value": YT_RED, "easing": "step"},
                                                 {"time": sub_t + 0.25 - sub_in, "value": "#E6E6E6"}]}}],
        sub_in, OUTRO_LEN - sub_in, (sx, sy),
        {"scale": {"keyframes": [{"time": 0, "value": [0, 0], "easing": POP}, {"time": 0.35, "value": [1, 1]},
                                 {"time": sub_t + 0.15 - sub_in, "value": [1, 1]}, {"time": sub_t + 0.25 - sub_in, "value": [0.9, 0.9], "easing": POP},
                                 {"time": sub_t + 0.55 - sub_in, "value": [1, 1]}]}}))
    L.append(text("out_sub_txt", "SUBSCRIBE", (sx, sy + 22), 66, sub_in + 0.2, sub_t + 0.25 - sub_in - 0.2, color=WHITE, stroke=None, pop=False))
    L.append(text("out_subd_txt", "SUBSCRIBED", (sx, sy + 22), 60, sub_t + 0.25, OUTRO_LEN - sub_t - 0.25, color="#606060", stroke=None, pop=False))
    L.append(shape_layer("out_bell", bell_icon(NAVY), sub_t + 0.45, OUTRO_LEN - sub_t - 0.45, (sx + 360, sy),
                         {"scale": pop_scale(OUTRO_LEN - sub_t - 0.45, 1.0),
                          "rotation": {"keyframes": [{"time": 0, "value": 0}],
                                       "expression": "if time<1.6 then return 25*math.sin(time*25)*(1-time/1.6) end; return 0"}}))

    # ---- tapping finger (tip is 90 px above the layer position)
    f0 = like_t - 0.7
    L.append(shape_layer("out_finger", finger_icon(), f0, sub_t + 1.3 - f0, (1900, 1250),
                         {"position": {"keyframes": [
                             {"time": 0, "value": [1900, 1250], "easing": "ease_out"},
                             {"time": like_t - f0, "value": [lx + 40, ly + 95], "easing": "ease_in_out"},
                             {"time": like_t + 0.5 - f0, "value": [lx + 40, ly + 95], "easing": "ease_in_out"},
                             {"time": sub_t - f0, "value": [sx + 40, sy + 95], "easing": "ease_in_out"},
                             {"time": sub_t + 0.6 - f0, "value": [sx + 40, sy + 95], "easing": "ease_in"},
                             {"time": sub_t + 1.3 - f0, "value": [1900, 1250]}]},
                          "scale": {"keyframes": [
                              {"time": 0, "value": [1, 1]}, {"time": like_t + 0.05 - f0, "value": [1, 1]},
                              {"time": like_t + 0.15 - f0, "value": [0.85, 0.85]}, {"time": like_t + 0.3 - f0, "value": [1, 1]},
                              {"time": sub_t + 0.15 - f0, "value": [1, 1]}, {"time": sub_t + 0.25 - f0, "value": [0.85, 0.85]},
                              {"time": sub_t + 0.4 - f0, "value": [1, 1]}]}}))
    L.append(text("out_ask", "Ask a grown-up!", (1300, 170), 84, VO + w["Ask"], bye_t - VO - w["Ask"] - 0.1, color=GREEN))
    L.append(text("out_bye", "Bye-bye, friends!\nSee you next time!", (1300, 170), 84, bye_t - 0.1, OUTRO_LEN - bye_t + 0.1, color=CORAL))
    L.append(audio("out_music", 0, OUTRO_MUSIC))
    L.append(audio("out_voice", VO, OUTRO_VOICE))
    return L


def comp_layer(id_, layers, start, dur):
    return {"id": id_, "start": snap(start), "duration": snap(dur), "timeMode": "layer",
            "content": {"kind": "composition", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": snap(dur)},
                        "layers": layers}}


def wrap_episode(ep_layers, ep_dur):
    """Full video = intro + episode + outro, each as its own nested composition, with wipes between."""
    t_ep, t_out = INTRO_LEN, INTRO_LEN + ep_dur
    total = snap(t_out + OUTRO_LEN)
    root = [comp_layer("intro", intro_layers(), 0, INTRO_LEN),
            comp_layer("episode", ep_layers, t_ep, ep_dur),
            comp_layer("outro", outro_layers(), t_out, OUTRO_LEN),
            wipe("wipe_in", t_ep - 0.4), wipe("wipe_out", t_out - 0.4)]
    return {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": total, "background": "#FFF1C1"},
            "layers": root}


def standalone(which):
    """Intro or outro alone (for previewing)."""
    layers, dur = (intro_layers(), INTRO_LEN) if which == "intro" else (outro_layers(), OUTRO_LEN)
    return {"version": "1.0", "composition": {"width": 1920, "height": 1080, "fps": 30, "duration": dur}, "layers": layers}


if __name__ == "__main__":
    import json, sys, os
    out = os.path.dirname(os.path.abspath(__file__))
    for w_ in ("intro", "outro"):
        json.dump(standalone(w_), open(os.path.join(out, f"{w_}-scene.json"), "w"), separators=(",", ":"))
    print("ok")
