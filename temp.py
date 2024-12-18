import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'filename': ['file1'] * 10,
    'page': range(1, 11),
    'class': [[] for _ in range(10)],  # Initialize 'class' column with empty lists
    'flag': [1, 0, 0, -1, 0, 1, 0, 0, -1, 0]
})

def process_pages(df):
    # Sort pages for each file
    df = df.sort_values(['filename', 'page'])

    # Loop through each unique file
    for filename in df['filename'].unique():
        file_df = df[df['filename'] == filename].reset_index(drop=True)
        
        i = 0
        while i < len(file_df):
            current_flag = file_df.loc[i, 'flag']
            
            if current_flag == +1:
                # Search next 30 pages for +1 or -1
                found = False
                for j in range(i + 1, min(i + 31, len(file_df))):
                    if file_df.loc[j, 'flag'] in [+1, -1]:
                        found = True
                        # Append 'pn' to the 'class' lists for pages i to j
                        for k in range(i, j + 1):
                            file_df.at[k, 'class'].append('pn')
                        i = j + 1  # Move to the next page after the found one
                        break
                
                # If no flag found, append 'pn' to the next 5 pages
                if not found:
                    for k in range(i, min(i + 5, len(file_df))):
                        file_df.at[k, 'class'].append('pn')
                    i += 5  # Move to the page after 5

            elif current_flag == -1:
                # Remove 'pn' from class until +1 found
                if 'pn' in file_df.at[i, 'class']:
                    file_df.at[i, 'class'].remove('pn')  # Remove 'pn' from current page
                for j in range(i + 1, len(file_df)):
                    if file_df.loc[j, 'flag'] == +1:
                        i = j  # Start from the next page where +1 is found
                        break
                    if 'pn' in file_df.at[j, 'class']:
                        file_df.at[j, 'class'].remove('pn')  # Remove 'pn' until +1 is found
                else:
                    i = len(file_df)  # End loop if +1 isn't found
                
            else:
                i += 1  # Move to the next page if flag is neither +1 nor -1

        # Update the main dataframe with the processed data
        df.update(file_df)

    return df

# Example usage
df = process_pages(df)
print(df)
