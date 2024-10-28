
import pandas as pd

# Example dataframe
data = {
    'filename': ['file1', 'file1', 'file1', 'file2', 'file2'],
    'page': [1, 2, 3, 1, 2],
    'class': ['A', 'A', 'B', 'B', 'C'],
    'flag': [1, 1, -1, -1, 1]
}
df = pd.DataFrame(data)

def process_pages(group):
    pages = sorted(group['page'])
    result = []
    i = 0
    while i < len(pages):
        current_page = pages[i]
        current_flag = group.loc[group['page'] == current_page, 'flag'].values[0]
        
        if current_flag == +1:
            # Check the next 30 pages
            found_flag = False
            for j in range(i + 1, min(i + 31, len(pages))):
                next_flag = group.loc[group['page'] == pages[j], 'flag'].values[0]
                if next_flag in [+1, -1]:
                    # Append pages up to this point
                    result.extend(pages[i:j + 1])
                    i = j
                    found_flag = True
                    break
            
            if not found_flag:
                # Append next 5 pages if no flag is found
                result.extend(pages[i:i + 5])
                i += 5

        elif current_flag == -1:
            # Remove until +1 is found
            for j in range(i + 1, len(pages)):
                next_flag = group.loc[group['page'] == pages[j], 'flag'].values[0]
                if next_flag == +1:
                    i = j - 1  # Start next loop from this page
                    break
            i += 1
        else:
            i += 1
    return result

# Group by filename and process each group
df['result'] = df.groupby('filename').apply(lambda x: process_pages(x)).explode().reset_index(drop=True)
