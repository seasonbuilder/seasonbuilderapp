# import openai
# import streamlit as st
# from openai import OpenAI
# import uuid

# client = OpenAI()

# st.set_page_config(page_title="Coach Edge - Virtual Life Coach",page_icon="https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png",layout="wide")

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
# st.session_state.prompt=st.query_params.get("prompt")

# additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of {st.session_state.team} at the {st.session_state.school} and their native language is {st.session_state.language}. If the response is not given to them in their native language, give a response in their native language too."

# st.markdown("#### **Ask a Question or Select a Topic**")    

# button_prompt1 = 'Mental Health Struggles'
# button_prompt2 = 'Relationships'
# button_prompt3 = 'Leadership'
# button_prompt4 = 'Understanding Certain Verses in Bible'
# button_prompt5 = 'Time Management'
# button_prompt6 = 'Grow My Faith'

# with st.expander("Topics To Get You Started"):
#    # Create Predefine prompt buttons
#     if st.button(button_prompt1):
#         st.session_state.prompt = 'I am struggling with my mental health. Ask me one question at a time via role play to help me identify my challenges and then develop a practical specific strategy to get better.'

#     if st.button(button_prompt2):
#         st.session_state.prompt = 'I need help with relationships. Ask me one question at a time via role play to help me identify my relationship challenges and then give me practical advice to improve that relationship.'

#     if st.button(button_prompt3):
#         st.session_state.prompt = 'I want to grow my leadership skills. Ask me one question at a time via role play to help me identify what areas of leadership I need to work on and then help me develop a plan to grow in that area.'

#     if st.button(button_prompt4):
#         st.session_state.prompt = 'I do not understand this verse. Ask me which verse or verses I do not understand and then break down that verse for me to help me understand the context and how that could apply to my life.'

#     if st.button(button_prompt5):
#         st.session_state.prompt = 'I need help with my time management.  Ask me one question at a time via role play to help me identify where I may be mismanaging my time or getting distracted and give me some tips to get better.'

#     if st.button(button_prompt6):
#         st.session_state.prompt = 'I want to grow my relationship with God. Ask me one question at a time via role play to help me determine where I need help doing that and then come up with a strategy to implement spiritual disciplines to grow.'


# typed_input = st.chat_input("What's on your mind?")

# if typed_input:
#     st.session_state.prompt = typed_input

# for message in st.session_state.messages:
#     if message["role"] == "user":
#        with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#           st.markdown(message["content"])
#     else:
#        with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#           st.markdown(message["content"])

# # Check if there is typed input
# if st.session_state.prompt:
#     delta = [] 
#     response = ""
#     st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
#     with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#         st.markdown(st.session_state.prompt)
#     with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#         container = st.empty()
#         st.session_state.thread_messages= client.beta.threads.messages.create(
#               st.session_state.thread.id, role="user",content=st.session_state.prompt
#         )

#         stream = client.beta.threads.runs.create(
#             assistant_id=st.session_state.assistant.id,
#             thread_id = st.session_state.thread.id,
#             additional_instructions = additional_instructions,
#             stream = True
#         )
#         if stream:
#            for event in stream:
#               if event.data.object == "thread.message.delta":
#                  for content in event.data.delta.content:
#                     if content.type == 'text':
#                        delta.append(content.text.value)
#                        response = "".join(item for item in delta if item).strip()
#                        container.markdown(response)
#     st.session_state.messages.append({"role": "assistant", "content": response})

# This is for a test


#  everything above this is prety old code but works ###########################

#  this is new code but still older than is on Render ########################

# import openai
# import streamlit as st
# from openai import OpenAI
# import uuid

# client = OpenAI()

# st.set_page_config(page_title="Coach Edge - Virtual Life Coach",layout="wide")

# #Initialize session state variables   

# if "messages" not in st.session_state:
#    st.session_state.messages = []

# if 'prompt' not in st.session_state:
#    st.session_state.prompt = ''

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

# # Initialize OpenAI assistant and thread
# if "assistant" not in st.session_state or "thread" not in st.session_state:
#     openai.api_key = st.secrets["OPENAI_API_KEY"]
#     st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])
#     st.session_state.thread = client.beta.threads.create()

# # Retrieve URL Parameters
# st.session_state.fname = st.query_params.get("fname", "Unknown")
# st.session_state.school = st.query_params.get("school", "Unknown")
# st.session_state.team = st.query_params.get("team", "Unknown")
# st.session_state.role = st.query_params.get("role", "Unknown")
# st.session_state.language = st.query_params.get("language", "Unknown")
# st.session_state.prompt=st.query_params.get("prompt")

# # Extract language from parentheses
# parts = st.session_state.language.split('(')
# if len(parts) > 1:
#     lang = parts[1].split(')')[0]
# else:
#     lang = "Unknown"

# additional_instructions = f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of {st.session_state.team} at the {st.session_state.school}.  Please note that their native language is {st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please respond in their native language regardless of the language they use to ask the question or they provide a response. Pay special attention not to accidentally use words from another language when providing a response."
# # additional_instructions = f"""
# # The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of {st.session_state.team} at the {st.session_state.school}.

# # Please note that the user's native language is {st.session_state.language}.

# # **Instructions:**

# # 1. **Detect the language** of any question/response the user gives.
# # 2. **If the user's question/response is in their native language ({st.session_state.language}):**
# #    - Respond **only** in their native language.
# #    - **Do not** provide a translation or duplicate the answer.
# # 3. **If the user's question/response is in a different language:**
# #    - First, provide your response in the **same language as the user's question/response**.
# #    - Then, provide **your same response translated into the user's native language** ({st.session_state.language}).
# # 4. **Ensure** that you **do not duplicate** the answer unnecessarily.
# # 5. **Follow these instructions precisely** for each response.
# # """

# # Define translations for each supported language
# translations = {
#     "English": {
#         "ask_question": "### **Ask a Question or Select a Topic**",
#         "expander_title": "Topics To Get You Started",
#         "typed_input_placeholder": "What's on your mind?",
#         "button_prompts": [
#             'Mental Health Struggles',
#             'Relationships',
#             'Leadership',
#             'Understanding Certain Verses in the Bible',
#             'Time Management',
#             'Grow My Faith'
#         ],
#         "prompts": [
#             'I am struggling with my mental health. Ask me one question at a time via role play to help me identify my challenges and then develop a practical specific strategy to get better.',
#             'I need help with relationships. Ask me one question at a time via role play to help me identify my relational challenge and then give me practical advice to improve that relationship.',
#             'I want to grow my leadership skills. Ask me one question at a time via role play to help me identify what areas of leadership I need to work on and then help me develop a plan to grow that area.',
#             'I do not understand this verse. Ask me which verse or verses I do not understand and then break down that verse for me to help me understand the context and how that could apply to my life.',
#             'I need help with my time management.  Ask me one question at a time via role play to help me identify where I may be mismanaging my time or getting distracted and give me some tips to get better.',
#             'I want to grow my relationship with God. Ask me one question at a time via role play to help me determine where I need help doing that and then come up with a strategy to implement spiritual disciplines to grow.'
#         ]
#     },
#     "Spanish": {
#         "ask_question": "### **Haz una pregunta o selecciona un tema**",
#         "expander_title": "Temas para empezar",
#         "typed_input_placeholder": "¿Qué tienes en mente?",
#         "button_prompts": [
#             'Luchas con la salud mental',
#             'Relaciones',
#             'Liderazgo',
#             'Comprender ciertos versículos de la Biblia',
#             'Gestión del tiempo',
#             'Crecer en mi fe'
#         ],
#         "prompts": [
#             'Estoy luchando con mi salud mental. Hazme una pregunta a la vez mediante un juego de roles para ayudarme a identificar mis desafíos y luego desarrollar una estrategia práctica y específica para mejorar.',
#             'Necesito ayuda con las relaciones. Hazme una pregunta a la vez mediante un juego de roles para ayudarme a identificar mi desafío relacional y luego dame consejos prácticos para mejorar esa relación.',
#             'Quiero crecer en mis habilidades de liderazgo. Hazme una pregunta a la vez mediante un juego de roles para ayudarme a identificar en qué áreas de liderazgo necesito trabajar y luego ayúdame a desarrollar un plan para crecer en esa área.',
#             'No entiendo este versículo. Pregúntame qué versículo o versículos no entiendo y luego desglosa ese versículo para ayudarme a entender el contexto y cómo podría aplicarse a mi vida.',
#             'Necesito ayuda con la gestión de mi tiempo. Hazme una pregunta a la vez mediante un juego de roles para ayudarme a identificar dónde puedo estar mal gestionando mi tiempo o distrayéndome y dame algunos consejos para mejorar.',
#             'Quiero crecer en mi relación con Dios. Hazme una pregunta a la vez mediante un juego de roles para ayudarme a determinar dónde necesito ayuda para hacer eso y luego elabora una estrategia para implementar disciplinas espirituales para crecer.'
#         ]
#     },
#     "Arabic": {
#         "ask_question": "### **اطرح سؤالاً أو اختر موضوعًا**",
#         "expander_title": "مواضيع لتبدأ بها",
#         "typed_input_placeholder": "ما الذي يدور في ذهنك؟",
#         "button_prompts": [
#             'صراعات الصحة النفسية',
#             'العلاقات',
#             'القيادة',
#             'فهم بعض الآيات في الكتاب المقدس',
#             'إدارة الوقت',
#             'تنمية إيماني'
#         ],
#         "prompts": [
#             'أعاني من مشاكل في صحتي النفسية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدياتي ثم تطوير استراتيجية عملية محددة للتحسن.',
#             'أحتاج إلى مساعدة في العلاقات. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد تحدي علاقتي ثم أعطني نصائح عملية لتحسين تلك العلاقة.',
#             'أريد أن أنمي مهاراتي القيادية. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد مجالات القيادة التي أحتاج للعمل عليها ثم ساعدني في تطوير خطة للنمو في هذا المجال.',
#             'لا أفهم هذه الآية. اسألني أي آية أو آيات لا أفهمها ثم قم بتفسير تلك الآية لمساعدتي على فهم السياق وكيف يمكن أن تنطبق على حياتي.',
#             'أحتاج إلى مساعدة في إدارة وقتي. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد أين قد أكون أساء إدارة وقتي أو مشتتاً ثم أعطني بعض النصائح للتحسن.',
#             'أريد أن أنمو في علاقتي مع الله. اسألني سؤالاً واحداً في كل مرة عبر لعب الأدوار لمساعدتي في تحديد أين أحتاج إلى مساعدة في ذلك ثم ابتكر استراتيجية لتنفيذ التمارين الروحية للنمو.'
#         ]
#     },
#     "Japanese": {
#         "ask_question": "### **質問するかトピックを選んでください**",
#         "expander_title": "始めるためのトピック",
#         "typed_input_placeholder": "何を考えていますか？",
#         "button_prompts": [
#             'メンタルヘルスの悩み',
#             '人間関係',
#             'リーダーシップ',
#             '聖書の特定の節の理解',
#             '時間管理',
#             '信仰を育てる'
#         ],
#         "prompts": [
#             'メンタルヘルスに悩んでいます。ロールプレイを通じて一度に一つの質問をして、私の課題を特定し、改善するための実用的で具体的な戦略を立てるのを手伝ってください。',
#             '人間関係について助けが必要です。ロールプレイを通じて一度に一つの質問をして、私の人間関係の課題を特定し、その関係を改善するための実用的なアドバイスをください。',
#             'リーダーシップスキルを伸ばしたいです。ロールプレイを通じて一度に一つの質問をして、どのリーダーシップ分野で働く必要があるかを特定し、その分野を成長させるための計画を立てるのを手伝ってください。',
#             'この節が理解できません。どの節または節が理解できないかを尋ね、その節を分解して、文脈を理解し、それが私の人生にどのように適用できるかを助けてください。',
#             '時間管理の助けが必要です。ロールプレイを通じて一度に一つの質問をして、時間を誤って管理している場所や気が散っている場所を特定し、改善するためのヒントをください。',
#             '神との関係を深めたいです。ロールプレイを通じて一度に一つの質問をして、それを行うためにどこで助けが必要かを判断し、成長するための霊的な訓練を実施する戦略を考えてください。'
#         ]
#     },
#     "French": {
#         "ask_question": "### **Posez une question ou sélectionnez un sujet**",
#         "expander_title": "Sujets pour vous lancer",
#         "typed_input_placeholder": "Qu'avez-vous en tête ?",
#         "button_prompts": [
#             'Difficultés de santé mentale',
#             'Relations',
#             'Leadership',
#             'Comprendre certains versets de la Bible',
#             'Gestion du temps',
#             'Développer ma foi'
#         ],
#         "prompts": [
#             'Je lutte avec ma santé mentale. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier mes défis puis élaborer une stratégie pratique et spécifique pour aller mieux.',
#             'J\'ai besoin d\'aide avec les relations. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier mon défi relationnel puis donnez-moi des conseils pratiques pour améliorer cette relation.',
#             'Je veux développer mes compétences en leadership. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier les domaines du leadership sur lesquels je dois travailler puis aidez-moi à élaborer un plan pour développer ce domaine.',
#             'Je ne comprends pas ce verset. Demandez-moi quel verset ou quels versets je ne comprends pas puis décomposez ce verset pour m\'aider à comprendre le contexte et comment il pourrait s\'appliquer à ma vie.',
#             'J\'ai besoin d\'aide avec la gestion de mon temps. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à identifier où je pourrais mal gérer mon temps ou être distrait et donnez-moi quelques conseils pour m\'améliorer.',
#             'Je veux développer ma relation avec Dieu. Posez-moi une question à la fois via un jeu de rôle pour m\'aider à déterminer où j\'ai besoin d\'aide pour cela puis élaborer une stratégie pour mettre en œuvre des disciplines spirituelles pour grandir.'
#         ]
#     },
#     "Portuguese": {
#         "ask_question": "### **Faça uma pergunta ou selecione um tópico**",
#         "expander_title": "Tópicos para começar",
#         "typed_input_placeholder": "O que está em sua mente?",
#         "button_prompts": [
#             'Dificuldades de saúde mental',
#             'Relacionamentos',
#             'Liderança',
#             'Compreendendo certos versículos da Bíblia',
#             'Gestão de tempo',
#             'Crescer na minha fé'
#         ],
#         "prompts": [
#             'Estou lutando com minha saúde mental. Faça-me uma pergunta de cada vez através de um role-play para me ajudar a identificar meus desafios e então desenvolver uma estratégia prática e específica para melhorar.',
#             'Preciso de ajuda com relacionamentos. Faça-me uma pergunta de cada vez através de um role-play para me ajudar a identificar meu desafio relacional e então me dê conselhos práticos para melhorar esse relacionamento.',
#             'Quero desenvolver minhas habilidades de liderança. Faça-me uma pergunta de cada vez através de um role-play para me ajudar a identificar em quais áreas de liderança preciso trabalhar e então me ajude a desenvolver um plano para crescer nessa área.',
#             'Não entendo este versículo. Pergunte-me qual versículo ou versículos eu não entendo e então desmonte esse versículo para me ajudar a entender o contexto e como isso poderia se aplicar à minha vida.',
#             'Preciso de ajuda com minha gestão de tempo. Faça-me uma pergunta de cada vez através de um role-play para me ajudar a identificar onde posso estar gerenciando mal meu tempo ou me distraindo e me dê algumas dicas para melhorar.',
#             'Quero crescer em meu relacionamento com Deus. Faça-me uma pergunta de cada vez através de um role-play para me ajudar a determinar onde preciso de ajuda para fazer isso e então criar uma estratégia para implementar disciplinas espirituais para crescer.'
#         ]
#     },
#     "Greek": {
#         "ask_question": "### **Κάντε μια ερώτηση ή επιλέξτε ένα θέμα**",
#         "expander_title": "Θέματα για να ξεκινήσετε",
#         "typed_input_placeholder": "Τι έχετε στο μυαλό σας;",
#         "button_prompts": [
#             'Δυσκολίες ψυχικής υγείας',
#             'Σχέσεις',
#             'Ηγεσία',
#             'Κατανόηση συγκεκριμένων στίχων στη Βίβλο',
#             'Διαχείριση χρόνου',
#             'Ανάπτυξη της πίστης μου'
#         ],
#         "prompts": [
#             'Αντιμετωπίζω προβλήματα με την ψυχική μου υγεία. Κάντε μου μία ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω τις προκλήσεις μου και στη συνέχεια να αναπτύξω μια πρακτική, συγκεκριμένη στρατηγική για να βελτιωθώ.',
#             'Χρειάζομαι βοήθεια με τις σχέσεις. Κάντε μου μία ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω την πρόκλησή μου στη σχέση και στη συνέχεια δώστε μου πρακτικές συμβουλές για να βελτιώσω αυτήν τη σχέση.',
#             'Θέλω να αναπτύξω τις ηγετικές μου δεξιότητες. Κάντε μου μία ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω σε ποιους τομείς ηγεσίας πρέπει να εργαστώ και στη συνέχεια να με βοηθήσετε να αναπτύξω ένα σχέδιο για να αναπτυχθώ σε αυτόν τον τομέα.',
#             'Δεν καταλαβαίνω αυτόν τον στίχο. Ρωτήστε με ποιον ή ποιους στίχους δεν καταλαβαίνω και στη συνέχεια αναλύστε αυτόν τον στίχο για να με βοηθήσετε να κατανοήσω το πλαίσιο και πώς μπορεί να εφαρμοστεί στη ζωή μου.',
#             'Χρειάζομαι βοήθεια με τη διαχείριση του χρόνου μου. Κάντε μου μία ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να εντοπίσω πού μπορεί να διαχειρίζομαι λάθος τον χρόνο μου ή να αποσπώμαι και να μου δώσετε μερικές συμβουλές για να βελτιωθώ.',
#             'Θέλω να αναπτύξω τη σχέση μου με τον Θεό. Κάντε μου μία ερώτηση τη φορά μέσω παιχνιδιού ρόλων για να με βοηθήσετε να προσδιορίσω πού χρειάζομαι βοήθεια για να το κάνω αυτό και στη συνέχεια να καταρτίσετε μια στρατηγική για να εφαρμόσω πνευματικές πρακτικές για να αναπτυχθώ.'
#         ]
#     },
#     "Dutch": {
#         "ask_question": "### **Stel een vraag of selecteer een onderwerp**",
#         "expander_title": "Onderwerpen om mee te beginnen",
#         "typed_input_placeholder": "Wat houdt je bezig?",
#         "button_prompts": [
#             'Mentale gezondheidsproblemen',
#             'Relaties',
#             'Leiderschap',
#             'Begrijpen van bepaalde verzen in de Bijbel',
#             'Tijdmanagement',
#             'Groei in mijn geloof'
#         ],
#         "prompts": [
#             'Ik worstel met mijn mentale gezondheid. Stel me één vraag tegelijk via rollenspel om me te helpen mijn uitdagingen te identificeren en vervolgens een praktische, specifieke strategie te ontwikkelen om beter te worden.',
#             'Ik heb hulp nodig met relaties. Stel me één vraag tegelijk via rollenspel om me te helpen mijn relationele uitdaging te identificeren en geef me vervolgens praktisch advies om die relatie te verbeteren.',
#             'Ik wil mijn leiderschapsvaardigheden ontwikkelen. Stel me één vraag tegelijk via rollenspel om me te helpen identificeren aan welke leiderschapsgebieden ik moet werken en help me vervolgens een plan te ontwikkelen om dat gebied te laten groeien.',
#             'Ik begrijp dit vers niet. Vraag me welk vers of verzen ik niet begrijp en breek dat vers vervolgens voor me af om me te helpen de context te begrijpen en hoe dat op mijn leven van toepassing kan zijn.',
#             'Ik heb hulp nodig met mijn tijdmanagement. Stel me één vraag tegelijk via rollenspel om me te helpen identificeren waar ik mijn tijd misschien verkeerd beheer of afgeleid raak en geef me enkele tips om beter te worden.',
#             'Ik wil groeien in mijn relatie met God. Stel me één vraag tegelijk via rollenspel om me te helpen bepalen waar ik hulp nodig heb om dat te doen en bedenk vervolgens een strategie om spirituele disciplines te implementeren om te groeien.'
#         ]
#     },
#     "Swedish": {
#         "ask_question": "### **Ställ en fråga eller välj ett ämne**",
#         "expander_title": "Ämnen för att komma igång",
#         "typed_input_placeholder": "Vad har du på hjärtat?",
#         "button_prompts": [
#             'Mentala hälsoproblem',
#             'Relationer',
#             'Ledarskap',
#             'Förstå vissa verser i Bibeln',
#             'Tidsplanering',
#             'Växa i min tro'
#         ],
#         "prompts": [
#             'Jag kämpar med min mentala hälsa. Ställ mig en fråga i taget via rollspel för att hjälpa mig identifiera mina utmaningar och sedan utveckla en praktisk, specifik strategi för att bli bättre.',
#             'Jag behöver hjälp med relationer. Ställ mig en fråga i taget via rollspel för att hjälpa mig identifiera min relationsutmaning och sedan ge mig praktiska råd för att förbättra den relationen.',
#             'Jag vill utveckla mina ledarskapsförmågor. Ställ mig en fråga i taget via rollspel för att hjälpa mig identifiera vilka områden inom ledarskap jag behöver arbeta med och sedan hjälpa mig att utveckla en plan för att växa inom det området.',
#             'Jag förstår inte denna vers. Fråga mig vilken vers eller vilka verser jag inte förstår och bryt sedan ner den versen för att hjälpa mig förstå sammanhanget och hur det kan tillämpas på mitt liv.',
#             'Jag behöver hjälp med min tidsplanering. Ställ mig en fråga i taget via rollspel för att hjälpa mig identifiera var jag kanske missköter min tid eller blir distraherad och ge mig några tips för att bli bättre.',
#             'Jag vill växa i min relation med Gud. Ställ mig en fråga i taget via rollspel för att hjälpa mig avgöra var jag behöver hjälp med det och kom sedan på en strategi för att implementera andliga discipliner för att växa.'
#         ]
#     },
#     "Bengali": {
#         "ask_question": "### **একটি প্রশ্ন জিজ্ঞাসা করুন বা একটি বিষয় নির্বাচন করুন**",
#         "expander_title": "আপনার শুরু করার জন্য বিষয়গুলি",
#         "typed_input_placeholder": "আপনার মনে কী আছে?",
#         "button_prompts": [
#             'মানসিক স্বাস্থ্যের সংগ্রাম',
#             'সম্পর্কসমূহ',
#             'নেতৃত্ব',
#             'বাইবেলের কিছু আয়াত বোঝা',
#             'সময় ব্যবস্থাপনা',
#             'আমার বিশ্বাস বৃদ্ধি করুন'
#         ],
#         "prompts": [
#             'আমি আমার মানসিক স্বাস্থ্যের সাথে সংগ্রাম করছি। আমাকে এক সময়ে একটি প্রশ্ন জিজ্ঞাসা করুন রোল প্লের মাধ্যমে যাতে আমি আমার চ্যালেঞ্জগুলি সনাক্ত করতে পারি এবং তারপর উন্নতির জন্য একটি ব্যবহারিক নির্দিষ্ট কৌশল বিকাশ করতে পারি।',
#             'আমি সম্পর্কের বিষয়ে সাহায্য প্রয়োজন। আমাকে এক সময়ে একটি প্রশ্ন জিজ্ঞাসা করুন রোল প্লের মাধ্যমে যাতে আমি আমার সম্পর্কগত চ্যালেঞ্জ সনাক্ত করতে পারি এবং তারপর সেই সম্পর্ক উন্নত করার জন্য আমাকে ব্যবহারিক পরামর্শ দিন।',
#             'আমি আমার নেতৃত্বের দক্ষতা বৃদ্ধি করতে চাই। আমাকে এক সময়ে একটি প্রশ্ন জিজ্ঞাসা করুন রোল প্লের মাধ্যমে যাতে আমি কোন নেতৃত্বের ক্ষেত্রগুলিতে কাজ করা প্রয়োজন তা সনাক্ত করতে পারি এবং তারপর সেই ক্ষেত্রটিকে বৃদ্ধি করতে একটি পরিকল্পনা তৈরি করতে আমাকে সাহায্য করুন।',
#             'আমি এই আয়াতটি বুঝতে পারি না। আমাকে জিজ্ঞাসা করুন কোন আয়াত বা আয়াতগুলি আমি বুঝতে পারি না এবং তারপর সেই আয়াতটি আমার জন্য ভেঙে দিন যাতে আমি প্রসঙ্গটি বুঝতে পারি এবং তা কীভাবে আমার জীবনে প্রয়োগ হতে পারে।',
#             'আমার সময় ব্যবস্থাপনা নিয়ে সাহায্য দরকার। আমাকে এক সময়ে একটি প্রশ্ন জিজ্ঞাসা করুন রোল প্লের মাধ্যমে যাতে আমি সনাক্ত করতে পারি কোথায় আমি আমার সময় ভুলভাবে পরিচালনা করছি বা বিভ্রান্ত হচ্ছি এবং আমাকে কিছু টিপস দিন উন্নতি করতে।',
#             'আমি ঈশ্বরের সাথে আমার সম্পর্ক বৃদ্ধি করতে চাই। আমাকে এক সময়ে একটি প্রশ্ন জিজ্ঞাসা করুন রোল প্লের মাধ্যমে যাতে আমি নির্ধারণ করতে পারি কোথায় আমাকে সাহায্য দরকার এবং তারপর আত্মিক চর্চা বাস্তবায়নের জন্য একটি কৌশল তৈরি করুন।'
#         ]
#     },
#     "Hindi": {
#         "ask_question": "### **एक प्रश्न पूछें या एक विषय चुनें**",
#         "expander_title": "शुरू करने के लिए विषय",
#         "typed_input_placeholder": "आपके मन में क्या है?",
#         "button_prompts": [
#             'मानसिक स्वास्थ्य संघर्ष',
#             'संबंध',
#             'नेतृत्व',
#             'बाइबिल के कुछ पदों को समझना',
#             'समय प्रबंधन',
#             'अपने विश्वास को बढ़ाएं'
#         ],
#         "prompts": [
#             'मैं अपने मानसिक स्वास्थ्य के साथ संघर्ष कर रहा हूँ। मुझे एक बार में एक प्रश्न पूछें रोल प्ले के माध्यम से ताकि मैं अपनी चुनौतियों की पहचान कर सकूं और फिर बेहतर होने के लिए एक व्यावहारिक विशेष रणनीति विकसित कर सकूं।',
#             'मुझे संबंधों में मदद की आवश्यकता है। मुझे एक बार में एक प्रश्न पूछें रोल प्ले के माध्यम से ताकि मैं अपने संबंधी चुनौती की पहचान कर सकूं और फिर उस संबंध को सुधारने के लिए मुझे व्यावहारिक सलाह दें।',
#             'मैं अपनी नेतृत्व कौशल को बढ़ाना चाहता हूँ। मुझे एक बार में एक प्रश्न पूछें रोल प्ले के माध्यम से ताकि मैं नेतृत्व के किन क्षेत्रों पर काम करने की आवश्यकता है, इसे पहचान सकूं और फिर उस क्षेत्र को बढ़ाने के लिए मुझे एक योजना विकसित करने में मदद करें।',
#             'मैं इस पद को समझ नहीं पा रहा हूँ। मुझसे पूछें कि कौन सा पद या पद मैं नहीं समझ पा रहा हूँ और फिर उस पद को मेरे लिए तोड़कर समझाएं ताकि मैं संदर्भ को समझ सकूं और यह मेरे जीवन में कैसे लागू हो सकता है।',
#             'मुझे अपने समय प्रबंधन में मदद की आवश्यकता है। मुझे एक बार में एक प्रश्न पूछें रोल प्ले के माध्यम से ताकि मैं पहचान सकूं कि मैं कहाँ अपने समय का गलत प्रबंधन कर रहा हूँ या विचलित हो रहा हूँ और मुझे बेहतर होने के लिए कुछ टिप्स दें।',
#             'मैं ईश्वर के साथ अपने संबंध को बढ़ाना चाहता हूँ। मुझे एक बार में एक प्रश्न पूछें रोल प्ले के माध्यम से ताकि मैं निर्धारित कर सकूं कि मुझे कहाँ मदद की आवश्यकता है और फिर बढ़ने के लिए आध्यात्मिक अनुशासन लागू करने की एक रणनीति लेकर आएं।'
#         ]
#     },
#     "Ukrainian": {
#         "ask_question": "### **Поставте запитання або виберіть тему**",
#         "expander_title": "Теми для початку",
#         "typed_input_placeholder": "Що у вас на думці?",
#         "button_prompts": [
#             'Проблеми з психічним здоров’ям',
#             'Відносини',
#             'Лідерство',
#             'Розуміння певних віршів у Біблії',
#             'Управління часом',
#             'Зростити свою віру'
#         ],
#         "prompts": [
#             'Я маю труднощі з психічним здоров’ям. Задавайте мені по одному запитанню через рольову гру, щоб допомогти мені визначити мої виклики, а потім розробити практичну конкретну стратегію для покращення.',
#             'Мені потрібна допомога з відносинами. Задавайте мені по одному запитанню через рольову гру, щоб допомогти мені визначити мою проблему у відносинах, а потім дайте мені практичні поради для покращення цих відносин.',
#             'Я хочу розвивати свої лідерські навички. Задавайте мені по одному запитанню через рольову гру, щоб допомогти мені визначити, над якими аспектами лідерства мені потрібно працювати, а потім допоможіть мені розробити план для розвитку цієї області.',
#             'Я не розумію цей вірш. Запитайте мене, який саме вірш або вірші я не розумію, а потім розберіть цей вірш для мене, щоб допомогти мені зрозуміти контекст і як це може застосовуватися до мого життя.',
#             'Мені потрібна допомога з управлінням часом. Задавайте мені по одному запитанню через рольову гру, щоб допомогти мені визначити, де я можу неправильно керувати своїм часом або відволікатися, і дайте мені кілька порад для покращення.',
#             'Я хочу зміцнити свої відносини з Богом. Задавайте мені по одному запитанню через рольову гру, щоб допомогти мені визначити, де мені потрібна допомога в цьому, а потім розробіть стратегію впровадження духовних дисциплін для зростання.'
#         ]
#     },
#     "Indonesian": {
#         "ask_question": "### **Ajukan Pertanyaan atau Pilih Topik**",
#         "expander_title": "Topik untuk Memulai Anda",
#         "typed_input_placeholder": "Apa yang ada di pikiran Anda?",
#         "button_prompts": [
#             'Masalah Kesehatan Mental',
#             'Hubungan',
#             'Kepemimpinan',
#             'Memahami Ayat-Ayat Tertentu dalam Alkitab',
#             'Manajemen Waktu',
#             'Kembangkan Iman Saya'
#         ],
#         "prompts": [
#             'Saya sedang berjuang dengan kesehatan mental saya. Tanyakan kepada saya satu pertanyaan pada satu waktu melalui role play untuk membantu saya mengidentifikasi tantangan saya dan kemudian mengembangkan strategi spesifik yang praktis untuk menjadi lebih baik.',
#             'Saya membutuhkan bantuan dengan hubungan. Tanyakan kepada saya satu pertanyaan pada satu waktu melalui role play untuk membantu saya mengidentifikasi tantangan relasional saya dan kemudian berikan saya saran praktis untuk memperbaiki hubungan tersebut.',
#             'Saya ingin mengembangkan keterampilan kepemimpinan saya. Tanyakan kepada saya satu pertanyaan pada satu waktu melalui role play untuk membantu saya mengidentifikasi area kepemimpinan apa yang perlu saya kerjakan dan kemudian bantu saya mengembangkan rencana untuk mengembangkan area tersebut.',
#             'Saya tidak memahami ayat ini. Tanyakan kepada saya ayat atau ayat-ayat mana yang tidak saya mengerti dan kemudian jelaskan ayat tersebut untuk membantu saya memahami konteksnya dan bagaimana itu dapat diterapkan dalam hidup saya.',
#             'Saya membutuhkan bantuan dengan manajemen waktu saya. Tanyakan kepada saya satu pertanyaan pada satu waktu melalui role play untuk membantu saya mengidentifikasi di mana saya mungkin salah mengatur waktu saya atau teralihkan dan berikan saya beberapa tips untuk menjadi lebih baik.',
#             'Saya ingin mengembangkan hubungan saya dengan Tuhan. Tanyakan kepada saya satu pertanyaan pada satu waktu melalui role play untuk membantu saya menentukan di mana saya perlu bantuan melakukannya dan kemudian buat strategi untuk menerapkan disiplin spiritual untuk bertumbuh.'
#         ]
#     }
#     # Add more languages if needed
# }

# # Get the translations for the selected language, default to English
# lang_translations = translations.get(lang, translations["English"])

# st.markdown(lang_translations["ask_question"])

# with st.expander(lang_translations["expander_title"]):
#     for idx, button_text in enumerate(lang_translations["button_prompts"]):
#         if st.button(button_text):
#             st.session_state.prompt = lang_translations["prompts"][idx]

# typed_input = st.chat_input(lang_translations["typed_input_placeholder"])

# # Check if there is typed input
# if typed_input:
#     st.session_state.prompt = typed_input

# for message in st.session_state.messages:
#     if message["role"] == "user":
#        with st.chat_message('user', avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#           st.markdown(message["content"])
#     else:
#        with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#           st.markdown(message["content"])

# if st.session_state.prompt:
#     delta = [] 
#     response = ""
#     st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
#     with st.chat_message('user',avatar='https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png'):
#         st.markdown(st.session_state.prompt)
#     with st.chat_message('assistant', avatar='https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png'):
#         container = st.empty()
#         st.session_state.thread_messages= client.beta.threads.messages.create(
#               st.session_state.thread.id, role="user",content=st.session_state.prompt
#         )

#         stream = client.beta.threads.runs.create(
#             assistant_id=st.session_state.assistant.id,
#             thread_id = st.session_state.thread.id,
#             additional_instructions = additional_instructions,
#             stream = True
#         )
#         if stream:
#            for event in stream:
#               if event.data.object == "thread.message.delta":
#                  for content in event.data.delta.content:
#                     if content.type == 'text':
#                        delta.append(content.text.value)
#                        response = "".join(item for item in delta if item).strip()
#                        container.markdown(response)
#     st.session_state.messages.append({"role": "assistant", "content": response}) 
                                                           
#                                       
#  THIS IS VERY NEW CODE TRYING TO STORE THE THREAD ID AND KEEP A PERSISTENT CONVERSATION GOING

import openai
import requests
import streamlit as st
from openai import OpenAI
from translations_spiritual import translations

# Constants for avatar URLs
USER_AVATAR = "https://static.wixstatic.com/media/b748e0_2cdbf70f0a8e477ba01940f6f1d19ab9~mv2.png"
ASSISTANT_AVATAR = "https://static.wixstatic.com/media/b748e0_fb82989e216f4e15b81dc26e8c773c20~mv2.png"

# Initialize OpenAI client
client = OpenAI()

# Set page configuration
st.set_page_config(page_title="Coach Edge - Virtual Life Coach", layout="wide")

# Initialize session state with defaults.
defaults = {
    "messages": [],
    "prompt": "",             # Not used for storing submitted text.
    "submitted_prompt": "",   # This will hold the user's submitted prompt.
    "fname": "",
    "school": "",
    "team": "",
    "role": "",
    "language": "",
    "processing": False,      # When True, chat_input is disabled.
    "thread": None,           # Will store the OpenAI conversation thread.
    "assistant": None,        # The OpenAI assistant.
}
for key, default in defaults.items():
    st.session_state.setdefault(key, default)

# -----------------------------
# Adalo Integration Functions
# -----------------------------
def update_adalo_user_thread(email, thread_id):
    """
    Look up the Adalo user record by email and update its thread_id.
    """
    # Retrieve secrets from st.secrets
    ADALO_APP_ID = st.secrets["APP_ID"]
    ADALO_COLLECTION_ID = st.secrets["ADALO_COLLECTION_ID"]
    ADALO_API_KEY = st.secrets["ADALO_API_KEY"]
    headers = {
        "Authorization": f"Bearer {ADALO_API_KEY}",
        "Content-Type": "application/json"
    }
    # URL to get user records filtered by email.
    get_url = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}?filterKey=Email&filterValue={email}"
    response = requests.get(get_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("records") and len(data["records"]) > 0:
            # Assume the first record is the correct one.
            record = data["records"][0]
            element_id = record.get("id")  # Adjust this if your field name is different.
            update_url = f"https://api.adalo.com/v0/apps/{ADALO_APP_ID}/collections/{ADALO_COLLECTION_ID}/{element_id}"
            # st.write("DEBUG:", update_url)
            # st.write("DEBUG:", headers)
            payload = {"thread_id": thread_id}
            update_response = requests.put(update_url, json=payload, headers=headers)
            if update_response.status_code == 200:
                st.write("DEBUG: Successfully updated Adalo user record with thread_id.")
            else:
                st.write("DEBUG: Failed to update Adalo record:", update_response.text)
        else:
            st.write("DEBUG: No Adalo record found for email:", email)
    else:
        st.write("DEBUG: Failed to retrieve Adalo records:", response.text)

# -----------------------------
# OpenAI Thread Handling
# -----------------------------
def initialize_openai_assistant():
    """Initialize the OpenAI assistant if not already set."""
    if not st.session_state.assistant:
        # Use secrets for API keys.
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        st.session_state.assistant = openai.beta.assistants.retrieve(st.secrets["OPENAI_ASSISTANT"])

def handle_thread():
    """
    Handle the OpenAI thread. If a thread_id is provided via URL parameters, retrieve that thread.
    Otherwise, create a new thread, update the Adalo user record, and use the new thread.
    """
    params = st.query_params
    if "thread_id" in params and params["thread_id"]:
        thread_id = params["thread_id"]
        st.session_state.thread = openai.beta.threads.retrieve(thread_id)
        st.write("DEBUG: Retrieved thread with id:", thread_id)
    else:
        # Create a new thread.
        new_thread = client.beta.threads.create()
        st.session_state.thread = new_thread
        st.write("DEBUG: Created new thread with id:", new_thread.id)
        # Update the Adalo user record with the new thread id.
        email = params.get("email", "")
        if email:
            update_adalo_user_thread(email, new_thread.id)
        else:
            st.write("DEBUG: No email provided; cannot update Adalo record.")

def get_url_parameters():
    """Retrieve URL parameters and update session state."""
    params = st.query_params
    st.session_state.fname = params.get("fname", "Unknown")
    st.session_state.school = params.get("school", "Unknown")
    st.session_state.team = params.get("team", "Unknown")
    st.session_state.role = params.get("role", "Unknown")
    st.session_state.language = params.get("language", "Unknown")
    # Also capture an optional prompt.
    st.session_state.prompt = params.get("prompt", "")

def extract_language(lang_str):
    """Extract language from a string formatted as '... (Language)'."""
    parts = lang_str.split('(')
    if len(parts) > 1:
        return parts[1].split(')')[0]
    return "Unknown"

# -----------------------------
# Chat and Message Functions
# -----------------------------
def display_chat_messages():
    """Display all chat messages stored in session state."""
    for message in st.session_state.messages:
        role = message["role"]
        avatar = USER_AVATAR if role == "user" else ASSISTANT_AVATAR
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

def process_user_prompt(prompt, additional_instructions):
    """Send the user prompt to the assistant and stream the response."""
    # Append and display the user's message.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Send the user's prompt to the thread.
    st.session_state.thread_messages = client.beta.threads.messages.create(
        st.session_state.thread.id, role="user", content=prompt
    )

    response_chunks = []
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        container = st.empty()
        stream = client.beta.threads.runs.create(
            assistant_id=st.session_state.assistant.id,
            thread_id=st.session_state.thread.id,
            additional_instructions=additional_instructions,
            stream=True
        )
        if stream:
            for event in stream:
                if event.data.object == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == "text":
                            response_chunks.append(content.text.value)
                            current_response = "".join(response_chunks).strip()
                            container.markdown(current_response)

    final_response = "".join(response_chunks).strip()
    st.session_state.messages.append({"role": "assistant", "content": final_response})
    
    # Clear the submitted prompt and re-enable chat input.
    st.session_state.submitted_prompt = ""
    st.session_state.processing = False
    st.rerun()  # Force a UI refresh so the chat input is re-enabled.

def chat_submit_callback():
    """Callback invoked on chat input submission.
    It copies the chat input value into 'submitted_prompt' and disables further input.
    """
    st.session_state.submitted_prompt = st.session_state.user_input
    st.session_state.processing = True

# -----------------------------
# Main Execution Flow
# -----------------------------
initialize_openai_assistant()
get_url_parameters()
handle_thread()  # Use URL thread_id if available; otherwise, create a new one and update Adalo.

# Get language translations.
lang = extract_language(st.session_state.language)
lang_translations = translations.get(lang, translations["English"])

st.markdown(lang_translations["ask_question"])

# Display preset prompt buttons inside an expander.
with st.expander(lang_translations["expander_title"]):
    for idx, button_text in enumerate(lang_translations["button_prompts"]):
        if st.button(button_text):
            st.session_state.submitted_prompt = lang_translations["prompts"][idx]
            st.session_state.processing = True

# Display existing chat messages.
display_chat_messages()

# Render the chat input widget.
if st.session_state.processing:
    st.chat_input(lang_translations["typed_input_placeholder"], disabled=True)
else:
    _ = st.chat_input(
        lang_translations["typed_input_placeholder"],
        key="user_input",
        on_submit=chat_submit_callback
    )

# Process the prompt if set.
if st.session_state.submitted_prompt and st.session_state.processing:
    additional_instructions = (
        f"The user's name is {st.session_state.fname}. They are a {st.session_state.role} in the sport of "
        f"{st.session_state.team} at the {st.session_state.school}. Please note that their native language is "
        f"{st.session_state.language}. THIS IS IMPORTANT ... When I ask a question or provide a response, please "
        f"respond in their native language regardless of the language they use to ask the question or provide a response. "
        "Pay special attention not to accidentally use words from another language when providing a response."
    )
    process_user_prompt(st.session_state.submitted_prompt, additional_instructions)     