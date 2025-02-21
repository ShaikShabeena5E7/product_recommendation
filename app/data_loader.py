import pandas as pd

# Load product data from CSV
def load_product_data(file_path="products.csv"):
    try:
        df = pd.read_csv(file_path)
        # Ensure required columns exist
        required_columns = {"id", "name", "category", "description", "price"}
        if not required_columns.issubset(df.columns):
            raise ValueError("Missing required columns in product data")
        return df
    except Exception as e:
        print(f"Error loading product data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    data = load_product_data()
    print(data.head())  # Display first few rows
