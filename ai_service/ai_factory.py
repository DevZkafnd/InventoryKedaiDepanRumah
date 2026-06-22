"""
AI Factory - Dynamic AI Provider Selection
Support multiple AI providers: Groq, Gemini, etc.
"""
import os
import logging

logger = logging.getLogger(__name__)


class AIFactory:
    """
    Factory untuk membuat AI client berdasarkan provider yang dipilih
    """
    
    @staticmethod
    def get_client():
        """
        Dapatkan AI client berdasarkan environment variable AI_PROVIDER
        
        Returns:
            AI Client instance (GroqClient atau GeminiClient)
        
        Raises:
            ValueError: Jika provider tidak valid atau API key tidak ada
        """
        provider = os.getenv('AI_PROVIDER', 'groq').lower()
        
        if provider == 'groq':
            from .groq_client import GroqClient
            logger.info("Using Groq AI Provider")
            return GroqClient()
        
        elif provider == 'gemini':
            from .gemini_client import GeminiClient
            logger.info("Using Google Gemini AI Provider")
            return GeminiClient()
        
        else:
            raise ValueError(
                f"Unknown AI provider: {provider}. "
                f"Valid options: 'groq', 'gemini'"
            )
    
    @staticmethod
    def get_provider_info():
        """
        Dapatkan informasi provider yang sedang digunakan
        
        Returns:
            dict: Provider information
        """
        provider = os.getenv('AI_PROVIDER', 'groq').lower()
        
        providers_info = {
            'groq': {
                'name': 'Groq',
                'model': 'Llama 3.1-8B Instant',
                'speed': 'Very Fast',
                'description': 'Lightning fast inference with Llama models',
                'free_tier': True,
                'rate_limit': '10 req/min'
            },
            'gemini': {
                'name': 'Google Gemini',
                'model': 'Gemini 1.5 Flash',
                'speed': 'Fast',
                'description': 'Google\'s latest multimodal AI model',
                'free_tier': True,
                'rate_limit': '15 req/min'
            }
        }
        
        info = providers_info.get(provider, {})
        info['current_provider'] = provider
        
        return info
