import os
import gc
import base64
import asyncio
import subprocess
import requests
import edge_tts
from mutagen.mp3 import MP3

BASE_DIR = "2026-11-13_Project_18_9Hz_3D_V2"
os.makedirs(f"{BASE_DIR}/audio", exist_ok=True)
os.makedirs(f"{BASE_DIR}/images", exist_ok=True)
os.makedirs(f"{BASE_DIR}/subs", exist_ok=True)
os.makedirs(f"{BASE_DIR}/parts", exist_ok=True)

CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "").strip()
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "").strip()
MIN_PART_SECONDS = 190.0  # 8 x 190s = 25 मिनट 20 सेकंड गारंटीड

STYLE_3D = "3D Pixar style animation, cute expressive Indian young man character, spooky dark atmospheric lighting, soft volumetric fog, rich cinematic colors, Unreal Engine 5 render, 16:9, no text"

STORY_PARTS = {
    1: {
        "pace": "smooth",
        "narration": """क्या आपने कभी महसूस किया है... जब किसी खाली कमरे में अचानक आपकी रीढ़ की हड्डी में बर्फ़ जैसी ठंडक दौड़ती है, तो वो डर होता है... या कोई अनकही फिज़िक्स? मेरा नाम आरव है। तीन दिन पहले तक मेरे लिए भूत, आत्मा, ये सब सिर्फ़ कमज़ोर दिमाग का एक केमिकल लोचा था। लेकिन फिर... मैंने पाँच लाख की वो शर्त लगा ली। रात के ठीक बारह बजे, जब मुंबई की एक सौ बीस साल पुरानी बंद पड़ी कॉटन मिल के भारी लोहे के गेट पर बाहर से ताला जड़ा गया, तो मेरे हाथ में कोई ताबीज़ नहीं था। मेरे पास था एक थर्मल कैमरा, एक ईएमएफ मीटर, और अठारह हर्ट्ज़ पकड़ने वाला माइक। पहले दस मिनट बिल्कुल सन्नाटा रहा... इतना गहरा सन्नाटा कि मुझे अपनी ही साँसें भारी लगने लगीं। लेकिन बारह बजकर चौदह मिनट पर... मुझे अचानक ताज़ा भुनी हुई कॉफी की खुशबू आई। एक ऐसी जगह पर, जहाँ चालीस साल से बिजली का एक तार भी नहीं जुड़ा था। मैंने हँसकर कैमरा घुमाया—और तभी स्क्रीन पर वो दिखा, जिसने मेरा गला सुखा दिया। पूरे कमरे का तापमान अट्ठाईस डिग्री था, सिवाय एक कोने के... जहाँ तापमान चार डिग्री सेल्सियस दिखा रहा था, बिल्कुल एक इंसान के आकार में। मैंने तुरंत अपना साउंड एनालाइज़र ऑन किया। स्क्रीन पर अठारह दशमलव नौ हर्ट्ज़ की एक सीधी लाल लाइन चमक रही थी। साइंस कहता है कि अठारह दशमलव नौ हर्ट्ज़ की इन्फ्रासाउंड तरंगें इंसान की आँखों के पर्दे में कंपन पैदा करती हैं, जिससे दिमाग को सामने भूत दिखने का भ्रम होता है। मैं राहत से मुस्कुराया—चलो, विज्ञान जीत गया। मैंने कैमरे में धीरे से कहा कि यहाँ कोई भूत नहीं, सिर्फ़ साउंड वेव्स हैं। लेकिन तभी... मेरी पीठ के ठीक दो इंच पीछे से किसी ने मेरे कान में धीमे से फुसफुसाया। मेरी धड़कनें जैसे थम गईं। मैंने काँपते हाथों से अपने साउंड मीटर की तरफ़ देखा... और उस वक्त मेरा अठारह दशमलव नौ हर्ट्ज़ डिटेक्टर बिल्कुल शांत था।""",
        "prompts": [
            f"{STYLE_3D}, wide shot of eerie abandoned cotton mill in Mumbai at midnight, glowing moonlight, mist",
            f"{STYLE_3D}, close up of cute young Indian engineer Aarav with glasses holding thermal camera inside dark mill",
            f"{STYLE_3D}, POV of thermal camera screen showing glowing blue 4 degree human silhouette in dark corner",
            f"{STYLE_3D}, glowing red 18.9 Hz waveform spike on handheld analyzer in dark room",
            f"{STYLE_3D}, Aarav looking back terrified over shoulder, subtle ghostly mist behind his ear"
        ]
    },
    2: {
        "pace": "smooth",
        "narration": """आरव बिजली की रफ़्तार से पीछे पलटा, लेकिन टॉर्च की रोशनी में सिर्फ़ धूल के उड़ते कण थे... वहाँ कोई नहीं था। उसका दिल ज़ोर-ज़ोर से धड़क रहा था, पर उसने खुद को संभाला—क्योंकि कमज़ोर पड़ने का मतलब था अपने ही विश्वास से हार जाना। तभी उसकी नज़र छत के जंग लगे लोहे के पाइपों पर पड़ी, जहाँ से रात की तेज़ हवा टकराकर एक अजीब सीटी जैसी आवाज़ बना रही थी। आरव को लगा उसे जवाब मिल गया। उसने तुरंत अपना जैकेट उतारा और एक टूटे पाइप के मुँह पर कसकर बाँध दिया। लेकिन तीस सेकंड भी नहीं बीते थे कि मीटर की सुई फिर से लाल निशान पर पहुँच गई। आवाज़ बंद नहीं हुई थी, बल्कि और गहरी हो गई थी। आरव ने माइक को धूल भरी ज़मीन से सटाया। स्पेक्ट्रम एनालाइज़र ने जो दिखाया वह नामुमकिन था—यह आवाज़ छत की हवा से नहीं, बल्कि उसके पैरों के दस फीट नीचे ज़मीन के अंदर से आ रही थी। तभी उसके जूते के नीचे कोई सख्त चीज़ टकराई। उसने झुककर धूल हटाई—तो वहाँ उन्नीस सौ बयासी का एक आधा जला हुआ मिल का रजिस्टर पड़ा था। आरव ने काँपते हाथों से पन्ना पलटा... और उसकी आँखें नम होने से पहले ही जम गईं। उस रजिस्टर के आखिरी पन्ने पर ठीक आज ही की तारीख—तेरह नवंबर—दर्ज थी, और लाल स्याही से लिखा था: नाइट शिफ्ट हमेशा के लिए बंद। तभी उसकी जेब में रखा फोन वाइब्रेट हुआ, जो बाहर दोस्तों को लाइव स्ट्रीम कर रहा था। आरव ने फोन निकाला—स्क्रीन पूरी काली पड़ चुकी थी। और अगले ही सेकंड, बंद फोन के काँच के अंदर से... किसी की धुंधली, छोटी उंगलियों के निशान धीरे-धीरे स्क्रीन पर उभरने लगे।""",
        "prompts": [
            f"{STYLE_3D}, Aarav shining bright flashlight into dusty empty dark factory hall, floating dust",
            f"{STYLE_3D}, Aarav tying his jacket around rusty ceiling metal pipe to block wind",
            f"{STYLE_3D}, Aarav kneeling and pressing digital microphone onto cracked concrete floor",
            f"{STYLE_3D}, half burnt vintage 1982 paper register on dusty floor under warm flashlight",
            f"{STYLE_3D}, close up of black smartphone screen with faint glowing ghostly fingerprints inside glass"
        ]
    },
    3: {
        "pace": "smooth",
        "narration": """फोन हाथ से छूटते-छूटते बचा। आरव ने अपनी काँपती साँसें अंदर रोकीं और दीवार के सहारे बैठ गया। उसकी आँखों के कोनों में हल्की नमी थी, पर उसने उसे पोंछा नहीं—बस खुद से फुसफुसाया, हर चीज़ का एक कारण होता है, आरव... रुकना मत। उसने अपनी टॉर्च मिल की पुरानी लाल ईंटों वाली दीवार पर मारी—ईंटों में छोटे-छोटे चमकते हुए कण दिख रहे थे। अचानक उसके दिमाग में स्टोन टेप थ्योरी कौंधी। विज्ञान कहता है कि जिन दीवारों में आयरन ऑक्साइड और क्वार्ट्ज़ क्रिस्टल ज़्यादा होते हैं, वे किसी पुराने कैसेट टेप की तरह तेज़ इमोशनल और इलेक्ट्रोमैग्नेटिक ऊर्जा को रिकॉर्ड कर सकती हैं। आरव ने सोचा—क्या यह पूरी मिल एक विशाल हार्ड ड्राइव बन चुकी है? उसने अपने बैग से एक छोटा कॉपर ट्रांसड्यूसर और नौ वोल्ट की बैटरी निकाली, और सीधे दीवार की ईंटों पर हल्का करंट छोड़ा। बीस सेकंड तक सिर्फ़ चर्र-चर्र की आवाज़ आई... और फिर अचानक उसके पोर्टेबल स्पीकर से ऐसी आवाज़ फूटी कि कमरे की हवा भारी हो गई। स्पीकर से उन्नीस सौ बयासी की मशीनों का शोर, लोहे के टकराने की गूँज और दर्जनों लोगों के रोने-चीखने की आवाज़ें साफ़ सुनाई दे रही थीं। आरव की आँखें चमक उठीं—उसने भूत को साइंस से डीकोड कर लिया था! यह कोई आत्मा नहीं, बल्कि दीवारों में फंसी एक पुरानी इलेक्ट्रोमैग्नेटिक रिकॉर्डिंग थी। वह मुस्कुराने ही वाला था कि तभी स्पीकर से मशीनों का शोर अचानक कट गया... बिल्कुल गहरा सन्नाटा। और फिर, उस चालीस साल पुरानी रिकॉर्डिंग के बीच से एक भारी, जानी-पहचानी काँपती आवाज़ ने साफ़ हिंदी में कहा—आरव... बेटा, बाहर मत जाओ।""",
        "prompts": [
            f"{STYLE_3D}, Aarav sitting against damp red brick wall looking determined with suppressed emotion",
            f"{STYLE_3D}, close up of sparkling quartz crystals inside old red bricks under flashlight",
            f"{STYLE_3D}, cute DIY copper wire and 9V battery sensor connected to brick wall",
            f"{STYLE_3D}, vintage portable speaker glowing green in dark room with sound ripple effect",
            f"{STYLE_3D}, Aarav frozen in shock staring at speaker, deep shadows in long dark corridor"
        ]
    },
    4: {
        "pace": "fast",
        "narration": """आरव... बेटा, बाहर मत जाओ। वो आवाज़... किसी अनजान की नहीं थी। उसका गला भर आया, क्योंकि उस आवाज़ का लहज़ा बिल्कुल वैसा था जैसे सालों पहले घर में कोई उसे पुकारता था। तभी अचानक आरव का सिर तेज़ी से घूमने लगा। सामने की दीवार से एक लंबा, काला साया धीरे-धीरे बाहर निकलता दिखा। आरव के हाथ-पैर सुन्न पड़ने लगे—तभी उसकी बेल्ट पर लगा छोटा-सा पीला डिवाइस ज़ोर-ज़ोर से बीप करने लगा! यह उसका कार्बन मोनोऑक्साइड डिटेक्टर था। कमरे में ज़हरीली गैस खतरनाक लेवल पार कर चुकी थी। आरव को तुरंत समझ आया कि वह साया और वो आवाज़ दरअसल ज़हरीली गैस के कारण होने वाला दिमागी भ्रम है। उसने अपनी पूरी ताकत बटोरी, एक भारी लोहे की रॉड उठाई और सामने की पुरानी काँच की खिड़की तोड़ दी! ठंडी, ताज़ा हवा का झोंका अंदर आया। जैसे-जैसे ऑक्सीजन उसके फेफड़ों में गई, उसका सिर हल्का हुआ... और दीवार के पास खड़ा वह काला साया हवा में गायब हो गया। आरव ज़ोर से हँस पड़ा, पर उसकी हँसी में एक अजीब-सी थकान थी। उसने कैमरे की तरफ़ देखकर कहा—देखा? हर डर के पीछे कोई न कोई गैस या केमिकल होता है। अपनी बात पक्की करने के लिए उसने कोने में लगे बैकअप वाइड-एंगल कैमरे की फुटेज रिवाइंड करके देखी। और जैसे ही स्क्रीन पर दस सेकंड पहले का वीडियो चला... आरव के चेहरे से सारी रंगत उड़ गई। वीडियो में कोई गैस नहीं थी—उस काले साये ने सचमुच आगे बढ़कर कमरे के बीच रखी एक भारी लोहे की कुर्सी को घसीटकर दरवाज़े के सामने लगा दिया था। ज़हरीली गैस दिमाग को धोखा दे सकती है... पर लोहे की कुर्सी नहीं हिला सकती।""",
        "prompts": [
            f"{STYLE_3D}, dizzy Aarav holding his forehead as tall shadowy figure emerges from brick wall",
            f"{STYLE_3D}, close up of yellow carbon monoxide detector flashing bright red warning light",
            f"{STYLE_3D}, dramatic action shot of Aarav smashing dusty factory window with iron rod, moonlight rushing in",
            f"{STYLE_3D}, heavy rusty iron chair blocking wooden doorway in eerie dark room",
            f"{STYLE_3D}, Aarav staring in sheer disbelief at laptop playback screen showing shadow moving chair"
        ]
    },
    5: {
        "pace": "smooth",
        "narration": """अब आरव के पास कोई बहाना नहीं बचा था। न कोई गैस, न कोई साउंड वेव—कुछ तो सचमुच इस इमारत में मौजूद था, और उसका रास्ता ज़मीन के नीचे जाता था। उसने भारी मन से दरवाज़े के सामने से वह लोहे की कुर्सी हटाई और बेसमेंट की टूटी हुई सीढ़ियों से नीचे उतरने लगा। हर कदम के साथ हवा और ज़्यादा ठंडी होती जा रही थी। जैसे ही वह बेसमेंट में पहुँचा, उसे एक धीमी गूँज सुनाई दी—जैसे कोई पुरानी धड़कन या भारी मशीन चल रही हो। कोने में उन्नीस सौ अस्सी के दशक का एक विशाल डीज़ल जनरेटर रखा था, जिसके सारे तार कटे हुए थे और टैंक सूखा था। लेकिन जब आरव ने थर्मल कैमरा उसकी तरफ़ घुमाया, तो जनरेटर का इंजन नब्बे डिग्री सेल्सियस पर लाल दहक रहा था—बिना किसी ईंधन के वह अपने आप गर्म हो रहा था। आरव का ईएमएफ मीटर पागल हो गया—रीडिंग सौ मिलीगॉस के पार चली गई, इतनी तेज़ इलेक्ट्रोमैग्नेटिक फील्ड कि आरव के हाथों के सारे रोंगटे अपने आप खड़े हो गए। वह उस ऊर्जा का पीछा करते हुए बेसमेंट के सबसे आखिरी कोने में पहुँचा। वहाँ एक भारी स्टील का दरवाज़ा था, जिस पर जंग लगे अक्षरों में लिखा था—लैब चार। यह कोई कॉटन मिल नहीं थी। अंदर कदम रखते ही आरव की साँस रुक गई। पूरे कमरे में तांबे के विशाल कॉइल्स, पुराने ऑसिलोस्कोप और काँच के टूटे चैंबर लगे थे। कमरे के बीचों-बीच एक लोहे की मेज़ थी। आरव ने मेज़ पर टॉर्च मारी... तो उसकी आँखों से एक आँसू टपकने से पहले ही थम गया। उस धूल भरी मेज़ पर एक पुरानी रंगीन तस्वीर पड़ी थी—वह आरव के खुद के बचपन की तस्वीर थी, जो कल रात तक उसके घर की अलमारी में रखी थी।""",
        "prompts": [
            f"{STYLE_3D}, Aarav walking down broken dark concrete basement stairs with warm flashlight beam",
            f"{STYLE_3D}, thermal view of old diesel generator glowing fiery red at 90 degrees with cut wires",
            f"{STYLE_3D}, glowing red EMF meter maxed out in dark underground corridor",
            f"{STYLE_3D}, heavy rusted steel door with faded label LAB 4 in foggy dark basement",
            f"{STYLE_3D}, vintage childhood photo on dusty metal table inside secret 1980s copper coil lab"
        ]
    },
    6: {
        "pace": "fast",
        "narration": """वह तस्वीर यहाँ कैसे आई? आरव के हाथ काँप रहे थे। उसने काँपते हाथों से तस्वीर के नीचे दबी चमड़े की एक पुरानी डायरी निकाली। पहले पन्ने पर जो नाम लिखा था, उसे पढ़कर उसके पैरों तले ज़मीन खिसक गई—डॉक्टर विश्वनाथ शर्मा, चीफ साइंटिस्ट, उन्नीस सौ बयासी। वह आरव के खुद के दादाजी थे... जिनके बारे में परिवार ने सिर्फ़ इतना बताया था कि वे एक मिल में काम करते थे और एक हादसे में लापता हो गए। आरव ने तेज़ी से पन्ने पलटे, उसकी पलकें भीग चुकी थीं पर उसने खुद को रोने नहीं दिया। डायरी में लिखा था कि यह मिल दरअसल एक गुप्त बायो-इलेक्ट्रोमैग्नेटिक प्रोजेक्ट का अड्डा थी। वैज्ञानिक यह साबित कर रहे थे कि मौत के बाद इंसान की चेतना नष्ट नहीं होती, बल्कि क्वार्ट्ज़ और हाई-वोल्टेज मैग्नेटिक फील्ड में कैद की जा सकती है। आखिरी पन्ने पर काँपते अक्षरों में लिखा था—तेरह नवंबर उन्नीस सौ बयासी: एक्सपेरिमेंट सफल रहा, लेकिन एनर्जी कंटेनमेंट टूट गया। मैं बाहर नहीं निकल पाऊँगा... अगर कोई अपना यहाँ आए, तो कहना मैं यहीं हूँ। तभी... धड़ाम! लैब चार का भारी स्टील का दरवाज़ा अपने आप बंद होकर लॉक हो गया! कमरे का तापमान एक झटके में माइनस दो डिग्री पर गिर गया—आरव के मुँह से भाप निकलने लगी। कोने के टूटे चैंबर के पास नीली बिजली की चिंगारियाँ चमकीं। वह काला साया आकार लेने लगा—यह कोई भूत नहीं, बल्कि क्वांटम फील्ड में फँसी एक भूखी ऊर्जा थी। आरव ने मदद के लिए अपनी स्मार्टवॉच की तरफ़ देखा... उसकी बैटरी सौ प्रतिशत से एक सेकंड में सीधे एक प्रतिशत पर गिर चुकी थी।""",
        "prompts": [
            f"{STYLE_3D}, emotional Aarav holding dusty old leather diary with tears held back in his eyes",
            f"{STYLE_3D}, close up of handwritten 1982 science journal with magnetic coil diagrams",
            f"{STYLE_3D}, heavy steel door slamming shut in dark lab, frost mist in the air",
            f"{STYLE_3D}, spooky cute-yet-chilling glowing blue static silhouette forming inside broken glass chamber",
            f"{STYLE_3D}, smartwatch on wrist dropping to 1 percent red battery warning in freezing dark room"
        ]
    },
    7: {
        "pace": "fast",
        "narration": """वह काला साया अब तेज़ी से आरव की तरफ़ बढ़ रहा था—कमरे की सारी बची-खुची गर्मी उसकी तरफ़ खिंच रही थी। भागने का कोई रास्ता नहीं था। पर इसी डर के बीच आरव के अंदर का इंजीनियर और दादाजी का पोता दोनों जाग उठे। अगर यह एंटिटी शुद्ध इलेक्ट्रोमैग्नेटिक फील्ड से बनी है, तो जैसे किसी हार्ड ड्राइव का डेटा एक तेज़ मैग्नेटिक पल्स से मिट जाता है—वैसे ही एक रिवर्स-फेज़ ईएमपी शॉक इसके फील्ड को आज़ाद कर सकता है! उसके पास सिर्फ़ बीस सेकंड थे। उसने तुरंत अपने कैमरे का हाई-वोल्टेज फ्लैश कैपेसिटर तोड़ा, लैब की मेज़ पर पड़ा तांबे का तार लपेटा, और अपने पावर बैंक की लिथियम सेल से शॉर्ट-सर्किट कर दिया। ठीक उसी पल, बर्फ़ जैसा ठंडा एक अदृश्य हाथ आरव के गले पर कस गया। उसका दम घुटने लगा, आँखों के आगे अँधेरा छाने लगा। साया उसके बिल्कुल चेहरे के सामने था—और एक पल के लिए, उस काली ऊर्जा के भीतर आरव को अपने दादाजी की धुंधली, उदास आँखें दिखीं। आरव की आवाज़ गले में अटक गई, उसने धीरे से कहा—माफ़ करना दादाजी। आखिरी सेकंड में, गिरते हुए उसने दोनों खुले तार जोड़ दिए! एक तेज़ नीली इलेक्ट्रिक चमक और कान फाड़ देने वाली शॉकवेव पूरे कमरे में फूट पड़ी। काँच के सारे चैंबर चकनाचूर हो गए और वह साया सुनहरी-नीली चिंगारियों में बदलकर हवा में बिखर गया। आरव हाँफते हुए ज़मीन पर गिर पड़ा। उसने साइंस से एक भूत को आज़ाद कर दिया था। लेकिन तभी... चालीस साल से बंद पड़ी इस पूरी मिल की छत की सारी ट्यूबलाइट्स एक साथ तेज़ आवाज़ के साथ जल उठीं।""",
        "prompts": [
            f"{STYLE_3D}, Aarav urgently connecting camera flash capacitor with copper coil and power bank, sparks",
            f"{STYLE_3D}, dramatic close up of Aarav struggling to breathe as glowing blue shadow approaches, emotional",
            f"{STYLE_3D}, massive bright blue electromagnetic pulse shockwave exploding in dark laboratory",
            f"{STYLE_3D}, Aarav lying exhausted on dusty lab floor amidst glowing blue dust and shattered glass",
            f"{STYLE_3D}, abandoned mill hallway suddenly lighting up with bright flickering fluorescent lights"
        ]
    },
    8: {
        "pace": "smooth",
        "narration": """जैसे ही लाइटें जलीं, लैब चार का इलेक्ट्रॉनिक लॉक अपने आप खुल गया। आरव अपनी टूटी मशीनें और बैकअप एसडी कार्ड समेटकर बाहर भागा और सुबह होने का इंतज़ार किया। अगले दो दिनों तक उसने अपने कमरे में बंद होकर वह सारा डेटा लैपटॉप पर एनालाइज़ किया—थर्मल कैमरे की चार-डिग्री वाली फुटेज, अठारह दशमलव नौ हर्ट्ज़ की वेव्स, सौ मिलीगॉस का ईएमएफ स्पाइक, और स्पीकर की वो आवाज़। हर एक फाइल सौ प्रतिशत असली थी, कोई एडिटिंग नहीं, कोई ट्रिक नहीं। आरव ने वह पाँच लाख की शर्त तो जीत ही ली, साथ ही उसने विज्ञान और पैरानॉर्मल की दुनिया को हिला देने वाला पहला ठोस सबूत दुनिया के सामने रख दिया—कि भूत कोई अंधविश्वास नहीं, बल्कि अनदेखी फिज़िक्स, क्वांटम मेमोरी और फंसी हुई बायो-इलेक्ट्रिक एनर्जी है। कहानी खत्म हो चुकी थी, पर आरव के दिल में दादाजी की अधूरी बात अभी भी गूँज रही थी। तीन दिन बाद वह पहली बार चैन की नींद सोने के लिए बिस्तर पर लेटा। बाहर मुंबई की रात शांत थी। ठीक तीन बजकर एक मिनट पर... आरव की नींद अचानक एक तेज़ ठंड से खुली। उसने आँखें खोलीं—उसके बेडरूम के कोने में लगा डिजिटल थर्मोस्टेट लाल चमक रहा था, और कमरे का तापमान चार डिग्री सेल्सियस दिखा रहा था। उसकी टेबल पर रखे बंद लैपटॉप की स्क्रीन अपने आप ऑन हुई... और माइक पर वही अठारह दशमलव नौ हर्ट्ज़ की सीधी लाल लाइन फिर से बननी शुरू हो गई। वह ऊर्जा मिल में खत्म नहीं हुई थी... जब आरव ने अपनी बैटरी से कॉइल जोड़ा था, वह ऊर्जा उसके बैकअप डेटा के साथ उसके घर आ चुकी थी।""",
        "prompts": [
            f"{STYLE_3D}, golden sunrise over abandoned cotton mill, Aarav walking out exhausted holding camera bag",
            f"{STYLE_3D}, Aarav sitting in cozy dark Mumbai apartment analyzing glowing waveforms on laptop",
            f"{STYLE_3D}, peaceful dark bedroom at night, Aarav sleeping under soft city light outside window",
            f"{STYLE_3D}, digital wall clock and thermostat glowing red showing 3:01 AM and 4 degrees celsius",
            f"{STYLE_3D}, laptop turning on by itself in dark room showing glowing red 18.9 Hz wave spike, chilling ending"
        ]
    }
}

def generate_cf_image(prompt, out_path):
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        return False
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}"}
    try:
        r = requests.post(url, headers=headers, json={"prompt": prompt, "num_steps": 4}, timeout=45)
        if r.status_code != 200:
            print(f"[CF Error {r.status_code}] {r.text[:120]}")
            return False
        ctype = r.headers.get("Content-Type", "")
        if "application/json" in ctype:
            img_b64 = r.json().get("result", {}).get("image")
            if not img_b64:
                return False
            img_bytes = base64.b64decode(img_b64)
        else:
            img_bytes = r.content
        if len(img_bytes) < 5000:
            return False
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        return True
    except Exception as e:
        print(f"[CF Exception] {e}")
        return False

def fmt_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int((sec - int(sec)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def build_left_ass(sentences, ass_path):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: LeftHindi,Noto Sans Devanagari,36,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,3,2,1,55,420,48,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for st, en, txt in sentences:
        clean = txt.replace("\n", " ").strip()
        if clean:
            lines.append(f"Dialogue: 0,{fmt_ass_time(st)},{fmt_ass_time(en)},LeftHindi,,0,0,0,,{clean}")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")

async def make_voice_and_subs(text, mp3_path, ass_path):
    for attempt in range(1, 6):
        try:
            comm = edge_tts.Communicate(text=text.strip(), voice="hi-IN-MadhurNeural", rate="-8%", pitch="-4Hz")
            submaker = edge_tts.SubMaker()
            audio_chunks = []
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio_chunks.append(chunk["data"])
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    submaker.feed(chunk)
            if not audio_chunks:
                raise RuntimeError("Empty audio chunks")
            with open(mp3_path, "wb") as f:
                for c in audio_chunks:
                    f.write(c)

            srt_text = submaker.get_srt()
            sentence_events = []
            blocks = [b.strip() for b in srt_text.strip().split("\n\n") if b.strip()]
            for b in blocks:
                parts = b.splitlines()
                if len(parts) >= 3 and "-->" in parts[1]:
                    t1, t2 = [p.strip().replace(",", ".") for p in parts[1].split("-->")]
                    def to_sec(ts):
                        hh, mm, ss = ts.split(":")
                        return int(hh) * 3600 + int(mm) * 60 + float(ss)
                    sentence_events.append((to_sec(t1), to_sec(t2), " ".join(parts[2:])))
            build_left_ass(sentence_events, ass_path)
            return
        except Exception as e:
            print(f"[TTS Retry {attempt}/5] {e}")
            await asyncio.sleep(4)
    raise RuntimeError("TTS failed after 5 attempts")

async def main():
    part_videos = []
    for part_id, data in STORY_PARTS.items():
        final_part = f"{BASE_DIR}/parts/part_{part_id:02d}.mp4"
        if os.path.exists(final_part):
            part_videos.append(final_part)
            continue

        raw_mp3 = f"{BASE_DIR}/audio/part_{part_id:02d}.mp3"
        ass_path = f"{BASE_DIR}/subs/part_{part_id:02d}.ass"
        if not os.path.exists(raw_mp3) or not os.path.exists(ass_path):
            await make_voice_and_subs(data["narration"], raw_mp3, ass_path)
            await asyncio.sleep(3)

        voice_dur = MP3(raw_mp3).info.length
        target_dur = max(voice_dur + 3.0, MIN_PART_SECONDS)
        print(f"[Part {part_id}/8] Voice={voice_dur:.1f}s -> Target={target_dur:.1f}s")

        padded_wav = f"/tmp/voice_pad_{part_id}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_mp3,
            "-af", f"apad=whole_dur={target_dur:.2f}",
            padded_wav
        ], check=True)

        prompts = data["prompts"]
        clip_dur = target_dur / len(prompts)
        frames = int(clip_dur * 24) + 12
        clip_list = f"/tmp/clips_{part_id}.txt"

        with open(clip_list, "w") as f:
            for idx, prompt in enumerate(prompts):
                img_path = f"{BASE_DIR}/images/p{part_id}_i{idx}.png"
                clip_out = f"/tmp/p{part_id}_c{idx}.mp4"

                if not os.path.exists(img_path):
                    ok = generate_cf_image(prompt, img_path)
                    if not ok:
                        subprocess.run([
                            "ffmpeg", "-y", "-f", "lavfi",
                            "-i", "color=c=#080c14:s=1280x720:d=1",
                            "-frames:v", "1", img_path
                        ], check=True)

                if idx % 2 == 0:
                    zp = f"zoompan=z='min(zoom+0.0008,1.15)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24"
                else:
                    zp = f"zoompan=z='if(eq(on,1),1.15,max(zoom-0.0008,1.0))':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=24"

                subprocess.run([
                    "ffmpeg", "-y", "-loop", "1", "-i", img_path,
                    "-vf", f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,{zp},vignette=PI/4",
                    "-t", f"{clip_dur:.2f}", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", clip_out
                ], check=True)
                f.write(f"file '{os.path.abspath(clip_out)}'\n")

        raw_vid = f"/tmp/raw_part_{part_id}.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clip_list, "-c", "copy", raw_vid], check=True)

        drone_wav = f"/tmp/drone_{part_id}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"aevalsrc=0.12*sin(2*PI*55*t)+0.06*sin(2*PI*110*t)+0.07*sin(2*PI*18.9*t):s=44100:d={target_dur:.2f}",
            drone_wav
        ], check=True)

        ass_escaped = os.path.abspath(ass_path).replace(":", "\\:")
        subprocess.run([
            "ffmpeg", "-y", "-i", raw_vid, "-i", padded_wav, "-i", drone_wav,
            "-vf", f"ass={ass_escaped}",
            "-filter_complex", "[1:a]volume=1.0[vo];[2:a]volume=0.18[bg];[vo][bg]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", final_part
        ], check=True)

        part_videos.append(final_part)
        gc.collect()

    with open("/tmp/all_parts.txt", "w") as f:
        for pv in part_videos:
            f.write(f"file '{os.path.abspath(pv)}'\n")

    final_master = f"{BASE_DIR}/FINAL_3D_V2_25MIN_2026-11-13.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "/tmp/all_parts.txt", "-c", "copy", final_master], check=True)
    print(f"SUCCESS! 3D V2 25-Min Video Ready: {final_master}")

if __name__ == "__main__":
    asyncio.run(main())
