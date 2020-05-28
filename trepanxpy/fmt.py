from numbers import Number as NumberType
from pygments.token import Number, Text

from trepan.lib.format import (
    Filename,
    Function,
    LineNumber,
    Name,
    Opcode,
    Operator,
    String,
    format_token,
)


LINE_NUMBER_WIDTH = 4
LINE_NUMBER_WIDTH_FMT = "%%-%dd" % LINE_NUMBER_WIDTH
LINE_NUMBER_SPACES = " " * (LINE_NUMBER_WIDTH + len("L. ")) + "@"


def format_instruction_with_highlight(
    frame,
    opc,
    byte_name,
    int_arg,
    arguments,
    offset,
    line_number,
    extra_debug,
    highlight,
    vm = None,
    show_line = True,
):
    """A version of x-python's format_instruction() with terminal highlighting"""
    code = frame.f_code if frame else None
    byteCode = opc.opmap.get(byte_name, 0)
    if isinstance(arguments, list) and arguments:
        arguments = arguments[0]
    argrepr = arguments

    fmt_type = Text
    if hasattr(opc, "opcode_arg_fmt") and byte_name in opc.opcode_arg_fmt:
        argrepr = opc.opcode_arg_fmt[byte_name](int_arg)
    elif int_arg is None:
        argrepr = ""
    elif byteCode in opc.NAME_OPS | opc.FREE_OPS | opc.LOCAL_OPS:
        fmt_type = Name
    elif byteCode in opc.NAME_OPS | opc.FREE_OPS | opc.LOCAL_OPS:
        fmt_type = Name
    elif byteCode in opc.JREL_OPS | opc.JABS_OPS:
        fmt_type = Number
        argrepr = str(argrepr)
    elif byteCode in opc.COMPARE_OPS:
        fmt_type = Operator
        argrepr = opc.cmp_op[int_arg]
    elif byteCode == opc.LOAD_CONST:
        if isinstance(argrepr, str):
            fmt_type = String
        elif isinstance(argrepr, NumberType):
            fmt_type = Number
        argrepr = repr(argrepr)

    if line_number is None or not show_line:
        line_str = LINE_NUMBER_SPACES
    else:
        number_str = format_token(
            LineNumber, LINE_NUMBER_WIDTH_FMT % line_number, highlight=highlight
        )
        line_str = "L. %s@" % number_str
    try:
        format_token(fmt_type, argrepr),
    except:
        from trepan.api import debug; debug()

    mess = "%s%3d: %s %s" % (
        line_str,
        offset,
        format_token(Opcode, byte_name),
        format_token(fmt_type, argrepr),
    )
    if extra_debug and frame:
        mess += " %s in %s:%s" % (
            format_token(Function, code.co_name, highlight=highlight),
            format_token(Filename, code.co_filename, highlight=highlight),
            format_token(LineNumber, str(frame.f_lineno), highlight=highlight),
        )
    return mess
