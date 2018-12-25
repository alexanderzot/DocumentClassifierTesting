# RTF parser
import os
import html


# Stack class
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


# check file exists
def file_exists(filepath):
    try:
        os.stat(filepath)
    except OSError:
        return False
    return True


def rtf_is_plain_text(s):
    for i in {"*", "fonttbl", "colortbl", "datastore", "themedata", "stylesheet", "info", "picw", "pich"}:
        if i in s:
            return False
    return True


def hex_char_to_dec(ch):
    if ch >= '0' and ch <= '9':
        return ord(ch) - ord('0')
    elif ch >= 'a' and ch <= 'f':
        return ord(ch) - ord('a') + 10
    elif ch >= 'A' and ch <= 'F':
        return ord(ch) - ord('A') + 10
    raise Exception("Char error input")


def hexdec(str):
    str = str.lower().replace("0x", "")
    res = 0;
    for ch in str:
        res *= 16
        try:
            res += hex_char_to_dec(ch)
        except:
            raise Exception("String error. have value %c" % ch)
    return res


def from_mac_roman(value):
    table = {
        0x83: 'c9', 0x84: 'd1', 0x87: 'e1', 0x8e: 'e9', 0x92: 'ed',
        0x96: 'f1', 0x97: 'f3', 0x9c: 'fa', 0xe7: 'c1', 0xea: 'cd',
        0xee: 'd3', 0xf2: 'da'
    }

    if value in table:
        value = "&#x00%s;" % table[value]
    return value


t = {"*" : 1, "test" : 2}
print(rtf_is_plain_text(t))
# main
filepath = '/home/moskov/Projects/test_rtf.rtf'

if not file_exists(filepath=filepath):
    exit(1)

f = open(file=filepath)

data = f.read()
data_size = len(data)

if data_size == 0:
    exit(2)

#print(data)
#print(data_size)

data.replace("#[\r\n]#", "")
data.replace("#[0-9a-f]{128,}#is", "")

data = data.replace("\\\'3f", "?") # replace \'3f
data = data.replace("\\\'3F", "?") # replace \'3F

# udate data size
data_size = len(data)

# result data
document = ""

stack = Stack()
fonts = dict()
i = 0
while i < data_size:
    ch = data[i]

    if ch == '\\':
        nc = data[i + 1]

        if nc == '\\' and rtf_is_plain_text(stack.peek()):
            document += "\\"
        elif nc == '~' and rtf_is_plain_text(stack.peek()):
            document += " "
        elif nc == '_' and rtf_is_plain_text(stack.peek()):
            document += "-"
        elif nc == '*':
            stack.peek()["*"] = True
        elif nc == '\'':
            hex_val = data[i + 2:i + 4]
            if rtf_is_plain_text(stack.peek()):
                if "mac" in stack.peek() or ("f" in stack.peek() and fonts[stack.peek()["f"]] == 77):
                    document += from_mac_roman(hexdec(hex_val))
                elif ("ansicpg" in stack.peek() and stack.peek()["ansicpg"] == "1251") or ("lang" in stack.peek() and stack.peek()["lang"] == "1029"):
                    document += chr(hexdec(hex_val))
                else:
                    document += "&#%d;" % hexdec(hex_val)
            i += 2
        elif (nc >= 'a' and nc <= 'z') or (nc >= 'A' and nc <= 'Z'):
            word = ""
            param = ""

            m = 0
            for k in range(i + 1, data_size):
                nc = data[k]

                if (nc >= 'a' and nc <= 'z') or (nc >= 'A' and nc <= 'Z'):
                    if len(param) == 0:
                        word += nc
                    else:
                        break
                elif nc >= '0' and nc <= '9':
                    param += nc
                elif nc == '-':
                    if len(param) == 0:
                        param += nc
                    else:
                        break
                else:
                    break
                m += 1

            i += m - 1

            to_text = ""

            lword = word.lower()

            if lword == "u":
                tmp = "&#x%s;" % param
                to_text += html.unescape(tmp)
                uc_delta = 1;
                if "uc" in stack.peek():
                    uc_delta = stack.peek()["uc"]
                if int(uc_delta) > 0:
                    i += int(uc_delta)
            elif lword == "par" or lword == "page" or lword == "column" or lword == "line" or lword == "lbr":
                to_text += "\n"
            elif lword == "emspace" or lword == "enspace" or lword == "qmspace":
                to_text += " "
            elif lword == "tab":
                to_text += "\t"
            elif lword == "chdate":
                to_text += ""
            elif lword == "chdpl":
                to_text += ""
            elif lword == "chdpa":
                to_text += ""
            elif lword == "chtime":
                to_text += ""
            elif lword == "emdash":
                to_text += ""
            elif lword == "endash":
                to_text += ""
            elif lword == "bullet":
                to_text += ""
            elif lword == "lquote":
                to_text += ""
            elif lword == "rquote":
                to_text += ""
            elif lword == "ldblquote":
                to_text += ""
            elif lword == "rdblquote":
                to_text += ""
            elif lword == "bin":
                i += int(param)
            elif lword == "fcharset":
                fonts[stack.peek()["f"]] = param
            else:
                if len(param) == 0:
                    stack.peek()[word.lower()] = True
                else:
                    stack.peek()[word.lower()] = param

            if rtf_is_plain_text(stack.peek()):
                document += to_text
        else:
            document += " "
        i += 1
    elif ch == '{':
        # new group, add velues from prev group
        # TODO
        if stack.size() == 0:
            stack.push(dict())
        else:
            prev = stack.peek()
            stack.push(prev.copy())
    elif ch == '}':
        # group end
        stack.pop()
    elif ch in {'\0', '\r', '\f', '\b', '\t'}:
        pass
    elif ch == '\n':
        document += " "
    else:
        if rtf_is_plain_text(stack.peek()):
            document += ch
    i += 1

print(document)

#print(html.entities(document))

#print(data)

#print('\'')
#sprint("1\n2")

#print(hexdec("0xAf"))

#print(hexdec('AA'))

#print(from_mac_roman(0x83))