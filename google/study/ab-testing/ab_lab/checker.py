"""Validate user's analysis and experiment design decisions."""

from scipy import stats


def check_design(design: dict) -> None:
    """Check an experiment design dict for completeness and common mistakes.

    Expected keys: hypothesis, oec, guardrails, randomization_unit,
                   population, min_duration_weeks
    """
    required = ["hypothesis", "oec", "guardrails", "randomization_unit",
                "population", "min_duration_weeks"]
    missing = [k for k in required if k not in design]
    if missing:
        print(f"MISSING fields: {missing}")
        print("A complete design needs all 5 steps + duration.")
        return

    issues = []
    if not isinstance(design["guardrails"], list) or len(design["guardrails"]) == 0:
        issues.append("guardrails should be a list with at least 1 metric (e.g. latency, crash rate)")
    if design.get("min_duration_weeks", 0) < 1:
        issues.append("min_duration_weeks should be >= 1 (need full week for day-of-week effect)")
    if "profit" in design.get("oec", "").lower():
        issues.append("'profit' is usually a bad OEC — too slow, gameable. Consider revenue-per-user.")
    if design.get("randomization_unit", "").lower() == "page":
        issues.append("page-level randomization gives inconsistent UX. Consider user-level.")

    if issues:
        print("ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("DESIGN LOOKS GOOD!")
        print(f"  Hypothesis: {design['hypothesis']}")
        print(f"  OEC: {design['oec']}")
        print(f"  Guardrails: {design['guardrails']}")
        print(f"  Randomization: {design['randomization_unit']}")
        print(f"  Population: {design['population']}")
        print(f"  Duration: {design['min_duration_weeks']} week(s)")


def check_launch_decision(
    decision: str,
    p_value: float,
    effect_pct: float,
    ci_lower: float,
    ci_upper: float,
    guardrails_ok: bool = True,
) -> None:
    """Evaluate a launch/no-launch decision given experiment results."""
    decision = decision.lower().strip()

    print("=" * 50)
    print(f"  p-value:     {p_value:.4f}")
    print(f"  effect:      {effect_pct:+.2%}")
    print(f"  95% CI:      [{ci_lower:+.2%}, {ci_upper:+.2%}]")
    print(f"  guardrails:  {'OK' if guardrails_ok else 'BROKEN'}")
    print(f"  your call:   {decision}")
    print("=" * 50)

    if not guardrails_ok:
        if "launch" in decision:
            print("BAD CALL. Guardrails are broken — you can't trust these results.")
            print("Investigate the guardrail issue first.")
        else:
            print("CORRECT. Never launch when guardrails are broken.")
        return

    stat_sig = p_value < 0.05
    zero_in_ci = ci_lower <= 0 <= ci_upper

    if stat_sig and abs(effect_pct) > 0.005:
        expected = "launch" if effect_pct > 0 else "don't launch"
        if expected in decision or ("no" in decision and effect_pct < 0):
            print("GOOD CALL.")
        else:
            print(f"QUESTIONABLE. Effect is {effect_pct:+.2%} and significant.")
            print(f"Expected: {expected}")
    elif stat_sig and abs(effect_pct) <= 0.005:
        print("TRICKY ONE. Statistically significant but tiny effect.")
        print("Reasonable answers: 'not worth the cost' or 'launch if cost is zero'.")
    elif not stat_sig:
        if "launch" in decision:
            print("RISKY. Result is not statistically significant — could be noise.")
            print("Better: rerun with more power, or drop.")
        else:
            print("REASONABLE. Not significant = not enough evidence.")
    print()


def check_aa_analysis(p_values: list[float], alpha: float = 0.05) -> None:
    """Check if an A/A analysis shows the expected false positive rate."""
    n = len(p_values)
    n_sig = sum(1 for p in p_values if p < alpha)
    rate = n_sig / n if n > 0 else 0
    expected = alpha

    print(f"You ran {n} A/A tests at alpha={alpha}")
    print(f"Significant results: {n_sig}/{n} = {rate:.1%}")
    print(f"Expected: ~{expected:.0%}")
    print()

    if abs(rate - expected) < 0.03:
        print("PLATFORM LOOKS HEALTHY. False positive rate is near expected.")
    elif rate > expected + 0.03:
        print("TOO MANY FALSE POSITIVES!")
        print("Something is wrong: check variance calculation, randomization, or data pipeline.")
    else:
        print("Fewer than expected — unusual but not necessarily a problem.")
        print("Could mean your test is conservative (variance overestimated).")


def check_srm(n_control: int, n_treatment: int, expected_ratio: float = 0.5) -> None:
    """Check for Sample Ratio Mismatch using chi-squared test."""
    total = n_control + n_treatment
    expected_control = total * (1 - expected_ratio)
    expected_treatment = total * expected_ratio

    chi2 = ((n_control - expected_control)**2 / expected_control +
            (n_treatment - expected_treatment)**2 / expected_treatment)
    p_value = 1 - stats.chi2.cdf(chi2, df=1)

    actual_ratio = n_treatment / total
    print(f"Expected split: {1-expected_ratio:.0%} / {expected_ratio:.0%}")
    print(f"Actual split:   {n_control/total:.1%} / {n_treatment/total:.1%}")
    print(f"SRM test p-value: {p_value:.6f}")
    print()

    if p_value < 0.001:
        print("SRM DETECTED! Do NOT trust this experiment's results.")
        print("Investigate: randomization bug, bot filtering, logging issue.")
    else:
        print("No SRM detected. Split looks fine.")
