
import re

s = "Bei Personengesellschaften ohne eigene Rechtspersönlichkeit (z. B. OHG, KG, GbR) ist eine Erlaubnis für jede/n geschäftsführende/n Gesellschafter*in erforderlich. Das gilt auch hinsichtlich der Kommanditist*innen, sofern sie Geschäftsführungsbefugnis besitzen und damit als Gewerbetreibende anzusehen sind. Die Gesellschaft als solche kann im Gegensatz zur juristischen Person keine Erlaubnis erhalten."
STRLTN = r"(([\t-\n\r -~¡-¬®-ćĊ-ěĞ-ģĦ-ıĴ-śŞ-ūŮ-žƏƠ-ơƯ-ưƷǍ-ǔǞ-ǟǤ-ǰǴ-ǵǺ-ǿȘ-țȞ-ȟȪ-ȫȮ-ȳəʒḂ-ḃḊ-ḋḐ-ḑḞ-ḡḤ-ḧḰ-ḱṀ-ṁṄ-ṅṖ-ṗṠ-ṣṪ-ṫẀ-ẅẌ-ẓẞẠ-ầẪ-ẬẮ-ềỄ-ồỖ-ờỤ-ỹ€])|(M̂|N̂|m̂|n̂|D̂|d̂|J̌|L̂|l̂))*"


print(len(re.sub(STRLTN, "", s)))
