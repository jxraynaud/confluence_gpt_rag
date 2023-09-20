import yaml
import os
from dotenv import load_dotenv

# langchain imports
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# source imports
from .load_all_faiss import load_all_faiss

class Chatbot:

    def __init__(self):
        load_dotenv()
        self.db = self.get_db()
        # Load configuration from YAML
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, '..', 'config.yaml')

        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        self.model = config['chat_model']['model']
        self.temperature = config['chat_model']['temperature']
        self.conversation_chain = self.get_conversation_chain()

    def get_conversation_chain(self):
        llm = ChatOpenAI(model=self.model, temperature=self.temperature)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(llm = llm, retriever = self.db.as_retriever(), memory=memory)
        return conversation_chain

    def get_db(self):
        db = load_all_faiss()
        return db

    def handle_user_input(self, user_input):
        print('In ChatBot.handle_user_input, received question: {question}'.format(question=user_input))
        results = self.conversation_chain({"question": user_input})
        last_response = results['chat_history'].pop()
        print(last_response)
        return {
            'question': user_input,
            'response': last_response.content,
        }
