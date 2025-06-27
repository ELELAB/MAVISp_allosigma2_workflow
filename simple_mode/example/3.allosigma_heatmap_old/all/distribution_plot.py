#python distribution_plot.py data_matrix.txt  output_plot.pdf  my_statistics.log
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Function to plot the distribution and save it as a PDF
def plot_distribution(data, output_file):
    plt.figure(figsize=(10, 6))
    plt.hist(data.values.flatten(), bins=50, edgecolor='k')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Distribution of Values')
    plt.savefig(output_file)
    plt.close()

# Function to calculate statistics and write them to a log file
def write_statistics(data, log_file):
    with open(log_file, 'w') as f:
        f.write(f"Number of rows: {data.shape[0]}\n")
        f.write(f"Number of columns: {data.shape[1]}\n")
        f.write(f"Minimum value: {data.values.min()}\n")
        f.write(f"Maximum value: {data.values.max()}\n")
        f.write(f"Average value: {data.values.mean()}\n")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Plot distribution of values from a data matrix.')
    parser.add_argument('input_file', help='Input data matrix file')
    parser.add_argument('output_file', help='Output PDF file for distribution plot')
    parser.add_argument('log_file', help='Output log file for statistics')
    args = parser.parse_args()

    # Read data from the input file (assuming it's tab-separated)
    try:
        data = pd.read_csv(args.input_file, sep='\t', index_col=0)
    except Exception as e:
        print(f"Error loading data from '{args.input_file}': {e}")
        return

    # Plot distribution of values
    plot_distribution(data, args.output_file)
    print(f"Distribution plot saved as '{args.output_file}'")

    # Calculate statistics and write to log file
    write_statistics(data, args.log_file)
    print(f"Statistics saved in '{args.log_file}'")

if __name__ == '__main__':
    main()

