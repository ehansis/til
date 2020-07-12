"""Make geonames population distribution chart (for TIL post)"""

import pandas as pd
import numpy as np
import altair


def weighted_percentile_rank(s):
    """Get weighted percentile rank

    Highest rank is guaranteed to be 100.
    Equal values get the same (max) rank.

    Args:
        s (pd.Series): input data

    Returns:
        pd.Series: percentile rank of values, in range 0-100; same index and order as input data
    """
    if len(s) == 0:
        return pd.Series()

    if (s < 0).any():
        raise ValueError(
            "Cannot compute weighted percentile rank of series including negative values"
        )

    data = s.sort_values()

    # compute weighted percentile per value
    cumsum = data.cumsum()
    cmax = cumsum.max()

    if cmax > 0:
        ranks = cumsum / cumsum.max() * 100.0
    else:
        ranks = cumsum

    # map from values to rank, map values to ranks via max of ranks for each value
    v2r = ranks.groupby(data.values).max()
    perc_rank = data.map(v2r)

    return perc_rank.loc[s.index]


# read feature class (6) and population (14) columns, select features of class 'P'
# (populated place) only.
df = pd.read_csv(
    "DE.txt",
    usecols=[2, 6, 14],
    names=["asciiname", "feature_class", "pop"],
    header=None,
    sep="\t",
)
df = df[df["feature_class"] == "P"]
df = df[df["pop"] > 0].sort_values(by="pop")

df["rank"] = np.arange(len(df)) + 1
df["percentile_rank"] = df["rank"] / (len(df)) * 100
df["inverse_rank"] = len(df) - df["rank"] + 1
df["weighted_percentile_rank"] = weighted_percentile_rank(df["pop"])


# compute measures for some example places
def print_values(sel, name):
    sel = sel[sel["asciiname"] == name]
    assert len(sel) == 1
    sel = sel.iloc[0]
    print(
        f"{sel['asciiname']:12s}: population = {sel['pop']:8d}, n-th largest = {sel['inverse_rank']:6d}, "
        f"percentile rank = {sel['percentile_rank']:8.3f}, "
        f"weighted percentile rank = {sel['weighted_percentile_rank']:8.3f}"
    )


print("\nAll:")
print_values(df, "Berlin")
print_values(df, "Hamburg")
print_values(df, "Stuttgart")
print_values(df, "Heidelberg")
print_values(df, "Buxtehude")
print_values(df, "Asselfingen")
print_values(df, "Elend")
print_values(df, "Sorge")

small_clipped = df[df["pop"] >= 1000].copy()
small_clipped["rank"] = np.arange(len(small_clipped)) + 1
small_clipped["percentile_rank"] = small_clipped["rank"] / (len(small_clipped)) * 100
small_clipped["inverse_rank"] = len(small_clipped) - small_clipped["rank"] + 1
small_clipped["weighted_percentile_rank"] = weighted_percentile_rank(small_clipped["pop"])

print("\nSmall clipped:")
print_values(small_clipped, "Berlin")
print_values(small_clipped, "Hamburg")
print_values(small_clipped, "Stuttgart")
print_values(small_clipped, "Heidelberg")
print_values(small_clipped, "Buxtehude")
print_values(small_clipped, "Asselfingen")


# compute cumulative distribution
df["distrib"] = np.arange(len(df)) / len(df) * 100


# plot the cumulative distribution
chart = (
    altair.Chart(df, width=700, height=400)
    .mark_line()
    .encode(
        x=altair.X(
            "distrib", axis=altair.Axis(title="Cumulative probability (percent)")
        )
    )
)

chart.encode(
    y=altair.Y(
        "pop", axis=altair.Axis(title="Population"), scale=altair.Scale(type="log")
    )
).save("geonames_population_distribution_log.png")

chart.encode(y=altair.Y("pop", axis=altair.Axis(title="Population"))).save(
    "geonames_population_distribution_linear.png"
)

# plot a size histogram
altair.Chart(df[df["pop"] <= 100_000], width=500, height=400).mark_bar().encode(
    x=altair.X("pop", bin=altair.Bin(maxbins=100), axis=altair.Axis(title="Population")),
    y='count()',
).save(
    "geonames_population_histogram.png"
)
