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
        ["ADC",],
        ["ADC0","ADC1",],
        ["",]
    ],
    [
        "Air Damper 1 Tach Signal",
        ["ADC",],
        ["ADC0","ADC1",],
        ["",]
    ],
    [
        "Grundfos 2 Pressure Signal",
        ["ADC",],
        ["ADC0","ADC1",],
        ["",]
    ],
]

def Remove_Channel(ChannelMap, Channel):
    ChannelMap.remove(Channel)

def Remove_Subfeature(SubfeatureMap, SubFeature):
    del SubfeatureMap[SubFeature]

def Remove_Feature(PinMap, Feature):
    del PinMap[Feature]

def Remove_Pin(PinMap, Pin):
    PinMap.remove(Pin)

def Generate_Requirement(Requirements):
    for NetName, RequiredFeatures, RequiredSubfeatures, RequiredChannels in Requirements:
        for RequiredFeature in RequiredFeatures:
            for RequiredSubfeature in RequiredSubfeatures:
                for RequiredChannel in RequiredChannels:
                    yield [NetName, RequiredFeature, RequiredSubfeature, RequiredChannel]

def Find_Valid_Pins_For_Nets(Requirements, PinDefinition):
    ValidPins = []
    Pins = PinDefinition.copy()
    for NetName, RequiredFeature, RequiredSubfeature, RequiredChannel in Generate_Requirement(Requirements):
        ValidOptions = 0
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
                        ValidPins.append(f"{NetName} on Pin {PinNumber} using feature {Feature}, subfeature {SubFeature}, and channel {Channel}")
                        ValidOptions += 1
        if ValidOptions == 0:
            print(f"Net {NetName} does not have any valid pins available to it")
    
    return ValidPins

MySolutions = Find_Valid_Pins_For_Nets(Requirements, MCU_Pins)
print("*"*50)
for Solution in MySolutions:
    print(Solution)
print("*"*50)
