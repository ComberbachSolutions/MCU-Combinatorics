# Ideas for future functionality:
#   Add "NotFeature", "NotSubfeature", and "NotChannel" functionality
#       Specify functionality which must be avoided
#   Add "MustMatchFeature", "MustMatchSubfeature", and "MustMatchChannel" functionality
#       This can be used to keep matched nets on the same feature/subfeature/channel

from itertools import product
import ImportFromCSV
from concurrent.futures import ProcessPoolExecutor, as_completed
import cProfile
import pstats



# These are used for testing only
Requirements = {
    "Net1":
    {
        "ADC":
        {
            "ADC0":
            {
                "":"",
            },
        },
    },
    "Net2":
    {
        "ADC":
        {
            "":"",
        },
    },
    "Net3":
    {
        "GPIO":
        {
            "":
            {
                "":
                {
                    "Read":"",
                }
            },
        },
    },
}

Definitions = {
    "Pin 1":
    {
        "GPIO":
        {
            "Port0":
            {
                "0":
                {
                    "Read":"",
                    "Write":"",
                }
            },
        },
        "ADC":
        {
            "ADC0":
            {
                "0":"",
            },
        },
    },
    "Pin 2":
    {
     "GPIO":
        {
            "Port0":
            {
                "1":
                {
                    "Read":"",
                    "Write":"",
                }
            },
        },
        "ADC":
        {
            "ADC1":
            {
                "0":"",
            },
        },
    },
    "Pin 3":
    {
        "GPIO":
        {
            "Port0":
            {
                "3":
                {
                    "Read":"",
                }
            },
        },
        "ADC":
        {
            "ADC1":
            {
                "0":"",
            },
            "ADC1":
            {
                "1":"",
            },
        },
    },
}

def Expand_Dictionary(Multidictionary, CurrentPath=[]):
    # This is a recursive function that reduces a dictionary of dictionaries to a list of all the key values along each path
    Paths = []
    for Key, Value in Multidictionary.items():
        new_path = CurrentPath + [Key]
        if isinstance(Value, dict):
            Paths.extend(Expand_Dictionary(Value, new_path))
        elif Value != "":
            Paths.append(new_path + [Value])
        else:
            Paths.append(new_path)
    return Paths

def Definition_Satisfies_Requirement(Definition, Requirement):
    # First element is the Definition and Requirement IDs, ignore these for matching purposes
    Definition = Definition[1:]
    Requirement = Requirement[1:]
    
    # Search only to a depth of the shortest list
    ShortestList = min(len(Definition), len(Requirement))
    
    # Compare Definitions to Requirements
    for Index in range(ShortestList):
        # The empty string "" is a wildcard match
        if Definition[Index] != Requirement[Index] and \
            "" not in (Definition[Index], Requirement[Index]):
            # The Definition does not meet the Requirement
                return False
    # The Definition meets the Requirement
    return True

def Find_Potential_Solutions(Definitions, Requirements):
    Definitions = Expand_Dictionary(Definitions)
    Requirements = Expand_Dictionary(Requirements)
    PinSolutions = {}
    for Requirement in Requirements:
        # Check if the requirement ID already exists in the solutions dictionary
        if Requirement[0] not in PinSolutions:
            PinSolutions[Requirement[0]] = []
        for Definition in Definitions:
            if Definition_Satisfies_Requirement(Definition, Requirement) == True:
                PinSolutions[Requirement[0]].append(Definition)
    return PinSolutions

def Generate_Next_Solution(SolutionList):
    ErrorInData = False
    for Key, Value in SolutionList.items():
        if Value == []:
            print(f"Error on {Key} - {Value}")
            ErrorInData = True
    if ErrorInData == True:
        return []
    Count = 0
    for combo in product(*SolutionList.values()):
        Count += 1
        if Count % 10000 == 0:
            print(Count)
            break
        yield {key: value for key, value in zip(SolutionList.keys(), combo)}

def Find_All_Valid_Solutions(Definitions, Requirements):
    AllSolutions = []
    print(f"{'*'*36} Start {'*'*37}")
    SolutionList = Find_Potential_Solutions(Definitions, Requirements)
    print(f"{'*'*24} Find_Potential_Solutions Done {'*'*25}")
    for PotentialSolution in Generate_Next_Solution(SolutionList):
        if Solution_Is_Valid(PotentialSolution) == True:
            AllSolutions.append(PotentialSolution)
            print(AllSolutions)
    print(f"{'*'*24} Find_All_Valid_Solutions Done {'*'*25}")
    return AllSolutions

def Print_Full_Solution_List(outputs):
    for index, output in enumerate(outputs):
        print(f"{'*'*34} Option {index} {'*'*34}")
        # Directly sort by Pin Number and iterate through items for printing
        for net, pin in sorted(output.items(), key=lambda item: item[1][0]):
            print(f"{net}\t{pin}")
    print("*"*80)

def Solution_Is_Valid(PotentialSolution):
    SolutionValidityTest = []
    for net, pin in PotentialSolution.items():
        SolutionValidityTest += [pin[0]]
    if len(SolutionValidityTest) == len(set(SolutionValidityTest)):
        return True
    else:
        return False

def continuous_generate_and_validate_solutions(Definitions, Requirements):
    AllSolutions = []
    print(f"{'*'*36} Start {'*'*37}")
    SolutionList = Find_Potential_Solutions(Definitions, Requirements)
    print(f"{'*'*24} Find_Potential_Solutions Done {'*'*25}")
    
    # Initialize ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        # Create a future-to-solution mapping
        future_to_solution = {}
        
        # Submit potential solutions for validation as they are generated
        for PotentialSolution in Generate_Next_Solution(SolutionList):
            future = executor.submit(Solution_Is_Valid, PotentialSolution)
            future_to_solution[future] = PotentialSolution
        
        # Collect and store valid solutions
        for future in as_completed(future_to_solution):
            if future.result():
                valid_solution = future_to_solution[future]
                AllSolutions.append(valid_solution)
                print(valid_solution)
    
    print(f"{'*'*24} Find_All_Valid_Solutions Done {'*'*25}")
    return AllSolutions

def Function_To_Test():
    # ValidSolutions = continuous_generate_and_validate_solutions(Definitions, Requirements)
    ValidSolutions = Find_All_Valid_Solutions(Definitions, Requirements)
    Print_Full_Solution_List(ValidSolutions)
    print(f"{'*'*35} Fin Done {'*'*35}")


if __name__ == '__main__':
    Function_To_Test()

    Definitions = ImportFromCSV.read_dict_from_file("RA6M3 LQFP176 Pinout.JSON")
    Requirements = ImportFromCSV.read_dict_from_file("MUA Requirements.JSON")

    profile = cProfile.Profile()
    profile.runctx("Function_To_Test()", globals(), locals())
    ps = pstats.Stats(profile)
    ps.sort_stats('tottime')
    ps.print_stats()

    # Function_To_Test()
