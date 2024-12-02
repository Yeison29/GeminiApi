import google.generativeai as genai
from app.config.config import Config
from app.utils.markdown import to_markdown
from app.schema.prompt import RequestBodyPrompt
from app.utils.image import upload_image
import sqlite3


class Gemini:
    def __init__(self):
        self.config = Config()
        self.gemini = genai.configure(api_key=self.config.gemini_api_key)
        self.model_text = genai.GenerativeModel('gemini-pro')
        self.model_img = genai.GenerativeModel('gemini-1.5-flash')

    async def gemini_response(self, request: RequestBodyPrompt):
        if request.img is None:
            response = self.model_text.generate_content(request.prompt)
            return to_markdown(response.text)
        else:
            response = self.model_img.generate_content([request.prompt, upload_image(request.img)], stream=True)
            response.resolve()
            return to_markdown(response.text)

    async def gemini_chat(self, request: str):
        history = await self.get_history_from_db()
        print(history)
        chat = self.model_text.start_chat(history=history)

        response = await chat.send_message_async(request)
        response = to_markdown(response.text)
        await self.save_message_to_db(request, response)
        return response

    async def gemini_clear_chat(self):
        result = ''
        conn = sqlite3.connect('chat_history.db')
        try:
            cursor = conn.cursor()
            cursor.execute('''
                                DELETE FROM chat_history WHERE TRUE
                            ''')
            conn.commit()
            result = "Se restablecio el chat"
        except Exception as e:
            result = e
        finally:
            conn.rollback()
            conn.close()
            return result


    async def save_message_to_db(self, menssage, response):
        result = ''
        conn = sqlite3.connect('chat_history.db')
        try:
            cursor = conn.cursor()
            sql, params = self.insert_message_to_db('user', menssage)
            cursor.execute(sql, params)
            sql, params = self.insert_message_to_db('model', response)
            cursor.execute(sql, params)
            conn.commit()
        except Exception as e:
            result = e
        finally:
            conn.rollback()
            conn.close()
            return result

    @staticmethod
    def insert_message_to_db(role, text)->tuple:
        return ('''
            INSERT INTO chat_history (role, text)
            VALUES (?, ?)''', (role, text))

    async def get_history_from_db(self):
        conn = sqlite3.connect('chat_history.db')
        result = ''
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role, text, timestamp
                FROM chat_history
                ORDER BY id ASC
            ''', )

            data = cursor.fetchall()

            history = []
            for row in data:
                history.append({
                    'parts': {row[1]},
                    "role": row[0]
                })
            result = history
        except Exception as e:
            result = e

        finally:
            conn.close()
            return result
