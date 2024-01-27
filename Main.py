# Function (Interchangeable)
#   eg. ADC
# Sub Function (Interchangeable/Specific)
#   eg. ADC0 or ADC1
# Channel (Specific)
#   AN001, AN002, AN100, etc

ExamplePin = {"ADC":{"ADC0":["AN001"], "ADC1":["AN001"]}, "GPT":{"GPT5":["A"]}}

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

Requirements = [
    [
        "Indoor Temperature Signal",
        "ADC",
        "",
        ""
    ],
    [
        "Air Damper 1 Tach Signal",
        "ADC",
        "",
        ""
    ],
    [
        "Grundfos 2 Pressure Signal",
        "ADC",
        "",
        ""
    ],
]

def Number_Of_Potential_Combinations(Pins):
    Count = 1
    for PinNumber, Features in enumerate(Pins):
        UniqueChannels = 0
        for Feature, SubFeatures in Features.items():
            for SubFeature, Channels in SubFeatures.items():
                for Channel in Channels:
                    UniqueChannels += 1
        Count *= UniqueChannels
    return Count

def Remove_Channel(ChannelMap, Channel):
    ChannelMap.remove(Channel)

def Remove_Subfeature(SubfeatureMap, SubFeature):
    del SubfeatureMap[SubFeature]

def Remove_Feature(PinMap, Feature):
    del PinMap[Feature]

def Remove_Pin(PinMap, Pin):
    PinMap.remove(Pin)

def Solve(Requirements, PinDefinition):
    Solutions = []
    for Attempt in range(Number_Of_Potential_Combinations(MCU_Pins)):
        print("*"*50)
        WorkingSolution = []
        Pins = PinDefinition.copy()
        for NetName, RequiredFeature, RequiredSubfeature, RequiredChannel in Requirements:
            for PinNumber, Features in enumerate(Pins):
                for Feature, SubFeatures in Features.items():
                    if Feature == RequiredFeature:
                        for SubFeature, Channels in SubFeatures.items():
                            if SubFeature == RequiredSubfeature or RequiredSubfeature == "":
                                for Channel in Channels:
                                    if Channel == RequiredChannel or RequiredChannel == "":
                                        WorkingSolution.append(f"{NetName} on Pin {PinNumber} using feature {Feature}, subfeature {SubFeature}, and channel {Channel}")
        Solutions.append(WorkingSolution)                            
    return Solutions

MySolutions = Solve(Requirements, MCU_Pins)
for Solution in MySolutions:
    for Pin in Solution:
        print(Pin)
    print("*"*50)
print(f"Combinations {Number_Of_Potential_Combinations(MCU_Pins)}")
