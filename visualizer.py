# visualizer.py

import matplotlib.pyplot as plt

def visualize_wallet_analysis(tx_count, unique_contracts, risk_level):
    """
    Creates a bar chart to visualize wallet's on-chain behavior.
    Saves the figure as 'wallet_analysis.png'.
    """
    labels = ["Transactions", "Unique Contracts"]
    values = [tx_count, unique_contracts]
    colors = ["skyblue", "lightgreen"]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(labels, values, color=colors, width=0.4, edgecolor="black")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10)

    ax.set_ylim(0, max(values) + 5)
    ax.set_title(f"Wallet Activity Overview (Risk: {risk_level.upper()})")
    ax.set_ylabel("Count")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig("wallet_analysis.png")
    plt.close()
