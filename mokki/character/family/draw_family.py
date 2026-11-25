"""Draws Mokki's family in Mokki's exact style (scalloped body, thick outline, curly antenna, round eyes, pink cheeks).

Outputs, per character: <id>.png (full), <id>-nomouth.png (for lip-sync), and family.json (face positions for the rig).
All characters share one pixel scale (BASE = Mokki's body radius), so their relative sizes are true.
"""
import json, math, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 2                                   # supersampling
NAVY, WHITE, CHEEK = (20, 34, 79), (255, 255, 255), (255, 159, 178)
BASE = 520                               # Mokki's body radius in px (matches the official picture)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


FAMILY = [
    # id, name, size, body, outline, accent, eyes(left r, right r), n bumps, extras
    dict(id="papa", name="Papa Moko", size=1.22, body="#8CCBFA", line="#2A6FB0", bead="#FFD23F", eyes=(0.27, 0.27), bumps=14,
         extras=["mustache", "brows"]),
    dict(id="mama", name="Mama Mimi", size=1.12, body="#FFB8CF", line="#D65A86", bead="#FF6B9A", eyes=(0.27, 0.27), bumps=13,
         extras=["flower", "lashes"]),
    dict(id="pia", name="Pia (little sister)", size=0.82, body="#D5BDF7", line="#7B55C7", bead="#FF6B9A", eyes=(0.33, 0.33), bumps=11,
         extras=["bow", "lashes"]),
    dict(id="pip", name="Pip (baby brother)", size=0.66, body="#FFE58A", line="#D19A12", bead="#4A90E2", eyes=(0.36, 0.36), bumps=10,
         extras=["sprout", "pacifier"]),
    dict(id="grandpa", name="Grandpa Moss", size=1.12, body="#FFC99A", line="#C9733A", bead="#B0B7BF", eyes=(0.22, 0.22), bumps=13,
         extras=["glasses", "white_brows", "white_mustache", "droopy"]),
    dict(id="grandma", name="Granny Mo", size=1.06, body="#F9CFC3", line="#B9705E", bead="#C9A2E8", eyes=(0.22, 0.22), bumps=12,
         extras=["glasses", "bun", "pearls", "lashes"]),
]


def draw_char(c, mouth=True):
    R = BASE * c["size"] * SS
    t = 0.065 * BASE * SS                                     # outline thickness (same for everyone, like a real line)
    W = int(R * 2.6); H = int(R * 3.0)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H - R * 1.12
    body, line = hexc(c["body"]), hexc(c["line"])
    n = c["bumps"]
    ring, bump = 0.80 * R, 0.25 * R * 12 / n + 0.03 * R

    def blob(col, grow):
        d.ellipse([cx - ring - grow, cy - ring * 0.97 - grow, cx + ring + grow, cy + ring * 0.97 + grow], fill=col)
        for i in range(n):
            a = 2 * math.pi * i / n - math.pi / 2
            x, y = cx + ring * math.cos(a), cy + ring * 0.97 * math.sin(a)
            r = bump + grow
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    # ---- antenna (behind body) : curly stalk + bead, or accessory
    top = cy - ring * 0.97 - bump
    lw = int(t * 1.1)
    if "sprout" in c["extras"]:
        d.line([(cx, top + bump * 0.6), (cx, top - 0.18 * R)], fill=line, width=lw)
        for sx in (-1, 1):
            lx, ly = cx + sx * 0.12 * R, top - 0.2 * R
            d.ellipse([lx - 0.11 * R, ly - 0.06 * R, lx + 0.11 * R, ly + 0.06 * R], fill=hexc("#7BC043"), outline=line, width=int(t * 0.6))
    else:
        droop = "droopy" in c["extras"]
        sx = -1 if droop else 1
        lw = int(t * 1.5)
        # Mokki-style antenna: a thick stalk curving up and over, ending in a loop that hugs a round bead
        loop_r = 0.13 * R
        lx, ly = cx + sx * 0.22 * R, top - 0.30 * R            # loop centre
        stalk = []
        for k in range(41):
            u = k / 40
            x = cx + sx * 0.02 * R + (lx - sx * loop_r - cx) * (u ** 1.6)
            y = top + bump * 0.7 + (ly - (top + bump * 0.7)) * math.sin(u * math.pi / 2)
            stalk.append((x, y))
        d.line(stalk, fill=line, width=lw, joint="curve")
        d.ellipse([lx - loop_r - lw / 2, ly - loop_r - lw / 2, lx + loop_r + lw / 2, ly + loop_r + lw / 2], outline=line, width=lw)
        br = 0.085 * R
        bx, by = lx - sx * 0.03 * R, ly + 0.03 * R
        d.ellipse([bx - br - t * 0.7, by - br - t * 0.7, bx + br + t * 0.7, by + br + t * 0.7], fill=line)
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=hexc(c["bead"]))

    blob(line, t)
    blob(body, 0)

    # ---- hair / hats that sit on the head
    if "bun" in c["extras"]:
        for (dx, dy, r) in [(-0.16, -0.02, 0.15), (0.16, -0.02, 0.15), (0, -0.1, 0.17)]:
            x, y, rr = cx + dx * R, top + dy * R, r * R
            d.ellipse([x - rr - t * 0.5, y - rr - t * 0.5, x + rr + t * 0.5, y + rr + t * 0.5], fill=hexc("#B9BEC8"))
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=hexc("#F4F5F8"))

    # ---- eyes (Mokki: big left, small right; family: own sizes)
    face = {}
    ey0 = cy - 0.08 * R
    for side, (dx, rr) in (("L", (-0.29, c["eyes"][0])), ("R", (0.29, c["eyes"][1]))):
        if c["id"] == "mokki":
            pass
        x, r = cx + dx * R, rr * R
        ring_w = 0.045 * BASE * SS
        d.ellipse([x - r, ey0 - r, x + r, ey0 + r], fill=NAVY)
        d.ellipse([x - r + ring_w, ey0 - r + ring_w, x + r - ring_w, ey0 + r - ring_w], fill=WHITE)
        pr = r * 0.52
        px, py = x + r * 0.06, ey0 + r * 0.06
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=NAVY)
        sr = pr * 0.38
        d.ellipse([px - pr * 0.45 - sr, py - pr * 0.45 - sr, px - pr * 0.45 + sr, py - pr * 0.45 + sr], fill=WHITE)
        face["eye" + side] = [x / SS, ey0 / SS, 2 * r / SS]
        if "lashes" in c["extras"]:
            for k in (-1, 0, 1):
                a = -math.pi / 2 + k * 0.45 + (0.5 if side == "R" else -0.5)
                x1, y1 = x + r * math.cos(a), ey0 + r * math.sin(a)
                x2, y2 = x + (r + 0.07 * R) * math.cos(a), ey0 + (r + 0.07 * R) * math.sin(a)
                d.line([(x1, y1), (x2, y2)], fill=NAVY, width=int(t * 0.7))
        if "brows" in c["extras"] or "white_brows" in c["extras"]:
            col = WHITE if "white_brows" in c["extras"] else NAVY
            bw = r * 1.1
            d.rounded_rectangle([x - bw, ey0 - r - 0.13 * R, x + bw, ey0 - r - 0.05 * R], radius=int(0.04 * R), fill=col,
                                outline=hexc(c["line"]) if col == WHITE else None, width=int(t * 0.4))
        if "glasses" in c["extras"]:
            gr = r * 1.28
            d.ellipse([x - gr, ey0 - gr, x + gr, ey0 + gr], outline=hexc("#8A5A3C"), width=int(t * 0.9))
    if "glasses" in c["extras"]:
        d.line([(cx - 0.29 * R + c["eyes"][0] * R * 1.28, ey0), (cx + 0.29 * R - c["eyes"][1] * R * 1.28, ey0)], fill=hexc("#8A5A3C"), width=int(t * 0.9))

    # ---- cheeks
    for sx in (-1, 1):
        x, y = cx + sx * 0.56 * R, cy + 0.22 * R
        d.ellipse([x - 0.14 * R, y - 0.08 * R, x + 0.14 * R, y + 0.08 * R], fill=CHEEK)

    # ---- mouth (smile)
    my = cy + 0.30 * R
    mw = 0.26 * R
    face["mouth"] = [cx / SS, my / SS, 2 * mw / SS]
    if mouth:
        d.arc([cx - mw, my - mw * 0.75, cx + mw, my + mw * 0.55], 20, 160, fill=NAVY, width=int(0.045 * BASE * SS))
    # ---- mustache (over the mouth area, above it)
    for key, col in (("mustache", NAVY), ("white_mustache", WHITE)):
        if key in c["extras"]:
            for sx in (-1, 1):
                x = cx + sx * 0.13 * R
                d.ellipse([x - 0.16 * R, my - 0.2 * R, x + 0.16 * R, my - 0.04 * R], fill=col,
                          outline=hexc(c["line"]) if col == WHITE else None, width=int(t * 0.4))
    if "pacifier" in c["extras"] and mouth:
        d.ellipse([cx - 0.16 * R, my - 0.02 * R, cx + 0.16 * R, my + 0.16 * R], fill=hexc("#FFB3CC"), outline=hexc("#E86A8A"), width=int(t * 0.5))
        d.ellipse([cx - 0.05 * R, my + 0.03 * R, cx + 0.05 * R, my + 0.11 * R], fill=hexc("#FFE58A"))
    # ---- accessories on the antenna / body
    if "flower" in c["extras"]:
        fx, fy = cx - 0.42 * R, top + 0.12 * R
        for k in range(5):
            a = 2 * math.pi * k / 5
            px, py = fx + 0.09 * R * math.cos(a), fy + 0.09 * R * math.sin(a)
            d.ellipse([px - 0.075 * R, py - 0.075 * R, px + 0.075 * R, py + 0.075 * R], fill=hexc("#FFFFFF"), outline=hexc("#D65A86"), width=int(t * 0.35))
        d.ellipse([fx - 0.05 * R, fy - 0.05 * R, fx + 0.05 * R, fy + 0.05 * R], fill=hexc("#FFD23F"))
    if "bow" in c["extras"]:
        bx, by = cx - 0.36 * R, top + 0.14 * R
        for sx in (-1, 1):
            d.polygon([(bx, by), (bx + sx * 0.2 * R, by - 0.12 * R), (bx + sx * 0.2 * R, by + 0.12 * R)], fill=hexc("#FF6B9A"))
        d.ellipse([bx - 0.05 * R, by - 0.05 * R, bx + 0.05 * R, by + 0.05 * R], fill=hexc("#E84393"))
    if "pearls" in c["extras"]:
        for k in range(9):
            a = math.pi * (0.25 + 0.5 * k / 8)
            px, py = cx + 0.5 * R * math.cos(a), cy + 0.36 * R + 0.25 * R * math.sin(a)
            d.ellipse([px - 0.045 * R, py - 0.045 * R, px + 0.045 * R, py + 0.045 * R], fill=WHITE, outline=hexc("#B9BEC8"), width=2)

    img = img.resize((W // SS, H // SS), Image.LANCZOS)
    bbox = img.getbbox()
    img = img.crop(bbox)
    for k, v in face.items():
        v[0] -= bbox[0]; v[1] -= bbox[1]
    return img, {k: [round(x, 1) for x in v] for k, v in face.items()}


if __name__ == "__main__":
    meta = {}
    imgs = []
    for c in FAMILY:
        full, face = draw_char(c, mouth=True)
        nom, _ = draw_char(c, mouth=False)
        full.save(os.path.join(HERE, f"{c['id']}.png"))
        nom.save(os.path.join(HERE, f"{c['id']}-nomouth.png"))
        meta[c["id"]] = {"name": c["name"], "size": c["size"], "w": full.width, "h": full.height, "face": face,
                         "body": c["body"], "outline": c["line"]}
        imgs.append((c, full))
    json.dump(meta, open(os.path.join(HERE, "family.json"), "w"), indent=1)
    # lineup with Mokki in the middle
    mok = Image.open(os.path.join(HERE, "..", "mokki-cutout.png")).convert("RGBA")
    order = ["grandpa", "grandma", "papa", "MOKKI", "pia", "pip", "mama"]
    order = ["grandpa", "papa", "pia", "MOKKI", "pip", "mama", "grandma"]
    pics = [mok if o == "MOKKI" else dict((c["id"], im) for c, im in imgs)[o] for o in order]
    gap = 40
    Wt = sum(p.width for p in pics) + gap * (len(pics) + 1)
    Ht = max(p.height for p in pics) + 2 * gap
    sheet = Image.new("RGBA", (Wt, Ht), (255, 241, 193, 255))
    x = gap
    for p in pics:
        sheet.alpha_composite(p, (x, Ht - gap - p.height))
        x += p.width + gap
    sheet.convert("RGB").save(os.path.join(HERE, "family-lineup.png"))
    sheet.convert("RGB").resize((Wt // 4, Ht // 4)).save(os.path.join(HERE, "family-lineup-small.png"))
    print("ok", Wt, Ht)
