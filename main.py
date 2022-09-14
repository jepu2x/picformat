import re
import string
from js import document
from js import navigator
from pyodide import create_proxy


title_letters_set = ''.join([chr(x) for x in range(0x1D5D4, 0x1D607 + 1)])
title_ascii_letters = string.ascii_uppercase + string.ascii_lowercase
title_trans_table = title_ascii_letters.maketrans(title_ascii_letters, title_letters_set)


title_numbers_set = {
    '0': 0x1D7EC,
    '1': 0x1D7ED,
    '2': 0x1D7EE,
    '3': 0x1D7EF,
    '4': 0x1D7F0,
    '5': 0x1D7F1,
    '6': 0x1D7F2,
    '7': 0x1D7F3,
    '8': 0x1D7F4,
    '9': 0x1D7F5
}


def replace_title(text):
    title = text.split('\n')[0]
    original_title = title
    numbers = list(dict.fromkeys(''.join(re.findall(r'\d+', title))))
    parsed_title = title.translate(title_trans_table)
    for x in numbers:
        parsed_title = parsed_title.replace(x, chr(title_numbers_set[x]))
    final_output = parsed_title + text.replace(original_title, '')
    return final_output


credits_letters_set = ''.join([chr(x) for x in range(0x1D670, 0x1D6A3 + 1)])
credits_ascii_letters = string.ascii_uppercase + string.ascii_lowercase
credits_trans_table = credits_ascii_letters.maketrans(credits_ascii_letters, credits_letters_set)


def replace_credits(text):
    if text.rfind(')') == len(text) - 1:
        credits_text = text[text.rfind('('):]
        parsed_credits_text = credits_text.translate(credits_trans_table)
        final_output = text.replace(credits_text, '') + parsed_credits_text
        return final_output
    return text


hashtags = "\n\n#provincialinformationcenterzanorte\n#piczanorteofficial"
def display_output(*args, **kwargs):
    text = str(Element("userInput").element.value).strip()
    text = replace_title(text)
    text = replace_credits(text)
    result = text + hashtags
    Element("userOutput").element.value = result


def copy_output(*args, **kwargs):
    output = str(Element("userOutput").element.value)
    navigator.clipboard.writeText(output)


Element("userOutput").element.value = hashtags
function_proxy = create_proxy(display_output)
document.getElementById("userInput").addEventListener("input", function_proxy);