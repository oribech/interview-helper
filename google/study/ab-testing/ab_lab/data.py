"""Generate realistic fake experiment data for hands-on practice."""

import numpy as np
import pandas as pd


def generate_experiment(
    n_control: int = 5000,
    n_treatment: int = 5000,
    control_mean: float = 3.20,
    effect_pct: float = -0.03,  # -3% effect
    noise_std: float = 8.0,
    metric_name: str = "revenue_per_user",
    seed: int = 42,
) -> pd.DataFrame:
    """Generate a two-group experiment dataset.

    Returns a DataFrame with columns: user_id, variant, <metric_name>.
    The user must analyze this themselves.
    """
    rng = np.random.default_rng(seed)
    treatment_mean = control_mean * (1 + effect_pct)

    control_vals = rng.normal(control_mean, noise_std, n_control).clip(0)
    treatment_vals = rng.normal(treatment_mean, noise_std, n_treatment).clip(0)

    df = pd.DataFrame({
        "user_id": range(n_control + n_treatment),
        "variant": ["control"] * n_control + ["treatment"] * n_treatment,
        metric_name: np.concatenate([control_vals, treatment_vals]),
    })
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def generate_aa_test(
    n_per_group: int = 5000,
    mean: float = 3.20,
    noise_std: float = 8.0,
    seed: int = 99,
) -> pd.DataFrame:
    """Generate an A/A test — both groups are identical. No real effect."""
    rng = np.random.default_rng(seed)
    a_vals = rng.normal(mean, noise_std, n_per_group).clip(0)
    b_vals = rng.normal(mean, noise_std, n_per_group).clip(0)

    return pd.DataFrame({
        "user_id": range(2 * n_per_group),
        "variant": ["A"] * n_per_group + ["B"] * n_per_group,
        "revenue_per_user": np.concatenate([a_vals, b_vals]),
    })


def generate_srm_experiment(
    n_control: int = 5200,
    n_treatment: int = 4800,
    control_mean: float = 3.20,
    effect_pct: float = 0.05,
    noise_std: float = 8.0,
    seed: int = 77,
) -> pd.DataFrame:
    """Generate experiment with Sample Ratio Mismatch.

    Configured as 50/50 but actual split is skewed.
    """
    return generate_experiment(
        n_control=n_control,
        n_treatment=n_treatment,
        control_mean=control_mean,
        effect_pct=effect_pct,
        noise_std=noise_std,
        seed=seed,
    )


def generate_outlier_experiment(
    n_per_group: int = 5000,
    control_mean: float = 3.20,
    effect_pct: float = 0.02,
    noise_std: float = 8.0,
    n_outliers: int = 3,
    outlier_value: float = 50000.0,
    seed: int = 123,
) -> pd.DataFrame:
    """Generate experiment where a few outliers dominate the result."""
    df = generate_experiment(
        n_control=n_per_group,
        n_treatment=n_per_group,
        control_mean=control_mean,
        effect_pct=effect_pct,
        noise_std=noise_std,
        seed=seed,
    )
    rng = np.random.default_rng(seed)
    # inject outliers into treatment
    treatment_idx = df[df["variant"] == "treatment"].index
    outlier_idx = rng.choice(treatment_idx, n_outliers, replace=False)
    df.loc[outlier_idx, "revenue_per_user"] = outlier_value
    return df


def generate_experiment_with_covariate(
    n_per_group: int = 5000,
    control_mean: float = 3.20,
    effect_pct: float = 0.01,  # small 1% effect
    noise_std: float = 8.0,
    covariate_correlation: float = 0.6,
    seed: int = 55,
) -> pd.DataFrame:
    """Generate experiment with a pre-experiment covariate (for CUPED practice)."""
    rng = np.random.default_rng(seed)
    treatment_mean = control_mean * (1 + effect_pct)

    # pre-experiment values (correlated with post)
    pre_control = rng.normal(control_mean, noise_std, n_per_group).clip(0)
    pre_treatment = rng.normal(control_mean, noise_std, n_per_group).clip(0)

    # post = correlated with pre + treatment effect
    noise_c = rng.normal(0, noise_std * np.sqrt(1 - covariate_correlation**2), n_per_group)
    noise_t = rng.normal(0, noise_std * np.sqrt(1 - covariate_correlation**2), n_per_group)

    post_control = covariate_correlation * pre_control + (1 - covariate_correlation) * control_mean + noise_c
    post_treatment = covariate_correlation * pre_treatment + (1 - covariate_correlation) * treatment_mean + noise_t
    # add the treatment effect on top
    post_treatment += (treatment_mean - control_mean)

    df = pd.DataFrame({
        "user_id": range(2 * n_per_group),
        "variant": ["control"] * n_per_group + ["treatment"] * n_per_group,
        "pre_experiment_revenue": np.concatenate([pre_control, pre_treatment]).clip(0),
        "revenue_per_user": np.concatenate([post_control, post_treatment]).clip(0),
    })
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)
