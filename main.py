"""
Zoom Voice Gallery — AWS Polly TTS Generator (All Languages)
Generates MP3 files for all available neural + standard voices.

Prerequisites:
  pip install boto3

Set credentials before running:
  export AWS_ACCESS_KEY_ID=your_key
  export AWS_SECRET_ACCESS_KEY=your_secret
  export AWS_DEFAULT_REGION=us-east-1
"""

import os

import boto3

OUTPUT_BASE = "audios"

# Each voice: (VoiceId, type, closing, engine)
# engine: "neural" or "standard"

CLOSINGS = [
    "Nice to meet you!",
    "Hope you enjoy the demo!",
    "Thanks for listening!",
    "Looking forward to working with you!",
    "Have a wonderful day!",
]


def rotate_closing(i):
    return CLOSINGS[i % len(CLOSINGS)]


LANGUAGES = [
    {
        "folder": "en-us",
        "polly_lang": "en-US",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Matthew", "male", "Nice to meet you!", "neural"),
            ("Danielle", "female", "Hope you enjoy the demo!", "neural"),
            ("Gregory", "male", "Thanks for listening!", "neural"),
            ("Joanna", "female", "Looking forward to working with you!", "neural"),
            ("Ruth", "female", "Have a wonderful day!", "neural"),
            ("Kevin", "male-child", "Nice to meet you!", "neural"),
            ("Salli", "female", "Hope you enjoy the demo!", "neural"),
            ("Kimberly", "female", "Thanks for listening!", "neural"),
            ("Kendra", "female", "Looking forward to working with you!", "neural"),
            ("Justin", "male-child", "Have a wonderful day!", "neural"),
            ("Joey", "male", "Nice to meet you!", "neural"),
            ("Ivy", "female-child", "Hope you enjoy the demo!", "neural"),
            ("Stephen", "male", "Thanks for listening!", "neural"),
        ],
    },
    {
        "folder": "en-au",
        "polly_lang": "en-AU",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Olivia", "female", "Nice to meet you!", "neural"),
            ("Nicole", "female", "Hope you enjoy the demo!", "standard"),
            ("Russell", "male", "Thanks for listening!", "standard"),
        ],
    },
    {
        "folder": "en-gb",
        "polly_lang": "en-GB",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Amy", "female", "Nice to meet you!", "neural"),
            ("Emma", "female", "Hope you enjoy the demo!", "neural"),
            ("Brian", "male", "Thanks for listening!", "neural"),
            ("Arthur", "male", "Looking forward to working with you!", "neural"),
        ],
    },
    {
        "folder": "en-gb-wls",
        "polly_lang": "en-GB-WLS",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Geraint", "male", "Nice to meet you!", "standard"),
        ],
    },
    {
        "folder": "en-ie",
        "polly_lang": "en-IE",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Niamh", "female", "Nice to meet you!", "neural"),
        ],
    },
    {
        "folder": "en-in",
        "polly_lang": "en-IN",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Kajal", "female", "Nice to meet you!", "neural"),
            ("Aditi", "female", "Hope you enjoy the demo!", "standard"),
            ("Raveena", "female", "Thanks for listening!", "standard"),
        ],
    },
    {
        "folder": "en-nz",
        "polly_lang": "en-NZ",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Aria", "female", "Nice to meet you!", "neural"),
        ],
    },
    {
        "folder": "en-za",
        "polly_lang": "en-ZA",
        "greeting": "Welcome to the Zoom Text to Speech Voice Gallery, powered by CDW! You are listening to the voice of {name}. {closing}",
        "voices": [
            ("Ayanda", "female", "Nice to meet you!", "neural"),
        ],
    },
    {
        "folder": "ar-gulf",
        "polly_lang": "ar-AE",
        "greeting": "مرحبا بكم في معرض أصوات Zoom للتحويل من نص إلى كلام، بدعم من CDW! أنتم تستمعون إلى صوت {name}. {closing}",
        "voices": [
            ("Hala", "female", "سعيدة بلقائكم!", "neural"),
            ("Zayd", "male", "نتمنى لكم يوماً سعيداً!", "neural"),
        ],
    },
    {
        "folder": "ar",
        "polly_lang": "arb",
        "greeting": "مرحبا بكم في معرض أصوات Zoom للتحويل من نص إلى كلام، بدعم من CDW! أنتم تستمعون إلى صوت {name}. {closing}",
        "voices": [
            ("Zeina", "female", "سعيدة بلقائكم!", "standard"),
        ],
    },
    {
        "folder": "ca",
        "polly_lang": "ca-ES",
        "greeting": "Benvinguts a la galeria de veus de Zoom, amb el suport de CDW! Esteu escoltant la veu de l'{name}. {closing}",
        "voices": [
            ("Arlet", "female", "Encantada de conèixer-vos!", "neural"),
        ],
    },
    {
        "folder": "zh-cn",
        "polly_lang": "cmn-CN",
        "greeting": "欢迎来到Zoom文字转语音声音展示，由CDW提供支持！您正在收听{name}的声音。{closing}",
        "voices": [
            ("Zhiyu", "female", "很高兴认识您！", "neural"),
        ],
    },
    {
        "folder": "zh-hk",
        "polly_lang": "yue-CN",
        "greeting": "歡迎嚟到Zoom文字轉語音聲音展示，由CDW提供支持！你而家聽緊嘅係{name}嘅聲音。{closing}",
        "voices": [
            ("Hiujin", "female", "好高興認識你！", "neural"),
        ],
    },
    {
        "folder": "cs",
        "polly_lang": "cs-CZ",
        "greeting": "Vítejte v galerii hlasů Zoom pro převod textu na řeč, s podporou CDW! Posloucháte hlas {name}. {closing}",
        "voices": [
            ("Jitka", "female", "Těší mě!", "neural"),
        ],
    },
    {
        "folder": "cy",
        "polly_lang": "cy-GB",
        "greeting": "Croeso i oriel lleisiau Zoom, wedi'i bweru gan CDW! Rydych chi'n gwrando ar lais {name}. {closing}",
        "voices": [
            ("Gwyneth", "female", "Braf cwrdd â chi!", "standard"),
        ],
    },
    {
        "folder": "da",
        "polly_lang": "da-DK",
        "greeting": "Velkommen til Zoom tekst-til-tale stemmegalleri, drevet af CDW! Du lytter til stemmen af {name}. {closing}",
        "voices": [
            ("Sofie", "female", "Dejligt at møde dig!", "neural"),
            ("Naja", "female", "Håber du nyder demoen!", "standard"),
            ("Mads", "male", "Tak fordi du lyttede med!", "standard"),
        ],
    },
    {
        "folder": "de-at",
        "polly_lang": "de-AT",
        "greeting": "Willkommen in der Zoom Text-to-Speech Stimmengalerie, unterstützt von CDW! Sie hören die Stimme von {name}. {closing}",
        "voices": [
            ("Hannah", "female", "Freut mich, Sie kennenzulernen!", "neural"),
        ],
    },
    {
        "folder": "de-de",
        "polly_lang": "de-DE",
        "greeting": "Willkommen in der Zoom Text-to-Speech Stimmengalerie, unterstützt von CDW! Sie hören die Stimme von {name}. {closing}",
        "voices": [
            ("Vicki", "female", "Freut mich, Sie kennenzulernen!", "neural"),
            ("Daniel", "male", "Vielen Dank fürs Zuhören!", "neural"),
            ("Marlene", "female", "Ich hoffe, die Demo gefällt Ihnen!", "standard"),
            ("Hans", "male", "Einen wunderschönen Tag noch!", "standard"),
        ],
    },
    {
        "folder": "es-es",
        "polly_lang": "es-ES",
        "greeting": "Bienvenidos a la galería de voces de Zoom, con el apoyo de CDW! Están escuchando la voz de {name}. {closing}",
        "voices": [
            ("Lucia", "female", "¡Encantada de conocerles!", "neural"),
            ("Sergio", "male", "¡Gracias por escuchar!", "neural"),
            ("Conchita", "female", "¡Esperamos que les guste!", "standard"),
            ("Enrique", "male", "¡Que tengan un buen día!", "standard"),
        ],
    },
    {
        "folder": "es-mx",
        "polly_lang": "es-MX",
        "greeting": "Bienvenidos a la galería de voces de Zoom, con el apoyo de CDW! Están escuchando la voz de {name}. {closing}",
        "voices": [
            ("Mia", "female", "¡Mucho gusto!", "neural"),
            ("Andres", "male", "¡Gracias por escuchar!", "neural"),
        ],
    },
    {
        "folder": "es-us",
        "polly_lang": "es-US",
        "greeting": "Bienvenidos a la galería de voces de Zoom, con el apoyo de CDW! Están escuchando la voz de {name}. {closing}",
        "voices": [
            ("Lupe", "female", "¡Mucho gusto en conocerlos!", "neural"),
            ("Pedro", "male", "¡Gracias por escuchar!", "neural"),
            ("Penelope", "female", "¡Esperamos que les guste!", "standard"),
            ("Miguel", "male", "¡Que tengan un buen día!", "standard"),
        ],
    },
    {
        "folder": "fi",
        "polly_lang": "fi-FI",
        "greeting": "Tervetuloa Zoomin tekstistä puheeksi ääni galleriaan, CDW:n tuella! Kuuntelet ääntä nimeltä {name}. {closing}",
        "voices": [
            ("Suvi", "female", "Hauska tavata!", "neural"),
        ],
    },
    {
        "folder": "fr-be",
        "polly_lang": "fr-BE",
        "greeting": "Bienvenue dans la galerie de voix Zoom, avec le soutien de CDW! Vous écoutez la voix de {name}. {closing}",
        "voices": [
            ("Isabelle", "female", "Enchantée de vous rencontrer!", "neural"),
        ],
    },
    {
        "folder": "fr-ca",
        "polly_lang": "fr-CA",
        "greeting": "Bienvenue dans la galerie de voix Zoom, avec le soutien de CDW! Vous écoutez la voix de {name}. {closing}",
        "voices": [
            ("Gabrielle", "female", "Enchantée de vous rencontrer!", "neural"),
            ("Liam", "male", "Merci de votre écoute!", "neural"),
            ("Chantal", "female", "Bonne journée!", "standard"),
        ],
    },
    {
        "folder": "fr",
        "polly_lang": "fr-FR",
        "greeting": "Bienvenue dans la galerie de voix Zoom, avec le soutien de CDW! Vous écoutez la voix de {name}. {closing}",
        "voices": [
            ("Lea", "female", "Enchantée de vous rencontrer!", "neural"),
            ("Remi", "male", "Merci de votre écoute!", "neural"),
            ("Celine", "female", "J'espère que la démo vous plaît!", "standard"),
            ("Mathieu", "male", "Passez une excellente journée!", "standard"),
        ],
    },
    {
        "folder": "hi",
        "polly_lang": "hi-IN",
        "greeting": "Zoom टेक्स्ट टू स्पीच वॉइस गैलरी में आपका स्वागत है, CDW द्वारा संचालित! आप {name} की आवाज़ सुन रहे हैं। {closing}",
        "voices": [
            ("Kajal", "female", "आपसे मिलकर खुशी हुई!", "neural"),
            ("Aditi", "female", "सुनने के लिए धन्यवाद!", "standard"),
        ],
    },
    {
        "folder": "is",
        "polly_lang": "is-IS",
        "greeting": "Velkomin í Zoom raddgallerí, knúið af CDW! Þú ert að hlusta á rödd {name}. {closing}",
        "voices": [
            ("Dora", "female", "Gaman að kynnast þér!", "standard"),
            ("Karl", "male", "Takk fyrir að hlusta!", "standard"),
        ],
    },
    {
        "folder": "it",
        "polly_lang": "it-IT",
        "greeting": "Benvenuti nella galleria vocale Zoom, con il supporto di CDW! State ascoltando la voce di {name}. {closing}",
        "voices": [
            ("Bianca", "female", "Piacere di conoscervi!", "neural"),
            ("Adriano", "male", "Grazie per l'ascolto!", "neural"),
            ("Carla", "female", "Spero vi piaccia la demo!", "standard"),
            ("Giorgio", "male", "Buona giornata!", "standard"),
        ],
    },
    {
        "folder": "ja",
        "polly_lang": "ja-JP",
        "greeting": "CDW提供、Zoomテキスト読み上げボイスギャラリーへようこそ！{name}の声をお聞きいただいています。{closing}",
        "voices": [
            ("Takumi", "male", "よろしくお願いします！", "neural"),
            ("Kazuha", "female", "お聞きいただきありがとうございます！", "neural"),
            ("Tomoko", "female", "素敵な一日をお過ごしください！", "neural"),
            ("Mizuki", "female", "デモをお楽しみください！", "standard"),
        ],
    },
    {
        "folder": "ko",
        "polly_lang": "ko-KR",
        "greeting": "CDW가 제공하는 Zoom 텍스트 음성 변환 보이스 갤러리에 오신 것을 환영합니다! 지금 듣고 계신 목소리는 {name}입니다. {closing}",
        "voices": [
            ("Seoyeon", "female", "만나서 반갑습니다!", "neural"),
            ("Jihye", "female", "들어주셔서 감사합니다!", "neural"),
        ],
    },
    {
        "folder": "nb",
        "polly_lang": "nb-NO",
        "greeting": "Velkommen til Zoom tekst-til-tale stemmegalleri, drevet av CDW! Du lytter til stemmen til {name}. {closing}",
        "voices": [
            ("Ida", "female", "Hyggelig å møte deg!", "neural"),
            ("Liv", "female", "Takk for at du lytter!", "standard"),
        ],
    },
    {
        "folder": "nl-be",
        "polly_lang": "nl-BE",
        "greeting": "Welkom bij de Zoom tekst-naar-spraak stemmengalerij, mogelijk gemaakt door CDW! U luistert naar de stem van {name}. {closing}",
        "voices": [
            ("Lisa", "female", "Aangenaam kennis te maken!", "neural"),
        ],
    },
    {
        "folder": "nl",
        "polly_lang": "nl-NL",
        "greeting": "Welkom bij de Zoom tekst-naar-spraak stemmengalerij, mogelijk gemaakt door CDW! U luistert naar de stem van {name}. {closing}",
        "voices": [
            ("Laura", "female", "Aangenaam kennis te maken!", "neural"),
            ("Lotte", "female", "Hopelijk bevalt de demo!", "standard"),
            ("Ruben", "male", "Bedankt voor het luisteren!", "standard"),
        ],
    },
    {
        "folder": "pl",
        "polly_lang": "pl-PL",
        "greeting": "Witamy w galerii głosów Zoom, wspieranej przez CDW! Słuchasz głosu {name}. {closing}",
        "voices": [
            ("Ola", "female", "Miło mi Cię poznać!", "neural"),
            ("Ewa", "female", "Mam nadzieję, że podoba się demo!", "standard"),
            ("Maja", "female", "Dziękuję za wysłuchanie!", "standard"),
            ("Jacek", "male", "Miłego dnia!", "standard"),
            ("Jan", "male", "Miło mi Cię poznać!", "standard"),
        ],
    },
    {
        "folder": "pt-br",
        "polly_lang": "pt-BR",
        "greeting": "Bem-vindos à galeria de vozes Zoom, com o apoio da CDW! Vocês estão ouvindo a voz de {name}. {closing}",
        "voices": [
            ("Camila", "female", "Prazer em conhecê-los!", "neural"),
            ("Vitoria", "female", "Obrigada por ouvir!", "neural"),
            ("Thiago", "male", "Tenham um ótimo dia!", "neural"),
            ("Ricardo", "male", "Espero que gostem da demo!", "standard"),
        ],
    },
    {
        "folder": "pt-pt",
        "polly_lang": "pt-PT",
        "greeting": "Bem-vindos à galeria de vozes Zoom, com o apoio da CDW! Estão a ouvir a voz de {name}. {closing}",
        "voices": [
            ("Ines", "female", "Prazer em conhecê-los!", "neural"),
            ("Cristiano", "male", "Obrigado por ouvir!", "standard"),
        ],
    },
    {
        "folder": "ro",
        "polly_lang": "ro-RO",
        "greeting": "Bine ați venit la galeria de voci Zoom, cu sprijinul CDW! Ascultați vocea lui {name}. {closing}",
        "voices": [
            ("Carmen", "female", "Încântată de cunoștință!", "standard"),
        ],
    },
    {
        "folder": "ru",
        "polly_lang": "ru-RU",
        "greeting": "Добро пожаловать в голосовую галерею Zoom, при поддержке CDW! Вы слушаете голос {name}. {closing}",
        "voices": [
            ("Tatyana", "female", "Приятно познакомиться!", "standard"),
            ("Maxim", "male", "Спасибо, что слушаете!", "standard"),
        ],
    },
    {
        "folder": "sv",
        "polly_lang": "sv-SE",
        "greeting": "Välkommen till Zoom text-till-tal röstgalleri, med stöd av CDW! Du lyssnar på rösten av {name}. {closing}",
        "voices": [
            ("Elin", "female", "Trevligt att träffas!", "neural"),
            ("Astrid", "female", "Tack för att du lyssnar!", "standard"),
        ],
    },
    {
        "folder": "tr",
        "polly_lang": "tr-TR",
        "greeting": "CDW desteğiyle Zoom Metinden Sese Ses Galerisine hoş geldiniz! {name} sesini dinliyorsunuz. {closing}",
        "voices": [
            ("Burcu", "female", "Tanıştığımıza memnun oldum!", "neural"),
            ("Filiz", "female", "Dinlediğiniz için teşekkürler!", "standard"),
        ],
    },
]


def main():
    polly = boto3.client("polly", region_name="us-east-1")

    total = sum(len(lang["voices"]) for lang in LANGUAGES)
    generated = 0
    errors = 0

    print(f"Generating {total} voice files across {len(LANGUAGES)} languages...\n")

    for lang in LANGUAGES:
        folder = os.path.join(OUTPUT_BASE, lang["folder"])
        os.makedirs(folder, exist_ok=True)

        if not lang["voices"]:
            continue

        print(f"── {lang['folder']} ({len(lang['voices'])} voices) ──")

        for voice_id, vtype, closing, engine in lang["voices"]:
            text = lang["greeting"].format(name=voice_id, closing=closing)
            filename = os.path.join(folder, f"{voice_id.lower()}.mp3")

            print(f"  {voice_id} ({vtype}, {engine})...", end=" ")

            try:
                params = {
                    "Text": text,
                    "VoiceId": voice_id,
                    "OutputFormat": "mp3",
                    "Engine": engine,
                    "LanguageCode": lang["polly_lang"],
                }

                response = polly.synthesize_speech(**params)

                with open(filename, "wb") as f:
                    f.write(response["AudioStream"].read())

                generated += 1
                print(f"✓ {filename}")

            except Exception as e:
                errors += 1
                print(f"✗ {e}")

        print()

    print(f"Done! {generated}/{total} files generated, {errors} errors.")
    print(f"Files saved to {OUTPUT_BASE}/")


if __name__ == "__main__":
    main()
