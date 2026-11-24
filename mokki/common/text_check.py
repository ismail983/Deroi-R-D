"""Find on-screen text that overlaps other text at the same time (approximate Fredoka One metrics)."""
import json, sys

def boxes(layers, t_off=0.0, comp=""):
    out = []
    for l in layers:
        c = l.get("content", {})
        if c.get("kind") == "composition":
            out += boxes(c["layers"], t_off + l.get("start", 0), l["id"])
        elif c.get("kind") == "text" and not l["id"].endswith("_sh"):
            size = c["font"]["size"]; lines = c["text"].split("\n")
            lh = c.get("lineHeight", 1.2)
            w = max(len(x) for x in lines) * size * 0.56
            h = size * (1 + (len(lines) - 1) * lh)
            x, y = l["transform"]["position"]
            s = t_off + l.get("start", 0); e = s + l.get("duration", 1e9)
            out.append((l["id"], s, e, x - w / 2, y - h * 0.8, x + w / 2, y + h * 0.3, c["text"].replace("\n", " / ")))
    return out

def resolve(layers):
    """Shorten the earlier of two overlapping texts so it is gone before the next one appears."""
    by_id = {l["id"]: l for l in layers}
    for _ in range(5):
        B = boxes(layers)
        changed = False
        for i in range(len(B)):
            for j in range(len(B)):
                a, b = B[i], B[j]
                if i == j or not (a[1] < b[1] or (a[1] == b[1] and i < j)):
                    continue
                if a[1] < b[2] - 0.05 and b[1] < a[2] - 0.05 and a[3] < b[5] and b[3] < a[5] and a[4] < b[6] and b[4] < a[6]:
                    new = round(max(0.3, b[1] - a[1] - 0.08), 4)
                    for lid in (a[0], a[0] + "_sh"):
                        if lid in by_id:
                            by_id[lid]["duration"] = new
                    changed = True
        if not changed:
            return


def check(path):
    B = boxes(json.load(open(path))["layers"])
    bad = []
    for i in range(len(B)):
        for j in range(i + 1, len(B)):
            a, b = B[i], B[j]
            if a[1] < b[2] - 0.05 and b[1] < a[2] - 0.05 and a[3] < b[5] and b[3] < a[5] and a[4] < b[6] and b[4] < a[6]:
                bad.append((max(a[1], b[1]), a[7], b[7]))
    return B, bad

if __name__ == "__main__":
    B, bad = check(sys.argv[1])
    for t, x, y in sorted(bad):
        print(f"{t:7.2f}s  '{x}'  <->  '{y}'")
    print(len(B), "texts,", len(bad), "overlaps")
