import os
import logging
from typing import Dict, List, Optional

from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from ..models.token import Token

class QuestionGenerationAgent:
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the Question Generation Agent with OpenAI configuration.

        :param openai_api_key: Optional API key for OpenAI. If not provided, uses environment variable.
        """
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.llm = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            model_name='gpt-4o',
            temperature=0.3
        )
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def generate_verification_questions(self, token: Token, context: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Generate verification questions for a specific token.

        :param token: Token model instance
        :param context: Additional context about the token from web extraction
        :return: List of generated verification questions
        """
        question_generation_prompt = PromptTemplate(
            input_variables=['token_name', 'token_symbol', 'context'],
            template="""
            Generate 3-5 concise, binary (yes/no) verification questions about the token: {token_name} ({token_symbol})

            Context: {context}

            Guidelines for questions:
            1. Focus on verifiable facts
            2. Avoid overly complex or technical language
            3. Ensure questions can be answered quickly
            4. Cover different aspects of token authenticity

            Example output format:
            1. Is [token_name] a native token of World Chain?
            2. Does the official website match the token's description?

            Generated Questions:
            """
        )

        questions_str = self.llm.predict(
            question_generation_prompt.format(
                token_name=token.name,
                token_symbol=token.symbol,
                context=str(context)
            )
        )

        # Parse the generated questions into a structured format
        questions = [
            {
                'token_id': token.id,
                'question_text': q.strip(),
                'type': 'binary',
                'difficulty': 'easy'
            }
            for q in questions_str.split('\n') if q.strip()
        ]

        return questions

    def distribute_questions(self, questions: List[Dict[str, str]]):
        """
        Distribute generated questions to the messaging system (Kafka).

        :param questions: List of generated verification questions
        """
        try:
            # Placeholder for Kafka message distribution
            # In a real implementation, this would publish to a Kafka topic
            for question in questions:
                self.logger.info(f"Generated Question: {question['question_text']}")
        except Exception as e:
            self.logger.error(f"Question distribution error: {e}")

    def process_token_questions(self, token: Token, context: Dict[str, str]):
        """
        Full workflow for generating and distributing verification questions.

        :param token: Token model instance
        :param context: Additional context about the token
        """
        questions = self.generate_verification_questions(token, context)
        self.distribute_questions(questions)
        return questions