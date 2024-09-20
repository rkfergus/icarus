import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns

def plot_scatter_with_regression(x, y, output_file: str, log_scale_x=False, log_scale_y=False):
    try:
        x_label = x.name
        y_label = y.name
    except:
        x_label = 'X Values'
        y_label = 'Y Values'

    # Convert input to numpy arrays (if they aren't already)
    x = np.array(x)
    y = np.array(y)
        
    # Handle logarithmic scales
    if log_scale_x:
        x = np.log10(x)
        x_label = f'log10({x_label})'
    if log_scale_y:
        y = np.log10(y)
        y_label = f'log10({y_label})'
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print(f'R Value: {r_value}, P Value: {p_value}')
    
    # Calculate the regression line
    reg_line = slope * x + intercept
    
    # Plot the scatter plot
    plt.scatter(x, y, color='blue', label='Data points')
    
    # Plot the regression line
    plt.plot(x, reg_line, color='red', label=f'Regression line (R={r_value:.2f})')
    
    if log_scale_x:
        plt.xscale('log')
        x_label = x_label.replace('log10(', '').replace(')', '')
    if log_scale_y:
        plt.yscale('log')
        y_label = y_label.replace('log10(', '').replace(')', '')

    # Add title and labels
    plt.title('Scatter Plot with Regression Line')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    
    # Save plot
    plt.savefig(output_file)
    
    # Print the R value
    print(f'R value (correlation coefficient): {r_value:.2f}')

    plt.clf()

def load_dataframe(filename: str) -> pd.DataFrame:
    extension = filename.split('.')[-1]

    # Dictionary to simulate switch statement
    file_loaders = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel,
        'tsv': lambda f: pd.read_csv(f, sep='\t')
    }

    # Get the appropriate loader function from the dictionary
    loader = file_loaders.get(extension)

    if loader:
        try:
            return loader(filename)
        except UnicodeDecodeError:
            return loader(filename, encoding='ISO-8859-1')
        # Load the dataframe using the loader function
       
    else:
        raise ValueError(f"Unsupported file type: {extension}")

def create_heatmap(data,  output_file, title="Heatmap", cmap="viridis", annot=True, figsize=(10, 8), center=None):
    """
    Creates a heatmap from a pandas DataFrame.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the data for the heatmap.
    - title (str): The title of the heatmap.
    - cmap (str): The colormap to use for the heatmap.
    - annot (bool): Whether to annotate the cells with their values.
    - figsize (tuple): The size of the figure.
    """
    print(center, type(center))
    plt.figure(figsize=figsize)
    sns.heatmap(data, annot=annot, cmap=cmap, center=center)

    plt.title(title)

    plt.xticks(rotation=45)
    # plt.yticks(rotation=90)

    plt.tight_layout()
    plt.savefig(output_file)

def create_circle_heatmap(data, output_file, title="Circle Heatmap", cmap="viridis", annot=True, figsize=(10, 8)):
    """
    Creates a heatmap with circular markers from a pandas DataFrame.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the data for the heatmap.
    - title (str): The title of the heatmap.
    - cmap (str): The colormap to use for the heatmap.
    - annot (bool): Whether to annotate the cells with their values.
    - figsize (tuple): The size of the figure.
    """
    # Create a meshgrid for plotting
    x, y = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
    
    # Flatten the data for scatter plot
    sizes = data.values.flatten()
    sizes = sizes / np.max(sizes) * 1000  # Scale sizes for better visualization
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Create a scatter plot with circular markers
    scatter = ax.scatter(x.flatten(), y.flatten(), s=sizes, c=data.values.flatten(), cmap=cmap, edgecolors='w')
    
    # Annotate the circles if needed
    if annot:
        for (i, j), val in np.ndenumerate(data):
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')
    
    # Set the ticks and labels
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(data.columns)
    ax.set_yticklabels(data.index)
    
    # Add a colorbar
    plt.colorbar(scatter)
    
    # Set the title
    plt.title(title)
    
    plt.gca().invert_yaxis()  # Invert y-axis to have the first row at the top
    plt.savefig(output_file)

def convert_to_float(currency_series):
    """
    Converts a pandas Series of currency values (strings) to floats.
    
    Parameters:
    currency_series (pd.Series): Series containing currency values as strings.
    
    Returns:
    pd.Series: Series with currency values converted to floats.
    """
    # Remove any non-numeric characters (e.g., '$', ',', etc.) and convert to float
    return currency_series.replace('[\$,%]', '', regex=True).astype(float)


def read_all_sheets_into_df(file_path):
    # Read all sheets into a dictionary of DataFrames
    all_sheets = pd.read_excel(file_path, sheet_name=None)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_sheets.values(), ignore_index=True)
    
    return combined_df


def plot_timestamps(timestamps):
    # Convert timestamps to a list of dates
    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(timestamps, bins='auto', edgecolor='black')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('out/frequency.png')
    plt.clf()

def calc_fig_size(desired_px, dpi):
    return desired_px / dpi

