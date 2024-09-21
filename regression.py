import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns

def plot_scatter_with_regression(x: np.ndarray, y: np.ndarray, output_file: str, log_scale_x: bool = False, log_scale_y: bool = False) -> None:
    """
    Plots a scatter plot with a regression line.

    Args:
        x (np.ndarray): Array of x values.
        y (np.ndarray): Array of y values.
        output_file (str): Path to save the output plot.
        log_scale_x (bool): Whether to use a logarithmic scale for the x-axis. Default is False.
        log_scale_y (bool): Whether to use a logarithmic scale for the y-axis. Default is False.

    Returns:
        None
    """
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
    """
    Loads a DataFrame from a file, supporting CSV, XLSX, and TSV formats.

    Args:
        filename (str): The path to the file to be loaded.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        ValueError: If the file type is unsupported.
    """
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
    Creates a heatmap from the given data and saves it to a file.

    Args:
        data (pd.DataFrame): The data to be used for the heatmap.
        output_file (str): The path to save the output heatmap image.
        title (str): The title of the heatmap. Default is "Heatmap".
        cmap (str): The colormap to be used. Default is "viridis".
        annot (bool): Whether to annotate the heatmap cells. Default is True.
        figsize (tuple): The size of the figure as (width, height). Default is (10, 8).
        center (float): The value at which to center the colormap. Default is None.

    Returns:
        None
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
    Creates a circular heatmap from the given data and saves it to a file.

    Args:
        data (pd.DataFrame): The data to be used for the circular heatmap.
        output_file (str): The path to save the output circular heatmap image.
        title (str): The title of the circular heatmap. Default is "Circle Heatmap".
        cmap (str): The colormap to be used. Default is "viridis".
        annot (bool): Whether to annotate the heatmap cells. Default is True.
        figsize (tuple): The size of the figure as (width, height). Default is (10, 8).

    Returns:
        None
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
    Converts a series of currency values to floats.

    Args:
        currency_series (pd.Series): The series of currency values to be converted.

    Returns:
        pd.Series: The series with currency values converted to floats.
    """
    # Remove any non-numeric characters (e.g., '$', ',', etc.) and convert to float
    return currency_series.replace('[\$,%]', '', regex=True).astype(float)


def read_all_sheets_into_df(file_path):
    """
    Reads all sheets from an Excel file into a dictionary of DataFrames.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        dict: A dictionary where the keys are sheet names and the values are DataFrames.
    """
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

