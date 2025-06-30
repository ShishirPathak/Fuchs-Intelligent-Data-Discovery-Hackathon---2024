import os
import pandas as pd
import io
import re


machine_mapping = pd.read_csv("machine_mapping.csv")
product_mapping = pd.read_csv("product_mapping.csv")
unit_mapping = pd.read_csv("unit_mapping.csv")

machine_dict = {name: idx for idx, name in enumerate(machine_mapping["machine_name"])}
product_dict = {name: idx for idx, name in enumerate(product_mapping["product_name"])}
unit_dict = {name: idx for idx, name in enumerate(unit_mapping["unit"])}



def machine_type_to_id(str1):
    if str1 == "":
        return ""
    elif str1 not in machine_dict:
        print(str1)
        return ""
    else:
        return machine_dict[str1]


def product_type_to_id(str1):
    if str1 == "":
        return ""
    elif str1 not in product_dict:
        return ""
    else:
        return product_dict[str1]


def unit_type_to_id(str1):
    if str1 == "":
        return ""
    elif str1 not in unit_dict:
        return ""
    else:
        return unit_dict[str1]


def parse_result(str1):
    if type(str1) == int or type(str1) == float:
        return str1
    # find a number in the string and return it
    nums = re.findall(r"\d+\.\d+", str1)
    if len(nums) == 0:
        return ""
    else:
        return nums[0]


if __name__ == "__main__":
    # get all files in the results_llm folder
    files = os.listdir("results_llm")
    # read all files into a pandas dataframe
    error_counter = 0
    df = pd.DataFrame()
    counter = 0
    for i, file in enumerate(files):
        print(f"{i+1}/{len(files)}")

        # clean the ``` characters from the file before reading
        with open(f"results_llm/{file}", "r") as f:
            file_content = f.read()
        file_content = file_content.replace("```", "")
        file_content = file_content.strip("\n")
        file_content = file_content.strip("csv")

        try:
            file_df = pd.read_csv(io.StringIO(file_content), on_bad_lines="skip")
        except Exception as e:
            error_counter += 1
            print(f"Error count: {error_counter}")
            continue
        
        # add report_id to the dataframe
        match = re.search(r"Report_(\d+)", file)
        if match:
            report_id = match.group(1)
        else:
            print(f"No match found for {file}")
            continue
        file_df["report_id"] = report_id

        # read the file content into a pandas dataframe
        df = pd.concat([df, file_df])
        counter += 1
        
        # every 1000th files save the dataframe to a csv file
        if counter % 500 == 0:
            
            columns_to_check = [
                "machine_type",
                "ingredient1",
                "ingredient2",
                "ingredient3",
                "unit",
                "result",
                "report_id",
            ]
            # drop all columns that are not in the columns_to_check list
            df = df[columns_to_check]

            # apply the functions to the dataframe
            df["machine_type"] = df["machine_type"].apply(machine_type_to_id)
            df["ingredient1"] = df["ingredient1"].apply(product_type_to_id)
            df["ingredient2"] = df["ingredient2"].apply(product_type_to_id)
            df["ingredient3"] = df["ingredient3"].apply(product_type_to_id)
            df["unit"] = df["unit"].apply(unit_type_to_id)
            df["result"] = df["result"].apply(parse_result)

            # change the column names to the correct names for example: machine_type to machine_id
            df.rename(columns={"machine_type": "machine_id"}, inplace=True)
            df.rename(columns={"ingredient1": "ing_1_id"}, inplace=True)
            df.rename(columns={"ingredient2": "ing_2_id"}, inplace=True)
            df.rename(columns={"ingredient3": "ing_3_id"}, inplace=True)
            df.rename(columns={"unit": "unit_id"}, inplace=True)
            
            df.to_csv(f"llm_processed_results_{counter}_{len(files)}.csv", index=False)
            
            df = pd.DataFrame()
            
        
    columns_to_check = [
        "machine_type",
        "ingredient1",
        "ingredient2",
        "ingredient3",
        "unit",
        "result",
        "report_id",
    ]
    # drop all columns that are not in the columns_to_check list
    df = df[columns_to_check]

    # apply the functions to the dataframe
    df["machine_type"] = df["machine_type"].apply(machine_type_to_id)
    df["ingredient1"] = df["ingredient1"].apply(product_type_to_id)
    df["ingredient2"] = df["ingredient2"].apply(product_type_to_id)
    df["ingredient3"] = df["ingredient3"].apply(product_type_to_id)
    df["unit"] = df["unit"].apply(unit_type_to_id)
    df["result"] = df["result"].apply(parse_result)

    # change the column names to the correct names for example: machine_type to machine_id
    df.rename(columns={"machine_type": "machine_id"}, inplace=True)
    df.rename(columns={"ingredient1": "ing_1_id"}, inplace=True)
    df.rename(columns={"ingredient2": "ing_2_id"}, inplace=True)
    df.rename(columns={"ingredient3": "ing_3_id"}, inplace=True)
    df.rename(columns={"unit": "unit_id"}, inplace=True)

    print(df.head())
    print(df.columns)
    print(df.info())

    # save the dataframe to a csv file
    df.to_csv("llm_processed_results_final.csv", index=False)
