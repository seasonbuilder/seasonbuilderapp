import openai
import streamlit as st
from openai import OpenAI
import uuid

client = OpenAI()

st.set_page_config(page_title="Coach Edge - Virtual Life Coach",layout="wide")

#Initialize session state variables

if "messages" not in st.session_state:
   st.session_state.messages = []

if 'prompt' not in st.session_state:
   st.session_state.prompt = ''

if 'fname' not in st.session_state:
    st.session_state.fname = ''  

if 'school' not in st.session_state:
    st.session_state.school = ''  

if 'team' not in st.session_state:
    st.session_state.team = ''  

if 'role' not in st.session_state:
    st.session_state.role = ''  

if 'language' not in st.session_state:
    st.session_state.language = ''  

# Initialize OpenAI assistant and thread
if "assistant" not in st.session_state or "thread" not in st.session_state:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
    st.session_state.thread = client.beta.threads.create()

# Retrieve URL Parameters
st.session_state.fname = st.query_params.get("fname", "Unknown")
st.session_state.school = st.query_params.get("school", "Unknown")
st.session_state.team = st.query_params.get("team", "Unknown")
st.session_state.role = st.query_params.get("role", "Unknown")
st.session_state.language = st.query_params.get("language", "Unknown")

# Extract language from parentheses
parts = st.session_state.language.split('(')
if len(parts) > 1:
    lang = parts[1].split(')')[0]
else:
    lang = "Unknown"

additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of {st.session_state.team} at the {st.session_state.school} and their native language is {st.session_state.language}. If the response is not given to them in their native language, give a response in their native language too."


# Define translations for each supported language
translations = {
    "Spanish": {
        "ask_question": "### **Haz una pregunta o selecciona un tema**",
        "expander_title": "Temas Para Comenzar",
        "typed_input_placeholder": "¿Qué tienes en mente?",
        "button_prompts": [
            'Luchas con la Salud Mental',
            'Relaciones',
            'Liderazgo',
            'Reducir el Impacto del Estrés',
            'Gestión del Tiempo',
            '¡Me siento raro! No estoy seguro de lo que está pasando'
        ],
        "prompts": [
            'Estoy luchando con mi salud mental. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar mis desafíos y luego desarrollar una estrategia práctica y específica para mejorar.',
            'Estoy luchando con una relación. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar mi desafío relacional y luego dame consejos prácticos para mejorar esa relación.',
            'Quiero mejorar mis habilidades de liderazgo. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar en qué áreas de liderazgo necesito trabajar y luego ayúdame a desarrollar un plan para crecer en esa área.',
            'Estoy muy estresado. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar qué puede estar causando mi estrés (estoy abierto a la posibilidad de que pueda estar causándolo) y luego ayúdame a desarrollar un plan para afrontarlo de manera saludable y, con suerte, reducir el impacto que el estrés tiene en mí para que pueda ser más feliz.',
            'Necesito ayuda con la gestión de mi tiempo. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar dónde puedo estar mal gestionando mi tiempo o distrayéndome y dame algunos consejos para mejorar.',
            'Me siento raro pero no sé realmente qué está pasando. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar mis desafíos y luego desarrollar una estrategia para enfrentarlos.'
        ]
    },
    "Arabic": {
        "ask_question": "### **اطرح سؤالاً أو اختر موضوعًا**",
        "expander_title": "مواضيع لتبدأ بها",
        "typed_input_placeholder": "ما الذي يدور في ذهنك؟",
        "button_prompts": [
            'الصعوبات النفسية',
            'العلاقات',
            'القيادة',
            'تقليل تأثير التوتر',
            'إدارة الوقت',
            'أشعر بأنني لست على ما يرام! لست متأكدًا مما يجري'
        ],
        "prompts": [
            'أعاني من صعوبات نفسية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدياتي ومن ثم تطوير استراتيجية عملية محددة للتحسن.',
            'أعاني من مشكلة في علاقة. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدي العلاقة ومن ثم تقديم نصائح عملية لتحسين تلك العلاقة.',
            'أريد تطوير مهاراتي القيادية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد مجالات القيادة التي أحتاج للعمل عليها ومن ثم مساعدتي في وضع خطة للنمو في هذا المجال.',
            'أنا متوتر للغاية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد ما قد يسبب توتري (وأنا منفتح لاحتمالية أن أكون أنا السبب) ومن ثم مساعدتي في وضع خطة للتعامل مع التوتر بطرق صحية وتقليل تأثيره علي حتى أتمكن من أن أكون أكثر سعادة.',
            'أحتاج مساعدة في إدارة وقتي. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد أين يمكن أن أكون أسيء إدارة وقتي أو مشتت وأعطني بعض النصائح للتحسن.',
            'أشعر بأنني لست على ما يرام ولكن لا أعرف ما يحدث حقاً. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدياتي ومن ثم وضع استراتيجية لمواجهتها.'
        ]
    },
    "Japanese": {
        "ask_question": "### **質問するかトピックを選んでください**",
        "expander_title": "スタートするためのトピック",
        "typed_input_placeholder": "何を考えていますか？",
        "button_prompts": [
            'メンタルヘルスの悩み',
            '人間関係',
            'リーダーシップ',
            'ストレスの影響を減らす',
            '時間管理',
            'なんだか調子が悪い！何が起きているのかよくわからない'
        ],
        "prompts": [
            'メンタルヘルスで悩んでいます。ロールプレイを通じて1つずつ質問して、私の課題を特定し、それを改善するための実用的で具体的な戦略を立てるのを手伝ってください。',
            '人間関係で悩んでいます。ロールプレイを通じて1つずつ質問して、私の人間関係の課題を特定し、その関係を改善するための実用的なアドバイスをしてください。',
            'リーダーシップスキルを伸ばしたいです。ロールプレイを通じて1つずつ質問して、リーダーシップのどの分野を改善する必要があるかを特定し、その分野を成長させる計画を立てるのを手伝ってください。',
            'とてもストレスを感じています。ロールプレイを通じて1つずつ質問して、私のストレスの原因となっているものを特定し（私が原因かもしれないことも考慮しています）、それに対処するための健康的な方法での計画を立てるのを手伝ってください。ストレスの影響を減らし、より幸せになることを目指します。',
            '時間管理が苦手です。ロールプレイを通じて1つずつ質問して、時間の管理が悪いところや集中できていないところを特定し、改善のためのアドバイスをください。',
            '調子が悪いのですが、何が起きているのかよくわかりません。ロールプレイを通じて1つずつ質問して、私の課題を特定し、それに対処するための戦略を考え出してください。'
        ]
    },
    "English": {
        "ask_question": "### **Ask a Question or Select a Topic**",
        "expander_title": "Topics To Get You Started",
        "typed_input_placeholder": "What's on your mind?",
        "button_prompts": [
            'Mental Health Struggles',
            'Relationships',
            'Leadership',
            'Reducing Impact of Stress',
            'Time Management',
            'I just feel off! Not sure what is going on'
        ],
        "prompts": [
            'I am struggling with my mental health. Ask me one question at a time via role play to help me identify my challenges and then develop a practical specific strategy to get better.',
            'I am struggling with a relationship. Ask me one question at a time via role play to help me identify my relational challenge and then give me practical advice to improve that relationship.',
            'I want to grow my leadership skills. Ask me one question at a time via role play to help me identify what areas of leadership I need to work on and then help me develop a plan to grow that area.',
            'I am so stressed out. Ask me one question at a time via role play to help me identify what may be causing my stress (I am open to the possibility that I may be causing it) and then help me develop a plan to cope with it in healthy ways and hopefully reduce the impact stress has on me so I can be happier.',
            'I need help with my time management.  Ask me one question at a time via role play to help me identify where I may be mismanaging my time or getting distracted and give me some tips to get better.',
            'I feel off but do not know what is really going on. Ask me one question at a time via role play to help me identify my challenges and then come up with a strategy to attack them.'
        ]
    },
    "French": {
        "ask_question": "### **Posez une question ou sélectionnez un sujet**",
        "expander_title": "Sujets pour commencer",
        "typed_input_placeholder": "Qu'avez-vous en tête ?",
        "button_prompts": [
            'Difficultés de santé mentale',
            'Relations',
            'Leadership',
            'Réduire l\'impact du stress',
            'Gestion du temps',
            'Je me sens bizarre ! Je ne suis pas sûr de ce qui se passe'
        ],
        "prompts": [
            'Je lutte avec ma santé mentale. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier mes défis puis élaborer une stratégie pratique et spécifique pour aller mieux.',
            'Je rencontre des difficultés dans une relation. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier mon défi relationnel puis donnez-moi des conseils pratiques pour améliorer cette relation.',
            'Je veux développer mes compétences en leadership. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier les domaines du leadership sur lesquels je dois travailler puis aidez-moi à élaborer un plan pour développer cette compétence.',
            'Je suis tellement stressé. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier ce qui peut causer mon stress (je suis ouvert à la possibilité que je puisse en être la cause) puis aidez-moi à élaborer un plan pour y faire face de manière saine et, espérons-le, réduire l\'impact du stress sur moi afin que je puisse être plus heureux.',
            'J\'ai besoin d\'aide pour gérer mon temps. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier où je pourrais mal gérer mon temps ou être distrait et donnez-moi quelques conseils pour m\'améliorer.',
            'Je me sens bizarre mais je ne sais pas vraiment ce qui se passe. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier mes défis puis proposez une stratégie pour les attaquer.'
        ]
    },
    "Portuguese": {
        "ask_question": "### **Faça uma pergunta ou selecione um tópico**",
        "expander_title": "Tópicos para começar",
        "typed_input_placeholder": "O que está na sua mente?",
        "button_prompts": [
            'Dificuldades de saúde mental',
            'Relacionamentos',
            'Liderança',
            'Reduzindo o impacto do estresse',
            'Gestão de tempo',
            'Eu simplesmente não me sinto bem! Não tenho certeza do que está acontecendo'
        ],
        "prompts": [
            'Estou enfrentando dificuldades com minha saúde mental. Faça-me uma pergunta de cada vez através de um jogo de papéis para me ajudar a identificar meus desafios e então desenvolver uma estratégia prática e específica para melhorar.',
            'Estou tendo problemas em um relacionamento. Faça-me uma pergunta de cada vez através de um jogo de papéis para me ajudar a identificar meu desafio relacional e então me dê conselhos práticos para melhorar esse relacionamento.',
            'Quero desenvolver minhas habilidades de liderança. Faça-me uma pergunta de cada vez através de um jogo de papéis para me ajudar a identificar em quais áreas de liderança preciso trabalhar e então me ajude a desenvolver um plano para crescer nessa área.',
            'Estou muito estressado. Faça-me uma pergunta de cada vez através de um jogo de papéis para me ajudar a identificar o que pode estar causando meu estresse (estou aberto à possibilidade de que eu possa estar causando isso) e então me ajude a desenvolver um plano para lidar com isso de maneiras saudáveis e, com sorte, reduzir o impacto que o estresse tem sobre mim para que eu possa ser mais feliz.',
            'Preciso de ajuda com minha gestão de tempo. Faça-me uma pergunta de cada vez através de um jogo de papéis para me ajudar a identificar onde posso estar gerenciando mal meu tempo ou me distraindo e me dê algumas dicas para melhorar.',
            'Eu me sinto estranho, mas não sei o que realmente está acontecendo. Faça-me uma pergunta de cada vez através de um jogo de papéis para me ajudar a identificar meus desafios e então elaborar uma estratégia para enfrentá-los.'
        ]
    },
    "Greek": {
        "ask_question": "### **Κάντε μια ερώτηση ή επιλέξτε ένα θέμα**",
        "expander_title": "Θέματα για να ξεκινήσετε",
        "typed_input_placeholder": "Τι έχετε στο μυαλό σας;",
        "button_prompts": [
            'Δυσκολίες ψυχικής υγείας',
            'Σχέσεις',
            'Ηγεσία',
            'Μείωση του αντίκτυπου του στρες',
            'Διαχείριση χρόνου',
            'Απλά δεν αισθάνομαι καλά! Δεν είμαι σίγουρος τι συμβαίνει'
        ],
        "prompts": [
            'Αντιμετωπίζω δυσκολίες με την ψυχική μου υγεία. Κάντε μου μια ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω τις προκλήσεις μου και στη συνέχεια να αναπτύξω μια πρακτική και συγκεκριμένη στρατηγική για να βελτιωθώ.',
            'Αντιμετωπίζω προβλήματα σε μια σχέση. Κάντε μου μια ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω την πρόκλησή μου στη σχέση και στη συνέχεια να μου δώσετε πρακτικές συμβουλές για να βελτιώσω αυτή τη σχέση.',
            'Θέλω να αναπτύξω τις ηγετικές μου ικανότητες. Κάντε μου μια ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω σε ποιους τομείς της ηγεσίας πρέπει να εργαστώ και στη συνέχεια να με βοηθήσετε να αναπτύξω ένα σχέδιο για να αναπτυχθώ σε αυτόν τον τομέα.',
            'Είμαι τόσο αγχωμένος. Κάντε μου μια ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω τι μπορεί να προκαλεί το άγχος μου (είμαι ανοιχτός στην πιθανότητα ότι μπορεί να το προκαλώ εγώ) και στη συνέχεια να με βοηθήσετε να αναπτύξω ένα σχέδιο για να το αντιμετωπίσω με υγιείς τρόπους και, ελπίζω, να μειώσω τον αντίκτυπο που έχει το άγχος πάνω μου ώστε να μπορώ να είμαι πιο ευτυχισμένος.',
            'Χρειάζομαι βοήθεια με τη διαχείριση του χρόνου μου. Κάντε μου μια ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω πού μπορεί να διαχειρίζομαι λάθος τον χρόνο μου ή να αποσπώμαι και να μου δώσετε μερικές συμβουλές για να βελτιωθώ.',
            'Νιώθω παράξενα αλλά δεν ξέρω πραγματικά τι συμβαίνει. Κάντε μου μια ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω τις προκλήσεις μου και στη συνέχεια να βρείτε μια στρατηγική για να τις αντιμετωπίσω.'
        ]
    },
    "Dutch": {
        "ask_question": "### **Stel een vraag of selecteer een onderwerp**",
        "expander_title": "Onderwerpen om mee te beginnen",
        "typed_input_placeholder": "Wat houdt je bezig?",
        "button_prompts": [
            'Mentale gezondheidsproblemen',
            'Relaties',
            'Leiderschap',
            'Impact van stress verminderen',
            'Tijdmanagement',
            'Ik voel me gewoon niet lekker! Niet zeker wat er aan de hand is'
        ],
        "prompts": [
            'Ik worstel met mijn mentale gezondheid. Stel me één vraag tegelijk via een rollenspel om me te helpen mijn uitdagingen te identificeren en vervolgens een praktische, specifieke strategie te ontwikkelen om beter te worden.',
            'Ik heb moeite met een relatie. Stel me één vraag tegelijk via een rollenspel om me te helpen mijn relationele uitdaging te identificeren en geef me vervolgens praktisch advies om die relatie te verbeteren.',
            'Ik wil mijn leiderschapsvaardigheden ontwikkelen. Stel me één vraag tegelijk via een rollenspel om me te helpen identificeren aan welke leiderschapsgebieden ik moet werken en help me vervolgens een plan te ontwikkelen om dat gebied te laten groeien.',
            'Ik ben zo gestrest. Stel me één vraag tegelijk via een rollenspel om me te helpen identificeren wat mijn stress kan veroorzaken (ik sta open voor de mogelijkheid dat ik het zelf veroorzaak) en help me vervolgens een plan te ontwikkelen om er op een gezonde manier mee om te gaan en hopelijk de impact van stress op mij te verminderen zodat ik gelukkiger kan zijn.',
            'Ik heb hulp nodig met mijn tijdmanagement. Stel me één vraag tegelijk via een rollenspel om me te helpen identificeren waar ik mijn tijd misschien verkeerd beheer of afgeleid raak en geef me enkele tips om beter te worden.',
            'Ik voel me niet lekker maar weet niet echt wat er aan de hand is. Stel me één vraag tegelijk via een rollenspel om me te helpen mijn uitdagingen te identificeren en vervolgens een strategie te bedenken om ze aan te pakken.'
        ]
    }
}

# Get the translations for the selected language, default to English
lang_translations = translations.get(lang, translations["English"])

st.markdown(lang_translations["ask_question"])

with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text):
            st.session_state.prompt = lang_translations["prompts"][idx]

typed_input = st.chat_input(lang_translations["typed_input_placeholder"])

if typed_input:
    st.session_state.prompt = typed_input


# # Initialize session state variables

# if "messages" not in st.session_state:
#    st.session_state.messages = []

# if 'prompt' not in st.session_state:
#    st.session_state.prompt = ''
   
# if "assistant" not in st.session_state:
#    openai.api_key = st.secrets["OPENAI_API_KEY"]
#    st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
#    st.session_state.thread = client.beta.threads.create()

# if 'fname' not in st.session_state:
#     st.session_state.fname = ''  

# if 'school' not in st.session_state:
#     st.session_state.school = ''  

# if 'team' not in st.session_state:
#     st.session_state.team = ''  

# if 'role' not in st.session_state:
#     st.session_state.role = ''  

# if 'language' not in st.session_state:
#     st.session_state.language = ''  


# #Retrieve URL Parameters
# st.session_state.fname = st.query_params.get("fname", "Unknown")
# st.session_state.school = st.query_params.get("school", "Unknown")
# st.session_state.team = st.query_params.get("team", "Unknown")
# st.session_state.role = st.query_params.get("role", "Unknown")
# st.session_state.language=st.query_params.get("language","Unknown")

# additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of {st.session_state.team} at the {st.session_state.school} and their native language is {st.session_state.language}. If the response is not given to them in their native language, give a response in their native language too."

# #st.write(st.session_state.language)

# # Find the english translation of the language in the parenthesis
# parts = st.session_state.language.split('(')
# if len(parts) > 1:
#     lang = parts[1].split(')')[0]


# # Homepage in Spanish
# if lang == "Spanish":  
#     st.markdown("### **Haz una pregunta o selecciona un tema**")    

#     button_prompt1 = 'Luchas con la Salud Mental'
#     button_prompt2 = 'Relaciones'
#     button_prompt3 = 'Liderazgo'
#     button_prompt4 = 'Reducir el Impacto del Estrés'
#     button_prompt5 = 'Gestión del Tiempo'
#     button_prompt6 = '¡Me siento raro! No estoy seguro de lo que está pasando'

#     with st.expander("Temas Para Comenzar"):
#        # Crear botones de mensajes predefinidos
#         if st.button(button_prompt1):
#             st.session_state.prompt = 'Estoy luchando con mi salud mental. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar mis desafíos y luego desarrollar una estrategia práctica y específica para mejorar.'

#         if st.button(button_prompt2):
#             st.session_state.prompt = 'Estoy luchando con una relación. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar mi desafío relacional y luego dame consejos prácticos para mejorar esa relación.'

#         if st.button(button_prompt3):
#             st.session_state.prompt = 'Quiero mejorar mis habilidades de liderazgo. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar en qué áreas de liderazgo necesito trabajar y luego ayúdame a desarrollar un plan para crecer en esa área.'

#         if st.button(button_prompt4):
#             st.session_state.prompt = 'Estoy muy estresado. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar qué puede estar causando mi estrés (estoy abierto a la posibilidad de que pueda estar causándolo) y luego ayúdame a desarrollar un plan para afrontarlo de manera saludable y, con suerte, reducir el impacto que el estrés tiene en mí para que pueda ser más feliz.'

#         if st.button(button_prompt5):
#             st.session_state.prompt = 'Necesito ayuda con la gestión de mi tiempo. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar dónde puedo estar mal gestionando mi tiempo o distrayéndome y dame algunos consejos para mejorar.'

#         if st.button(button_prompt6):
#             st.session_state.prompt = 'Me siento raro pero no sé realmente qué está pasando. Hazme una pregunta a la vez a través de un juego de roles para ayudarme a identificar mis desafíos y luego desarrollar una estrategia para enfrentarlos.'

#     typed_input = st.chat_input("¿Qué tienes en mente?")

# #Homepage in Arabic
# elif lang == "Arabic":
#     st.markdown("### **اطرح سؤالاً أو اختر موضوعًا**")    

#     button_prompt1 = 'الصعوبات النفسية'
#     button_prompt2 = 'العلاقات'
#     button_prompt3 = 'القيادة'
#     button_prompt4 = 'تقليل تأثير التوتر'
#     button_prompt5 = 'إدارة الوقت'
#     button_prompt6 = 'أشعر بأنني لست على ما يرام! لست متأكدًا مما يجري'

#     with st.expander("مواضيع لتبدأ بها"):
#        # إنشاء أزرار بالرسائل المحددة مسبقًا
#         if st.button(button_prompt1):
#             st.session_state.prompt = 'أعاني من صعوبات نفسية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدياتي ومن ثم تطوير استراتيجية عملية محددة للتحسن.'

#         if st.button(button_prompt2):
#             st.session_state.prompt = 'أعاني من مشكلة في علاقة. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدي العلاقة ومن ثم تقديم نصائح عملية لتحسين تلك العلاقة.'

#         if st.button(button_prompt3):
#             st.session_state.prompt = 'أريد تطوير مهاراتي القيادية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد مجالات القيادة التي أحتاج للعمل عليها ومن ثم مساعدتي في وضع خطة للنمو في هذا المجال.'

#         if st.button(button_prompt4):
#             st.session_state.prompt = 'أنا متوتر للغاية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد ما قد يسبب توتري (وأنا منفتح لاحتمالية أن أكون أنا السبب) ومن ثم مساعدتي في وضع خطة للتعامل مع التوتر بطرق صحية وتقليل تأثيره علي حتى أتمكن من أن أكون أكثر سعادة.'

#         if st.button(button_prompt5):
#             st.session_state.prompt = 'أحتاج مساعدة في إدارة وقتي. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد أين يمكن أن أكون أسيء إدارة وقتي أو مشتت وأعطني بعض النصائح للتحسن.'

#         if st.button(button_prompt6):
#             st.session_state.prompt = 'أشعر بأنني لست على ما يرام ولكن لا أعرف ما يحدث حقاً. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدياتي ومن ثم وضع استراتيجية لمواجهتها.'

#     typed_input = st.chat_input("ما الذي يدور في ذهنك؟")

# #Homepage in Japanese
# elif lang=="Japanese":

#     st.markdown("### **質問するかトピックを選んでください**")    

#     button_prompt1 = 'メンタルヘルスの悩み'
#     button_prompt2 = '人間関係'
#     button_prompt3 = 'リーダーシップ'
#     button_prompt4 = 'ストレスの影響を減らす'
#     button_prompt5 = '時間管理'
#     button_prompt6 = 'なんだか調子が悪い！何が起きているのかよくわからない'

#     with st.expander("スタートするためのトピック"):
#        # 事前定義のプロンプトボタンを作成
#         if st.button(button_prompt1):
#             st.session_state.prompt = 'メンタルヘルスで悩んでいます。ロールプレイを通じて1つずつ質問して、私の課題を特定し、それを改善するための実用的で具体的な戦略を立てるのを手伝ってください。'

#         if st.button(button_prompt2):
#             st.session_state.prompt = '人間関係で悩んでいます。ロールプレイを通じて1つずつ質問して、私の人間関係の課題を特定し、その関係を改善するための実用的なアドバイスをしてください。'

#         if st.button(button_prompt3):
#             st.session_state.prompt = 'リーダーシップスキルを伸ばしたいです。ロールプレイを通じて1つずつ質問して、リーダーシップのどの分野を改善する必要があるかを特定し、その分野を成長させる計画を立てるのを手伝ってください。'

#         if st.button(button_prompt4):
#             st.session_state.prompt = 'とてもストレスを感じています。ロールプレイを通じて1つずつ質問して、私のストレスの原因となっているものを特定し（私が原因かもしれないことも考慮しています）、それに対処するための健康的な方法での計画を立てるのを手伝ってください。ストレスの影響を減らし、より幸せになることを目指します。'

#         if st.button(button_prompt5):
#             st.session_state.prompt = '時間管理が苦手です。ロールプレイを通じて1つずつ質問して、時間の管理が悪いところや集中できていないところを特定し、改善のためのアドバイスをください。'

#         if st.button(button_prompt6):
#             st.session_state.prompt = '調子が悪いのですが、何が起きているのかよくわかりません。ロールプレイを通じて1つずつ質問して、私の課題を特定し、それに対処するための戦略を考え出してください。'

#     typed_input = st.chat_input("何を考えていますか？")

# #Default homepage in English    
# else:
#     st.markdown("### **Ask a Question or Select a Topic**")    

#     button_prompt1 = 'Mental Health Struggles'
#     button_prompt2 = 'Relationships'
#     button_prompt3 = 'Leadership'
#     button_prompt4 = 'Reducing Impact of Stress'
#     button_prompt5 = 'Time Management'
#     button_prompt6 = 'I just feel off! Not sure what is going on'

#     with st.expander("Topics To Get Your Started"):
#        # Create Predefine prompt buttons
#         if st.button(button_prompt1):
#             st.session_state.prompt = 'I am struggling with my mental health. Ask me one question at a time via role play to help me identify my challenges and then develop a practical specific strategy to get better.'

#         if st.button(button_prompt2):
#             st.session_state.prompt = 'I am struggling with a relationship. Ask me one question at a time via role play to help me identify my relational challenge and then give me practical advice to improve that relationship.'

#         if st.button(button_prompt3):
#             st.session_state.prompt = 'I want to grow my leadership skills. Ask me one question at a time via role play to help me identify what areas of leadership I need to work on and then help me develop a plan to grow that area.'

#         if st.button(button_prompt4):
#             st.session_state.prompt = 'I am so stressed out. Ask me one question at a time via role play to help me identify what may be causing my stress (I am open to the possibility that I may be causing it) and then help me develop a plan to cope with it in healthy ways and hopefully reduce the impact stress has on me so I can be happier.'

#         if st.button(button_prompt5):
#             st.session_state.prompt = 'I need help with my time management.  Ask me one questions at a time via roe play to help me identify where I may be mismanaging my time or getting distracted and give me some tips to get better.'

#         if st.button(button_prompt6):
#             st.session_state.prompt = 'I feel off but do not know what is really going on. Ask me one question one at a time via role play to help me identify my challenges and then come up with a strategy to attack them.'

#     typed_input = st.chat_input("What's on your mind?")

# if typed_input:
#     st.session_state.prompt = typed_input

for message in st.session_state.messages:
    if message["role"] == "user":
       with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
          st.markdown(message["content"])
    else:
       with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
          st.markdown(message["content"])

# Check if there is typed input
if st.session_state.prompt:
    delta = [] 
    response = ""
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
        st.markdown(st.session_state.prompt)
    with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
        container = st.empty()
        st.session_state.thread_messages= client.beta.threads.messages.create(
              st.session_state.thread.id, role="user",content=st.session_state.prompt
        )

        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id = st.session_state.thread.id,
            additional_instructions = additional_instructions,
            stream = True
        )
        if stream:
           for event in stream:
              if event.data.object == "thread.message.delta":
                 for content in event.data.delta.content:
                    if content.type == 'text':
                       delta.append(content.text.value)
                       response = "".join(item for item in delta if item).strip()
                       container.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
