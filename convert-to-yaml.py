import yaml

MEASURE_NAME_MAP = {
    "Measure A": "A",
    "Measure B": "B",
    "Break": "T",
}

def parse_drum_pattern(pattern_text):
    lines = pattern_text.split('\n')

    patterns = {}
    pattern_info = {}
    measures = {}
    measure = None
    idx = 0
    
    for line in lines:
        if line.startswith("### "):  # Extract pattern name
            if pattern_info:
                idx += 1
                pattern_info["measures"] = measures
                patterns[idx] = pattern_info

                # reset 
                pattern_info = {}
                measures = {}
                measure = None

            pattern_info["name"] = line[4:]
        elif line.startswith("|----"):  # Header row, ignore
            continue
        elif line.startswith("|"):  # Process subpattern rows
            parts = line.strip('|').split('|')
            drum_name = parts[0].strip()

            beats = parts[1:]
            transformed_beats = "".join(["X" if "X" in beat else " " for beat in beats])
            
            if drum_name == 'Drum':
                continue
            
            if drum_name not in measure:
                measure[drum_name] = ""
            
            measure[drum_name] = transformed_beats
            pattern_info["length"] = len(transformed_beats)

        elif line.startswith("4/4"):  # Extract time signature and tempo range
            parts = line.split(',')
            pattern_info["time_signature"] = parts[0].strip()
            pattern_info["tempo_range"] = parts[1].strip()
        elif line.startswith("#### "):  # Extract subpattern name
            measureName = MEASURE_NAME_MAP.get(line[5:], line[5:])
            measure = {}
            measures[measureName] = measure
    
    # add last pattern
    pattern_info["measures"] = measures
    idx += 1
    patterns[idx] = pattern_info

    return patterns

# Example usage:
sample_text = '''
### Rock 1

4/4, quarter note 112-139

#### Measure A

|Drum|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|
|----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|AC  |  |  |  |  | X|  |  |  |  |  |  |  | X|  |  |  |
|CH  | X|  |  |  | X|  |  |  | X|  |  |  | X|  |  |  |
|SD  |  |  |  |  | X|  |  |  |  |  |  |  | X|  |  |  |
|BD  | X|  |  |  |  |  | X|  | X|  |  |  |  |  |  |  |

#### Measure B

|Drum|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|
|----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|CH  | X|  |  |  | X|  |  |  | X|  |  |  | X|  |  |  |
|SD  |  |  |  |  | X|  |  |  |  |  |  |  | X|  |  |  |
|BD  | X|  |  |  |  |  | X|  | X|  | X|  |  |  | X|  |

#### Break

|Drum|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|
|----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|AC  | X|  |  |  |  |  |  |  |  |  |  |  | X|  |  | X|
|CH  | X|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|HT  |  |  |  | X| X|  |  | X| X|  |  | X|  |  |  |  |
|SD  |  |  | X|  |  |  | X|  |  |  | X|  | X| X| X| X|
|BD  | X|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### Rock 2

4/4, quarter note 64-109

#### Measure A

|Drum|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|
|----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|AC  | X|  | X|  | X|  | X|  | X|  | X|  | X|  | X|  |
|CH  | X| X| X| X| X| X| X| X| X| X| X| X| X| X| X|  |
|OH  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X|
|SD  |  |  |  |  | X|  |  |  |  |  |  |  | X|  |  |  |
|BD  | X|  | X|  |  | X|  |  | X|  |  |  |  |  |  | X|

#### Measure B

|Drum|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|
|----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|CH  | X| X| X| X| X| X| X|  | X| X| X| X| X| X| X|  |
|OH  |  |  |  |  |  |  |  | X|  |  |  |  |  |  |  | X|
|SD  |  |  |  |  | X|  |  |  |  |  |  |  | X|  | X|  |
|BD  | X|  | X|  |  | X|  |  | X|  |  |  |  |  |  | X|

#### Break

|Drum|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|
|----|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|CY  |  |  |  |  |  |  |  |  |  |  |  |  | X|  | X|  |
|MT  |  |  |  |  | X| X| X| X|  |  |  |  |  |  |  |  |
|SD  | X| X| X| X|  |  |  |  |  |  |  |  |  |  |  |  |
|LT  |  |  |  |  |  |  |  |  | X| X| X| X|  |  |  |  |
|BD  | X|  | X|  |  | X|  |  | X|  | X|  | X|  | X|  |
'''

# open a file and read it in
with open('README.md', 'r') as f:
    pattern_text = f.read()

patterns = parse_drum_pattern(pattern_text)
# output yaml

print("# Patterns from https://github.com/montoyamoraga/drum-machine-patterns")
print(yaml.dump({"patterns": patterns}))
