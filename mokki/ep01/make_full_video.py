"""Episode 1 with the channel intro and outro: writes ep01-full-scene.json."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from branding import wrap_episode

ep = json.load(open(os.path.join(HERE, "ep01-scene.json")))
full = wrap_episode(ep["layers"], ep["composition"]["duration"])
json.dump(full, open(os.path.join(HERE, "ep01-full-scene.json"), "w"), separators=(",", ":"))
print("total", full["composition"]["duration"], "s")
