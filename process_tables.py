import pandas as pd
import os
import random

machine_mappings = pd.read_csv("./machine_mapping.csv")
product_mappings = pd.read_csv("./product_mapping.csv")


machine_names = machine_mappings["machine_name"].tolist()
product_names = product_mappings["product_name"].tolist()


def process_table(file_path):
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"Error reading {file_path}")
        return None

    columns = df.columns

    # Check if there are any columns that doesn't have any values that are in the
    # machine_mappings, product_mappings
    for column in columns:
        series = df[column]

        # column values can be equal to one of the machine_names, product_names,
        # or column values can include one of the machine_names, product_names,
        if not any(
            series.apply(
                lambda x: any(name in str(x) for name in machine_names + product_names)
            )
        ) and not pd.api.types.is_numeric_dtype(series):

            print(f"Column {column} has no machine names, product names")

            # drop the column
            df.drop(columns=[column], inplace=True)
            continue

        # check what kind of data from the mappings is in the column
        machine_data = series[
            series.apply(lambda x: any(name in str(x) for name in machine_names))
        ]
        product_data = series[
            series.apply(lambda x: any(name in str(x) for name in product_names))
        ]

        if machine_data.shape[0] > 0:
            # print(f"Column {column} has {machine_data.shape[0]} machine names")
            name = "machine_name"
        elif product_data.shape[0] > 0:
            # print(f"Column {column} has {product_data.shape[0]} product names")
            name = "product_name"
        elif pd.api.types.is_numeric_dtype(series):
            name = "result"

        # change the column name to the machine name, product name
        # if the column name already exists, add a number to the end of the column name
        if name in df.columns:
            df.rename(
                columns={column: f"{name}_{random.randint(0, 1000)}"},
                inplace=True,
            )
        else:
            df.rename(columns={column: name}, inplace=True)

    return df


if __name__ == "__main__":
    files = os.listdir("./texts")

    for file in files:
        print(file)
        if file.endswith(".txt"):
            continue
        results = process_table("./texts/" + file)
        if results is None:
            continue
        results.to_csv(f"./processed_tables/{file}")
