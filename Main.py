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
    "Pin Deleteable":
    {
        "Feature DeleteMe Eventually":
        {
            "Subfeature":
            {
                "Channel":""
            },
        },
        "Feature DeleteMe":
        {
            "Subfeature DeleteMe":
            {
                "DeleteMe":"",
                "Channel":"",
            },
        },
    },
}

Requirements = {
    "Indoor Temperature Signal":
    {
        "ADC":
        {
            "ADC0":
            [
                ""
            ],
        },
    },
    "Air Damper 1 Tach Signal":
    {
        "ADC":
        {
            "ADC1":
            [
                "",
            ],
        },
    },
    "Grundfos 2 Pressure Signal":
    {
        "GPIO":
        {
            "":
            [
                "Write",
            ]
        },
    },
}

def Remove_Channel(ChannelMap, Channel):
    ChannelMap.remove(Channel)

def Remove_Subfeature(SubfeatureMap, SubFeature):
    del SubfeatureMap[SubFeature]

def Remove_Feature(PinMap, Feature):
    del PinMap[Feature]

def Remove_Pin(PinMaps, Pin):
    del PinMaps[Pin]

def Generate_Requirement(Requirements):
    for NetName in Requirements:
        for RequiredFeature in Requirements[NetName]:
            for RequiredSubfeature in Requirements[NetName][RequiredFeature]:
                for RequiredChannel in Requirements[NetName][RequiredFeature][RequiredSubfeature]:
                    yield NetName, RequiredFeature, RequiredSubfeature, RequiredChannel

def Generate_Pin_Mappings(PinMaps):
    for PinName, Features in PinMaps.items():
        for Feature, Subfeatures in Features.items():
            for Subfeature, Channels in Subfeatures.items():
                for Channel in Channels:
                    yield [PinName, Feature, Subfeature, Channel]

def Find_Valid_Pins_For_Nets(Requirements, PinMaps):
    ValidPins = {}
    for NetName in Requirements:
        ValidPins[NetName] = []
    for NetName, RequiredFeature, RequiredSubfeature, RequiredChannel in Generate_Requirement(Requirements):
        for PinName, Features in PinMaps.items():
            for Feature, Subfeatures in Features.items():
                if Feature != RequiredFeature:
                    continue
                for Subfeature, Channels in Subfeatures.items():
                    if Subfeature != RequiredSubfeature and RequiredSubfeature != "":
                        continue
                    for Channel in Channels:
                        if Channel != RequiredChannel and RequiredChannel != "":
                            continue
                        ValidPins[NetName].append([PinName, Feature, Subfeature, Channel])
    for Net in ValidPins:
        if len(ValidPins[Net]) == 0:
            print("*"*50)
            print(f"Net '{NetName}' does not have any valid pins available to it")
            print("*"*50)
    return ValidPins

def Print_Pin_Map(PinMaps):
    for PinName, Features in PinMaps.items():
        for Feature, Subfeatures in Features.items():
            for Subfeature, Channels in Subfeatures.items():
                for Channel in Channels:
                    print(f"{[PinName, Feature, Subfeature, Channel]}")

def Print_Solutions(Solutions):
    for NetName in Solutions:
        for AvailablePin in Solutions[NetName]:
            print(f"{NetName}\t{AvailablePin}")

def Print_Full_Solution(outputs):
    print("*"*50)
    for index, output in enumerate(outputs):
        test = set()
        for net, pin in output.items():
            test.add(pin[0])
            print(f"{net}\t{pin}")
        print("*"*50)

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

def Another_Way(MultiDict, CurrentPath=[]):
    Paths = []
    for Key, Value in MultiDict.items():
        new_path = CurrentPath + [Key]
        if isinstance(Value, dict):
            Paths.extend(Another_Way(Value, new_path))
        elif Value != "":
            Paths.append(new_path + [Value])
        else:
            Paths.append(new_path)
    return Paths

# MySolutions = Find_Valid_Pins_For_Nets(Requirements, MCU_Pins)
# ValidSolutions = Find_All_Valid_Solutions(MySolutions)
# Print_Full_Solution(ValidSolutions)

durp = Another_Way(MCU_Pins)
print(durp)