# Ideas for future functionality:
#   Add "NotFeature", "NotSubfeature", and "NotChannel" functionality
#       Specify functionality which must be avoided
#   Add "MustMatchFeature", "MustMatchSubfeature", and "MustMatchChannel" functionality
#       This can be used to keep matched nets on the same feature/subfeature/channel

from itertools import product
import ImportFromCSV



Definitions = ImportFromCSV.read_dict_from_file("RA6M3 LQFP176 Pinout.JSON")

Requirements = ImportFromCSV.read_dict_from_file("MUA Requirements.JSON")

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

def Find_All_Solutions(SolutionList):
    ErrorInData = False
    for Key, Value in SolutionList.items():
        if Value == []:
            print(f"Error on {Key} - {Value}")
            ErrorInData = True
    if ErrorInData == True:
        return []
    combinations = list(product(*SolutionList.values()))
    return [{key: value for key, value in zip(SolutionList.keys(), combo)} for combo in combinations]

def Find_All_Valid_Solutions(Definitions, Requirements):
    SolutionList = Find_Potential_Solutions(Definitions, Requirements)
    AllSolutions = Find_All_Solutions(SolutionList)
    for PotentialSolution in reversed(AllSolutions):
        SolutionValidityTest = []
        for net, pin in PotentialSolution.items():
            SolutionValidityTest.extend([pin[0]])
        if len(SolutionValidityTest) != len(set(SolutionValidityTest)):
            AllSolutions.remove(PotentialSolution)
    return AllSolutions

def Print_Full_Solution_List(outputs):
    for index, output in enumerate(outputs):
        print(f"{'*'*25} Option {index} {'*'*25}")
        test = set()
        for net, pin in output.items():
            test.add(pin[0])
            print(f"{net}\t{pin}")
    print("*"*50)

ValidSolutions = Find_All_Valid_Solutions(Definitions, Requirements)
Print_Full_Solution_List(ValidSolutions)
