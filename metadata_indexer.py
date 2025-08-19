import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def extract_metadata(file_path):
    df = pd.read_csv(file_path)
    metadata = []
    dataset_name = os.path.basename(file_path)
    metadata.append(f"Dataset: {dataset_name}")
    metadata.append(f"Number of rows: {df.shape[0]}")
    metadata.append(f"Number of columns: {df.shape[1]}")
    metadata.append("Columns:")
    for col in df.columns:
        col_type = df[col].dtype
        nulls = df[col].isnull().sum()
        stats = ""
        if pd.api.types.is_numeric_dtype(df[col]):
            stats = (
                f"mean={df[col].mean():.2f}, std={df[col].std():.2f}, min={df[col].min()}, max={df[col].max()}"
            )
        metadata.append(
            f"  - {col}: type={col_type}, nulls={nulls}{', ' + stats if stats else ''}"
        )
    return "\n".join(metadata)


def index_all_metadata(data_dir=DATA_DIR, output_file="metadata_index.txt"):
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    all_metadata = []
    for file in files:
        file_path = os.path.join(data_dir, file)
        meta = extract_metadata(file_path)
        all_metadata.append(meta)
        all_metadata.append("\n" + "-"*40 + "\n")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines("\n".join(all_metadata))
    print(f"Metadata indexed for {len(files)} datasets. Output: {output_file}")


if __name__ == "__main__":
    index_all_metadata()
