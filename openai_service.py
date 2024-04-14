import json

from openai import OpenAI
import os, dotenv


class OpenAiService:
    def __init__(self):
        dotenv.load_dotenv()
        self.OPENAI_KEY = os.getenv('OPENAI_KEY')
        self.OPENAI_ORG = os.getenv('OPENAI_ORG')
        self.TEMPERATURE = float(os.getenv('TEMPERATURE'))
        self.MAX_TOKENS = float(os.getenv('MAX_TOKENS'))
        self.TOP_P = float(os.getenv('TOP_P'))
        self.FREQUENCY_PENALTY = float(os.getenv('FREQUENCY_PENALTY'))
        self.PRESENCE_PENALTY = float(os.getenv('PRESENCE_PENALTY'))
        self.SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT')
        self.OPENAI_MODEL = os.getenv('OPENAI_MODEL')
        self.open_ai_client = OpenAI(api_key=self.OPENAI_KEY)

    def create_embedding(self, id, text):
        response = self.open_ai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return {
            "id": f"{id}",  # Metadata field for original article ID
            "values": response.data[0].embedding
        }

    def create_summary(self, text):
        response = self.open_ai_client.chat.completions.create(
            model=self.OPENAI_MODEL,
            response_format={"type": "json_object"},
            temperature=self.TEMPERATURE,
            top_p=self.TOP_P,
            messages=[
                {"role": "system",
                 "content": self.SYSTEM_PROMPT},
                {"role": "user",
                 "content": text}]
        )
        response_text = json.loads(response.choices[0].message.content)
        cost = json.loads(response.usage.json())
        return {'articol': response_text.get('Articol') if 'Articol' in response_text else None,
                'antet': response_text.get('Antet') if 'Antet' in response_text else None,
                'titlu': response_text.get('Titlu Obiectiv') if 'Titlu Obiectiv' in response_text else None,
                'price': (cost.get('prompt_tokens') * 1.5 + cost.get('completion_tokens') * 2) / 1000000,
                'model': self.OPENAI_MODEL
                }

    def create_category(self, article):
        response = self.open_ai_client.chat.completions.create(
            model=self.OPENAI_MODEL,
            response_format={"type": "json_object"},
            temperature=0,
            top_p=self.TOP_P,
            messages=[
                {"role": "system",
                 "content": "Aloca articolul la acea categorie care i se potriveste cel mai bine ['POLITICA',''ECONOMIE','EXTERN','SPORT', 'MONDEN']. Raspunsul sa fie de tip JSON : {'Categorie':}"
                 },
                {"role": "user",
                 "content": article.content}]
        )
        response_text = json.loads(response.choices[0].message.content)
        categorie = response_text.get('Categorie') if response_text.get('Categorie') else None
        if not categorie:
            categorie = response_text.get('CATEGORIE') if response_text.get('CATEGORIE') else "ACTUALITATE"
        print(f"{article.id},{categorie}")
        return categorie


