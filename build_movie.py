import os
import re
import time
import math
import wave
import base64
import asyncio
import urllib.parse
import subprocess
import numpy as np
import requests
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from mutagen.mp3 import MP3

# ---------------- CONFIG ----------------
OUT_DIR = "2026-11-13_Project_18_9Hz_3D_V3"
PARTS_DIR = os.path.join(OUT_DIR, "parts")
IMG_DIR = os.path.join(OUT_DIR, "images")
os.makedirs(PARTS_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

MIN_PART_SECONDS = 190.0  # 8 parts x 190s = 1520s (~25 min 20 sec)
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "").strip()

PIXAR_BASE = (
    "3D Pixar animation movie style, vibrant cinematic lighting, rich glowing cyan and warm amber neon colors, "
    "expressive Indian young male engineer Aarav in dark hoodie with glowing blue tech goggles and brass EMF meter, "
    "ultra detailed 3D character render, dramatic shadows, atmospheric fog, 8k, no text, no watermark"
)

# ---------------- 8-PART SPINE-CHILLING SCRIPT (80 SCENES) ----------------
PARTS = [
    {
        "part": 1,
        "bpm": 62,
        "hud": "REC ● LAB-04 | 02:14 AM | 18.9 Hz",
        "narration": (
            "रात के ठीक दो बजकर चौदह मिनट पर जब शहर की हर घड़ी थम चुकी थी, तब दिल्ली की उस वीरान लैब में मेरा ईएमएफ मीटर अचानक लाल होकर चीखने लगा। "
            "मेरा नाम आरव है और मैं एक इलेक्ट्रॉनिक्स इंजीनियर हूँ। मैं भूतों पर नहीं, सिर्फ विज्ञान और आंकड़ों पर यकीन करता था। "
            "लेकिन जब मैंने अपने हेडफोन में अठारह दशमलव नौ हर्ट्ज़ की वो अनसुनी फ्रीक्वेंसी रिकॉर्ड की, तो मेरी रीढ़ की हड्डी में बर्फीली सिहरन दौड़ गई। "
            "कमरे का तापमान पंद्रह डिग्री से गिरकर अचानक शून्य पर आ गया और मेरे ठीक पीछे किसी के धीमे सांस लेने की आवाज गूंजी। "
            "अठारह दशमलव नौ हर्ट्ज़ वो खूनी आवृत्ति है जिसे इंसान के कान सुन नहीं सकते, लेकिन हमारी आंखों की पुतलियां इससे कांपने लगती हैं। "
            "जब आंखें कांपती हैं, तो दिमाग को कोने में खड़ी एक काली परछाईं दिखाई देती है। क्या ये सच में सिर्फ मेरी आंखों का धोखा था, या लैब चार की दीवारों में कुछ जिंदा था? "
            "असली खौफ अभी शुरू भी नहीं हुआ था, क्योंकि मेरे लैपटॉप की स्क्रीन पर एक ऐसी फाइल अपने आप खुली, जिसे उन्नीस सौ बयासी में बंद कर दिया गया था।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, Aarav standing inside a colourful neon-lit dark science lab at 2 AM holding a glowing red EMF meter, eerie cyan mist",
            f"{PIXAR_BASE}, close up of Aarav shocked wide eyes reflecting glowing red oscilloscope wave 18.9 Hz on a monitor",
            f"{PIXAR_BASE}, dark misty laboratory corridor with flickering warm amber emergency lights and deep teal shadows",
            f"{PIXAR_BASE}, Aarav freezing in terror as icy frost forms on glass windows and a shadowy silhouette stands behind him",
            f"{PIXAR_BASE}, glowing 3D holographic human eye vibrating with neon purple soundwaves in dark room",
            f"{PIXAR_BASE}, Aarav wearing headphones trembling as ghostly blue energy wisps swirl around his desk",
            f"{PIXAR_BASE}, dusty metallic door labelled LAB 4 with glowing red warning light and swirling green-blue fog",
            f"{PIXAR_BASE}, vintage 1982 locked file opening automatically on a glowing holographic computer screen",
            f"{PIXAR_BASE}, Aarav turning back slowly with a flashlight beam cutting through colourful dark volumetric dust",
            f"{PIXAR_BASE}, dramatic close up of brass EMF detector needle slamming into glowing red danger zone"
        ]
    },
    {
        "part": 2,
        "bpm": 68,
        "hud": "REC ● ARCHIVE | 02:29 AM | CO-HIGH",
        "narration": (
            "स्क्रीन पर खुली वो पुरानी फाइल किसी और की नहीं, बल्कि मेरे दादाजी डॉक्टर विश्वनाथ शर्मा की थी। "
            "उन्नीस सौ बयासी में वे इसी सरकारी प्रयोगशाला के प्रमुख वैज्ञानिक थे और एक रात अचानक गायब हो गए थे। "
            "मैंने कांपते हाथों से जब अपनी जेब का गैस सेंसर चालू किया, तो हवा में कार्बन मोनोऑक्साइड का स्तर खतरे के निशान से चार गुना ऊपर था। "
            "विज्ञान कहता है कि ये जहरीली गैस इंसान के दिमाग में डर और मतिभ्रम पैदा करती है, जिससे उसे अपने आसपास मरे हुए लोग दिखने लगते हैं। "
            "लेकिन तभी लैब के पुराने वेंटिलेशन पाइप से एक ऐसी चीख निकली जिसने मेरे सेंसर की सुई को तोड़ दिया। "
            "क्या कार्बन मोनोऑक्साइड किसी लोहे के दरवाजे को अंदर से पीट सकती है? नहीं, हरगिज नहीं। "
            "मैंने टॉर्च की रोशनी उस बंद वेंट की तरफ घुमाई और वहां जो देखा, उसे देखकर मेरे हाथ से टॉर्च छूट गई।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, Aarav staring at a glowing 3D vintage photograph of his grandfather scientist in a 1982 lab",
            f"{PIXAR_BASE}, close up of Aarav holding a glowing orange gas detector flashing crimson danger warning",
            f"{PIXAR_BASE}, toxic emerald green and amber mist seeping out from rusty metallic laboratory air vents",
            f"{PIXAR_BASE}, Aarav hallucinating ghostly translucent figures floating in vibrant purple and cyan lab fog",
            f"{PIXAR_BASE}, heavy steel ventilation grate shaking violently with bright sparks and red emergency glow",
            f"{PIXAR_BASE}, Aarav dropping his glowing flashlight onto the wet reflective lab floor in sheer panic",
            f"{PIXAR_BASE}, eerie dark hallway with glowing blue sparks dancing along old copper electrical pipes",
            f"{PIXAR_BASE}, close up of a cracked glass gas meter gauge needle snapping in half",
            f"{PIXAR_BASE}, glowing pale eyes peering out from inside a dark metallic air duct with cyan rim light",
            f"{PIXAR_BASE}, Aarav backing away against a neon-lit control panel as red alarm lights spin"
        ]
    },
    {
        "part": 3,
        "bpm": 74,
        "hud": "REC ● STONE-TAPE | 02:45 AM | 480 V",
        "narration": (
            "फर्श पर गिरी टॉर्च की रोशनी सीधे बेसमेंट की सीढ़ियों पर पड़ी, जहां पत्थर की दीवारों से पानी नहीं बल्कि लाल जंग टपक रहा था। "
            "मैंने दादाजी की डायरी के पहले पन्ने पर लिखा एक शब्द पढ़ा, स्टोन टेप थ्योरी। "
            "इस सिद्धांत के मुताबिक जब किसी जगह पर भयानक दर्द, खौफ या मौत घटती है, तो उस घटना की ऊर्जा पत्थरों और लोहे में मैग्नेटिक टेप की तरह रिकॉर्ड हो जाती है। "
            "जैसे ही मैंने अपना चुंबकीय रिकॉर्डर उन भीगी दीवारों से सटाया, मेरे स्पीकर से उन्नीस सौ बयासी की एक भयानक रात की रिकॉर्डिंग अपने आप बजने लगी। "
            "उस आवाज में कोई चिल्ला रहा था कि मशीन बंद करो, अठारह दशमलव नौ हर्ट्ज़ ने दरवाजा खोल दिया है। "
            "यह कोई पुराना भूत नहीं था, यह वक्त के पत्थरों में कैद एक जिंदा चीख थी जो आज फिर से दोहराई जा रही थी। "
            "तभी मेरे पीछे सीढ़ियों पर गीले कदमों की आवाज आई, और ऊपर से आने वाला लोहे का दरवाजा धड़ाम से बंद हो गया।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, steep underground concrete staircase with glowing red rust stains and eerie cyan mist",
            f"{PIXAR_BASE}, Aarav holding an ancient leather diary glowing with warm golden candlelight and dust particles",
            f"{PIXAR_BASE}, 3D visualization of stone walls pulsing with glowing blue and crimson magnetic energy waves",
            f"{PIXAR_BASE}, Aarav pressing a retro magnetic tape recorder against wet dark basement stone wall",
            f"{PIXAR_BASE}, glowing neon audio waveforms erupting from a small speaker in the dark basement",
            f"{PIXAR_BASE}, ghostly 1982 hologram silhouette of a terrified scientist shouting near a glowing portal",
            f"{PIXAR_BASE}, wet glowing footprints appearing mysteriously on dark basement stairs",
            f"{PIXAR_BASE}, heavy iron basement door slamming shut with bright orange sparks and dust burst",
            f"{PIXAR_BASE}, Aarav trapped in dark stairwell illuminated only by bright blue phone screen glow",
            f"{PIXAR_BASE}, intense close up of Aarav sweating in fear listening to static radio voices"
        ]
    },
    {
        "part": 4,
        "bpm": 80,
        "hud": "REC ● BASEMENT | 03:02 AM | TEMP -4C",
        "narration": (
            "मैं अब जमीन से तीस फीट नीचे अंधेरे में कैद था, और मेरे फोन का सिग्नल पूरी तरह मर चुका था। "
            "लेकिन मेरे हाथ में मौजूद थर्मल कैमरे ने जो दिखाया, उसने विज्ञान के हर नियम को पलट कर रख दिया। "
            "सामने खाली कोने में कुछ भी नहीं था, पर थर्मल स्क्रीन पर वहां एक सात फीट ऊंची बर्फीली नीली आकृति खड़ी थी, जिसका तापमान माइनस दस डिग्री था। "
            "साधारण इंसान के शरीर से गर्मी निकलती है, लेकिन यह चीज कमरे की सारी गर्मी को अपने अंदर सोख रही थी। "
            "जैसे ही मैंने एक कदम आगे बढ़ाया, मेरे थर्मोमीटर का पारा कांच के अंदर ही जम गया और मेरे मुंह से भाप निकलने लगी। "
            "वह नीली आकृति धीरे-धीरे मेरी तरफ मुड़ी, और उसके सीने के ठीक बीच में एक चमकता हुआ क्वांटम चक्र घूम रहा था। "
            "क्या दादाजी ने उन्नीस सौ बयासी में किसी दूसरी दुनिया से ऊर्जा खींचने की कोशिश की थी?"
        ),
        "scenes": [
            f"{PIXAR_BASE}, Aarav trapped 30 feet underground looking at his dead smartphone screen in neon blue shadows",
            f"{PIXAR_BASE}, Aarav looking through a glowing thermal camera showing a 7-foot tall icy blue human figure in empty corner",
            f"{PIXAR_BASE}, glowing neon heat-map silhouettes shifting from fiery orange to freezing electric blue",
            f"{PIXAR_BASE}, close up of glass thermometer mercury freezing into glowing ice crystals",
            f"{PIXAR_BASE}, Aarav exhaling visible glowing white cold breath in a dark icy server basement",
            f"{PIXAR_BASE}, towering translucent icy-blue entity turning slowly with a spinning golden quantum vortex in its chest",
            f"{PIXAR_BASE}, vibrant swirling cyan and magenta energy tendrils spreading across dark metallic lab floor",
            f"{PIXAR_BASE}, Aarav shielding his eyes from blinding neon blue light radiating from the cold entity",
            f"{PIXAR_BASE}, vintage 1982 copper coils humming with bright purple lightning arcs in the background",
            f"{PIXAR_BASE}, dramatic low-angle shot of Aarav standing bravely against the towering glowing blue phantom"
        ]
    },
    {
        "part": 5,
        "bpm": 86,
        "hud": "REC ● DIARY-82 | 03:18 AM | QUANTUM",
        "narration": (
            "मैं भागकर एक पुरानी लोहे की मेज के नीचे छिप गया, और कांपती टॉर्च में दादाजी की डायरी के बाकी पन्ने पलटने लगा। "
            "पन्ना नंबर चवालीस पर लिखा था कि इंसान की चेतना सिर्फ दिमाग के रसायनों का खेल नहीं है, बल्कि यह एक क्वांटम बायो-एनर्जी है। "
            "ऊर्जा न कभी पैदा होती है और न ही कभी नष्ट होती है, मौत के बाद वह सिर्फ अपना रूप बदलती है। "
            "दादाजी ने एक ऐसी मशीन बनाई थी जो अठारह दशमलव नौ हर्ट्ज़ की ध्वनि तरंगों से उस बायो-एनर्जी को पकड़ सकती थी। "
            "लेकिन तीन नवंबर उन्नीस सौ बयासी की रात, जब उन्होंने मशीन की ताकत सौ गुना बढ़ाई, तो लैब चार की दीवार समय और आयाम के बीच फट गई। "
            "जो चीज उस रात अंदर आई, उसने दादाजी को मारा नहीं, बल्कि उन्हें अपने ही समय के जाल में कैद कर लिया। "
            "तभी मेज के ऊपर रखे पुराने कांच के बीकर एक-एक करके हवा में तैरने लगे और मेरी तरफ मुड़ गए।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, Aarav hiding beneath a heavy steel lab table clutching the glowing leather diary",
            f"{PIXAR_BASE}, open handwritten 1982 diary page 44 with glowing golden quantum bio-energy diagrams",
            f"{PIXAR_BASE}, vibrant 3D glowing neural energy particles swirling in shape of a human soul above dark desk",
            f"{PIXAR_BASE}, retro futuristic 1982 brass frequency generator glowing with intense emerald and amber lights",
            f"{PIXAR_BASE}, dramatic dimensional tear glowing bright purple and cyan opening in the middle of Lab 4 wall",
            f"{PIXAR_BASE}, silhouette of grandfather scientist reaching out from inside a swirling golden time vortex",
            f"{PIXAR_BASE}, glass laboratory beakers filled with colourful glowing liquids levitating in mid-air",
            f"{PIXAR_BASE}, floating glass shards spinning slowly in dramatic crimson and blue rim lighting",
            f"{PIXAR_BASE}, Aarav looking up in shock from under the table as glowing green beakers point at him",
            f"{PIXAR_BASE}, intense close up of diary ink letters glowing bright gold in the darkness"
        ]
    },
    {
        "part": 6,
        "bpm": 92,
        "hud": "REC ● LAB-04 | 03:33 AM | DANGER",
        "narration": (
            "हवा में तैरते वे कांच के बीकर किसी अदृश्य ताकत के इशारे पर मेरी ओर गोली की तरह लपके, लेकिन ठीक मेरे चेहरे से दो इंच पहले रुक गए। "
            "कमरे के चारों कोनों से एक भारी गूंज उठी, जिसमें सैकड़ों फुसफुसाती आवाजें एक साथ बोल रही थीं। "
            "मैंने तुरंत अपना स्पेक्ट्रम एनालाइजर खोला और देखा कि वे आवाजें किसी हवा से नहीं, बल्कि सीधे मेरे दिमाग के ऑडिटरी कॉर्टेक्स में इलेक्ट्रोमैग्नेटिक तरंगों से भेजी जा रही थीं। "
            "लैब चार का भारी सीलबंद दरवाजा बिना किसी चाबी के अपने आप चरमराते हुए खुलने लगा। "
            "अंदर से नीली और बैंगनी रोशनी की ऐसी तेज किरण बाहर आई कि पूरे बेसमेंट की धूल हवा में जम गई। "
            "बीच कमरे में तांबे के तारों से बनी दादाजी की वह मुख्य मशीन आज भी बिना बिजली के चल रही थी। "
            "और उस मशीन के कांच के चैंबर के अंदर एक बुजुर्ग वैज्ञानिक का हाथ धीरे-धीरे कांच पर टकराया।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, glowing glass beakers frozen mid-air just two inches from Aarav terrified face",
            f"{PIXAR_BASE}, swirling colourful ghostly soundwaves whispering around Aarav head in dark lab",
            f"{PIXAR_BASE}, close up of glowing digital spectrum analyzer showing crazy neon red electromagnetic spikes",
            f"{PIXAR_BASE}, massive rusted vault door of LAB 4 creaking open with blinding cyan and purple light",
            f"{PIXAR_BASE}, dust particles suspended mid-air in vibrant neon purple and blue volumetric light beams",
            f"{PIXAR_BASE}, giant 1982 copper Tesla coil machine humming with bright electric blue plasma arcs",
            f"{PIXAR_BASE}, cylindrical glowing glass chamber in center of dark lab pulsing with golden energy",
            f"{PIXAR_BASE}, close up of an elderly hand pressing against foggy glowing glass from inside the chamber",
            f"{PIXAR_BASE}, Aarav stepping slowly into glowing Lab 4 bathed in dramatic cyan and amber light",
            f"{PIXAR_BASE}, wide cinematic 3D shot of the mysterious glowing quantum laboratory"
        ]
    },
    {
        "part": 7,
        "bpm": 98,
        "hud": "REC ● CLIMAX | 03:45 AM | 18.9 Hz!",
        "narration": (
            "मेरे पैर मानो पत्थर के हो गए थे, जब मैंने उस कांच के चैंबर के अंदर अपने दादाजी डॉक्टर विश्वनाथ को जिंदा देखा। "
            "उनकी उम्र उन्नीस सौ बयासी से एक दिन भी नहीं बढ़ी थी, क्योंकि उस चैंबर के अंदर वक्त पूरी तरह थम चुका था। "
            "लेकिन उनके ठीक पीछे उस नीली रोशनी में एक और डरावना साया हिल रहा था, जिसकी आंखें अंगारों की तरह लाल चमक रही थीं। "
            "दादाजी ने कांच पर उंगली से उल्टा लिखा, फ्रीक्वेंसी काटो, वरना यह पूरे शहर को निगल लेगा। "
            "मेरा ईएमएफ मीटर चिंगारियां छोड़ने लगा और पूरे कमरे की लोहे की कुर्सियां दीवारों से चिपक गईं। "
            "मैंने बिना एक पल गंवाए अपनी जेब से मल्टी-टूल निकाला और उस मुख्य तांबे की केबल को काटने के लिए आगे दौड़ा। "
            "तभी उस लाल आंखों वाले साये ने एक ऐसी चीख मारी कि लैब की सारी ट्यूबलाइटें एक साथ फट गईं।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, Aarav crying and shocked seeing his grandfather alive inside the glowing time-frozen glass chamber",
            f"{PIXAR_BASE}, close up of grandfather scientist with glowing red-eyed shadow creature looming behind him",
            f"{PIXAR_BASE}, foggy glass showing backwards handwritten warning words glowing in bright red neon",
            f"{PIXAR_BASE}, Aarav EMF meter exploding with bright orange electrical sparks",
            f"{PIXAR_BASE}, heavy metal chairs flying and sticking violently to magnetic glowing walls",
            f"{PIXAR_BASE}, Aarav sprinting forward bravely holding glowing steel pliers toward thick sparking copper cable",
            f"{PIXAR_BASE}, terrifying dark phantom with glowing crimson eyes roaring with electric purple shockwaves",
            f"{PIXAR_BASE}, ceiling neon tube lights shattering simultaneously in slow motion with bright sparks",
            f"{PIXAR_BASE}, Aarav lunging through flying glass shards toward the glowing red power core",
            f"{PIXAR_BASE}, intense dramatic lighting with red alarms and blue lightning filling Lab 4"
        ]
    },
    {
        "part": 8,
        "bpm": 105,
        "hud": "REC ● SIGNAL LOST | 04:00 AM",
        "narration": (
            "कांच के टूटते टुकड़ों के बीच मैंने पूरी ताकत से उस मुख्य तांबे की केबल को काट दिया, और एक पल में पूरा बेसमेंट सन्नाटे में डूब गया। "
            "वह लाल आंखों वाला साया धुएं के एक नीले बवंडर में बदलकर गायब हो गया और तापमान फिर से सामान्य हो गया। "
            "जब मैं कांपते हुए उस कांच के चैंबर के पास पहुंचा, तो चैंबर खाली था, लेकिन फर्श पर उन्नीस सौ बयासी की एक सुनहरी घड़ी रखी थी जो अभी भी चल रही थी। "
            "मैंने साबित कर दिया था कि भूत और साये अंधविश्वास नहीं, बल्कि अठारह दशमलव नौ हर्ट्ज़ और क्वांटम ऊर्जा का वो रहस्य हैं जिसे विज्ञान ने अभी ठीक से समझा नहीं है। "
            "मैं सुबह चार बजे जब लैब से बाहर निकला, तो सूरज की पहली किरण आसमान को लाल कर रही थी। "
            "लेकिन जैसे ही मैंने घर जाकर अपनी ऑडियो रिकॉर्डिंग दोबारा सुनी, रिकॉर्डिंग के आखिरी सेकंड में मेरे दादाजी की आवाज आई, आरव, दरवाजा अभी पूरी तरह बंद नहीं हुआ है। "
            "क्या आप भी रात के सन्नाटे में कभी-कभी अजीब सी गूंज महसूस करते हैं? अपनी राय कमेंट में लिखें, क्योंकि अगली जांच अब आपके शहर में हो सकती है।"
        ),
        "scenes": [
            f"{PIXAR_BASE}, Aarav slicing thick glowing copper cable with bright golden spark explosion",
            f"{PIXAR_BASE}, terrifying crimson shadow dissolving into swirling cyan smoke vortex",
            f"{PIXAR_BASE}, quiet peaceful Lab 4 bathed in soft morning blue light and fading mist",
            f"{PIXAR_BASE}, Aarav kneeling beside empty glass chamber picking up a glowing golden 1982 pocket watch",
            f"{PIXAR_BASE}, close up of antique golden watch ticking inside glowing dust beams",
            f"{PIXAR_BASE}, Aarav walking out of the dark facility into a colourful fiery orange sunrise sky",
            f"{PIXAR_BASE}, Aarav back in his modern colourful home studio putting on headphones",
            f"{PIXAR_BASE}, close up of laptop audio waveform spiking suddenly in bright blood red at the last second",
            f"{PIXAR_BASE}, Aarav eyes widening in sudden horror as a faint glowing shadow reflects in his monitor",
            f"{PIXAR_BASE}, cinematic glowing title frame mystery aura with 18.9 Hz neon wave and dark fog"
        ]
    }
]

# ---------------- IMAGE GENERATOR (CF + POLLINATIONS + HUD) ----------------
def is_valid_bright_image(path):
    if not os.path.exists(path) or os.path.getsize(path) < 18000:
        return False
    try:
        with Image.open(path) as im:
            rgb = im.convert("RGB")
            arr = np.asarray(rgb, dtype=np.float32)
            if arr.mean() < 12.0:
                return False
        return True
    except Exception:
        return False

def add_cctv_hud(path, hud_text):
    try:
        with Image.open(path) as im:
            im = im.convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(im, "RGBA")
            draw.rounded_rectangle([850, 18, 1260, 56], radius=8, fill=(8, 12, 20, 175), outline=(220, 45, 45, 200), width=2)
            draw.ellipse([866, 30, 880, 44], fill=(255, 40, 40, 255))
            font = ImageFont.load_default()
            draw.text((890, 31), hud_text, fill=(245, 245, 255, 240), font=font)
            im.save(path, "PNG")
    except Exception as e:
        print(f"[HUD Warn] {e}")

def generate_3d_image(prompt, out_path, hud_text, seed):
    if is_valid_bright_image(out_path):
        return out_path
    if os.path.exists(out_path):
        os.remove(out_path)

    if CF_ACCOUNT_ID and CF_API_TOKEN:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
        headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "steps": 4}
        for attempt in range(3):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=90)
                ctype = r.headers.get("Content-Type", "")
                if r.status_code == 200 and "application/json" in ctype:
                    b64 = r.json().get("result", {}).get("image")
                    if b64:
                        with open(out_path, "wb") as f:
                            f.write(base64.b64decode(b64))
                        if is_valid_bright_image(out_path):
                            add_cctv_hud(out_path, hud_text)
                            return out_path
                elif r.status_code == 200 and len(r.content) > 18000:
                    with open(out_path, "wb") as f:
                        f.write(r.content)
                    if is_valid_bright_image(out_path):
                        add_cctv_hud(out_path, hud_text)
                        return out_path
                print(f"[CF Attempt {attempt+1}] HTTP {r.status_code} | {r.text[:160]}")
            except Exception as e:
                print(f"[CF Err] {e}")
            time.sleep(2)
    else:
        print("[CF Missing] CF_ACCOUNT_ID or CF_API_TOKEN not set!")

    encoded = urllib.parse.quote(prompt)
    pol_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&model=flux&seed={seed}&nologo=true"
    for attempt in range(2):
        try:
            r = requests.get(pol_url, timeout=90)
            if r.status_code == 200 and len(r.content) > 18000 and "image" in r.headers.get("Content-Type", ""):
                with open(out_path, "wb") as f:
                    f.write(r.content)
                if is_valid_bright_image(out_path):
                    add_cctv_hud(out_path, hud_text)
                    return out_path
        except Exception as e:
            print(f"[Pollinations Err] {e}")
        time.sleep(3)

    print(f"[Fallback Gradient] Creating atmospheric frame for {out_path}")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"color=c=#0f283c:s=1280x720:d=1,geq=r='15+45*sin(X/120)':g='30+50*cos(Y/90)':b='75+80*sin((X+Y)/150)'",
        "-frames:v", "1", out_path
    ], check=True)
    add_cctv_hud(out_path, hud_text)
    return out_path

# ---------------- NUMPY BINAURAL HORROR AUDIO ENGINE ----------------
def generate_horror_bg_wav(wav_path, duration_sec, bpm=75):
    sr = 22050
    n_samples = int(sr * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False, dtype=np.float32)

    drone = (
        0.22 * np.sin(2 * np.pi * 55.0 * t)
        + 0.18 * np.sin(2 * np.pi * 58.5 * t)
        + 0.12 * np.sin(2 * np.pi * 110.0 * t + 0.5 * np.sin(2 * np.pi * 0.25 * t))
    )

    swell_env = (0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * t - 1.2)) ** 3
    metal_mod = 45.0 * np.sin(2 * np.pi * 19.0 * t)
    metal_screech = 0.16 * swell_env * np.sin(2 * np.pi * 311.0 * t + metal_mod)

    beat_period = 60.0 / bpm
    phase = np.mod(t, beat_period)
    lub = np.exp(-((phase - 0.06) ** 2) / (2 * 0.022 ** 2)) * np.sin(2 * np.pi * 52.0 * t)
    dub = np.exp(-((phase - 0.24) ** 2) / (2 * 0.028 ** 2)) * np.sin(2 * np.pi * 44.0 * t)
    heartbeat = 0.55 * (lub + 0.78 * dub)

    rng = np.random.default_rng(seed=int(bpm))
    noise = rng.normal(0.0, 0.035, n_samples).astype(np.float32)

    mix = drone + metal_screech + heartbeat + noise
    mix = np.clip(mix * 0.72, -0.95, 0.95)
    pcm = (mix * 32767.0).astype(np.int16)

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())

# ---------------- HINDI TTS + LEFT-SIDE DEVANAGARI CAPTIONS ----------------
def srt_to_ass(srt_text, ass_path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HorrorLeft,Noto Sans Devanagari,40,&H00FFFFFF,&H0000FFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,3,2,1,45,420,46,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    blocks = re.split(r"\n\s*\n", srt_text.strip())
    events = []
    for b in blocks:
        lines = [ln.strip() for ln in b.splitlines() if ln.strip()]
        if len(lines) >= 3 and "-->" in lines[1]:
            start_s, end_s = [x.strip() for x in lines[1].split("-->")]
            def fmt(ts):
                ts = ts.replace(",", ".")
                hh, mm, ss = ts.split(":")
                return f"{int(hh)}:{mm}:{float(ss):05.2f}"
            txt = " ".join(lines[2:]).replace("{", "").replace("}", "")
            events.append(f"Dialogue: 0,{fmt(start_s)},{fmt(end_s)},HorrorLeft,,0,0,0,,{txt}")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

async def make_voice_and_subs(text, mp3_path, ass_path):
    for attempt in range(5):
        try:
            comm = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural", rate="-8%", pitch="-5Hz")
            submaker = edge_tts.SubMaker()
            with open(mp3_path, "wb") as f:
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                        submaker.feed(chunk)
            if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 5000:
                srt_to_ass(submaker.get_srt(), ass_path)
                return
        except Exception as e:
            print(f"[TTS Retry {attempt+1}/5] {e}")
            await asyncio.sleep(4)
    raise RuntimeError("TTS failed after 5 attempts")

# ---------------- BUILD PART WITH XFADE, SHAKE & VOICE-GAP SWELL ----------------
def render_part(part_data, img_paths, raw_mp3, ass_path, out_mp4):
    voice_dur = float(MP3(raw_mp3).info.length)
    part_dur = max(MIN_PART_SECONDS, voice_dur + 8.0)

    abs_imgs = [os.path.abspath(p) for p in img_paths]
    abs_mp3 = os.path.abspath(raw_mp3)
    abs_out = os.path.abspath(out_mp4)
    abs_bg_wav = os.path.abspath(out_mp4.replace(".mp4", "_bg.wav"))
    generate_horror_bg_wav(abs_bg_wav, part_dur, bpm=part_data["bpm"])

    n_scenes = len(abs_imgs)
    fade_dur = 0.6
    scene_dur = (part_dur + (n_scenes - 1) * fade_dur) / n_scenes
    frames = max(24, int(math.ceil(scene_dur * 24)))
    transitions = ["fade", "smoothleft", "circleopen", "dissolve", "radial", "smoothright", "fade", "circleopen", "dissolve"]

    inputs = []
    filters = []
    for i, img in enumerate(abs_imgs):
        inputs.extend(["-loop", "1", "-t", f"{scene_dur:.3f}", "-i", img])
        if i in (3, 7, 9):
            zp = f"zoompan=z='1.06+0.0008*on':x='iw/2-(iw/zoom/2)+sin(on*1.7)*7':y='ih/2-(ih/zoom/2)+cos(on*1.3)*5':d={frames}:s=1280x720:fps=24"
        elif i % 2 == 0:
            zp = f"zoompan=z='min(zoom+0.0009,1.16)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1280x720:fps=24"
        else:
            zp = f"zoompan=z='max(1.16-0.0009*on,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1280x720:fps=24"
        filters.append(f"[{i}:v]{zp},eq=saturation=1.28:contrast=1.10,format=yuv420p,setsar=1[v{i}]")

    last_v = "[v0]"
    for i in range(1, n_scenes):
        offset = i * (scene_dur - fade_dur)
        trans = transitions[(i - 1) % len(transitions)]
        out_lbl = f"[vx{i}]" if i < n_scenes - 1 else "[v_all]"
        filters.append(f"{last_v}[v{i}]xfade=transition={trans}:duration={fade_dur}:offset={offset:.3f}{out_lbl}")
        last_v = out_lbl

    ass_name = os.path.basename(ass_path)
    filters.append(f"[v_all]ass={ass_name}[vout]")

    v_idx = n_scenes
    bg_idx = n_scenes + 1
    filters.append(
        f"[{v_idx}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=whole_dur={part_dur:.2f},aecho=0.8:0.7:45:0.18,volume=1.35,asplit=2[voice1][voice2]"
    )
    filters.append(
        f"[{bg_idx}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,volume=0.85[bg]"
    )
    filters.append("[bg][voice1]sidechaincompress=threshold=0.015:ratio=8:attack=30:release=350[bg_ducked]")
    filters.append("[voice2][bg_ducked]amix=inputs=2:duration=first:normalize=0[aout]")

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-i", abs_mp3, "-i", abs_bg_wav,
        "-filter_complex", ";".join(filters),
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{part_dur:.2f}", abs_out
    ]
    orig_cwd = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.abspath(ass_path)))
        subprocess.run(cmd, check=True)
    finally:
        os.chdir(orig_cwd)

async def main():
    part_files = []
    for data in PARTS:
        p = data["part"]
        out_mp4 = os.path.join(PARTS_DIR, f"part_{p:02d}.mp4")
        raw_mp3 = os.path.join(PARTS_DIR, f"voice_{p:02d}.mp3")
        ass_path = os.path.join(PARTS_DIR, f"subs_{p:02d}.ass")

        if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 500000:
            print(f"[Part {p}] Already cached, skipping.")
            part_files.append(out_mp4)
            continue

        print(f"[Part {p}] Generating 10 vibrant 3D horror scenes...")
        imgs = []
        for s_idx, prompt in enumerate(data["scenes"]):
            img_p = os.path.join(IMG_DIR, f"p{p:02d}_s{s_idx:02d}.png")
            generate_3d_image(prompt, img_p, data["hud"], seed=p * 100 + s_idx)
            imgs.append(img_p)

        print(f"[Part {p}] Generating Hindi voiceover & Devanagari captions...")
        await make_voice_and_subs(data["narration"], raw_mp3, ass_path)

        print(f"[Part {p}] Rendering horror video with shake, xfade & gap-swell audio...")
        render_part(data, imgs, raw_mp3, ass_path, out_mp4)
        part_files.append(out_mp4)
        await asyncio.sleep(3)

    concat_txt = "/tmp/all_parts_v3.txt"
    with open(concat_txt, "w") as f:
        for pf in part_files:
            f.write(f"file '{os.path.abspath(pf)}'\n")

    final_mp4 = os.path.join(OUT_DIR, "FINAL_3D_HORROR_V3_25MIN_2026-11-13.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", final_mp4
    ], check=True)
    print(f"SUCCESS! Final 25+ min Horror Video ready: {final_mp4}")

if __name__ == "__main__":
    asyncio.run(main())
