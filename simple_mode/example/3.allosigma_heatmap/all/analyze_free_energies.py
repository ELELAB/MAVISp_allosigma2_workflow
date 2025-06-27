import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro

def analyze_free_energy(input_file, output_prefix):
    """
    Analyze the distribution of free energy changes from the input file.

    Parameters:
    - input_file: str, path to the TSV file containing the data.
    - output_prefix: str, prefix for the output files (e.g., "down_mutations_analysis").
    """
    # Load the data
    print(f"Loading data from {input_file}...")
    data = pd.read_csv(input_file, sep="\t", skiprows=1)

    # Extract numeric free energy values
    free_energy_values = data.iloc[:, 1:].to_numpy(dtype=float).flatten()
    free_energy_values = free_energy_values[~np.isnan(free_energy_values)]  # Remove NaNs

    # Compute summary statistics
    summary_stats = {
        "mean": free_energy_values.mean(),
        "median": np.median(free_energy_values),
        "std_dev": free_energy_values.std(),
        "min": free_energy_values.min(),
        "max": free_energy_values.max(),
    }

    # Perform Shapiro-Wilk test for normality
    shapiro_test = shapiro(free_energy_values)
    summary_stats["shapiro_statistic"] = shapiro_test.statistic
    summary_stats["shapiro_p_value"] = shapiro_test.pvalue

    # Save summary statistics to a log file
    stats_file = f"{output_prefix}_summary_stats.txt"
    with open(stats_file, "w") as f:
        f.write("Summary Statistics:\n")
        for key, value in summary_stats.items():
            f.write(f"{key}: {value}\n")
        f.write("\n")
        f.write("Shapiro-Wilk Test for Normality:\n")
        f.write(f"Statistic: {shapiro_test.statistic}\n")
        f.write(f"P-value: {shapiro_test.pvalue}\n")

    print(f"Summary statistics saved to {stats_file}")

    # Plot the distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(free_energy_values, kde=True, bins=50, color="blue")
    plt.title("Distribution of Free Energy Changes")
    plt.xlabel("Free Energy Change (ΔΔG)")
    plt.ylabel("Frequency")
    plt.grid(True)

    # Save the plot
    plot_file = f"{output_prefix}_distribution.png"
    plt.savefig(plot_file)
    print(f"Distribution plot saved to {plot_file}")
    plt.show()

if __name__ == "__main__":
    # Example usage: python analyze_free_energy.py down_mutations.tsv down_mutations_analysis
    import sys
    if len(sys.argv) != 3:
        print("Usage: python analyze_free_energy.py <input_file> <output_prefix>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_prefix = sys.argv[2]

    analyze_free_energy(input_file, output_prefix)

