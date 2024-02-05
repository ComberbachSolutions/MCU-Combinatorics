# Ideas for future functionality:
#   Add "NotFeature", "NotSubfeature", and "NotChannel" functionality
#       Specify functionality which must be avoided
#   Add "MustMatchFeature", "MustMatchSubfeature", and "MustMatchChannel" functionality
#       This can be used to keep matched nets on the same feature/subfeature/channel

from itertools import product

ExamplePin = {
    "Pin Unique ID":
    {
        "Feature":
        {
            "Subfeature":
            {
                "Channel":
                {
                    "Subchannel":"",
                },
            },
        },
    },
}

ExampleRequirements = {
    "Net Name":
    {
        "Feature":
        {
            "Subfeature":
            {
                "Channel":
                {
                    "Subchannel":"",
                },
            },
        },
    },
}

Definitions = {
    "Pin 140":
    {
        "GPIO":
        {
            "P500":
            {
                "Read":"",
                "Write":"",
            },
        },
        "GPT":
        {
            "GTIOC11":
            {
                "A":"",
            },
        },
        "ADC":
        {
            "ADC0":
            {
                "AN016":"",
            },
        },
    },
    "Pin 152":
    {
        "GPIO":
        {
            "P014":
            {
                "Read":"",
                "Write":"",
            },
        },
        "ADC":
        {
            "ADC0":
            {
                "AN005":"",
            },
            "ADC1":
            {
                "AN105":"",
            },
        },
    },
    "Pin 162":
    {
        "GPIO":
        {
            "P007":
            {
                "Read":"",
            },
        },
        "ADC":
        {
            "PGAVSS":
            {
                "PGAVSS100":"",
            },
            "ADC1":
            {
                "AN107":"",
            },
        },
    },
}

Requirements = {
    "Indoor Temperature Signal":
    {
        "ADC":
        {
            "ADC0":""
        },
    },
    "Air Damper 1 Tach Signal":
    {
        "ADC":
        {
            "ADC1":""
        },
    },
    "Grundfos 2 Pressure Signal":
    {
        "GPIO":
        {
            "":
            {
                "Write":"",
            }
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
    # First element is the Definition and Requirment IDs, ignore these for matching purposes
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
    PinSolutions = {}
    for Requirement in Requirements:
        PinSolutions[Requirement[0]] = []
        for Definition in Definitions:
            if Definition_Satisfies_Requirement(Definition, Requirement) == True:
                PinSolutions[Requirement[0]].append(Definition)
    return PinSolutions

def Find_All_Solutions(SolutionList):
    combinations = list(product(*SolutionList.values()))
    return [{key: value for key, value in zip(SolutionList.keys(), combo)} for combo in combinations]

def Find_All_Valid_Solutions(SolutionList):
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

Definitions = Expand_Dictionary(Definitions)
Requirements = Expand_Dictionary(Requirements)
PotentialSolutions = Find_Potential_Solutions(Definitions, Requirements)
ValidSolutions = Find_All_Valid_Solutions(PotentialSolutions)
Print_Full_Solution_List(ValidSolutions)
