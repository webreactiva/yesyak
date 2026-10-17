#!/usr/bin/env python3
"""Model prices from models.dev, the ban list, and a price cap for the puppet agent.

models.py list [--max-output N]   models that OpenCode offers, cheapest first, banned ones left out
models.py check <provider/model>  exit 1 if banned or over the cap (YAKBENCH_MAX_OUTPUT, default 5 $/M output)
models.py cost <provider/model> <input> <output> <cache_read> <cache_write>   equivalent cost in $
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BANNED = re.compile(r"kimi[-_. ]?k[-_. ]?3|astra", re.I)
YESYAK = Path(__file__).resolve().parents[4]
BENCH = Path(os.environ.get("YAKBENCH_DIR", YESYAK / ".scratchpad" / "bench"))
CACHE = BENCH / "models-dev.json"
MAX_OUTPUT = float(os.environ.get("YAKBENCH_MAX_OUTPUT", "5"))


def catalog():
    if not CACHE.exists() or time.time() - CACHE.stat().st_mtime > 86400:
        BENCH.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request("https://models.dev/api.json", headers={"User-Agent": "yak-bench"})  # the default urllib agent gets 403
        with urllib.request.urlopen(request, timeout=30) as r:
            CACHE.write_bytes(r.read())
    return json.loads(CACHE.read_text())


def price(model_id, data):
    """Price of provider/model; a reseller without prices falls back to the same model id elsewhere."""
    provider, _, name = model_id.partition("/")
    name = name.split("#")[0]
    found = data.get(provider, {}).get("models", {}).get(name, {}).get("cost")
    if found:
        return found, provider
    for other, entry in data.items():
        cost = entry.get("models", {}).get(name, {}).get("cost")
        if cost:
            return cost, other
    return None, None


def check(model_id, data):
    if BANNED.search(model_id):
        return f"banned model: {model_id}"
    cost, _ = price(model_id, data)
    if cost is None:
        return None
    if cost.get("output", 0) > MAX_OUTPUT and os.environ.get("YAKBENCH_ALLOW_EXPENSIVE") != "1":
        return f"too expensive: {model_id} costs {cost['output']} $/M output (cap {MAX_OUTPUT}; set YAKBENCH_ALLOW_EXPENSIVE=1 only when the user asks)"
    return None


def cost_of(model_id, tokens, data):
    cost, _ = price(model_id, data)
    if not cost:
        return None
    keys = ("input", "output", "cache_read", "cache_write")
    return sum(tokens.get(k, 0) * cost.get(k, 0) for k in keys) / 1e6


def main():
    data = catalog()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "check":
        problem = check(sys.argv[2], data)
        if problem:
            sys.exit(problem)
        cost, source = price(sys.argv[2], data)
        print(f"ok: {sys.argv[2]} " + (f"{cost.get('input')}/{cost.get('output')} $/M ({source})" if cost else "price unknown on models.dev"), file=sys.stderr)
    elif cmd == "cost":
        tokens = dict(zip(("input", "output", "cache_read", "cache_write"), map(int, sys.argv[3:7])))
        value = cost_of(sys.argv[2], tokens, data)
        print("unknown" if value is None else f"{value:.4f}")
    elif cmd == "list":
        cap = float(sys.argv[sys.argv.index("--max-output") + 1]) if "--max-output" in sys.argv else MAX_OUTPUT
        offered = subprocess.run(["opencode", "models"], capture_output=True, text=True).stdout.split()
        rows = []
        for model_id in offered:
            if BANNED.search(model_id):
                continue
            cost, source = price(model_id, data)
            if cost and cost.get("output", 0) <= cap:
                rows.append((cost.get("output", 0), cost.get("input", 0), model_id, source))
        for out, inp, model_id, source in sorted(rows):
            print(f"{inp:>7} {out:>7}  {model_id}  ({source})")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
