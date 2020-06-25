# interactive-ml-project-2
Second project in the course 'Machine learning as a tool for interactive products'

## Description
This project tries to use [S.C.A.M.P.E.R](https://en.wikipedia.org/wiki/S.C.A.M.P.E.R) 
in order to encourage [Mindfulness](https://en.wikipedia.org/wiki/Mindfulness) in day to day actions.

## Installation

### Dependencies

#### OS
This program has not been tested on any OS other than windows, however there is no OS specific code so it should run on any standard OS.

#### Python and Packages
Python version 3.7 is required with the following packages:

| package                              | version |
|--------------------------------------|---------|
| [numpy](https://numpy.org/)          | 1.18.5  |
| [pandas](https://pandas.pydata.org/) | 1.0.4   |

## Instructions
The program requires that the `data/alternatives/user/` directory contain the following files:
- `food.json`: available disruptions related to food
- `free.json`: available disruptions to the user's free time
- `general.json`: available day long disruptions
- `hygiene.json`: available disruptions related to hygiene
- `sleep.json`: available disruptions related to sleep

These files have a specific format:
```
{
    "<action>": {
        "types": [
            "<type1>",
            "<type2>"
        ],
        "<type1>": <related-disruptions>,
        "<type2>": <related-disruptions>
    }
    .
    .
    .
}
```
The "types" field specifies in what ways this action could be disrupted (in its order/time/etc). 
If a type is specified, the action also has to contain that type's field. Example files can be found in `data/alternatives/user/`.

To run the program, run `main.py` in `src`. Please consider the dependencies first.


## Files

### Directory tree
```
.
├── README.md
├── data
│   ├── alternatives
│   │   ├── <user1>
│   │   │   ├── food.json
│   │   │   ├── free.json
│   │   │   ├── general.json
│   │   │   ├── hygiene.json
│   │   │   └── sleep.json
│   │   └── <user2>
│   │       ├── food.json
│   │       ├── free.json
│   │       ├── general.json
│   │       ├── hygiene.json
│   │       └── sleep.json
│   └── schedules
│       ├── <user1>160620.csv
│       ├── <user2>090620.csv
│       └── <user2>100620.csv
└── src
    ├── Action.py
    ├── constants.py
    ├── data_io.py
    └── main.py
```
