from __future__ import annotations

import argparse
import random
import textwrap
from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    prompt: str
    answer: str
    tags: tuple[str, ...]


CARDS = [
    Card(
        prompt="Why is correlation between feature usage and lower churn not enough to claim the feature causes lower churn?",
        answer=(
            "Because adoption is not randomized. A confounder such as user engagement "
            "can drive both higher feature usage and lower churn, so the observed "
            "relationship may be non-causal."
        ),
        tags=("causality", "basics"),
    ),
    Card(
        prompt="What is an OEC?",
        answer=(
            "OEC stands for Overall Evaluation Criterion: the main metric or metric "
            "combination used to judge whether the treatment is better for the business "
            "and users."
        ),
        tags=("oec", "basics"),
    ),
    Card(
        prompt="Why should an OEC usually be measurable over a short period such as one to two weeks?",
        answer=(
            "Because experiment decisions need a timely signal. A useful OEC must be "
            "sensitive enough to move during the experiment while still predicting "
            "long-term value."
        ),
        tags=("oec", "design"),
    ),
    Card(
        prompt="Name the four practical ingredients for useful controlled experiments in software.",
        answer=(
            "Assignable units with little interference, enough units, measurable key "
            "metrics or a good surrogate/OEC, and changes that are feasible to ship and test."
        ),
        tags=("basics", "design"),
    ),
    Card(
        prompt="What is the randomization unit?",
        answer=(
            "The entity assigned to control or treatment, such as a user, session, "
            "query, cookie, or device."
        ),
        tags=("design", "randomization"),
    ),
    Card(
        prompt="Why is user-level randomization often preferred?",
        answer=(
            "It aligns well with many product decisions, usually makes independence "
            "assumptions more reasonable, and avoids some spillover and variance pitfalls."
        ),
        tags=("randomization", "design"),
    ),
    Card(
        prompt="What goes wrong if you randomize by user but analyze pageviews as if they are independent?",
        answer=(
            "Pageviews from the same user are correlated. Treating them as independent "
            "underestimates variance and inflates false positives."
        ),
        tags=("randomization", "variance"),
    ),
    Card(
        prompt="Why run an experiment for at least a full week in many consumer products?",
        answer=(
            "To cover day-of-week effects and reduce the chance of calling a result "
            "too early based on short-term noise."
        ),
        tags=("design", "runtime"),
    ),
    Card(
        prompt="What are novelty and primacy effects?",
        answer=(
            "They are time-dependent effects after a change ships. Novelty is a short-term "
            "reaction to something new; primacy is a lasting effect caused by early exposure "
            "or first impressions."
        ),
        tags=("runtime", "design"),
    ),
    Card(
        prompt="Why not ramp a risky experiment directly to 100% even if that would measure impact faster?",
        answer=(
            "Because it maximizes blast radius if something breaks. Ramping controls risk "
            "while still collecting evidence."
        ),
        tags=("ramping", "risk"),
    ),
    Card(
        prompt="What is MPR in ramping?",
        answer=(
            "Maximum Power Ramp: the traffic allocation used to maximize measurement "
            "sensitivity for the experiment, often a 50/50 split when the treatment is "
            "intended to go to 100%."
        ),
        tags=("ramping", "stats"),
    ),
    Card(
        prompt="What are the main goals balanced by the SQR ramping framework?",
        answer="Speed, quality, and risk.",
        tags=("ramping",),
    ),
    Card(
        prompt="What is a two-sample t-test used for in experimentation?",
        answer=(
            "To test whether the difference between treatment and control means is "
            "likely due to a real effect rather than random noise."
        ),
        tags=("stats",),
    ),
    Card(
        prompt="What is the correct interpretation of a p-value?",
        answer=(
            "It is the probability of observing the measured effect or something more "
            "extreme if the null hypothesis were true."
        ),
        tags=("stats",),
    ),
    Card(
        prompt="What is a common wrong interpretation of the p-value?",
        answer="That it is the probability the null hypothesis is true.",
        tags=("stats", "traps"),
    ),
    Card(
        prompt="What is a Type I error?",
        answer=(
            "A false positive: concluding there is a treatment effect when there is no real effect."
        ),
        tags=("stats",),
    ),
    Card(
        prompt="What is a Type II error?",
        answer=(
            "A false negative: missing a real treatment effect."
        ),
        tags=("stats",),
    ),
    Card(
        prompt="What is statistical power?",
        answer=(
            "The probability of detecting a real effect of a specified size. It equals "
            "1 minus the Type II error rate."
        ),
        tags=("stats", "power"),
    ),
    Card(
        prompt="Why is 'no statistically significant result' not the same as 'no effect'?",
        answer=(
            "Because the experiment may be underpowered or too noisy. The data may simply "
            "be insufficient to distinguish the effect from noise."
        ),
        tags=("stats", "power", "traps"),
    ),
    Card(
        prompt="What problem appears when you test many metrics repeatedly?",
        answer=(
            "Multiple testing increases the chance of false positives, so thresholds or "
            "adjustments must be handled carefully."
        ),
        tags=("stats", "trust"),
    ),
    Card(
        prompt="Why does lower variance improve an experiment?",
        answer=(
            "Lower variance makes the estimate more precise, which improves sensitivity "
            "and makes it easier to detect smaller effects."
        ),
        tags=("variance", "power"),
    ),
    Card(
        prompt="Why are ratio metrics tricky for variance estimation?",
        answer=(
            "Because the variance of a ratio is not obtained by naively dividing variances. "
            "You often need the delta method or another correct ratio-variance approach."
        ),
        tags=("variance",),
    ),
    Card(
        prompt="Why are outliers dangerous in experimentation metrics like revenue?",
        answer=(
            "A few extreme values can heavily inflate variance, which reduces power and "
            "can dominate the signal."
        ),
        tags=("variance", "power"),
    ),
    Card(
        prompt="How does triggered analysis improve sensitivity?",
        answer=(
            "By focusing on users who could actually have been affected, which removes "
            "irrelevant noise from unaffected users."
        ),
        tags=("variance", "triggering"),
    ),
    Card(
        prompt="What is CUPED trying to do?",
        answer=(
            "Use pre-experiment covariates to reduce variance without introducing bias, "
            "so the experiment becomes more sensitive."
        ),
        tags=("variance", "triggering"),
    ),
    Card(
        prompt="What is an A/A test?",
        answer=(
            "An experiment where both groups receive the same experience, used to test "
            "the trustworthiness of the experimentation system."
        ),
        tags=("aa", "trust"),
    ),
    Card(
        prompt="Why run A/A tests if there is no product difference?",
        answer=(
            "Because they reveal problems in assignment, logging, metric definitions, "
            "variance estimation, and false positive control."
        ),
        tags=("aa", "trust"),
    ),
    Card(
        prompt="What does it imply if your platform shows many wins in A/A tests?",
        answer=(
            "The system may be producing inflated false positives, often due to bugs or "
            "incorrect statistical assumptions."
        ),
        tags=("aa", "trust", "traps"),
    ),
    Card(
        prompt="How can A/A tests help with future A/B planning?",
        answer=(
            "They provide realistic variance estimates and help calibrate runtime and power planning."
        ),
        tags=("aa", "power"),
    ),
    Card(
        prompt="Interview prompt: A PM asks you to design an A/B test. What is your answer skeleton?",
        answer=(
            "Hypothesis, OEC and guardrails, target population, randomization unit, "
            "assignment and ramp plan, runtime and power, trust checks such as SRM and "
            "logging quality, then interpretation and launch decision."
        ),
        tags=("interview", "design"),
    ),
]


def format_block(text: str) -> str:
    return textwrap.fill(text, width=88)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Short interactive quiz for the A/B experimentation PDF subset."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=7,
        help="Number of cards to practice in this round.",
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        default=[],
        help="Optional tag filter, e.g. --tags stats power or --tags aa.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for a repeatable order.",
    )
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="Print available tags and exit.",
    )
    parser.add_argument(
        "--ordered",
        action="store_true",
        help="Keep the original card order instead of shuffling.",
    )
    return parser


def select_cards(tags: list[str], ordered: bool, seed: int | None) -> list[Card]:
    if tags:
        wanted = {tag.lower() for tag in tags}
        cards = [card for card in CARDS if wanted.intersection(card.tags)]
    else:
        cards = list(CARDS)

    if not ordered:
        random.Random(seed).shuffle(cards)
    return cards


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    all_tags = sorted({tag for card in CARDS for tag in card.tags})
    if args.list_tags:
        print("Available tags:")
        for tag in all_tags:
            print(f"- {tag}")
        return 0

    cards = select_cards(args.tags, args.ordered, args.seed)
    if not cards:
        parser.error("No cards matched the requested tags.")

    limit = max(1, min(args.limit, len(cards)))
    seen = 0
    hard = 0
    good = 0

    print("A/B experimentation drill")
    print("Say the answer out loud, then press Enter to reveal it.")
    print("After each card: g = good, h = hard, q = quit")
    print()

    for index, card in enumerate(cards[:limit], start=1):
        print(f"Card {index}/{limit}")
        print(format_block(card.prompt))
        print(f"Tags: {', '.join(card.tags)}")
        input("\nPress Enter to reveal > ")
        print()
        print(format_block(card.answer))
        print()
        seen += 1

        while True:
            choice = input("[g]ood / [h]ard / [q]uit > ").strip().lower()
            if choice in {"g", "h", "q", ""}:
                break
            print("Use g, h, or q.")

        if choice == "q":
            break
        if choice == "h":
            hard += 1
        else:
            good += 1
        print()

    print("Round summary")
    print(f"- Seen: {seen}")
    print(f"- Good: {good}")
    print(f"- Hard: {hard}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
