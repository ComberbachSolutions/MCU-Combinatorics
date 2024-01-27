# Function (Interchangeable)
#   eg. ADC
# Sub Function (Interchangeable/Specific)
#   eg. ADC0 or ADC1
# Channel (Specific)
#   AN001, AN002, AN100, etc

ExamplePin = {"ADC":{"ADC0":["AN001"], "ADC1":["AN001"]}, "GPT":{"GPT5":["A"]}}

MCU_Pins = [
    {
        "Feature 1":
        {
            "Subfeature A":
            [
                ""
            ],
            "Subfeature B":
            [
                ""
            ],
            "Subfeature C":
            [
                "Channel 0",
                "Channel 1",
                "Channel 2"
            ],
        }
    },
    {
        "Feature 2":
        {
            "Subfeature A":
            [
                ""
            ],
            "Subfeature C":
            [
                "Channel 0",
                "Channel 2"
            ],
        }
    },
    {
        "Feature 3":
        {
            "Subfeature B":
            [
                ""
            ],
            "Subfeature C":
            [
                "Channel 1",
                "DeleteMe"
            ],
        },
    },
    {
        "Feature 4":
        {
            "Subfeature C":
            [
                "Channel 1",
                "Channel 2",
            ],
            "Subfeature DeleteMe":
            [
                "Channel 3",
            ],
        },
    },
    {
        "Feature DeleteMe":
        {
            "Subfeature C":
            [
                "Channel 1",
                "Channel 2",
            ],
            "Subfeature A":
            [
                "Channel 3",
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

def Remove_Subfeature(PinMap, Feature, SubFeature):
    del PinMap[Feature][SubFeature]

def Remove_Feature(PinMap, Feature):
    del PinMap[Feature]

print("*"*50)
print(MCU_Pins[2])
Remove_Channel(MCU_Pins[2], "Feature 3", "Subfeature C", "DeleteMe")
print(MCU_Pins[2])
print("*"*50)
print(MCU_Pins[3])
Remove_Subfeature(MCU_Pins[3], "Feature 4", "Subfeature DeleteMe")
print(MCU_Pins[3])
print("*"*50)
print(MCU_Pins[4])
Remove_Feature(MCU_Pins[4], "Feature DeleteMe")
print(MCU_Pins[4])
print("*"*50)

Solve(Requirements, MCU_Pins)
print(f"Combinations {Number_Of_Potential_Combinations(MCU_Pins)}")
