# Ideas for future functionality:
#   Add "NotFeature", "NotSubfeature", and "NotChannel" functionality
#       Specify functionality which must be avoided
#   Add "MustMatchFeature", "MustMatchSubfeature", and "MustMatchChannel" functionality
#       This can be used to keep matched nets on the same feature/subfeature/channel

# Function (Interchangeable)
#   eg. ADC
# Sub Function (Interchangeable/Specific)
#   eg. ADC0 or ADC1
# Channel (Specific)
#   AN001, AN002, AN100, etc
from itertools import product

ExamplePin = {
    "Pin Unique ID":
    {
        "Feature":
        {
            "Subfeature":
            {
                "Channel":"Subchannel",
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
                "Channel":"Subchannel"
            },
        },
    },
}

MCU_Pins = {
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

def Print_Titled_Section(text, section):
    print(f"{'*'*25}{text}{'*'*25}")
    print(section)

def Convert_Multidictionary_To_Lists(Multidictionary, CurrentPath=[]):
    Paths = []
    for Key, Value in Multidictionary.items():
        new_path = CurrentPath + [Key]
        if isinstance(Value, dict):
            Paths.extend(Convert_Multidictionary_To_Lists(Value, new_path))
        elif Value != "":
            Paths.append(new_path + [Value])
        else:
            Paths.append(new_path)
    return Paths

def compare_lists_ignore_first(list1, list2):
    # Exclude the first element from each list
    sublist1 = list1[1:]
    sublist2 = list2[1:]
    
    # Determine the length of the shorter list (excluding the first element)
    ShortestList = min(len(sublist1), len(sublist2))
    
    # Compare elements from the beginning to the shorter length
    for Index in range(ShortestList):
        # Treat "" as a wildcard match
        if sublist1[Index] != sublist2[Index] and "" not in (sublist1[Index], sublist2[Index]):
            return False

    # If we reach this point, all compared elements are considered matches,
    # and any extra elements in the longer list are automatically considered matches.
    return True

def Find_Potential_Solutions(Definitions, Requirements):
    PinSolutions = {}
    for Requirement in Requirements:
        PinSolutions[Requirement[0]] = []
        for Definition in Definitions:
            if compare_lists_ignore_first(Requirement, Definition) == True:
                PinSolutions[Requirement[0]].append(Definition)
                print("*"*50)
                print(Requirement)
                print(f"{Definition}")
    print("*"*50)
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

MCU_Pins = Convert_Multidictionary_To_Lists(MCU_Pins)
Requirements = Convert_Multidictionary_To_Lists(Requirements)
MySolutions = Find_Potential_Solutions(MCU_Pins, Requirements)
ValidSolutions = Find_All_Valid_Solutions(MySolutions)
print(ValidSolutions)

# *******************************************************
# Desired output, same string but formatted differently.
[{'Indoor Temperature Signal': ['Pin 140', 'ADC', 'ADC0', 'AN016'], 'Air Damper 1 Tach Signal': ['Pin 162', 'ADC', 'ADC1', 'AN107'], 'Grundfos 2 Pressure Signal': ['Pin 152', 'GPIO', 'P014', 'Write']}, {'Indoor Temperature Signal': ['Pin 152', 'ADC', 'ADC0', 'AN005'], 'Air Damper 1 Tach Signal': ['Pin 162', 'ADC', 'ADC1', 'AN107'], 'Grundfos 2 Pressure Signal': ['Pin 140', 'GPIO', 'P500', 'Write']}]
[
    {
        'Indoor Temperature Signal': ['Pin 140', 'ADC', 'ADC0', 'AN016'],
        'Air Damper 1 Tach Signal': ['Pin 162', 'ADC', 'ADC1', 'AN107'],
        'Grundfos 2 Pressure Signal': ['Pin 152', 'GPIO', 'P014', 'Write']
    },
    {
        'Indoor Temperature Signal': ['Pin 152', 'ADC', 'ADC0', 'AN005'],
        'Air Damper 1 Tach Signal': ['Pin 162', 'ADC', 'ADC1', 'AN107'],
        'Grundfos 2 Pressure Signal': ['Pin 140', 'GPIO', 'P500', 'Write']
    }
]
# *******************************************************

