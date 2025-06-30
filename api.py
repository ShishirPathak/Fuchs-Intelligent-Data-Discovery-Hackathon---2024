from openai import AzureOpenAI
from dotenv import load_dotenv
import os

gpt4o_endpoint = os.getenv("GPT4O_ENDPOINT")
gpt4o_key = os.getenv("GPT4O_KEY")

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI model and client configuration
model_name = "gpt-4o-2024-08-06"
client = AzureOpenAI(
    azure_endpoint=gpt4o_endpoint,
    api_key=gpt4o_key,
    api_version="2024-02-01",  # Required by AzureOpenAI
)


def openai_prompt_response(prompt):
    """
    Function to generate a response from the Azure OpenAI API.

    Parameters:
    - prompt (str): The input text prompt for the model.

    Returns:
    - response_text (str): The generated text from the Azure OpenAI API.
    """
    try:
        # Call the Azure OpenAI API for chat completions
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract and return the generated text
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Error generating text: {e}")
        return None


def openai_sequence_response(prompt_list):
    """
    Function to generate a response from the Azure OpenAI API.

    Parameters:
    - prompt (str): The input text prompt for the model.

    Returns:
    - response_text (str): The generated text from the Azure OpenAI API.
    """
    try:
        # Call the Azure OpenAI API for chat completions
        response = client.chat.completions.create(
            model=model_name, messages=prompt_list
        )

        # Extract and return the generated text
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Error generating text: {e}")
        return None


# Example of a single prompt
example_prompt = "Hello, tell me about yourself"


p1 = "⁠I have some csv files. These files are the results of an experiment. There might be multiple experiments in a csv file. For an experiment, there are some parameters. These parameters are, machine name used in the experiment, ingredients used in the experiment, result of the experiment and the unit of the result. All of these parameters can be limited things. Now I am going to share the machine types, ingredient types and unit types with you. You are going to read and understand them, then I am going to give you a csv file so that you can  extract the machine types, ingredients, result and unit types. Okay? ⁠"
p2 = """machine_id,machine_name
0,Centrifuge X100
1,Spectrometer Alpha-300
2,Thermocycler TC-5000
3,Microplate Reader MRX
4,Gas Chromatograph GC-2010
5,Liquid Chromatograph LC-400
6,Mass Spectrometer MS-20
7,pH Meter PH-700
8,Conductivity Meter CM-215
9,UV-Vis Spectrophotometer UV-2600
10,HPLC System HPLC-9000
11,FTIR Spectrometer FTIR-8400
12,NMR Spectrometer NMR-500
13,X-Ray Diffractometer XRD-6000
14,Rheometer R-4500
15,Titrator T-905
16,PCR Machine PCR-96
17,Ion Chromatograph IC-2100
18,Four Ball FB-1000
19,Viscometer VS-300

These are the machine types and their ids ⁠"""
p3 = """
these are the ingredients or product types and their ids

product_id,product_name
0,Jojoba Oil
1,Beeswax
2,Gum
3,Cetyl Alcohol
4,Vitamin E
5,Glycerin
6,Coconut Oil
7,Almond Oil ⁠
"""

p4 = """
These are the unit types and their ids:
unit_id,unit
0,C
1,mM
2,ppm
3,1/cm
4,mg/L
5,cP
6,m/z
7,pH
8,Abs
9,mm
10,nm
11,ug/mL
12,Pa-s
13,Ct
14,uS/cm
15,OD
16,RPM
17,M
18,[4-99]
19,Abs.
20,[400-4000]
21,[0.0-4.0]
22,[0-20]
23,[0-180]
24,[0.001-10]
25,[0-2000]
26,[0-14]
27,[0-40]
28,[0.200-1.000]
29,[0.01-1000]
30,[0.1-1000]
31,[0.001-100]
32,[190-1100]
33,[0.01-500]
34,[0.200 - 1.000]
35,[0-3.5]
36,[50-2000]
37,[1000-15000]
"""
p5 = """
Please provide the machine type, ingredients, result and units with a csv format. Note that first row is going to be the column names, although  those column names might give you an idea of which is which, do not be limited to them. Only thing you need to extract the relevant information and give it in this format:

machine_type, ingredient1, ingredient2, ingredient3, result, unit

if there are more than 3 ingredients, pick 3. Also, you don't need to write code, you can do it by yourself. ⁠ Please do not provide any comments, explanations or anything else. Just the csv file.
"""

p6 = """
Here is the csv file:

Instrument,Primary Substance,Additional Ingredients,Condition Value,Unit,Remarks
Thermocycler TC-5000,Almond Oil,"Gum, Vitamin E",25.0,C,Slight phase separation noted
Ion Chromatograph IC-2100,Almond Oil,"Cetyl Alcohol, Glycerin",50.0,mM,High-resolution peaks detected
NMR Spectrometer NMR-500,Almond Oil,nan,15.0,ppm,Nuclear resonance observed moderately
FTIR Spectrometer FTIR-8400,Almond Oil,Glycerin,350.0,1/cm,Sharp absorption bands evident
HPLC System HPLC-9000,Almond Oil,"Beeswax, Vitamin E",500.0,mg/L,Consistent retention time
X-Ray Diffractometer XRD-6000,Jojoba Oil,"Cetyl Alcohol, Vitamin E",100.0,C,Diffraction patterns well-resolved
Viscometer VS-300,Almond Oil,"Beeswax, Glycerin",7242.37,cP,High viscosity consistent with mixture
Viscometer VS-300,Coconut Oil,Cetyl Alcohol,5199.37,cP,"Slightly less viscous, even distribution"

"""

# Example of a prompt list with multiple steps
example_prompt_list = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "system", "content": "You are searching through documents."},
    {"role": "user", "content": p1},
    {"role": "assistant", "content": p2},
    {"role": "user", "content": p3},
    {"role": "assistant", "content": p4},
    {"role": "user", "content": p5},
    {"role": "user", "content": p6},
]


if __name__ == "__main__":
    files = os.listdir("../texts")

    for i, file in enumerate(files):
        print(f"{i+1}/{len(files)}")

        file_name = os.path.basename(file)
        if os.path.exists(f"../results_llm/{file_name}.csv"):
            continue

        with open(f"../texts/{file}", "r") as f:
            text = f.read()
            print(text)

        prompt_list = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You are searching through documents."},
            {"role": "user", "content": p1},
            {"role": "assistant", "content": p2},
            {"role": "user", "content": p3},
            {"role": "assistant", "content": p4},
            {"role": "user", "content": p5},
            {"role": "user", "content": "Here is the csv file: \n" + text},
        ]

        response = openai_sequence_response(prompt_list)
        if response is None:
            print(f"Error generating text for {file_name}")
            continue
        # save the response to a file
        file_name = os.path.basename(file)
        with open(f"../results_llm/{file_name}.csv", "w") as f:
            f.write(response)
