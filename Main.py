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

Requirements = ["Feature 1", "Feature 1", "Feature 1"]
Solution = []
WorkingSolution = MCU_Pins.copy()

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

def Solve(Requirements, Pins):
    for PinNumber, Features in enumerate(Pins):
        print(f"Pin {PinNumber} has these features")
        for Feature, SubFeatures in Features.items():
            print(f"\t{Feature} has these Subfeatures")
            for SubFeature, Channels in SubFeatures.items():
                print(f"\t\t{SubFeature} has these channels")
                for Channel in Channels:
                    if Channel != "":
                        print(f"\t\t\t{Channel}")
def Remove_Channel(PinMap, Feature, SubFeature, Channel):
    PinMap[Feature][SubFeature].remove(Channel)

def Remove_Channel(ChannelMap, Channel):
    ChannelMap.remove(Channel)

def Remove_Subfeature(SubfeatureMap, SubFeature):
    del SubfeatureMap[SubFeature]

def Remove_Feature(PinMap, Feature):
    del PinMap[Feature]

def Remove_Pin(PinMap, Pin):
    PinMap.remove(Pin)

print("*"*50)
print(MCU_Pins[3])
Remove_Channel(MCU_Pins[3]["Feature DeleteMe"]["Subfeature DeleteMe"], "DeleteMe")
print(MCU_Pins[3])
print("*"*50)
print(MCU_Pins[3])
Remove_Subfeature(MCU_Pins[3]["Feature DeleteMe"], "Subfeature DeleteMe")
print(MCU_Pins[3])
print("*"*50)
print(MCU_Pins[3])
Remove_Feature(MCU_Pins[3], "Feature DeleteMe")
print(MCU_Pins[3])
print("*"*50)
print(MCU_Pins)
Remove_Feature(MCU_Pins, 3)
print(MCU_Pins)
print("*"*50)

Solve(Requirements, MCU_Pins)
print(f"Combinations {Number_Of_Potential_Combinations(MCU_Pins)}")
