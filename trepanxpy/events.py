ALL_EVENT_NAMES = (
    "c_call",
    "c_exception",
    "c_return",
    "call",
    "exception",
    "line",
    "return",
    "instruction",
    "yield",
)

# If you want short strings for the above event names
EVENT2SHORT = {
    "c_call": "C>",
    "c_exception": "C!",
    "c_return": "C<",
    "call": "->",
    "exception": "!!",
    "line": "--",
    "instruction": "..",
    "return": "<-",
    "yield": "<>",
    "fatal": "XX",
}

ALL_EVENTS = frozenset(ALL_EVENT_NAMES)
