# External imports
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import row, column
from bokeh.models import Title, Range1d
import os

# Defining folder and file names constants.
FOLDER_NAME = 'visualization'
PLOTS_FILE_URL = FOLDER_NAME + '/visualization.html'
PLOT_WIDTH = 450
PLOT_HEIGHT = 450

class DataVisualization():
    FOLDER_NAME = 'visualization'  # Folder to save visualization outputs
    PLOTS_FILE_URL = os.path.join(FOLDER_NAME, 'visualization.html')  # URL for the output HTML file
    PLOT_WIDTH = 450  # Width of the plots
    PLOT_HEIGHT = 450  # Height of the plots

    def __init__(self):
        os.makedirs(self.FOLDER_NAME, exist_ok=True)  # Create visualization folder if it doesn't exist

    # Function to visualize data
    def visualize(self, train_df, ideal_df, best_fit_functions, mapped_test_df):
         # Creating 3 plots i.e. train, ideal and test plots for Y1.
        train_plot_y1 = self.__plot_train_data(train_df, 'y1', 'red')
        ideal_plot_y1 = self.__plot_matched_ideal_data(ideal_df, best_fit_functions, 0, 'red')
        test_plot_y1 = self.__plot_mapped_test_data(ideal_df, best_fit_functions, mapped_test_df, 0, 'red')

        # Combine these 3 plots into a row layout.
        row_y1 = row(train_plot_y1, ideal_plot_y1, test_plot_y1)

        # Creating 3 plots i.e. train, ideal and test plots for Y2.
        train_plot_y2 = self.__plot_train_data(train_df, 'y2', 'darkgreen')
        ideal_plot_y2 = self.__plot_matched_ideal_data(ideal_df, best_fit_functions, 1, 'darkgreen')
        test_plot_y2 = self.__plot_mapped_test_data(ideal_df, best_fit_functions, mapped_test_df, 1, 'darkgreen')

        # Combine these 3 plots into a row layout.
        row_y2 = row(train_plot_y2, ideal_plot_y2, test_plot_y2)

        # Creating 3 plots i.e. train, ideal and test plots for Y3.
        train_plot_y3 = self.__plot_train_data(train_df, 'y3', 'blue')
        ideal_plot_y3 = self.__plot_matched_ideal_data(ideal_df, best_fit_functions, 2, 'blue')
        test_plot_y3 = self.__plot_mapped_test_data(ideal_df, best_fit_functions, mapped_test_df, 2, 'blue')

        # Combine these 3 plots into a row layout.
        row_y3 = row(train_plot_y3, ideal_plot_y3, test_plot_y3)

        # Creating 3 plots i.e. train, ideal and test plots for Y4.
        train_plot_y4 = self.__plot_train_data(train_df, 'y4', 'fuchsia')
        ideal_plot_y4 = self.__plot_matched_ideal_data(ideal_df, best_fit_functions, 3, 'fuchsia')
        test_plot_y4 = self.__plot_mapped_test_data(ideal_df, best_fit_functions, mapped_test_df, 3, 'fuchsia')

        # Combine these 3 plots into a row layout.
        row_y4 = row(train_plot_y4, ideal_plot_y4, test_plot_y4)

        # Combine all 4 row layouts into a column layout.
        combined_plots = column(row_y1, row_y2, row_y3, row_y4)
        # Save the combined column plots
        output_file(PLOTS_FILE_URL)
        save(combined_plots)

    # Function to plot training data
    def __plot_train_data(self, train_df, y_col, line_color):
        graph = figure(title=f'Train data graph with X and Train {y_col.upper()}', width=self.PLOT_WIDTH, height=self.PLOT_HEIGHT)  # Create figure
        graph.xaxis.axis_label = 'Train X'  # Set X axis label
        graph.yaxis.axis_label = f'Train {y_col.upper()}'  # Set Y axis label
        graph.y_range = Range1d(-50, 1000)
        graph.line(train_df.x, train_df[y_col], line_color=line_color, legend_label=f'Train {y_col.upper()}', line_width=2)  # Plot line
        return graph  # Return the plot

    # Function to plot matched ideal data
    def __plot_matched_ideal_data(self, ideal_df, best_fit_functions, y_index, line_color):
        matched_col = best_fit_functions[f'y{y_index + 1}']  # Get matched ideal column
        graph = figure(title=f'Ideal data graph with X & Ideal {matched_col.upper()}', width=self.PLOT_WIDTH, height=self.PLOT_HEIGHT)  # Create figure
        graph.xaxis.axis_label = 'Ideal X'  # Set X axis label
        graph.yaxis.axis_label = f'Ideal {matched_col.upper()}'  # Set Y axis label
        graph.y_range = Range1d(-50, 1000)
        graph.line(ideal_df['x'], ideal_df[matched_col], line_color=line_color, legend_label=f'Ideal {matched_col.upper()}', line_width=2)  # Plot line
        return graph  # Return the plot

    # Function to plot mapped test data
    def __plot_mapped_test_data(self, ideal_df, best_fit_functions, mapped_test_df, y_index, line_color):
        matched_col = best_fit_functions[f'y{y_index + 1}']  # Get matched ideal column
        graph = figure(title=f'Mapped test data graph with X & Ideal {matched_col.upper()}', width=self.PLOT_WIDTH, height=self.PLOT_HEIGHT)  # Create figure
        graph.xaxis.axis_label = 'Test X'  # Set X axis label
        graph.yaxis.axis_label = f'Test Y and Ideal {matched_col.upper()}'  # Set Y axis label
        graph.circle(mapped_test_df['x'], mapped_test_df['y'], fill_color='white', size=8)  # Plot test data points
        graph.line(ideal_df['x'], ideal_df[matched_col], line_color=line_color, legend_label=f'Ideal {matched_col.upper()}', line_width=2)  # Plot ideal data line
        return graph  # Return the plot

