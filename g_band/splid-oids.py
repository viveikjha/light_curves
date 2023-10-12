# import csv
# import os

# def split_csv_file(file_path):
#     # Open the CSV file
#     with open(file_path, 'r') as csv_file:
#         # Create a CSV reader
#         reader = csv.reader(csv_file)
        
#         # Initialize an empty dictionary to hold file writers for each unique first column value
#         writers = {}
        
#         # Iterate over each row in the CSV file
#         for row in reader:
#             # Get the first column value
#             first_col_value = row[0]
            
#             # If we haven't seen this value before, create a new CSV writer for it
#             if first_col_value not in writers:
#                 # Open a new CSV file for writing
#                 output_file = open(f'{first_col_value}.csv', 'w', newline='')
                
#                 # Create a new CSV writer
#                 writer = csv.writer(output_file)
                
#                 # Store the writer in our dictionary
#                 writers[first_col_value] = writer
            
#             # Write the row to the appropriate CSV file
#             writers[first_col_value].writerow(row)
        
#         # Close all of the CSV files we opened
#         # for writer in writers.values():
#         #     writer.close()

# # Call the function with the path to your CSV file
# split_csv_file('0.51098_-10.50811_g.csv')
# print('file split succesfully')


# import csv
# from collections import Counter

# def split_and_count_oid(file_path):
#     # Open the CSV file
#     with open(file_path, 'r') as csv_file:
#         # Create a CSV reader
#         reader = csv.reader(csv_file)
        
#         # Initialize an empty dictionary to hold file writers and counters for each unique first column value
#         writers = {}
#         counters = {}
        
#         # Iterate over each row in the CSV file
#         for row in reader:
#             # Get the first column value (OID)
#             oid = row[0]
            
#             # If we haven't seen this OID before, create a new CSV writer and a new Counter for it
#             if oid not in writers:
#                 # Open a new CSV file for writing
#                 output_file = open(f'{oid}.csv', 'w', newline='')
                
#                 # Create a new CSV writer
#                 writer = csv.writer(output_file)
                
#                 # Store the writer in our dictionary
#                 writers[oid] = writer
                
#                 # Create a new Counter and store it in our dictionary
#                 counters[oid] = Counter()
            
#             # Write the row to the appropriate CSV file
#             writers[oid].writerow(row)
            
#             # Increment the count for this OID
#             counters[oid][oid] += 1
        
#         # Close all of the CSV files we opened
#         # for output_file in writers.values():
#         #     output_file.close()
        
#         # Print the count of each OID in each file
#         for oid, counter in counters.items():
#             print(f'OID: {oid}, Count: {counter[oid]}')

# # Call the function with the path to your CSV file
# split_and_count_oid('0.51098_-10.50811_g.csv')
# print('file split succesfully')


import csv
from collections import Counter
import os

def split_and_count_oid(file_path):
    # Open the CSV file
    with open(file_path, 'r') as csv_file:
        # Create a CSV reader
        reader = csv.reader(csv_file)
        
        # Initialize an empty dictionary to hold file writers and counters for each unique first column value
        writers = {}
        counters = {}
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Get the first column value (OID)
            oid = row[0]
            
            # If we haven't seen this OID before, create a new CSV writer and a new Counter for it
            if oid not in writers:
                # Open a new CSV file for writing
                output_file = open(f'{oid}.csv', 'w', newline='')
                
                # Create a new CSV writer
                writer = csv.writer(output_file)
                
                # Store the writer and output file in our dictionary
                writers[oid] = (writer, output_file)
                
                # Create a new Counter and store it in our dictionary
                counters[oid] = Counter()
            
            # Write the row to the appropriate CSV file
            writers[oid][0].writerow(row)
            
            # Increment the count for this OID
            counters[oid][oid] += 1
        
        # Find the OID with the maximum count
        max_oid = max(counters.items(), key=lambda x: x[1][x[0]])[0]
        
        # Close all of the CSV files we opened except for the one with the maximum count
        for oid, (writer, output_file) in writers.items():
            if oid != max_oid:
                output_file.close()
                os.remove(f'{oid}.csv')
        
        # Rename the file with the maximum count
        os.rename(f'{max_oid}.csv', f'{os.path.splitext(file_path)[0]}_split.csv')
        
        print(f'The file with the maximum count of OID ({max_oid}) has been saved as {os.path.splitext(file_path)[0]}_split.csv')

# Call the function with the path to your CSV file
split_and_count_oid('0.51098_-10.50811_g.csv')
print('file split succesfully')
