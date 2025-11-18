
# --- imports ---
import re
import xml.etree.ElementTree as ET
import sys


# --- setup ---
# filename = "Krankheitserreger/S05000001323V0.1.0_Erlaubnis_von_Tätigkeiten_mit_Krankheitserregern_xdf3.xml"
# filename = "Krankheitserreger/S05000001324V0.1.0_Anzeige_von_Tätigkeiten_mit_Krankheitserregern_xdf3.xml"
# filename = "Fahrschule 2/S05000001287V2.4.0_Antrag_Erteilung_Fahrschulerlaubnis_xdf3.xml"
# filename = "Fahrschule 2/S05000001288V3.1.0_Antrag_Erteilung_Anwärterbefugnis_xdf3.xml"
# filename = "Fahrschule 2/S05000001289V3.1.0_Antrag_Erteilung_Fahrlehrerlaubnis_xdf3.xml"
output = "output.txt"


# pattern aus den Fehlermeldungen von Jessica Gettkandt
STRLTN = r"(([\t-\n\r -~¡-¬®-ćĊ-ěĞ-ģĦ-ıĴ-śŞ-ūŮ-žƏƠ-ơƯ-ưƷǍ-ǔǞ-ǟǤ-ǰǴ-ǵǺ-ǿȘ-țȞ-ȟȪ-ȫȮ-ȳəʒḂ-ḃḊ-ḋḐ-ḑḞ-ḡḤ-ḧḰ-ḱṀ-ṁṄ-ṅṖ-ṗṠ-ṣṪ-ṫẀ-ẅẌ-ẓẞẠ-ầẪ-ẬẮ-ềỄ-ồỖ-ờỤ-ỹ€])|(M̂|N̂|m̂|n̂|D̂|d̂|J̌|L̂|l̂))*"

# pattern von https://regex101.com/r/U0xBm1/1
# ergänzt um die erste Gruppe [\t\b\r]
# STRLTN = r"([\t\n\r]|[ - ]| |[ -~]|[ -¬]|[®-ž]|[Ƈ-ƈ]|Ə|Ɨ|[Ơ-ơ]|[Ư-ư]|Ʒ|[Ǎ-ǜ]|[Ǟ-ǟ]|[Ǣ-ǰ]|[Ǵ-ǵ]|[Ǹ-ǿ]|[Ȓ-ȓ]|[Ș-ț]|[Ȟ-ȟ]|[ȧ-ȳ]|ə|ɨ|ʒ|[ʹ-ʺ]|[ʾ-ʿ]|ˈ|ˌ|[Ḃ-ḃ]|[Ḇ-ḇ]|[Ḋ-ḑ]|[Ḝ-ḫ]|[ḯ-ḷ]|[Ḻ-ḻ]|[Ṁ-ṉ]|[Ṓ-ṛ]|[Ṟ-ṣ]|[Ṫ-ṯ]|[Ẁ-ẇ]|[Ẍ-ẗ]|ẞ|[Ạ-ỹ]|’|‡|€|A̋|C(̀|̄|̆|̈|̕|̣|̦|̨̆)|D̂|F(̀|̄)|G̀|H(̄|̦|̱)|J(́|̌)|K(̀|̂|̄|̇|̕|̛|̦|͟H|͟h)|L(̂|̥|̥̄|̦)|M(̀|̂|̆|̐)|N(̂|̄|̆|̦)|P(̀|̄|̕|̣)|R(̆|̥|̥̄)|S(̀|̄|̛̄|̱)|T(̀|̄|̈|̕|̛)|U̇|Z(̀|̄|̆|̈|̧)|a̋|c(̀|̄|̆|̈|̕|̣|̦|̨̆)|d̂|f(̀|̄)|g̀|h(̄|̦)|j́|k(̀|̂|̄|̇|̕|̛|̦|͟h)|l(̂|̥|̥̄|̦)|m(̀|̂|̆|̐)|n(̂|̄|̆|̦)|p(̀|̄|̕|̣)|r(̆|̥|̥̄)|s(̀|̄|̛̄|̱)|t(̀|̄|̕|̛)|u̇|z(̀|̄|̆|̈|̧)|Ç̆|Û̄|ç̆|û̄|ÿ́|Č(̕|̣)|č(̕|̣)|Ī́|ī́|Ž(̦|̧)|ž(̦|̧)|Ḳ̄|ḳ̄|Ṣ̄|ṣ̄|Ṭ̄|ṭ̄|Ạ̈|ạ̈|Ọ̈|ọ̈|Ụ(̄|̈)|ụ(̄|̈))*"


# --- functions ---
def validate_text(text: str, path: str):
    """Validiere einen input text gegen den vorgegebenen pattern in STRLTN.

    Args:
        text (str): zu validierender Input
        path (str): Pfad des Text-Elementes, für korrekten Output
    """
    fault = re.sub(STRLTN, "", text)
    if fault:
        fault_set = set(fault)
        for char in fault_set:
            text = text.replace(char, f">>>{char}<<<")
        fault_list = [str(hex(ord(char))) for char in fault]
        first = True
        for char in fault_list:
            if first:
                fault = char
                first = not first
            else:
                fault = f"{fault}, {char}"
        print(
            f"FEHLER in Element {path}\n"
            f"Text: {text}\n"
            f"verbotene unicode Zeichen: {fault}\n\n"
            )

    if "bitte" in text or "Bitte" in text:
        print(
            f"FEHLER in Element {path}\n"
            f"Text: {text}\n"
            f"Der Text enthält das Wort \"bitte\".\n\n"
            )

    if "müssen" in text or "muss" in text:
        if "/R" not in path:
            print(
                f"FEHLER in Element {path}\n"
                f"Text: {text}\n"
                f"Der Text enthält das Wort \"müssen\" oder das Wort \"muss\".\n\n"
                )


def iter_children(
        element: ET.Element,
        current_path: str = "",
        ) -> None:
    """iteriere durch alle Kinder eines Elementes.
    Diese Funktion stellt sicher, dass beim iterieren immer ein passender Pfad
    erzeugt wird. Gleichzeitig wird die Funktion zur Textvalidierung
    mit dem richtigen Pfad aufgerufen, sofern ein Element Text enthält.
    Diese Funktion funktioniert iterativ. Sie wendet sich am Ende selbst auf
    alle Kinder des aktuellen Elementes an.

    Args:
        element (ET.Element): zu prüfendes und zu iterierendes Element
        current_path (str, optional): aktueller Pfad. Defaults to "".
    """

    tag = ""
    for child in element:
        if re.sub(r"^{.+?}", "", child.tag) == "identifikation":
            for grandchild in child:
                if re.sub(r"^{.+?}", "", grandchild.tag) == "id":
                    tag = grandchild.text
                    break
            break
        elif re.sub(r"^{.+?}", "", child.tag) == "id":
            tag = child.text
            break
        elif re.sub(r"^{.+?}", "", child.tag) == "name":
            tag = child.text
            break

    if re.sub(r"^{.+?}", "", element.tag) == "identifikation":
        tag = "identifikation"

    if not tag:
        tag = re.sub(r"^{.+?}", "", element.tag)

    if current_path:
        current_path = f"{current_path}/{tag}"
    else:
        current_path = tag

    short_path = current_path.replace("struktur/enthaelt/", "")
    short_path = short_path.replace("xdatenfelder.stammdatenschema.0102/", "")
    if element.text:
        validate_text(element.text, short_path)

    for child in element:
        iter_children(child, current_path)


def preproces(xml: str) -> str:
    return xml


# --- code ---
with open(filename, "r", encoding="utf-8") as file:
    xml = file.read()

xml = preproces(xml)
root = ET.fromstring(xml)

with open(output, "w", encoding="utf-8") as sys.stdout:
    print("--- STARTING ITERATION ---\n\n")
    iter_children(root)
    print("\n--- FINISHED ITERATION ---")
