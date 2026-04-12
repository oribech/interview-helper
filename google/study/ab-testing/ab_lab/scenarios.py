"""Pre-built experiment scenarios for practice."""

SCENARIOS = {
    "coupon_field": {
        "title": "Coupon Code Field on Checkout",
        "description": (
            "Your e-commerce site wants to add a coupon code field to checkout.\n"
            "Concern: users might abandon checkout to hunt for codes."
        ),
        "your_task": "Design this experiment (fill in the design dict), then analyze the data.",
        "seed": 42,
        "true_effect": -0.028,
        "n_per_group": 5000,
        "control_mean": 3.21,
        "noise_std": 8.0,
    },
    "new_ranking": {
        "title": "New ML Ranking Model",
        "description": (
            "Your search team built a new ranking model.\n"
            "It should improve relevance, but might slow down page load."
        ),
        "your_task": "Design experiment, analyze results, check guardrails, make launch decision.",
        "seed": 88,
        "true_effect": 0.015,
        "n_per_group": 8000,
        "control_mean": 0.32,  # CTR
        "noise_std": 0.15,
        "metric_name": "ctr",
    },
    "homepage_recs": {
        "title": "Recommended For You on Homepage",
        "description": (
            "Product wants to add personalized recommendations to the homepage.\n"
            "Could increase engagement or distract from search."
        ),
        "your_task": "Design experiment with proper OEC and guardrails.",
        "seed": 33,
        "true_effect": 0.008,
        "n_per_group": 10000,
        "control_mean": 2.50,
        "noise_std": 6.0,
    },
    "button_color": {
        "title": "Green vs Blue Buy Button",
        "description": (
            "Designer wants to change the Buy button from blue to green.\n"
            "Seems trivial but Bing found $10M/year from color tweaks."
        ),
        "your_task": "Analyze the data. Is the effect real or noise?",
        "seed": 44,
        "true_effect": 0.001,  # tiny, probably not practically significant
        "n_per_group": 50000,
        "control_mean": 0.045,  # conversion rate
        "noise_std": 0.05,
        "metric_name": "conversion_rate",
    },
}


def get_scenario(name: str) -> dict:
    """Get a scenario by name."""
    if name not in SCENARIOS:
        print(f"Unknown scenario '{name}'. Available: {list(SCENARIOS.keys())}")
        return {}
    s = SCENARIOS[name].copy()
    print(f"SCENARIO: {s['title']}")
    print(f"  {s['description']}")
    print(f"\n  YOUR TASK: {s['your_task']}")
    print()
    return s


def list_scenarios() -> None:
    """Print all available scenarios."""
    print("Available scenarios:\n")
    for name, s in SCENARIOS.items():
        print(f"  {name:20s} — {s['title']}")
    print("\nUse: scenario = get_scenario('name')")
