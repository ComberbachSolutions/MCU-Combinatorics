# Function (Interchangeable)
#   eg. ADC
# Sub Function (Interchangeable/Specific)
#   eg. ADC0 or ADC1
# Channel (Specific)
#   AN001, AN002, AN100, etc

ExamplePin = [["Pin Number", {"GPIO":{"P500":["Read",], }, }], ]

MCU_Pins = [
    {
        "GPIO":
        {
            "P500":
            [
                "Read",
                "Write",
            ],
        },
        "GPT":
        {
            "GTIOC11":
            [
                "A",
            ],
        },
        "ADC":
        {
            "ADC0":
            [
                "AN016",
            ],
        },
    },
    {
        "GPIO":
        {
            "P014":
            [
                "Read",
                "Write",
            ],
        },
        "ADC":
        {
            "ADC0":
            [
                "AN005",
            ],
            "ADC1":
            [
                "AN105",
            ],
        },
    },
    {
        "GPIO":
        {
            "P007":
            [
                "Read",
            ],
        },
        "ADC":
        {
            "PGAVSS":
            [
                "PGAVSS100",
            ],
            "ADC1":
            [
                "AN107",
            ],
        },
    },
    {
        "Feature DeleteMe Eventually":
        {
            "Subfeature DeleteMe":
            [
                "DeleteMe"
            ],
        },
        "Feature DeleteMe":
        {
            "Subfeature DeleteMe":
            [
                "DeleteMe"
            ],
        },
    },
]

Requirements = {
    "Indoor Temperature Signal":
    {
        "ADC":
        {
            "ADC0":[""],
            "ADC1":[""],
        },
    },
    "Air Damper 1 Tach Signal":
    {
        "ADC":
        {
            "ADC0":["",],
            "ADC1":["",],
        },
    },
    "Grundfos 2 Pressure Signal":
    {
        "ADC":
        {
            "ADC0":["AN005",],
            "ADC1":["AN105",],
        },
        "GPIO":
        {
            "":["Write",]
        },
    },
}

def Remove_Channel(ChannelMap, Channel):
    ChannelMap.remove(Channel)

def Remove_Subfeature(SubfeatureMap, SubFeature):
    del SubfeatureMap[SubFeature]

def Remove_Feature(PinMap, Feature):
    del PinMap[Feature]

def Remove_Pin(PinMap, Pin):
    PinMap.remove(Pin)

def Generate_Requirement(Requirements):
    for NetName in Requirements:
        for RequiredFeature in Requirements[NetName]:
            for RequiredSubfeature in Requirements[NetName][RequiredFeature]:
                for RequiredChannel in Requirements[NetName][RequiredFeature][RequiredSubfeature]:
                    yield NetName, RequiredFeature, RequiredSubfeature, RequiredChannel

def Generate_Pin_Mappings(PinMap):
    for PinNumber, Pin in enumerate(PinMap):
        for Feature in Pin:
            for Subfeature in Pin[Feature]:
                for Channel in Pin[Feature][Subfeature]:
                    yield [PinNumber, Feature, Subfeature, Channel]

def Find_Valid_Pins_For_Nets(Requirements, Pins):
    ValidPins = {}
    for NetName in Requirements:
        ValidPins[NetName] = []

    for NetName, RequiredFeature, RequiredSubfeature, RequiredChannel in Generate_Requirement(Requirements):
        for PinNumber, Features in enumerate(Pins):
            for Feature, SubFeatures in Features.items():
                if Feature != RequiredFeature:
                    continue
                for SubFeature, Channels in SubFeatures.items():
                    if SubFeature != RequiredSubfeature and RequiredSubfeature != "":
                        continue
                    for Channel in Channels:
                        if Channel != RequiredChannel and RequiredChannel != "":
                            continue
                        ValidPins[NetName].append([PinNumber, Feature, SubFeature, Channel])

    for Net in ValidPins:
        if len(ValidPins[Net]) == 0:
            print("*"*50)
            print(f"Net '{NetName}' does not have any valid pins available to it")
            print("*"*50)

    return ValidPins

def Print_Pin_Map(PinMap):
    for PinNumber, Pin in enumerate(PinMap):
        for Feature in Pin:
            for Subfeature in Pin[Feature]:
                for Channel in Pin[Feature][Subfeature]:
                    print(f"Pin {PinNumber}\tFeature {Feature}\t{Subfeature}\tChannel {Channel}")

def Print_Solutions(Solutions):
    for NetSolutions in Solutions:
        for Solution in Solutions[NetSolutions]:
            print(f"{NetSolutions} {Solution}")

def Prune_Pin_Map(Solutions, PinMap):
    NewPinMap = []
    for PinNumber, Pin in enumerate(PinMap):
        for Feature in Pin:
            for Subfeature in Pin[Feature]:
                for Channel in Pin[Feature][Subfeature]:
                    KnownSolution = [PinNumber, Feature, Subfeature, Channel]
                    for PinMapping in Generate_Pin_Mappings(MCU_Pins):
                        if KnownSolution == PinMapping:
                            NewPinMap.append()
    print(NewPinMap)
    return NewPinMap

MySolutions = Find_Valid_Pins_For_Nets(Requirements, MCU_Pins)
# Print_Pin_Map(MCU_Pins)
# print("*"*50)
# Print_Solutions(MySolutions)
Prune_Pin_Map(MySolutions, MCU_Pins)
