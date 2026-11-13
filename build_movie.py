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
PARTS_DIR = os.path.join(OUT_DIR, "parts_v51")
IMG_DIR = os.path.join(OUT_DIR, "images_v51")
os.makedirs(PARTS_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

MIN_PART_SECONDS = 188.0
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "").strip()

OWL_CHAR = (
    "3D Pixar animation movie style, mysterious wise barn owl wearing vintage round brass spectacles and small headset, "
    "rich cyan and warm amber neon cinematic lighting, looking directly at camera as a horror storyteller, "
    "ultra detailed 3D character render, atmospheric fog, 8k, no text, no watermark"
)
ENV_STYLE = (
    "3D Pixar animation movie style environment shot, vibrant cyan amber crimson neon lighting, "
    "ultra detailed 3D cinematic scene, eerie volumetric fog, dramatic horror atmosphere, 8k, no text, no watermark"
)

# 12 Distinct Owl Locations (Flying + Sitting on Ground + Trees + Lab + Rooftop)
OWL_PROMPTS = [
    f"{OWL_CHAR}, wings spread wide flying swiftly down from a tall dark misty tree at night toward camera, glowing cyan moonlight",
    f"{OWL_CHAR}, sitting calmly on wet cobblestone ground beside a glowing vintage lantern in dark misty forest",
    f"{OWL_CHAR}, perched on a gnarled ancient tree branch overlooking a glowing dark science facility at night",
    f"{OWL_CHAR}, sitting on a dusty metallic laboratory table beside a glowing red EMF meter and headphones",
    f"{OWL_CHAR}, flying dynamically through dark rainy neon-lit alleyways with glowing blue wings edge-light",
    f"{OWL_CHAR}, sitting on wet concrete underground basement stairs with eerie red emergency lights behind",
    f"{OWL_CHAR}, perched on a rusted iron windowsill looking into camera with glowing fog outside",
    f"{OWL_CHAR}, sitting on a pile of old 1982 leather diaries and glowing cassette tapes on dark floor",
    f"{OWL_CHAR}, gliding low over misty dark ground under purple storm clouds with intense glowing eyes",
    f"{OWL_CHAR}, perched on top of a vintage copper Tesla coil humming with bright blue sparks",
    f"{OWL_CHAR}, sitting on a rooftop edge at 3 AM with glowing neon Delhi city lights far below in fog",
    f"{OWL_CHAR}, sitting in a dark neon podcast studio chair in front of a glowing condenser microphone"
]

# ---------------- 8-PART CONVERSATIONAL AMAAN-STYLE HORROR SCRIPT ----------------
PARTS = [
    {
        "part": 1,
        "bpm": 62,
        "hud": "OWL-CAST ● LAB-04 | 18.9 Hz",
        "narration": (
            "गाइस, क्या आपने कभी ऐसी जगह के बारे में सुना है जहाँ हवा तो बिल्कुल शांत होती है, लेकिन खड़े होते ही आपके रोंगटे अपने आप खड़े हो जाते हैं? "
            "सच बताऊँ तो आज जो कहानी मैं आपको सुनाने जा रहा हूँ, यह दिल्ली की एक सीलबंद सरकारी लैब के यंग इलेक्ट्रॉनिक्स इंजीनियर आरव की है। "
            "आरव बिल्कुल हमारी और आपकी तरह प्रैक्टिकल था — वह भूत-प्रेत पर नहीं, सिर्फ साइंस और डेटा पर यकीन करता था। "
            "लेकिन रात के ठीक दो बजकर चौदह मिनट पर जब शहर की हर घड़ी थम चुकी थी, तब उस वीरान लैब में आरव का ईएमएफ मीटर अचानक लाल होकर चीखने लगा। "
            "उसने अपने स्टूडियो हेडफोन लगाए और अठारह दशमलव नौ हर्ट्ज़ की एक अनसुनी फ्रीक्वेंसी रिकॉर्ड की। "
            "उसी सेकंड कमरे का तापमान पंद्रह डिग्री से गिरकर शून्य पर आ गया। आरव की सांसें भारी होने लगीं और ठीक उसकी गर्दन के पीछे किसी के ठंडे सांस लेने की आवाज गूंजी। "
            "गाइस, विज्ञान कहता है कि अठारह दशमलव नौ हर्ट्ज़ वो खूनी आवृत्ति है जिसे हमारे कान सुन नहीं सकते, लेकिन हमारी आंखों की पुतलियां इससे कांपने लगती हैं — और दिमाग को कोने में एक काली परछाईं दिखने लगती है। "
            "आरव ने सोचा यह सिर्फ उसकी आंखों का धोखा है, पर तभी बिना इंटरनेट के उसके लैपटॉप पर उन्नीस सौ बयासी की एक सील बंद फाइल अपने आप खुल गई। "
            "दोस्तो, असली खौफ अभी शुरू भी नहीं हुआ था। कहानी में आगे बढ़ने से पहले अगर आपको ऐसी असली साइंस-हॉरर कहानियां पसंद हैं, तो चैनल को सब्सक्राइब जरूर कर लीजिए।"
        ),
        "scenes": [
            f"{ENV_STYLE}, wide eerie shot of an abandoned underground science lab corridor at 2 AM with glowing cyan and red emergency lights",
            f"{ENV_STYLE}, close up of retro oscilloscope monitor showing jagged glowing crimson 18.9 Hz soundwave",
            f"{ENV_STYLE}, frosty glass window in dark laboratory with a tall shadowy silhouette looming behind it",
            f"{ENV_STYLE}, heavy rusted metallic door labelled LAB 4 with spinning red alarm light and thick teal fog",
            f"{ENV_STYLE}, laptop screen glowing bright blue in darkness automatically opening a classified 1982 red-stamped file"
        ]
    },
    {
        "part": 2,
        "bpm": 68,
        "hud": "OWL-CAST ● ARCHIVE | CO-HIGH",
        "narration": (
            "तो गाइस, आरव की स्क्रीन पर जो पुरानी फाइल खुली, वह किसी अनजान इंसान की नहीं, बल्कि खुद उसके दादाजी डॉक्टर विश्वनाथ शर्मा की थी। "
            "उन्नीस सौ बयासी में वे इसी सरकारी प्रयोगशाला के हेड साइंटिस्ट थे, और तीन नवंबर की एक काली रात को वे यहीं से रहस्यमय तरीके से गायब हो गए थे। "
            "आरव ने कांपते हाथों से अपनी जेब का डिजिटल गैस सेंसर चालू किया, तो उसका अलार्म पागल हो उठा — कमरे में कार्बन मोनोऑक्साइड खतरे के निशान से चार गुना ऊपर थी। "
            "अब आप कहेंगे कि यार, ये गैस तो दिमाग में डर और मतिभ्रम पैदा करती है, मरे हुए लोग दिखाती है। आरव ने भी ठीक यही सोचा और खुद को संभाला। "
            "उसने अपनी टॉर्च जलाई और छत के ऊपर लगे पुराने वेंटिलेशन शाफ्ट की तरफ बढ़ा। "
            "लेकिन दोस्तो, तभी उस बंद लोहे के पाइप के अंदर से एक ऐसी दर्दनाक चीख निकली जिसने आरव के गैस सेंसर की कांच की सुई को वहीं तोड़ दिया। "
            "आरव वहीं जम गया। क्या कार्बन मोनोऑक्साइड किसी लोहे के दरवाजे को अंदर से पीट सकती है? क्या जहरीली गैस किसी का नाम पुकार सकती है? नहीं, हरगिज नहीं। "
            "उस बंद वेंट के अंदर से किसी के नाखूनों के रगड़ने की खुरदुरी आवाज आ रही थी, जैसे कोई अंदर फंसा हो। "
            "आरव ने जैसे ही टॉर्च की तेज रोशनी जाली के अंदर घुमाई, वहां दो चमकती आंखें उसे घूर रही थीं — और उसके हाथ से टॉर्च नीचे गिर गई।"
        ),
        "scenes": [
            f"{ENV_STYLE}, glowing vintage 1982 black-and-white scientist photograph floating on a futuristic blue holographic display",
            f"{ENV_STYLE}, close up of handheld digital gas detector flashing bright crimson CO DANGER 400 PPM",
            f"{ENV_STYLE}, toxic emerald green and amber mist seeping out from rusty metallic ceiling air vents",
            f"{ENV_STYLE}, heavy steel ventilation grate shaking violently with bright orange electrical sparks",
            f"{ENV_STYLE}, two eerie pale glowing eyes peering out from inside a pitch-black metallic air duct"
        ]
    },
    {
        "part": 3,
        "bpm": 74,
        "hud": "OWL-CAST ● STONE-TAPE | 480 V",
        "narration": (
            "अब सुनिए आगे क्या हुआ। फर्श पर गिरी टॉर्च लुढ़कती हुई सीधे एक गुप्त लोहे के दरवाजे के सामने रुकी, जिसके नीचे से बेसमेंट की सीढ़ियां जाती थीं। "
            "पत्थर की उन सीली दीवारों से पानी नहीं, बल्कि गाढ़ा लाल जंग टपक रहा था। वहीं कोने में आरव को चमड़े की एक जली हुई पुरानी डायरी मिली। "
            "धूल झाड़कर जब उसने पहला पन्ना खोला, तो उस पर दादाजी की लिखावट में लिखा था, स्टोन टेप थ्योरी। "
            "गाइस, इस सिद्धांत के मुताबिक जब किसी जगह पर भयानक दर्द, खौफ या किसी की अकाल मौत होती है, तो उस घटना की एनर्जी आसपास के पत्थरों में मैग्नेटिक टेप की तरह रिकॉर्ड हो जाती है। "
            "आरव ने अपना चुंबकीय रिकॉर्डर उन भीगी हुई दीवारों से सटाया। अगले ही सेकंड स्पीकर से उन्नीस सौ बयासी की उस रात की रिकॉर्डिंग अपने आप बजने लगी। "
            "गोलियों और कांच टूटने की आवाजों के बीच कोई चिल्ला रहा था, विश्वनाथ, मशीन बंद करो, अठारह दशमलव नौ हर्ट्ज़ ने दूसरी तरफ का दरवाजा खोल दिया है। "
            "सोचो गाइस, आरव के रोंगटे खड़े हो गए होंगे। यह कोई पुरानी कहानी नहीं थी, यह वक्त के पत्थरों में कैद एक जिंदा चीख थी। "
            "तभी ऊपर सीढ़ियों पर किसी के गीले कदमों की छप-छप आवाज आई, और ऊपर का भारी लोहे का दरवाजा धड़ाम से बंद होकर लॉक हो गया।"
        ),
        "scenes": [
            f"{ENV_STYLE}, steep dark underground concrete staircase with glowing red rust stains and swirling cyan mist",
            f"{ENV_STYLE}, ancient burned leather diary lying on wet stone steps glowing softly in warm amber flashlight beam",
            f"{ENV_STYLE}, 3D visualization of dark stone basement walls pulsing with glowing blue and crimson magnetic energy waves",
            f"{ENV_STYLE}, retro cassette magnetic recorder pressed against wet concrete wall with glowing neon red LEDs",
            f"{ENV_STYLE}, massive heavy iron basement door slamming shut with bright orange sparks and dust explosion"
        ]
    },
    {
        "part": 4,
        "bpm": 80,
        "hud": "OWL-CAST ● BASEMENT | TEMP -4C",
        "narration": (
            "अब आरव जमीन से तीस फीट नीचे उस सील बंद बेसमेंट में कैद था, और फोन का नेटवर्क पूरी तरह मर चुका था। "
            "अपनी जान बचाने के लिए उसने बैग से अपना थर्मल इमेजिंग कैमरा निकाला — आप जानते हैं ना, थर्मल कैमरा अंधेरे में भी तापमान से हर चीज दिखा देता है। "
            "जैसे ही उसने स्क्रीन से हॉल को स्कैन किया, उसके हाथ कांपने लगे। नंगी आंखों से देखने पर सामने वाला कोना बिल्कुल खाली था, वहां हवा के सिवा कुछ नहीं था। "
            "लेकिन दोस्तो, थर्मल कैमरे की स्क्रीन पर ठीक उसी खाली कोने में एक सात फीट ऊंची बर्फीली नीली आकृति खड़ी थी, जिसका तापमान माइनस दस डिग्री दिखा रहा था। "
            "हर जिंदा शरीर से गर्मी निकलती है, पर यह चीज कमरे की सारी गर्मी को अपने अंदर सोख रही थी ताकि खुद को जिंदा रख सके। "
            "जैसे ही आरव ने एक कदम आगे बढ़ाया, उसके थर्मोमीटर का पारा कांच के अंदर ही जम गया और मुंह से सफेद भाप निकलने लगी। "
            "देखते ही देखते वह सात फीट लंबी नीली आकृति धीरे-धीरे उसकी तरफ घूमी। उसका कोई चेहरा नहीं था, लेकिन उसके सीने में एक चमकता हुआ क्वांटम चक्र घूम रहा था। "
            "उसने अपना बर्फीला हाथ उठाया, और एक सेकंड में पूरे कमरे की बिजली गुल हो गई। क्या दादाजी ने उन्नीस सौ बयासी में किसी दूसरी दुनिया से इस शैतान को बुलाया था?"
        ),
        "scenes": [
            f"{ENV_STYLE}, glowing thermal camera viewfinder showing a 7-foot tall icy electric-blue human entity standing in empty corner",
            f"{ENV_STYLE}, vibrant neon heat-map silhouettes shifting from fiery orange to freezing lethal cyan blue",
            f"{ENV_STYLE}, close up of glass thermometer mercury freezing into glowing sharp ice crystals",
            f"{ENV_STYLE}, towering translucent 7-foot icy-blue phantom turning slowly with a spinning golden quantum vortex in its chest",
            f"{ENV_STYLE}, vintage 1982 copper Tesla coils humming with bright purple lightning arcs in dark server room"
        ]
    },
    {
        "part": 5,
        "bpm": 86,
        "hud": "OWL-CAST ● DIARY-82 | QUANTUM",
        "narration": (
            "आरव किसी तरह जान बचाकर भागते हुए एक भारी लोहे की मेज के नीचे छिप गया, और कांपती टॉर्च में दादाजी की डायरी के बाकी पन्ने पलटने लगा। "
            "पन्ना नंबर चवालीस पर लाल स्याही से एक ऐसी बात लिखी थी जिसने उसके होश उड़ा दिए। "
            "दादाजी ने लिखा था कि इंसान की चेतना और आत्मा सिर्फ दिमाग के रसायनों का खेल नहीं है, बल्कि यह एक शुद्ध क्वांटम बायो-एनर्जी है। "
            "ऊर्जा न कभी पैदा होती है और न ही नष्ट होती है, मौत के बाद भी वह सिर्फ अपना रूप बदलकर हमारे आसपास घूमती रहती है। "
            "उन्नीस सौ बयासी में दादाजी ने तांबे के कॉइल से एक ऐसी मशीन बनाई थी जो अठारह दशमलव नौ हर्ट्ज़ से उस बायो-एनर्जी को पकड़ सकती थी। "
            "शुरुआत में वे सिर्फ आवाजें रिकॉर्ड करना चाहते थे। लेकिन तीन नवंबर उन्नीस सौ बयासी की रात, जब उन्होंने मशीन की ताकत सौ गुना बढ़ाई, तो लैब चार की दीवार समय और आयाम के बीच फट गई। "
            "दो दुनियाओं के बीच का दरवाजा खुल गया, और दूसरी तरफ से कोई ऐसी चीज अंदर आई जो समय की भूखी थी। उस चीज ने दादाजी को मारा नहीं, बल्कि समय के जाल में जिंदा कैद कर लिया। "
            "तभी गाइस, मेज के ऊपर रखे पुराने कांच के बीकर अपने आप हवा में तैरने लगे और आरव की तरफ मुड़ गए।"
        ),
        "scenes": [
            f"{ENV_STYLE}, close up of open handwritten 1982 diary page 44 with glowing golden quantum bio-energy diagrams",
            f"{ENV_STYLE}, vibrant 3D glowing neural energy particles swirling into shape of a human soul above dark desk",
            f"{ENV_STYLE}, dramatic dimensional tear glowing bright purple and cyan ripping open in the middle of Lab 4 wall",
            f"{ENV_STYLE}, silhouette of an elderly scientist reaching out from inside a swirling golden time vortex",
            f"{ENV_STYLE}, glass laboratory beakers filled with colourful glowing liquids levitating eerily in mid-air"
        ]
    },
    {
        "part": 6,
        "bpm": 92,
        "hud": "OWL-CAST ● LAB-04 | DANGER",
        "narration": (
            "हवा में तैरते वे कांच के बीकर आरव की तरफ गोली की तरह लपके, लेकिन ठीक उसके चेहरे से दो इंच पहले हवा में ही रुक गए। "
            "पूरे कमरे में सैकड़ों फुसफुसाती आवाजें एक साथ गूंजने लगीं। आरव ने दोनों कान बंद कर लिए, पर आवाजें कम नहीं हुईं। "
            "जब उसने स्पेक्ट्रम एनालाइजर खोला तो देखा कि वे आवाजें हवा से नहीं, बल्कि सीधे उसके दिमाग के ऑडिटरी कॉर्टेक्स में इलेक्ट्रोमैग्नेटिक तरंगों से भेजी जा रही थीं। "
            "तभी ठीक सामने लैब चार का वो भारी सीलबंद लोहे का दरवाजा, जिस पर चालीस साल से जंग लगा था, बिना किसी चाबी के अपने आप चरमराते हुए खुलने लगा। "
            "अंदर से नीली और बैंगनी रोशनी की ऐसी तेज किरण बाहर आई कि पूरे बेसमेंट की धूल हवा में जम गई। "
            "आरव ने हिम्मत जुटाई और अंदर कदम रखा। बीच कमरे में तांबे के तारों से बनी दादाजी की वह विशाल मशीन आज भी बिना बिजली के चल रही थी। "
            "मशीन के बीच में एक बड़ा सा कांच का बेलनाकार चैंबर था, जो सुनहरी धुंध से भरा था। "
            "और जैसे ही आरव उसके करीब गया, उस धुंधले कांच के अंदर से एक बुजुर्ग इंसान का कांपता हुआ हाथ धीरे-धीरे कांच पर टकराया। सोचो गाइस, अंदर कौन था?"
        ),
        "scenes": [
            f"{ENV_STYLE}, swirling colourful ghostly soundwaves and eerie shadows echoing in a dark laboratory",
            f"{ENV_STYLE}, close up of glowing digital spectrum analyzer showing crazy neon red electromagnetic spikes",
            f"{ENV_STYLE}, massive rusted vault door of LAB 4 creaking open with blinding cyan and purple light beams",
            f"{ENV_STYLE}, cylindrical glowing glass time-chamber in center of dark lab pulsing with golden quantum energy",
            f"{ENV_STYLE}, close up of an elderly human hand pressing desperately against foggy glowing glass from inside"
        ]
    },
    {
        "part": 7,
        "bpm": 98,
        "hud": "OWL-CAST ● CLIMAX | 18.9 Hz!",
        "narration": (
            "दोस्तो, आरव के पैर मानो पत्थर के हो गए और आंखों से आंसू निकल आए, जब उसने उस कांच के चैंबर के अंदर अपने दादाजी डॉक्टर विश्वनाथ को जिंदा देखा। "
            "उनकी उम्र उन्नीस सौ बयासी से एक दिन भी नहीं बढ़ी थी, क्योंकि उस चैंबर के अंदर वक्त पूरी तरह थम चुका था। "
            "लेकिन उसकी खुशी एक सेकंड में खौफ में बदल गई, जब उसने देखा कि दादाजी के ठीक पीछे उस नीली रोशनी में एक और विशाल साया हिल रहा है। "
            "उस साये की दोनों आंखें जलते अंगारों की तरह लाल चमक रही थीं। दादाजी ने कांच पर उंगली से उल्टा लिखा, आरव, मुख्य केबल काटो, वरना आज रात यह पूरे शहर को निगल लेगा। "
            "उसी पल आरव के हाथ का ईएमएफ मीटर चिंगारियां छोड़कर फट गया और कमरे की सारी लोहे की कुर्सियां दीवारों से जाकर चिपक गईं। "
            "सोचने के लिए एक सेकंड भी नहीं था। आरव ने जेब से हेवी-ड्यूटी मल्टी-टूल निकाला और उस मुख्य तांबे की केबल की तरफ दौड़ा। "
            "उसके दौड़ते ही उस लाल आंखों वाले शैतानी साये ने एक ऐसी कान फाड़ देने वाली चीख मारी कि लैब की सारी ट्यूबलाइटें एक साथ हवा में फट गईं और कांच चारों तरफ बरसने लगा।"
        ),
        "scenes": [
            f"{ENV_STYLE}, elderly grandfather scientist inside glass chamber with a terrifying glowing red-eyed shadow monster looming behind him",
            f"{ENV_STYLE}, foggy glass surface showing backwards handwritten warning words glowing in bright crimson neon",
            f"{ENV_STYLE}, heavy metal laboratory chairs flying and slamming violently onto glowing magnetic walls",
            f"{ENV_STYLE}, terrifying dark phantom monster with blazing crimson eyes roaring with electric purple shockwaves",
            f"{ENV_STYLE}, ceiling neon tube lights shattering simultaneously in slow motion with bright sparks"
        ]
    },
    {
        "part": 8,
        "bpm": 105,
        "hud": "OWL-CAST ● SIGNAL LOST | 04:00 AM",
        "narration": (
            "कांच के टूटते टुकड़ों के बीच आरव ने पूरी ताकत से उस मुख्य तांबे की केबल को बीच से काट दिया। "
            "एक जोरदार सुनहरी चिंगारी उठी, मशीन की गूंज थम गई, और पूरा बेसमेंट गहरे सन्नाटे में डूब गया। वह लाल आंखों वाला साया नीले धुएं में बदलकर गायब हो गया। "
            "जब आरव कांपते हुए उस कांच के चैंबर के पास पहुंचा, तो चैंबर खाली था — दादाजी को आखिरकार समय के उस जाल से आजादी मिल चुकी थी। "
            "पर फर्श पर उन्नीस सौ बयासी की एक सुनहरी पॉकेट घड़ी रखी थी, जिसकी सुई अभी भी टिक-टिक चल रही थी। "
            "सुबह ठीक चार बजे आरव सुरक्षित अपने घर लौट आया। गाइस, कहानी यहाँ खत्म नहीं होती। "
            "जब आरव ने घर जाकर लैपटॉप पर अपनी वो ऑडियो रिकॉर्डिंग दोबारा सुनी, तो रिकॉर्डिंग के आखिरी सेकंड में उसके दादाजी की साफ आवाज गूंजी, आरव, तुमने तार तो काट दिया, पर दरवाजा अभी पूरी तरह बंद नहीं हुआ है। "
            "तो दोस्तो, अगर आज रात आपको भी सन्नाटे में अजीब सी गूंज सुनाई दे, तो एक बार जरूर सोचना। कमेंट में बताइएगा कहानी कैसी लगी, और वीडियो को लाइक व सब्सक्राइब करना मत भूलिएगा। मिलते हैं अगली डरावनी रात में!"
        ),
        "scenes": [
            f"{ENV_STYLE}, terrifying crimson-eyed shadow dissolving into a swirling cyan smoke vortex in Lab 4",
            f"{ENV_STYLE}, quiet peaceful Lab 4 bathed in soft morning blue light and fading mist",
            f"{ENV_STYLE}, macro close up of antique golden pocket watch ticking inside warm glowing dust beams",
            f"{ENV_STYLE}, close up of laptop audio waveform spiking suddenly in bright blood red at the very last second",
            f"{ENV_STYLE}, cinematic mysterious glowing title aura with 18.9 Hz neon soundwave in dark mist"
        ]
    }
]

# ---------------- IMAGE GENERATOR (CF + POLLINATIONS + DARK HORROR FALLBACK) ----------------
def is_valid_bright_image(path):
    if not os.path.exists(path) or os.path.getsize(path) < 18000:
        return False
    try:
        with Image.open(path) as im:
            arr = np.asarray(im.convert("RGB"), dtype=np.float32)
            if arr.mean() < 10.0:
                return False
        return True
    except Exception:
        return False

def process_and_add_hud(path, hud_text):
    try:
        with Image.open(path) as im:
            w, h = im.size
            im = im.crop((0, 0, w, int(h * 0.94))).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(im, "RGBA")
            draw.rounded_rectangle([850, 18, 1260, 56], radius=8, fill=(8, 12, 20, 175), outline=(220, 45, 45, 200), width=2)
            draw.ellipse([866, 30, 880, 44], fill=(255, 40, 40, 255))
            font = ImageFont.load_default()
            draw.text((890, 31), hud_text, fill=(245, 245, 255, 240), font=font)
            im.save(path, "PNG")
    except Exception as e:
        print(f"[HUD Warn] {e}")

def create_dark_horror_oscilloscope(out_path, hud_text, seed):
    w, h = 1280, 720
    y_grid, x_grid = np.mgrid[0:h, 0:w].astype(np.float32)
    dist = np.sqrt(((x_grid - w / 2) / (w / 2)) ** 2 + ((y_grid - h / 2) / (h / 2)) ** 2)
    vig = np.clip(1.0 - 0.65 * dist, 0.12, 1.0)
    r = (14 + 28 * np.sin(seed + x_grid / 220.0) ** 2) * vig
    g = (32 + 34 * np.cos(seed + y_grid / 180.0) ** 2) * vig
    b = (58 + 48 * vig)
    rgb = np.stack([np.clip(r, 0, 255), np.clip(g, 0, 255), np.clip(b, 0, 255)], axis=-1).astype(np.uint8)
    im = Image.fromarray(rgb, "RGB")
    draw = ImageDraw.Draw(im, "RGBA")
    for yy in range(0, h, 4):
        draw.line([(0, yy), (w, yy)], fill=(0, 0, 0, 45), width=1)
    pts = [(xx, int(h * 0.48 + 75 * math.sin(xx * 0.025 + seed) * math.cos(xx * 0.008))) for xx in range(0, w, 6)]
    draw.line(pts, fill=(255, 45, 65, 210), width=4)
    im.save(out_path, "PNG")
    process_and_add_hud(out_path, hud_text)

def generate_3d_image(prompt, out_path, hud_text, seed):
    if is_valid_bright_image(out_path):
        return out_path
    if os.path.exists(out_path):
        os.remove(out_path)

    if CF_ACCOUNT_ID and CF_API_TOKEN:
        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
        headers = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "steps": 4}
        for attempt in range(2):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=90)
                ctype = r.headers.get("Content-Type", "")
                if r.status_code == 200 and "application/json" in ctype:
                    b64 = r.json().get("result", {}).get("image")
                    if b64:
                        with open(out_path, "wb") as f:
                            f.write(base64.b64decode(b64))
                        if is_valid_bright_image(out_path):
                            process_and_add_hud(out_path, hud_text)
                            return out_path
                elif r.status_code == 200 and len(r.content) > 18000:
                    with open(out_path, "wb") as f:
                        f.write(r.content)
                    if is_valid_bright_image(out_path):
                        process_and_add_hud(out_path, hud_text)
                        return out_path
                if r.status_code in (402, 429):
                    break
            except Exception as e:
                print(f"[CF Err] {e}")
            time.sleep(2)

    encoded = urllib.parse.quote(prompt)
    for model in ("flux", "turbo", "flux"):
        pol_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&model={model}&seed={seed}&nologo=true"
        try:
            r = requests.get(pol_url, timeout=110)
            if r.status_code == 200 and len(r.content) > 18000 and "image" in r.headers.get("Content-Type", ""):
                with open(out_path, "wb") as f:
                    f.write(r.content)
                if is_valid_bright_image(out_path):
                    process_and_add_hud(out_path, hud_text)
                    time.sleep(2)
                    return out_path
        except Exception as e:
            print(f"[Pollinations Err ({model})] {e}")
        time.sleep(4)

    create_dark_horror_oscilloscope(out_path, hud_text, seed)
    return out_path

# ---------------- CINEMATIC HORROR SCORE ENGINE (NO BUZZ!) ----------------
def generate_horror_bg_wav(wav_path, duration_sec, bpm=75):
    sr = 22050
    n_samples = int(sr * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False, dtype=np.float32)

    sub_lfo = 0.55 + 0.45 * np.sin(2 * np.pi * 0.12 * t)
    sub_bass = 0.24 * sub_lfo * np.sin(2 * np.pi * 48.0 * t)

    beat_period = 60.0 / bpm
    phase = np.mod(t, beat_period)
    lub = np.exp(-((phase - 0.06) ** 2) / (2 * 0.024 ** 2)) * np.sin(2 * np.pi * 55.0 * t)
    dub = np.exp(-((phase - 0.23) ** 2) / (2 * 0.030 ** 2)) * np.sin(2 * np.pi * 46.0 * t)
    heartbeat = 0.65 * (lub + 0.78 * dub)

    chimes = np.zeros(n_samples, dtype=np.float32)
    horror_freqs = [293.66, 311.13, 277.18, 440.0, 261.63, 392.0]
    step_sec = 5.5
    idx = 0
    cur = 1.5
    while cur < duration_sec - 2.0:
        f = horror_freqs[idx % len(horror_freqs)]
        start_i = int(cur * sr)
        note_len = min(int(4.2 * sr), n_samples - start_i)
        if note_len > 0:
            nt = np.linspace(0, note_len / sr, note_len, endpoint=False, dtype=np.float32)
            env = np.exp(-nt * 1.45) * (1.0 - np.exp(-nt * 45.0))
            tone = (0.65 * np.sin(2 * np.pi * f * nt) + 0.25 * np.sin(2 * np.pi * (f * 2.0) * nt)) * env
            chimes[start_i:start_i + note_len] += 0.26 * tone
        cur += step_sec
        idx += 1

    riser = np.zeros(n_samples, dtype=np.float32)
    r_len = min(int(5.0 * sr), n_samples)
    rt = np.linspace(0, r_len / sr, r_len, endpoint=False, dtype=np.float32)
    r_freq = 90.0 + 260.0 * (rt / (r_len / sr)) ** 2
    r_env = (rt / (r_len / sr)) ** 2
    riser[-r_len:] = 0.28 * r_env * np.sin(2 * np.pi * np.cumsum(r_freq) / sr)

    mix = sub_bass + heartbeat + chimes + riser
    mix = np.clip(mix * 0.78, -0.95, 0.95)
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
            comm = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural", rate="-6%", pitch="-4Hz")
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

# ---------------- BUILD PART: ALTERNATING MULTI-LOCATION OWL + SCENES ----------------
def render_part(part_data, timeline_imgs, raw_mp3, ass_path, out_mp4):
    voice_dur = float(MP3(raw_mp3).info.length)
    part_dur = max(MIN_PART_SECONDS, voice_dur + 4.0)

    abs_imgs = [os.path.abspath(p) for p in timeline_imgs]
    abs_mp3 = os.path.abspath(raw_mp3)
    abs_out = os.path.abspath(out_mp4)
    abs_bg_wav = os.path.abspath(out_mp4.replace(".mp4", "_bg.wav"))
    generate_horror_bg_wav(abs_bg_wav, part_dur, bpm=part_data["bpm"])

    n_scenes = len(abs_imgs)
    fade_dur = 0.6
    scene_dur = (part_dur + (n_scenes - 1) * fade_dur) / n_scenes
    frames = max(24, int(math.ceil(scene_dur * 24)))
    transitions = ["fade", "smoothleft", "dissolve", "smoothright", "fade", "circleopen", "dissolve", "smoothleft", "fade"]

    inputs = []
    filters = []
    for i, img in enumerate(abs_imgs):
        inputs.extend(["-loop", "1", "-t", f"{scene_dur:.3f}", "-i", img])
        if i % 2 == 0:
            # Flying/Talking Owl Motion: smooth forward glide + gentle bobbing
            zp = f"zoompan=z='1.02+0.0007*on+0.018*abs(sin(on*0.22))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+sin(on*0.28)*5':d={frames}:s=1280x720:fps=24"
        elif i in (5, 9):
            zp = f"zoompan=z='1.06+0.0008*on':x='iw/2-(iw/zoom/2)+sin(on*1.7)*7':y='ih/2-(ih/zoom/2)+cos(on*1.3)*5':d={frames}:s=1280x720:fps=24"
        else:
            zp = f"zoompan=z='min(zoom+0.0009,1.16)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1280x720:fps=24"
        filters.append(f"[{i}:v]{zp},eq=saturation=1.25:contrast=1.08,format=yuv420p,setsar=1[v{i}]")

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
        f"apad=whole_dur={part_dur:.2f},aecho=0.8:0.7:45:0.15,volume=1.40,asplit=2[voice1][voice2]"
    )
    filters.append(
        f"[{bg_idx}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,volume=0.88[bg]"
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
    # 1. Generate 12 distinct Owl locations (flying, ground, trees, lab, rooftop, studio)
    owl_imgs = []
    for idx, op in enumerate(OWL_PROMPTS):
        op_path = os.path.join(IMG_DIR, f"owl_loc_{idx:02d}.png")
        generate_3d_image(op, op_path, "OWL-CAST ● LIVE", seed=800 + idx)
        owl_imgs.append(op_path)

    part_files = []
    owl_cursor = 0
    for data in PARTS:
        p = data["part"]
        out_mp4 = os.path.join(PARTS_DIR, f"part_{p:02d}.mp4")
        raw_mp3 = os.path.join(PARTS_DIR, f"voice_{p:02d}.mp3")
        ass_path = os.path.join(PARTS_DIR, f"subs_{p:02d}.ass")

        if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 500000:
            part_files.append(out_mp4)
            owl_cursor += len(data["scenes"])
            continue

        timeline_imgs = []
        for s_idx, prompt in enumerate(data["scenes"]):
            owl_pick = owl_imgs[owl_cursor % len(owl_imgs)]
            owl_cursor += 1
            timeline_imgs.append(owl_pick)
            sc_path = os.path.join(IMG_DIR, f"p{p:02d}_s{s_idx:02d}.png")
            generate_3d_image(prompt, sc_path, data["hud"], seed=p * 100 + s_idx)
            timeline_imgs.append(sc_path)

        print(f"[Part {p}] Generating conversational Hindi narration...")
        await make_voice_and_subs(data["narration"], raw_mp3, ass_path)

        print(f"[Part {p}] Rendering Multi-Location Owl Host + Horror Scenes...")
        render_part(data, timeline_imgs, raw_mp3, ass_path, out_mp4)
        part_files.append(out_mp4)
        await asyncio.sleep(3)

    concat_txt = "/tmp/all_parts_v51.txt"
    with open(concat_txt, "w") as f:
        for pf in part_files:
            f.write(f"file '{os.path.abspath(pf)}'\n")

    final_mp4 = os.path.join(OUT_DIR, "FINAL_3D_OWL_HORROR_V51_25MIN_2026-11-13.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", final_mp4
    ], check=True)
    print(f"SUCCESS! Final 25+ min Multi-Location Owl Horror Video ready: {final_mp4}")

if __name__ == "__main__":
    asyncio.run(main())
