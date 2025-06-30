import pandas as pd
import os
import re

resulting_df = pd.DataFrame(
    columns=[
        "report_id",
        "machine_id",
        "ing_1_id",
        "ing_2_id",
        "ing_3_id",
        "result",
        "unit_id",
    ]
)

machine_mappings = pd.read_csv("./machine_mapping.csv")
product_mappings = pd.read_csv("./product_mapping.csv")

machine_dict = {name: idx for idx, name in enumerate(machine_mappings["machine_name"])}
product_dict = {name: idx for idx, name in enumerate(product_mappings["product_name"])}

print(product_dict)

things_to_strip = ['"', "", "(", ")", "[", "]", ".", ",", "!", "?"]

def strip_string(string):
    string = string.strip()
    for thing in things_to_strip:
        string = string.strip(thing)
    return string


def generate_rows(df, report_id):
    columns = df.columns
    new_rows = []
    for index, row in df.iterrows():
        new_row = {}
        new_row["report_id"] = report_id
        product_id = 1
        for column in columns:
            if "product_name" in column:
                if (
                    row[column] is not None
                    and row[column] != ""
                    and not pd.isna(row[column])
                ):
                    if product_id > 3:
                        print(f"More than 3 products found in {report_id}")
                        continue
                    
                    if row[column].find(",") != -1:
                        values = row[column].split(",")
                    elif row[column].count("+") > 0:
                        values = row[column].split("+")
                    else:
                        values = [row[column]]

                    for value in values:
                        # find the product_id in the product_mappings
                        value = strip_string(value)
                        if product_id > 3:
                            # print(f"More than 3 products found in {report_id}")
                            continue
                        if value != "" and value in product_dict:
                            new_row[f"ing_{product_id}_id"] = product_dict[value]
                            product_id += 1
                        else:
                            # print(f"Product {value} not found in product_mappings")
                            pass
            elif "machine_name" in column:
                if (
                    row[column] is not None
                    and row[column] != ""
                    and not pd.isna(row[column])
                ):
                    value = strip_string(row[column])
                    value = value.strip('"')
                    value = value
                    keys = machine_dict.keys()
                    # check if the value is inside the machine_dict keys
                    inkeys = [key for key in keys if value in key]

                    if value in machine_dict:
                        new_row["machine_id"] = machine_dict[value]
                    elif len(inkeys) > 0:
                        new_row["machine_id"] = machine_dict[inkeys[0]]
                    else:
                        print(f"Machine {value} not found in machine_mappings")
            elif "result" in column:
                if row[column] is not None and "result" not in new_row:
                    new_row["result"] = row[column]
                    new_row["unit_id"] = 0
        new_rows.append(new_row)
    return new_rows


if __name__ == "__main__":
    files = os.listdir("./processed_tables")
    # resulting_df = report_id, machine_id, product1_id, product2_id, product3_id,
    # result, unit

    for file in files:
        match = re.search(r"Report_(\d+)", file)
        if match:
            report_id = match.group(1)
        else:
            print(f"No match found for {file}")
            continue
        df = pd.read_csv(f"./processed_tables/{file}")
        rows = generate_rows(df, report_id)
        resulting_df = pd.concat([resulting_df, pd.DataFrame(rows)], ignore_index=True)

    # sort the resulting_df by report_id
    resulting_df = resulting_df.sort_values(by="report_id")
    resulting_df.to_csv("./results.csv", index=False)
