import pandas as pd

def log_table(log_path, data, column_name):
        # Try to read the CSV file if it exists, else create an empty DataFrame
        csv_file = f'{log_path}.csv'
        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            df = pd.DataFrame()

        # Check if the 'name' column exists in the DataFrame
        if 'name' not in df.columns:
            df['name'] = data.keys()
            df[column_name] = data.values()
        else:
            # Ensure the order of 'name' in the DataFrame and the data are the same
            # This assumes that the 'name' values in data are already present in the DataFrame
            ordered_values = [data[name] for name in df['name']]
            df[column_name] = ordered_values

        # Print the table and save it to CSV
        print(df)
        df.to_csv(csv_file, index=False)