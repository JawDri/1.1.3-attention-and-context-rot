"""Lesson 1.1.3 (optional experiment) - Hide one fact at the start, middle and end of a long prompt.

Needs an Anthropic API key. Uses Claude Haiku 5.5: the default run sends about 3 x 30,000 input
tokens, roughly $0.01 in total. --dry-run shows the prompt size and sends nothing.

  .\\run.ps1 lost_in_the_middle_test.py --dry-run
  .\\run.ps1 lost_in_the_middle_test.py                      3 runs: fact at 5%, 50%, 95%
  .\\run.ps1 lost_in_the_middle_test.py --tokens 60000 --distractors 40   make it harder

Honest note: new models find ONE clear fact very well, so all three may pass. Context rot shows up
on harder work: many look-alike facts (--distractors), messy text, reasoning across several facts.
"""
import argparse
import json
import random
import sys
import time

sys.dont_write_bytecode = True
from course_env import load_prices, require_anthropic_key  # noqa: E402

MODEL = "claude-haiku-5-5"
NEEDLE = "The refund approval code for the Lyon warehouse is FALCON-7731."
ANSWER = "FALCON-7731"
QUESTION = "What is the refund approval code for the Lyon warehouse? Reply with the code only."

TOPICS = ["shipping", "returns", "invoicing", "onboarding", "security", "holidays", "support hours",
          "data retention", "vendor payments", "travel expenses"]
SENTENCES = [
    "Requests about {t} are reviewed by the operations team within two business days.",
    "The {t} policy was last updated after the annual audit and applies to all regions.",
    "Managers must log every exception to the {t} rules in the shared tracker.",
    "Customers asking about {t} should receive the standard template reply first.",
    "For {t}, escalate to a team lead only when the amount or risk is unusual.",
    "Training on {t} is mandatory for new hires during their first month.",
]
CITIES = ["Paris", "Berlin", "Madrid", "Milan", "Porto", "Ghent", "Leeds", "Turin", "Seville", "Lille",
          "Munich", "Nantes", "Bilbao", "Bremen", "Genoa", "Lisbon", "Bristol", "Tunis", "Oslo", "Riga"]


def haystack(tokens, depth, distractors, seed=1):
    """Filler paragraphs (~4 characters per token) with the needle at `depth` (0.0 to 1.0)."""
    rng = random.Random(seed)
    lines = []
    while sum(len(x) for x in lines) < tokens * 4:
        lines.append(rng.choice(SENTENCES).format(t=rng.choice(TOPICS)))
    for i in range(distractors):  # look-alike facts for other warehouses
        code = f"{rng.choice(['HAWK', 'HERON', 'EAGLE', 'OWL', 'FALCON'])}-{rng.randint(1000, 9999)}"
        city = CITIES[i % len(CITIES)] + ("" if i < len(CITIES) else f" {i // len(CITIES) + 1}")
        lines.insert(rng.randrange(len(lines)), f"The refund approval code for the {city} warehouse is {code}.")
    lines.insert(round(depth * len(lines)), NEEDLE)
    return " ".join(lines)


def request(doc):
    return {"model": MODEL, "max_tokens": 2000, "output_config": {"effort": "low"},
            "system": "Answer questions using only the document in the user message.",
            "messages": [{"role": "user", "content": f"<document>\n{doc}\n</document>\n\n{QUESTION}"}]}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tokens", type=int, default=30000, help="approximate prompt size")
    p.add_argument("--distractors", type=int, default=0, help="look-alike codes for other warehouses")
    p.add_argument("--depths", default="0.05,0.5,0.95", help="where to hide the fact (0 = top, 1 = bottom)")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    depths = [float(d) for d in a.depths.split(",")]

    if a.dry_run:
        doc = haystack(a.tokens, depths[0], a.distractors)
        body = request(doc[:200] + f" ... [{len(doc):,} characters in total] ...")
        print(f"{len(depths)} requests like this one, each about {len(doc) // 4:,} tokens:")
        print(json.dumps(body, indent=2))
        return

    require_anthropic_key()
    import anthropic
    client = anthropic.Anthropic()
    price = load_prices()["models"]["haiku"]
    total_cost = 0.0
    print(f"{'fact at':>8}  {'answer':<16} {'result':<7} {'in tokens':>10}  seconds")
    for depth in depths:
        doc = haystack(a.tokens, depth, a.distractors)
        started = time.time()
        r = client.messages.create(**request(doc))
        text = "".join(b.text for b in r.content if b.type == "text").strip()
        ok = ANSWER in text
        cost = (r.usage.input_tokens * price["input"] + r.usage.output_tokens * price["output"]) / 1e6
        total_cost += cost
        print(f"{depth:>8.0%}  {text[:16]:<16} {'PASS' if ok else 'MISS':<7} {r.usage.input_tokens:>10,}"
              f"  {time.time() - started:5.1f}")
    print(f"\nTotal cost about ${total_cost:.4f}. Try --distractors 40 --tokens 60000 to make it harder (stay under 100,000 tokens: Haiku costs more above that).")


if __name__ == "__main__":
    main()
