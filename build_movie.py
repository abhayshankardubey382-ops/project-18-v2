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
PARTS_DIR = os.path.join(OUT_DIR, "parts_v4")
IMG_DIR = os.path.join(OUT_DIR, "images_v4")
os.makedirs(PARTS_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

MIN_PART_SECONDS = 188.0  # 8 parts x ~188s = ~25+ min continuous narration
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "").strip()

AARAV_STYLE = (
    "3D Pixar animation movie style, vibrant cinematic lighting, rich cyan and warm amber neon colors, "
    "expressive Indian young male engineer Aarav in dark hoodie with glowing blue tech goggles, "
    "ultra detailed 3D render, dramatic shadows, atmospheric fog, 8k, no text, no watermark"
)
ENV_STYLE = (
    "3D Pixar animation movie style environment shot, no people unless specified, vibrant cyan amber crimson neon lighting, "
    "ultra detailed 3D cinematic scene, eerie volumetric fog, dramatic horror atmosphere, 8k, no text, no watermark"
)

# ---------------- 8-PART FULL-LENGTH 25-MIN HORROR SCRIPT ----------------
PARTS = [
    {
        "part": 1,
        "bpm": 62,
        "hud": "REC ● LAB-04 | 02:14 AM | 18.9 Hz",
        "narration": (
            "रात के ठीक दो बजकर चौदह मिनट पर जब दिल्ली की हर सड़क और हर घड़ी मानो थम चुकी थी, तब इस सीलबंद सरकारी प्रयोगशाला के अंदर मेरा ईएमएफ मीटर अचानक लाल होकर चीखने लगा। "
            "मेरा नाम आरव है और मैं एक इलेक्ट्रॉनिक्स इंजीनियर हूँ। आज से पहले मैं भूत-प्रेत या किसी परलौकिक साये पर नहीं, बल्कि सिर्फ विज्ञान, तरंगों और आंकड़ों पर यकीन करता था। "
            "लेकिन जब मैंने अपने स्टूडियो हेडफोन में अठारह दशमलव नौ हर्ट्ज़ की वो अनसुनी फ्रीक्वेंसी रिकॉर्ड की, तो मेरी रीढ़ की हड्डी में एक बर्फीली सिहरन दौड़ गई। "
            "अचानक कमरे का तापमान पंद्रह डिग्री से गिरकर शून्य पर आ गया। मेरी सांसें भारी होने लगीं और ठीक मेरी गर्दन के पीछे किसी के धीमे, ठंडे सांस लेने की आवाज गूंजी। "
            "मैंने मुड़कर देखा तो वहां कोई नहीं था, सिर्फ ट्यूबलाइट की नीली रोशनी कांप रही थी। पर विज्ञान एक खौफनाक सच बताता है, अठारह दशमलव नौ हर्ट्ज़ वो खूनी आवृत्ति है जिसे इंसान के कान सुन नहीं सकते। "
            "जब यह फ्रीक्वेंसी हवा में गूंजती है, तो हमारी आंखों की पुतलियां अपने आप कांपने लगती हैं और दिमाग को कमरे के कोने में खड़ी एक लंबी काली परछाईं दिखाई देने लगती है। "
            "मेरा दिल कह रहा था कि यह सिर्फ मेरी आंखों का धोखा है, लेकिन मेरे सामने रखी कांच की बोतल का पानी बिना किसी हवा के हिल रहा था। "
            "क्या सच में सिर्फ मेरी आंखें कांप रही थीं, या इस बंद लैब चार की दीवारों में उन्नीस सौ बयासी से कोई जिंदा कैद था? "
            "मैं अभी अपना सामान समेटकर भागने ही वाला था कि तभी मेरे लैपटॉप की स्क्रीन अपने आप नीली पड़ गई। "
            "बिना इंटरनेट और बिना किसी क्लिक के, स्क्रीन पर एक ऐसी गुप्त फाइल खुली जिसे उन्नीस सौ बयासी में सरकार ने हमेशा के लिए सील कर दिया था। "
            "उस फाइल के पहले ही पन्ने पर बड़े लाल अक्षरों में लिखा था, प्रोजेक्ट अठारह दशमलव नौ, चेतावनी, इसे दोबारा कभी चालू मत करना।"
        ),
        "scenes": [
            f"{ENV_STYLE}, wide eerie shot of an abandoned underground science laboratory corridor at 2 AM with glowing cyan and red emergency lights",
            f"{AARAV_STYLE}, Aarav holding a glowing red EMF meter in shock inside dark misty laboratory",
            f"{ENV_STYLE}, close up of a retro oscilloscope monitor displaying a jagged glowing crimson 18.9 Hz soundwave in dark room",
            f"{AARAV_STYLE}, Aarav freezing in terror as icy frost forms on glass behind him and a tall dark shadow looms in the corner",
            f"{ENV_STYLE}, glowing 3D holographic human eye vibrating with neon purple infrasound waves",
            f"{AARAV_STYLE}, Aarav wearing headphones trembling as ghostly cyan energy wisps swirl around his desk",
            f"{ENV_STYLE}, heavy rusted metallic laboratory door labelled LAB 4 with spinning red alarm light and thick teal fog",
            f"{ENV_STYLE}, glass water bottle on metal table rippling with mysterious concentric shockwaves in neon lighting",
            f"{ENV_STYLE}, laptop screen glowing bright blue in darkness automatically opening a classified 1982 red-stamped file",
            f"{AARAV_STYLE}, dramatic close up of Aarav wide terrified eyes reflecting red warning text on laptop screen"
        ]
    },
    {
        "part": 2,
        "bpm": 68,
        "hud": "REC ● ARCHIVE | 02:29 AM | CO-HIGH",
        "narration": (
            "स्क्रीन पर खुली वो पुरानी गुप्त फाइल किसी अनजान व्यक्ति की नहीं, बल्कि मेरे अपने दादाजी डॉक्टर विश्वनाथ शर्मा की थी। "
            "उन्नीस सौ बयासी में वे इसी सरकारी प्रयोगशाला के प्रमुख वैज्ञानिक थे, और तीन नवंबर की एक काली रात को वे यहीं से रहस्यमय तरीके से गायब हो गए थे। "
            "फाइल के अंदर उनकी आखिरी ऑडियो लॉग और लैब का नक्शा था। मैंने कांपते हाथों से जब अपनी जेब का डिजिटल गैस सेंसर चालू किया, तो उसका अलार्म पागल हो उठा। "
            "इस बंद कमरे की हवा में कार्बन मोनोऑक्साइड का स्तर खतरे के निशान से चार गुना ऊपर था। "
            "आधुनिक विज्ञान कहता है कि जब कोई इंसान बंद जगह पर इस जहरीली गैस को सूंघता है, तो उसके दिमाग में भयानक डर, घुटन और मतिभ्रम पैदा होता है। "
            "इंसान को अपने आसपास मरे हुए लोगों के चेहरे दिखने लगते हैं, और उसे लगता है कि कोई उसका गला दबा रहा है। "
            "एक पल के लिए मैंने खुद को संभाला और सोचा कि शायद यही मेरे डर की असली वजह है। मैंने अपनी टॉर्च जलाई और वेंटिलेशन शाफ्ट की तरफ बढ़ा। "
            "लेकिन तभी छत के ऊपर लगे पुराने लोहे के वेंटिलेशन पाइप से एक ऐसी दर्दनाक चीख निकली जिसने मेरे गैस सेंसर की कांच की सुई को तोड़ दिया। "
            "मैं वहीं जम गया। क्या कार्बन मोनोऑक्साइड किसी मोटे लोहे के दरवाजे को अंदर से पीट सकती है? क्या जहरीली गैस मेरे नाम की आवाज लगा सकती है? नहीं, हरगिज नहीं। "
            "उस बंद वेंट के अंदर से किसी के नाखूनों के रगड़ने की खुरदुरी आवाज आ रही थी, जैसे कोई इंसान अंदर फंसा हो और बाहर निकलने की भीख मांग रहा हो। "
            "मैंने कांपती हुई टॉर्च की तेज रोशनी सीधे उस बंद जाली के अंदर घुमाई, और वहां जो दो चमकती आंखें देखीं, उन्हें देखकर मेरे हाथ से टॉर्च नीचे गिर गई।"
        ),
        "scenes": [
            f"{ENV_STYLE}, glowing vintage 1982 black-and-white scientist photograph floating on a futuristic blue holographic display",
            f"{AARAV_STYLE}, Aarav staring in disbelief at his grandfather photo on monitor in dark room",
            f"{ENV_STYLE}, close up of a handheld digital gas detector flashing bright crimson CO DANGER 400 PPM warning",
            f"{ENV_STYLE}, toxic emerald green and amber mist seeping slowly out from rusty ceiling air vents",
            f"{AARAV_STYLE}, Aarav coughing and hallucinating translucent ghostly figures swirling around him in purple fog",
            f"{ENV_STYLE}, heavy steel ventilation grate shaking violently with bright orange electrical sparks",
            f"{ENV_STYLE}, cracked glass gas meter gauge needle snapping in half under neon red light",
            f"{ENV_STYLE}, two eerie pale glowing eyes peering out from inside a pitch-black metallic air duct",
            f"{AARAV_STYLE}, Aarav dropping his glowing flashlight onto the wet reflective lab floor in pure panic",
            f"{ENV_STYLE}, rolling glowing flashlight on wet concrete floor casting long terrifying shadows down the hallway"
        ]
    },
    {
        "part": 3,
        "bpm": 74,
        "hud": "REC ● STONE-TAPE | 02:45 AM | 480 V",
        "narration": (
            "फर्श पर गिरी टॉर्च लुढ़कती हुई सीधे एक गुप्त लोहे के दरवाजे के सामने रुकी, जिसके नीचे से बेसमेंट की पुरानी सीढ़ियां नीचे उतरती थीं। "
            "पत्थर की उन सीली हुई दीवारों से पानी नहीं, बल्कि गाढ़ा लाल जंग टपक रहा था। मुझे वहीं सीढ़ियों के कोने में चमड़े की एक जली हुई पुरानी डायरी मिली। "
            "जैसे ही मैंने धूल झाड़कर पहला पन्ना खोला, उस पर दादाजी की लिखावट में एक शब्द लिखा था, स्टोन टेप थ्योरी। "
            "पैरासाइकोलॉजी और भौतिक विज्ञान के इस सिद्धांत के मुताबिक, जब किसी जगह पर भयानक दर्द, खौफ या किसी की अकाल मौत घटती है, तो उस घटना की ऊर्जा आसपास के पत्थरों, ईंटों और लोहे में मैग्नेटिक टेप की तरह रिकॉर्ड हो जाती है। "
            "और जब सही नमी या सही फ्रीक्वेंसी मिलती है, तो वे दीवारें उस खौफनाक घटना को दोबारा चलाने लगती हैं। "
            "मैंने अपनी जेब से चुंबकीय ऑडियो रिकॉर्डर निकाला और उसे उन भीगी हुई दीवारों से सटा दिया। "
            "अगले ही सेकंड मेरे छोटे स्पीकर से उन्नीस सौ बयासी की उस मनहूस रात की रिकॉर्डिंग अपने आप बजने लगी। "
            "उस रिकॉर्डिंग में गोलियों और कांच टूटने की आवाजों के बीच कोई जोर से चिल्ला रहा था, विश्वनाथ, मशीन बंद करो, अठारह दशमलव नौ हर्ट्ज़ ने दूसरी तरफ का दरवाजा खोल दिया है। "
            "मेरे रोंगटे खड़े हो गए। यह कोई पुरानी कहानी या भूत नहीं था, यह वक्त के पत्थरों में कैद एक जिंदा चीख थी जो आज फिर से दोहराई जा रही थी। "
            "तभी ऊपर की सीढ़ियों पर किसी के गीले और भारी कदमों की छप-छप आवाज आई, और मेरे ऊपर का भारी लोहे का दरवाजा धड़ाम से बंद होकर लॉक हो गया।"
        ),
        "scenes": [
            f"{ENV_STYLE}, steep dark underground concrete staircase with glowing red rust stains and swirling cyan mist",
            f"{ENV_STYLE}, ancient burned leather diary lying on wet stone steps glowing softly in warm amber flashlight beam",
            f"{AARAV_STYLE}, Aarav kneeling on dark stairs carefully opening the ancient 1982 leather diary",
            f"{ENV_STYLE}, 3D visualization of dark stone basement walls pulsing with glowing blue and crimson magnetic energy waves",
            f"{ENV_STYLE}, retro cassette magnetic recorder pressed against wet concrete wall with glowing neon red LEDs",
            f"{ENV_STYLE}, vibrant neon audio waveforms erupting from a small speaker into the misty dark stairwell",
            f"{ENV_STYLE}, ghostly 1982 hologram silhouette of a terrified scientist shouting near a glowing portal",
            f"{ENV_STYLE}, wet glowing footprints mysteriously appearing one by one on dark concrete stairs",
            f"{ENV_STYLE}, massive heavy iron basement door slamming shut with bright orange sparks and dust explosion",
            f"{AARAV_STYLE}, Aarav trapped in pitch-dark stairwell illuminated only by bright blue phone screen glow"
        ]
    },
    {
        "part": 4,
        "bpm": 80,
        "hud": "REC ● BASEMENT | 03:02 AM | TEMP -4C",
        "narration": (
            "मैं अब जमीन से तीस फीट नीचे एक सील बंद बेसमेंट में कैद था, और मेरे फोन का नेटवर्क पूरी तरह मर चुका था। "
            "ऊपर जाने वाला दरवाजा बाहर से नहीं बल्कि किसी भारी चुंबकीय ताकत से चिपका हुआ था। मैंने अपनी जान बचाने के लिए बैग से अपना थर्मल इमेजिंग कैमरा निकाला। "
            "थर्मल कैमरा तापमान के आधार पर अंधेरे में भी हर जिंदा या मुर्दा चीज को दिखा देता है। मैंने जैसे ही कैमरे की स्क्रीन से अंधेरे हॉल को स्कैन किया, मेरे हाथ कांपने लगे। "
            "नंगी आंखों से देखने पर सामने वाला कोना पूरी तरह खाली था, वहां हवा के सिवा कुछ भी नहीं था। "
            "लेकिन थर्मल कैमरे की स्क्रीन पर ठीक उसी खाली कोने में एक सात फीट ऊंची बर्फीली नीली आकृति खड़ी थी, जिसका तापमान माइनस दस डिग्री सेल्सियस दिखा रहा था। "
            "विज्ञान का पहला नियम कहता है कि हर जिंदा शरीर से गर्मी निकलती है, लेकिन यह चीज कमरे की सारी गर्मी को अपने अंदर सोख रही थी ताकि खुद को जिंदा रख सके। "
            "जैसे ही मैंने डरते हुए एक कदम आगे बढ़ाया, मेरी जेब में रखे थर्मोमीटर का पारा कांच के अंदर ही जम गया और मेरे मुंह से सफेद धुएं की भाप निकलने लगी। "
            "मेरे देखते ही देखते वह सात फीट लंबी नीली आकृति धीरे-धीरे मेरी तरफ घूमी। उसका कोई चेहरा नहीं था, लेकिन उसके सीने के ठीक बीच में एक चमकता हुआ क्वांटम चक्र घूम रहा था। "
            "उसने अपना लंबा बर्फीला हाथ मेरी ओर उठाया, और कमरे की सारी बिजली एक सेकंड में गुल हो गई। "
            "क्या दादाजी ने उन्नीस सौ बयासी में किसी दूसरी दुनिया से ऊर्जा खींचने के लिए इस शैतान को बुलाया था?"
        ),
        "scenes": [
            f"{AARAV_STYLE}, Aarav trapped 30 feet underground staring at dead no-signal smartphone in dark blue shadows",
            f"{ENV_STYLE}, glowing thermal camera viewfinder showing a 7-foot tall icy electric-blue human entity standing in empty corner",
            f"{ENV_STYLE}, vibrant neon heat-map silhouettes shifting from fiery orange to freezing lethal cyan blue",
            f"{ENV_STYLE}, close up of glass thermometer mercury freezing into glowing sharp ice crystals",
            f"{AARAV_STYLE}, Aarav exhaling thick visible glowing white cold breath in freezing dark server basement",
            f"{ENV_STYLE}, towering translucent 7-foot icy-blue phantom turning slowly with a spinning golden quantum vortex in its chest",
            f"{ENV_STYLE}, swirling neon cyan and magenta energy tendrils spreading across wet metallic laboratory floor",
            f"{AARAV_STYLE}, Aarav shielding his eyes from blinding electric blue light radiating from the cold phantom",
            f"{ENV_STYLE}, vintage 1982 copper Tesla coils humming with bright purple lightning arcs in background",
            f"{AARAV_STYLE}, dramatic low-angle shot of Aarav standing bravely against the towering glowing blue phantom"
        ]
    },
    {
        "part": 5,
        "bpm": 86,
        "hud": "REC ● DIARY-82 | 03:18 AM | QUANTUM",
        "narration": (
            "मैं किसी तरह अपनी जान बचाकर भागते हुए एक भारी लोहे की मेज के नीचे छिप गया, और कांपती टॉर्च की रोशनी में दादाजी की डायरी के बाकी जले हुए पन्ने पलटने लगा। "
            "पन्ना नंबर चवालीस पर लाल स्याही से एक ऐसी सच्चाई लिखी थी जिसने मेरे होश उड़ा दिए। "
            "दादाजी ने लिखा था कि इंसान की चेतना और उसकी आत्मा सिर्फ दिमाग के रसायनों का खेल नहीं है, बल्कि यह एक शुद्ध क्वांटम बायो-एनर्जी है। "
            "भौतिक विज्ञान का नियम है कि ऊर्जा न कभी पैदा होती है और न ही कभी नष्ट होती है, शरीर की मौत के बाद भी वह ऊर्जा सिर्फ अपना रूप बदलती है और हमारे ही आसपास घूमती रहती है। "
            "उन्नीस सौ बयासी में दादाजी ने तांबे के कॉइल और क्रिस्टल से एक ऐसी अद्भुत मशीन बनाई थी जो अठारह दशमलव नौ हर्ट्ज़ की ध्वनि तरंगों से उस अदृश्य बायो-एनर्जी को पकड़ सकती थी। "
            "शुरुआत में वे सिर्फ मरे हुए लोगों की आवाजों को रिकॉर्ड करना चाहते थे। लेकिन तीन नवंबर उन्नीस सौ बयासी की रात, जब ऊपर से आदेश आया और उन्होंने मशीन की ताकत सौ गुना बढ़ाई, तो लैब चार की दीवार समय और आयाम के बीच फट गई। "
            "दो दुनियाओं के बीच का दरवाजा खुल गया, और दूसरी तरफ से कोई ऐसी चीज अंदर आ गई जो समय की भूखी थी। "
            "उस रात उस चीज ने दादाजी को मारा नहीं, बल्कि उन्हें अपने ही समय के जाल में जिंदा कैद कर लिया। "
            "मैं अभी यह खौफनाक पन्ना पढ़ ही रहा था कि मेज के ऊपर रखे पुराने कांच के बीकर एक-एक करके बिना किसी के छुए हवा में तैरने लगे और मेरी तरफ मुड़ गए।"
        ),
        "scenes": [
            f"{AARAV_STYLE}, Aarav hiding in fear beneath a heavy steel lab table clutching the glowing leather diary",
            f"{ENV_STYLE}, close up of open handwritten 1982 diary page 44 with glowing golden quantum bio-energy diagrams",
            f"{ENV_STYLE}, vibrant 3D glowing neural energy particles swirling into shape of a human soul above dark desk",
            f"{ENV_STYLE}, retro futuristic 1982 brass frequency generator humming with intense emerald and amber lights",
            f"{ENV_STYLE}, dramatic dimensional tear glowing bright purple and cyan ripping open in the middle of Lab 4 wall",
            f"{ENV_STYLE}, silhouette of an elderly scientist reaching out from inside a swirling golden time vortex",
            f"{ENV_STYLE}, glass laboratory beakers filled with colourful glowing liquids levitating eerily in mid-air",
            f"{ENV_STYLE}, floating sharp glass shards spinning slowly in dramatic crimson and cyan rim lighting",
            f"{AARAV_STYLE}, Aarav looking up in sheer terror from under the table as glowing green beakers point at him",
            f"{ENV_STYLE}, intense macro shot of handwritten 1982 ink letters glowing bright gold in the darkness"
        ]
    },
    {
        "part": 6,
        "bpm": 92,
        "hud": "REC ● LAB-04 | 03:33 AM | DANGER",
        "narration": (
            "हवा में तैरते वे कांच के बीकर किसी अदृश्य ताकत के इशारे पर मेरी ओर गोली की तरह लपके, लेकिन ठीक मेरे चेहरे से दो इंच पहले हवा में ही रुक गए। "
            "मेरी सांसें अटक गईं और पूरा कमरा एक ऐसी भारी गूंज से भर गया जिसमें सैकड़ों फुसफुसाती आवाजें एक साथ मेरे कानों में बोल रही थीं। "
            "मैं अपने दोनों कान कसकर बंद कर लिए, पर आवाजें कम नहीं हुईं। मैंने तुरंत अपना स्पेक्ट्रम एनालाइजर खोला और देखा कि वे आवाजें हवा से नहीं आ रही थीं। "
            "लैब के अंदर की मशीन सीधे मेरे दिमाग के ऑडिटरी कॉर्टेक्स में इलेक्ट्रोमैग्नेटिक तरंगों के जरिए वे फुसफुसाहटें भेज रही थी। "
            "तभी मेरे ठीक सामने लैब चार का वो भारी सीलबंद लोहे का दरवाजा, जिस पर चालीस साल से जंग लगा था, बिना किसी चाबी के अपने आप चरमराते हुए खुलने लगा। "
            "अंदर से नीली और बैंगनी रोशनी की ऐसी तेज किरण बाहर आई कि पूरे बेसमेंट की धूल हवा में जहां की तहां जम गई। "
            "मैंने हिम्मत जुटाकर अंदर कदम रखा। बीच कमरे में तांबे के मोटे तारों से बनी दादाजी की वह विशाल मशीन आज भी बिना किसी बाहरी बिजली के चल रही थी। "
            "उस मशीन के ठीक बीच में एक बड़ा सा कांच का बेलनाकार चैंबर था, जो सुनहरी और नीली धुंध से भरा हुआ था। "
            "और जैसे ही मैं उसके करीब गया, उस धुंधले कांच के अंदर से एक बुजुर्ग इंसान का कांपता हुआ हाथ धीरे-धीरे कांच पर टकराया।"
        ),
        "scenes": [
            f"{AARAV_STYLE}, glowing glass beakers frozen mid-air just two inches from Aarav terrified face",
            f"{ENV_STYLE}, swirling colourful ghostly soundwaves and eerie shadows echoing in a dark laboratory",
            f"{ENV_STYLE}, close up of glowing digital spectrum analyzer showing crazy neon red electromagnetic spikes",
            f"{ENV_STYLE}, massive rusted vault door of LAB 4 creaking open with blinding cyan and purple light beams",
            f"{ENV_STYLE}, golden dust particles frozen mid-air inside vibrant neon purple and blue volumetric light",
            f"{ENV_STYLE}, giant 1982 copper Tesla coil machine humming with bright electric blue plasma arcs",
            f"{ENV_STYLE}, cylindrical glowing glass time-chamber in center of dark lab pulsing with golden quantum energy",
            f"{ENV_STYLE}, close up of an elderly human hand pressing desperately against foggy glowing glass from inside",
            f"{AARAV_STYLE}, Aarav stepping cautiously into glowing Lab 4 bathed in dramatic cyan and amber light",
            f"{ENV_STYLE}, wide cinematic 3D shot of the mysterious glowing quantum laboratory"
        ]
    },
    {
        "part": 7,
        "bpm": 98,
        "hud": "REC ● CLIMAX | 03:45 AM | 18.9 Hz!",
        "narration": (
            "मेरे पैर मानो पत्थर के हो गए थे और मेरी आंखों से आंसू निकल आए, जब मैंने उस कांच के चैंबर के अंदर अपने दादाजी डॉक्टर विश्वनाथ को जिंदा देखा। "
            "उनकी उम्र उन्नीस सौ बयासी से एक दिन भी नहीं बढ़ी थी, वे बिल्कुल वैसे ही दिख रहे थे जैसे पुरानी तस्वीरों में थे, क्योंकि उस चैंबर के अंदर वक्त पूरी तरह थम चुका था। "
            "लेकिन मेरी खुशी एक सेकंड में खौफ में बदल गई, जब मैंने देखा कि उनके ठीक पीछे उस नीली रोशनी में एक और डरावना, विशाल साया हिल रहा है। "
            "उस साये की दोनों आंखें जलते हुए अंगारों की तरह लाल चमक रही थीं और वह सीधे मुझे घूर रहा था। "
            "दादाजी ने कांच पर अपनी उंगली से उल्टा लिखा, आरव, मुख्य केबल काटो, फ्रीक्वेंसी बंद करो, वरना आज रात यह पूरे शहर को निगल लेगा। "
            "उसी पल मेरे हाथ का ईएमएफ मीटर चिंगारियां छोड़कर फट गया और कमरे की सारी लोहे की कुर्सियां किसी विशाल चुंबक की तरह दीवारों से जाकर चिपक गईं। "
            "मेरे पास सोचने के लिए एक सेकंड भी नहीं था। मैंने बिना एक पल गंवाए अपनी जेब से हेवी-ड्यूटी मल्टी-टूल निकाला और उस मुख्य चमकती तांबे की केबल की तरफ दौड़ा। "
            "मेरे दौड़ते ही उस लाल आंखों वाले शैतानी साये ने एक ऐसी कान फाड़ देने वाली चीख मारी कि लैब की सारी ट्यूबलाइटें एक साथ हवा में फट गईं और कांच के टुकड़े चारों तरफ बरसने लगे।"
        ),
        "scenes": [
            f"{AARAV_STYLE}, Aarav crying and shocked seeing his grandfather alive inside glowing glass chamber",
            f"{ENV_STYLE}, elderly grandfather scientist inside glass chamber with a terrifying glowing red-eyed shadow monster looming behind him",
            f"{ENV_STYLE}, foggy glass surface showing backwards handwritten warning words glowing in bright crimson neon",
            f"{ENV_STYLE}, handheld EMF meter exploding in shower of bright orange and yellow electrical sparks",
            f"{ENV_STYLE}, heavy metal laboratory chairs flying and slamming violently onto glowing magnetic walls",
            f"{AARAV_STYLE}, Aarav sprinting forward bravely holding glowing steel pliers toward thick sparking copper cable",
            f"{ENV_STYLE}, terrifying dark phantom monster with blazing crimson eyes roaring with electric purple shockwaves",
            f"{ENV_STYLE}, ceiling neon tube lights shattering simultaneously in slow motion with bright sparks",
            f"{AARAV_STYLE}, Aarav lunging heroically through flying glass shards toward the glowing red power core",
            f"{ENV_STYLE}, intense dramatic chaos with spinning red alarms and blue lightning filling Lab 4"
        ]
    },
    {
        "part": 8,
        "bpm": 105,
        "hud": "REC ● SIGNAL LOST | 04:00 AM",
        "narration": (
            "कांच के गिरते और टूटते टुकड़ों के बीच मैंने अपनी पूरी ताकत लगाकर उस मुख्य तांबे की केबल को बीच से काट दिया। "
            "एक जोरदार सुनहरी चिंगारी उठी, मशीन की कान फाड़ने वाली गूंज थम गई, और एक ही पल में पूरा बेसमेंट गहरे सन्नाटे में डूब गया। "
            "वह लाल आंखों वाला खौफनाक साया धुएं के एक नीले बवंडर में बदलकर हवा में गायब हो गया, और कमरे का जमा देने वाला तापमान फिर से सामान्य हो गया। "
            "जब मैं कांपते कदमों से उस कांच के चैंबर के पास पहुंचा, तो चैंबर पूरी तरह खाली था। दादाजी जा चुके थे, शायद उन्हें आखिरकार समय के उस जाल से आजादी मिल गई थी। "
            "लेकिन चैंबर के ठंडे फर्श पर उन्नीस सौ बयासी की एक सुनहरी पॉकेट घड़ी रखी थी, जिसकी सुई अभी भी टिक-टिक करके चल रही थी। "
            "उस रात मैंने विज्ञान और डर के बीच के उस पर्दे को हटा दिया था। भूत और साये अंधविश्वास नहीं, बल्कि अठारह दशमलव नौ हर्ट्ज़ और क्वांटम ऊर्जा का वो रहस्य हैं जिसे विज्ञान ने अभी ठीक से समझा नहीं है। "
            "मैं सुबह ठीक चार बजे जब उस वीरान लैब से बाहर निकला, तो सूरज की पहली लाल किरण आसमान को रंग रही थी। "
            "मैं सुरक्षित अपने घर लौट आया। लेकिन जब मैंने घर जाकर लैपटॉप पर अपनी वो ऑडियो रिकॉर्डिंग दोबारा सुनी, तो रिकॉर्डिंग के बिल्कुल आखिरी सेकंड में मेरे दादाजी की साफ आवाज गूंजी, आरव, तुमने तार तो काट दिया, पर दरवाजा अभी पूरी तरह बंद नहीं हुआ है। "
            "क्या आप भी रात के सन्नाटे में कभी-कभी अजीब सी गूंज महसूस करते हैं? कमेंट में जरूर लिखें, क्योंकि अगली जांच अब आपके शहर में हो सकती है।"
        ),
        "scenes": [
            f"{AARAV_STYLE}, Aarav slicing thick glowing copper cable with bright golden spark explosion",
            f"{ENV_STYLE}, terrifying crimson-eyed shadow dissolving into a swirling cyan smoke vortex",
            f"{ENV_STYLE}, quiet peaceful Lab 4 bathed in soft morning blue light and fading mist",
            f"{AARAV_STYLE}, Aarav kneeling beside empty glass chamber picking up a glowing golden 1982 pocket watch",
            f"{ENV_STYLE}, macro close up of antique golden pocket watch ticking inside warm glowing dust beams",
            f"{AARAV_STYLE}, Aarav walking out of the dark facility into a colourful fiery orange sunrise sky",
            f"{AARAV_STYLE}, Aarav back in his modern colourful home studio putting on studio headphones",
            f"{ENV_STYLE}, close up of laptop audio waveform spiking suddenly in bright blood red at the very last second",
            f"{AARAV_STYLE}, Aarav eyes widening in sudden horror as a faint glowing shadow reflects in his laptop monitor",
            f"{ENV_STYLE}, cinematic mysterious glowing title aura with 18.9 Hz neon soundwave in dark mist"
        ]
    }
]

# ---------------- IMAGE GENERATOR (CF + POLLINATIONS + HUD) ----------------
def is_valid_bright_image(path):
    if not os.path.exists(path) or os.path.getsize(path) < 18000:
        return False
    try:
        with Image.open(path) as im:
            arr = np.asarray(im.convert("RGB"), dtype=np.float32)
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

    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "color=c=#0f283c:s=1280x720:d=1,geq=r='15+45*sin(X/120)':g='30+50*cos(Y/90)':b='75+80*sin((X+Y)/150)'",
        "-frames:v", "1", out_path
    ], check=True)
    add_cctv_hud(out_path, hud_text)
    return out_path

# ---------------- CINEMATIC HORROR SCORE ENGINE (NO BUZZ!) ----------------
def generate_horror_bg_wav(wav_path, duration_sec, bpm=75):
    sr = 22050
    n_samples = int(sr * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False, dtype=np.float32)

    # 1. Deep smooth sub-bass pulse (warm 48 Hz + gentle LFO, no harsh buzz)
    sub_lfo = 0.55 + 0.45 * np.sin(2 * np.pi * 0.12 * t)
    sub_bass = 0.24 * sub_lfo * np.sin(2 * np.pi * 48.0 * t)

    # 2. Lub-Dub Heartbeat (clean low thump)
    beat_period = 60.0 / bpm
    phase = np.mod(t, beat_period)
    lub = np.exp(-((phase - 0.06) ** 2) / (2 * 0.024 ** 2)) * np.sin(2 * np.pi * 55.0 * t)
    dub = np.exp(-((phase - 0.23) ** 2) / (2 * 0.030 ** 2)) * np.sin(2 * np.pi * 46.0 * t)
    heartbeat = 0.65 * (lub + 0.78 * dub)

    # 3. Haunting Minor-Key Horror Piano / Bell Chimes every ~6 seconds
    chimes = np.zeros(n_samples, dtype=np.float32)
    horror_freqs = [293.66, 311.13, 277.18, 440.0, 261.63, 392.0]  # D4, Eb4, C#4, A4, C4, G4
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

    # 4. Sudden scary tension riser before part ending (last 5 seconds)
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
            comm = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural", rate="-7%", pitch="-5Hz")
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
    part_dur = max(MIN_PART_SECONDS, voice_dur + 4.0)

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
        f"apad=whole_dur={part_dur:.2f},aecho=0.8:0.7:45:0.15,volume=1.40,asplit=2[voice1][voice2]"
    )
    filters.append(
        f"[{bg_idx}:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,volume=0.90[bg]"
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
            part_files.append(out_mp4)
            continue

        print(f"[Part {p}] Generating 10 diverse 3D horror scenes...")
        imgs = []
        for s_idx, prompt in enumerate(data["scenes"]):
            img_p = os.path.join(IMG_DIR, f"p{p:02d}_s{s_idx:02d}.png")
            generate_3d_image(prompt, img_p, data["hud"], seed=p * 100 + s_idx)
            imgs.append(img_p)

        print(f"[Part {p}] Generating full ~185s Hindi voiceover & Devanagari captions...")
        await make_voice_and_subs(data["narration"], raw_mp3, ass_path)

        print(f"[Part {p}] Rendering horror video...")
        render_part(data, imgs, raw_mp3, ass_path, out_mp4)
        part_files.append(out_mp4)
        await asyncio.sleep(3)

    concat_txt = "/tmp/all_parts_v4.txt"
    with open(concat_txt, "w") as f:
        for pf in part_files:
            f.write(f"file '{os.path.abspath(pf)}'\n")

    final_mp4 = os.path.join(OUT_DIR, "FINAL_3D_HORROR_V4_25MIN_2026-11-13.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", final_mp4
    ], check=True)
    print(f"SUCCESS! Final 25+ min V4 Horror Video ready: {final_mp4}")

if __name__ == "__main__":
    asyncio.run(main())
