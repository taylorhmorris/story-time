from bs4 import BeautifulSoup
import json

fp = u'''<body><div><span class="pron type-">deʀule<span class="ptr hwd_sound type-hwd_sound"> <a class="hwd_sound sound audio_play_button icon-volume-up ptr" data-lang="en_GB" data-src-mp3="https://www.collinsdictionary.com/sounds/hwd_sounds/FR-W0096310.mp3" title="Pronunciation for "></a> </span></span></div></body>'''

soup = BeautifulSoup(fp, "html.parser")

text = soup.text

items = {'text': text}

with open('out.json', 'w', encoding='utf8') as out:
    json.dump(items, out, ensure_ascii=False)
