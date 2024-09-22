# Internal imports
from csv_helper import CSVHelper
from db_helper import DBHelper
from custom_exceptions import *

from data_visualization import DataVisualization
import numpy as np
import math
import pandas as pd

def main():
    '''
    Main function that uses all other different classes to perform the tasks required in the assignment description.
    The steps are printed sequentially, and the results are displayed at the end.
    '''
    # Step 1: Load the CSV data.
    print('Step 1: Loading the CSV files for train, ideal, and test data.')
    csv = None
    try:
        csv = CSVHelper()
    except DataSetNotFoundException as ex:
        print('Error loading CSVHelper.', ex)
    except InvalidDataFormatException as ex:
        print(ex)
    # Proceed further only if we have successfully loaded the CSV data.
    if csv is None: 
        print('Error loading the CSV, hence stopping the program execution. Please fix the error mentioned above and try to run the program again.')
        return
    
    # Step 2: Copy the loaded CSV data into SQLite Database.
    print('Step 2: Copying the loaded CSV data into SQLite Database (will overwrite tables if they exist).')
    try:
        db_helper = DBHelper('sqlite_database')
    except InitDatabaseException as ex:
        print(ex.message)
        return

    copy_train_success = db_helper.copy_train_to_db(csv.train)
    copy_ideal_success = db_helper.copy_ideal_to_db(csv.ideal)

    # Proceed further only if we have successfully copied the CSV data into SQLite DB. 
    if not copy_train_success or not copy_ideal_success: 
        print('Error copying the CSV data into SQLite DB, hence stopping the program execution. Please fix the error mentioned above and try again.')
        return

    # Step 3: Load the data from SQLite Database.
    print('Step 3: Loading the Pandas DataFrames (train and ideal) from SQLite database.')
    train_df = db_helper.load_train_from_db()
    ideal_df = db_helper.load_ideal_from_db()

    # Function to perform least squares fitting and find the best matching ideal functions
    def find_matching_ideal_functions(train_df, ideal_df):
        results = {}  # Dictionary to store results
        for train_col in train_df.columns[1:]:  # Iterate through each column in training DataFrame
            train_y = train_df[train_col]  # Get Y values for the current training column
            min_error = float('inf')  # Initialize minimum error
            best_fit_func = None  # Initialize best fit function
            for ideal_col in ideal_df.columns[1:]:  # Compare with each ideal function
                ideal_y = ideal_df[ideal_col]  # Get Y values for the current ideal column
                error = np.sum((train_y - ideal_y)**2)  # Calculate squared error
                if error < min_error:  # Update best fit function if a smaller error is found
                    min_error = error
                    best_fit_func = ideal_col
            results[train_col] = best_fit_func  # Store best fit function for the current train column
        return results  # Return dictionary of best fit functions
    
    # Function to map test data to best fitting ideal functions
    def map_test_to_ideal(test_df, ideal_df, best_fit_functions, train_df):
        results = []  # List to store results
        for _, row in test_df.iterrows():  # Iterate through each row in the test DataFrame
            x_test, y_test = row['x'], row['y']  # Get X and Y values from the test DataFrame
            best_func = None  # Initialize best function
            min_delta = float('inf')  # Initialize minimum delta
            
            # Check if the test X value exists in both training and ideal DataFrames
            if x_test in train_df['x'].values and x_test in ideal_df['x'].values:
                for train_col, ideal_col in best_fit_functions.items():  # Iterate through best fit functions
                    y_train = train_df[train_df['x'] == x_test][train_col].values[0]  # Get corresponding Y from train DataFrame
                    y_ideal = ideal_df[ideal_df['x'] == x_test][ideal_col].values[0]  # Get corresponding Y from ideal DataFrame
                    
                    delta_train = abs(y_train - y_ideal)  # Calculate delta for training
                    delta_test = abs(y_test - y_ideal)  # Calculate delta for test
                    
                    # Check if test delta is within an acceptable range
                    if delta_test <= delta_train * math.sqrt(2):
                        if delta_test < min_delta:  # Update minimum delta and best function if applicable
                            min_delta = delta_test
                            best_func = ideal_col
                if best_func:  # If a best function was found, store results
                    results.append({'x': x_test, 'y': y_test, 'delta_y': min_delta, 'ideal_func_no': best_func})
            else:
                print(f"x value {x_test} from test_df not found in train_df or ideal_df.")  # Warn if X not found in both DataFrames
                continue
    
        return results  # Return list of mapped test data


    # Step 4: Find the best ideal functions for each train function.
    print('Step 4: Finding the best ideal functions for each train function.')
    train_ideal_match = find_matching_ideal_functions(train_df, ideal_df)
    
    # Step 5: Map the test data to the best fitting ideal functions.
    print('Step 5: Mapping test data to matched ideal functions.')
    test_map_result = map_test_to_ideal(csv.test, ideal_df, train_ideal_match, train_df)
    test_mapped_df = pd.DataFrame(test_map_result)  # Convert results to DataFrame

    # Step 6: Data visualization (plotting).
    print('Step 6: Data visualization (plotting).')
    data_visualization = DataVisualization()
    data_visualization.visualize(train_df, ideal_df, train_ideal_match, test_mapped_df)

    print('\nAll steps are completed successfully.')

    # Printing outcome results.
    print('\nResults: ')
    print('-- Visualization: You can now see the visualization (Bokeh HTML) reports inside the "visualization" folder. The file "visualization.html" contains all plots.\n')
    print('-- Database: You can also browse the SQLite database file "database/sqlite_database.db".\n')

if __name__ == '__main__':
    main()
