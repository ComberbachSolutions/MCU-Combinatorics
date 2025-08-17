# Ideas for future functionality:
#   Add "NotFeature", "NotSubfeature", and "NotChannel" functionality
#       Specify functionality which must be avoided
#   Add "MustMatchFeature", "MustMatchSubfeature", and "MustMatchChannel" functionality
#       This can be used to keep matched nets on the same feature/subfeature/channel

from itertools import product
import ImportFromCSV
from math import prod
import time
# import cProfile
# import pstats



ITERATIONS_PER_SECOND = 695251

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

def product_size(iterables):
    """
    Return the number of results itertools.product(*iterables) would yield,
    without actually generating them.
    """
    lengths = [len(list(it)) for it in iterables]  # convert if not sized
    if not lengths:
        return 1  # product of zero iterables = 1 (empty tuple)
    if any(L == 0 for L in lengths):
        return 0
    return prod(lengths)

def Generate_Next_Solution(SolutionList):
    # Check for empty values and return immediately if found
    if any(not value for value in SolutionList.values()):
        print("Error in data")
        return []
    SearchSpace = product_size(SolutionList.values())
    print(f"{SearchSpace} iterations or...\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND} seconds\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/60} minutes\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600} hours\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24} days\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/7} weeks\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/31} months\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/365.24} years\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/365.24/10} decades\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/365.24/100} centuries\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/365.24/1000} milleniums\n \
          {product_size(SolutionList.values())/ITERATIONS_PER_SECOND/3600/24/365.24/1000000} eons"
          )
    input("Are you sure you want to continue? Press Enter to continue...")
    print("Yeehaw, let's goooooo!")
    for combo in product(*SolutionList.values()):
        yield dict(zip(SolutionList.keys(), combo))

def Find_A_Valid_Solution(Definitions, Requirements):
    SolutionList = Find_Potential_Solutions(Definitions, Requirements)
    solution = find_unique_solution(SolutionList)
    return solution

def find_unique_solution(nets):
    def backtrack(solution, nets_keys, used_pins, index=0):
        """Recursive function to find a valid solution."""
        # Base case: if the solution includes all nets, return True
        if index == len(nets_keys):
            return True
        print(f"Solving for pin: {index}")
        net = nets_keys[index]
        for pin in nets[net]:
            if pin[0] not in used_pins:  # Check if pin is not already used
                solution[net] = pin
                used_pins.add(pin[0])  # Mark pin as used
                
                if backtrack(solution, nets_keys, used_pins, index + 1):
                    return True
                
                # Backtrack: remove the last pin added to the solution and mark it as unused
                del solution[net]
                used_pins.remove(pin[0])
        
        return False

    solution = {}
    used_pins = set()  # Keep track of used pins to avoid duplicates
    nets_keys = list(nets.keys())
    if backtrack(solution, nets_keys, used_pins):
        return solution
    else:
        return None  # No valid solution found








def Find_All_Valid_Solutions(Definitions, Requirements):
    AllSolutions = []
    print(f"{'*'*36} Start {'*'*37}")
    SolutionList = Find_Potential_Solutions(Definitions, Requirements)
    print(f"{'*'*24} Find_Potential_Solutions Done {'*'*25}")
    Count = 0
    timer = time.time()
    for PotentialSolution in Generate_Next_Solution(SolutionList):
        Count += 1
        if Count % 65536 == 0:
            if time.time() - timer >= 1:
                timer = time.time()
                print(f"Iterations = {Count:,}\tSolutions = {len(AllSolutions)}")
        if Solution_Is_Valid(PotentialSolution) == True:
            AllSolutions.append(PotentialSolution)
            # print(AllSolutions)
    print(f"{'*'*24} Find_All_Valid_Solutions Done {'*'*25}")
    return AllSolutions

def Print_Full_Solution_List(outputs):
    for index, output in enumerate(outputs):
        print(f"{'*'*34} Option {index} {'*'*34}")
        # Directly sort by Pin Number and iterate through items for printing
        for net, pin in sorted(output.items(), key=lambda item: item[1][0]):
            print(f"{net}\t{pin}")
    print("*"*80)

def Solution_Is_Valid(potential_solution):
    seen_pins = set()
    for net, pin in potential_solution.items():
        if pin[0] in seen_pins:
            return False  # Early termination on finding a duplicate
        seen_pins.add(pin[0])
    return True  # If no duplicates found, the solution is valid


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
    ValidSolutions = Find_All_Valid_Solutions(Definitions, Requirements)

if __name__ == '__main__':
    # ValidSolutions = Find_A_Valid_Solution(Definitions, Requirements)

    # CorrectSolution = [{'Net1': ['Pin 1', 'ADC', 'ADC0', '0'], 'Net2': ['Pin 2', 'ADC', 'ADC1', '0'], 'Net3': ['Pin 3', 'GPIO', 'Port0', '3', 'Read']}, {'Net1': ['Pin 1', 'ADC', 'ADC0', '0'], 'Net2': ['Pin 3', 'ADC', 'ADC1', '1'], 'Net3': ['Pin 2', 'GPIO', 'Port0', '1', 'Read']}];
    # ValidSolutions = Find_All_Valid_Solutions(Definitions, Requirements)
    # if ValidSolutions == CorrectSolution:
    #     print("Passed"*100)
    # else:
    #     print("Failed"*100)
    # Print_Full_Solution_List(ValidSolutions)
    # print(f"{'*'*35} Fin Done {'*'*35}")

    ImportFromCSV.convert_CSV_to_JSON("RA6M3 LQFP176 Pinout")
    ImportFromCSV.convert_CSV_to_JSON("MCU Requirements")
    Definitions = ImportFromCSV.read_dict_from_file("RA6M3 LQFP176 Pinout.JSON")
    Requirements = ImportFromCSV.read_dict_from_file("MCU Requirements.JSON")

    # profile = cProfile.Profile()
    # profile.runctx("Function_To_Test()", globals(), locals())
    # ps = pstats.Stats(profile)
    # ps.sort_stats('tottime')
    # ps.print_stats()

    # ValidSolutions = Find_A_Valid_Solution(Definitions, Requirements)
    # print(f"->{ValidSolutions}")

    ValidSolutions = Find_All_Valid_Solutions(Definitions, Requirements)
    Print_Full_Solution_List(ValidSolutions)
    print(f"{'*'*35} Fin Done {'*'*35}")
