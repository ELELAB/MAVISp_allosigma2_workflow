import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_free_energy_data(input_file):
    """
    Load free energy data from a tab-delimited file and flatten it into a 1D array.
    """
    data = pd.read_csv(input_file, sep="\t", skiprows=1)
    free_energy_values = data.iloc[:, 1:].to_numpy(dtype=float).flatten()
    free_energy_values = free_energy_values[~np.isnan(free_energy_values)]  # Remove NaNs
    return free_energy_values

def compute_percentile_thresholds(values, lower_percentile=5, upper_percentile=95):
    """
    Compute thresholds based on percentiles.
    """
    lower_threshold = np.percentile(values, lower_percentile)
    upper_threshold = np.percentile(values, upper_percentile)
    return lower_threshold, upper_threshold

def plot_distribution(values, lower_threshold, upper_threshold, lower_percentile, upper_percentile, output_file=None):
    """
    Plot the distribution of values with thresholds marked.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(values, kde=True, bins=50, color="blue")
    plt.axvline(lower_threshold, color="red", linestyle="--", label=f"{lower_percentile}th Percentile ({lower_threshold:.2f})")
    plt.axvline(upper_threshold, color="green", linestyle="--", label=f"{upper_percentile}th Percentile ({upper_threshold:.2f})")
    plt.title("Distribution of Free Energy Changes with Thresholds")
    plt.xlabel("Free Energy Change (ΔΔG)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    if output_file:
        plt.savefig(output_file)
    plt.show()

def save_thresholds(output_file, lower_threshold, upper_threshold, lower_percentile, upper_percentile):
    """
    Save the computed thresholds to a file.
    """
    with open(output_file, "w") as f:
        f.write(f"Lower Threshold ({lower_percentile}th Percentile): {lower_threshold:.2f}\n")
        f.write(f"Upper Threshold ({upper_percentile}th Percentile): {upper_threshold:.2f}\n")
    print(f"Thresholds saved to {output_file}")

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Compute percentile thresholds for free energy changes.")
    parser.add_argument("input_file", type=str, help="Path to the input TSV file containing free energy values.")
    parser.add_argument("--lower_percentile", type=float, default=5, help="Lower percentile for threshold calculation (default: 5).")
    parser.add_argument("--upper_percentile", type=float, default=95, help="Upper percentile for threshold calculation (default: 95).")
    parser.add_argument("--output_plot", type=str, default="distribution_with_thresholds.png", help="Output file for the plot (default: 'distribution_with_thresholds.png').")
    parser.add_argument("--output_thresholds", type=str, default="thresholds.txt", help="Output file for the thresholds (default: 'thresholds.txt').")
    args = parser.parse_args()

    # Load data
    values = load_free_energy_data(args.input_file)

    # Compute thresholds
    lower_threshold, upper_threshold = compute_percentile_thresholds(values, args.lower_percentile, args.upper_percentile)

    # Print thresholds
    print(f"Lower Threshold ({args.lower_percentile}th Percentile): {lower_threshold:.2f}")
    print(f"Upper Threshold ({args.upper_percentile}th Percentile): {upper_threshold:.2f}")

    # Save thresholds to a file
    save_thresholds(args.output_thresholds, lower_threshold, upper_threshold, args.lower_percentile, args.upper_percentile)

    # Plot and save the distribution
    plot_distribution(values, lower_threshold, upper_threshold, args.lower_percentile, args.upper_percentile, args.output_plot)

