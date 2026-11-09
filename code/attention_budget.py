"""Lesson 1.1.3 - The attention budget: why one rule gets "thinner" as the prompt grows.

Free, offline, no packages. A toy model of ONE attention head: real models have dozens of heads
and layers, so treat this as the intuition, not a measurement of any real model.

  .\\run.ps1 attention_budget.py
"""
import math
import random
import sys

sys.dont_write_bytecode = True
import course_env  # noqa: E402,F401  (sets UTF-8 output)


def softmax(scores):
    top = max(scores)
    exps = [math.exp(s - top) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def main():
    # 1) Softmax turns raw scores into weights that always add up to exactly 1.0 (100%).
    words = ["Never", "refund", "over", "$50"]
    weights = softmax([2.0, 3.0, 1.0, 2.5])
    print("1) SOFTMAX: one token spreads its attention over the others")
    for word, w in zip(words, weights):
        print(f"   {word:<7} {w:6.1%}  {'#' * round(w * 50)}")
    print(f"   total   {sum(weights):6.1%}   <- always exactly 100%: a fixed budget\n")

    # 2) The same rule, buried in more and more filler. The rule always gets the same high score;
    #    each filler token gets a small random score. Only the amount of filler changes.
    rng = random.Random(7)
    rule_score = 6.0
    print("2) THE SAME RULE IN A BIGGER PROMPT (one head, toy numbers)")
    print("   prompt size      attention on the rule")
    for n in (500, 5_000, 80_000, 500_000):
        filler = [rng.gauss(0, 1) for _ in range(n)]
        share = softmax([rule_score] + filler)[0]
        print(f"   {n:>8,} tokens   {share:7.2%}  {'#' * max(1, round(share * 100))}")
    print("\n   Same rule, same score: it just gets a thinner slice of the same 100%."
          "\n   That is attention dilution. Send the minimum context each step needs.")


if __name__ == "__main__":
    main()
