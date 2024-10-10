from openai import OpenAI

from src.main.utils.commons import LLMUtils, LLMModels


class AssistantBuilder:
    def __init__(self, model_title: str, temperature: float = 0, assistant_id=LLMUtils.assistant_id,
                 model_name=LLMModels.gpt_4o_mini):
        self.model_title = model_title
        self._temperature = temperature if 0 <= temperature <= 1 else 0
        if not assistant_id:
            raise ValueError("Assistant ID not provided")
        self._assistant_id = assistant_id
        self._model_name = model_name
        self.client = OpenAI()

    def build(self):
        return self.client.beta.assistants.retrieve(self._assistant_id)
