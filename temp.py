import pandas as pd

class PageProcessor:
    def __init__(self, df_data):
        self.df_data = df_data
        self.results = {}

    def filter_data(self, file_name, page):
        """Filter the data by filename and page."""
        return self.df_data[(self.df_data['file_name'] == file_name) & (self.df_data['page'] == page)].reset_index(drop=True)

    def update_dict(self, file_name, page, target_class, status, category):
        """Update the results dictionary with missed or noise information."""
        self.results.setdefault(file_name, []).append({
            "page": page,
            "class": target_class,
            "status": status,
            "cat": category
        })

    def process_pages(self, pages, file_name, target_class, columns, category):
        """Process pages to check for missed or noise classes."""
        for page in pages:
            dfx_filtered = self.filter_data(file_name, page)
            if not dfx_filtered.empty:
                if category == "missed":
                    # Check that target_class is not in any missed columns
                    if all(target_class not in dfx_filtered[col].values for col in columns):
                        self.update_dict(file_name, page, target_class, 1, "missed")
                elif category == "noise":
                    # Check if target_class is in any noise columns
                    if any(target_class in dfx_filtered[col].values for col in columns):
                        self.update_dict(file_name, page, target_class, 1, "noise")

    def process_file(self, df_temp, missed_class_cols, noise_class_cols):
        """Main function to process missed and noise pages for each file in df_temp."""
        for _, row in df_temp.iterrows():
            file_name = row['file_name']
            target_class = row['pred_final']
            
            # Process missed pages
            self.process_pages(row['missed'], file_name, target_class, missed_class_cols, "missed")

            # Process noise pages
            self.process_pages(row['added'], file_name, target_class, noise_class_cols, "noise")
        
        return self.results

# Example usage
# df_temp and df_data should be your actual DataFrames
# missed_class_cols = ['col1', 'col2', 'col3']  # Replace with actual missed class column names
# noise_class_cols = ['col4', 'col5', 'col6']   # Replace with actual noise class column names

# processor = PageProcessor(df_data)
# result_dic = processor.process_file(df_temp, missed_class_cols, noise_class_cols)
# print(result_dic)
