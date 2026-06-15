"""
Groq AI Client with Token Efficiency and Simple Queue System
Menggunakan model gratis dengan optimasi token
"""
import os
import time
import json
import logging
from datetime import datetime, timedelta
from collections import deque
from threading import Lock
import requests

logger = logging.getLogger(__name__)


class SimpleQueue:
    """Simple FIFO queue dengan rate limiting sederhana"""
    def __init__(self, max_requests_per_minute=10):
        self.queue = deque()
        self.lock = Lock()
        self.max_requests = max_requests_per_minute
        self.request_times = deque()
    
    def can_process(self):
        """Check apakah bisa process request (rate limiting)"""
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)
        
        with self.lock:
            # Hapus request yang sudah > 1 menit
            while self.request_times and self.request_times[0] < cutoff:
                self.request_times.popleft()
            
            return len(self.request_times) < self.max_requests
    
    def add_request(self):
        """Track request baru"""
        with self.lock:
            self.request_times.append(datetime.now())


class GroqClient:
    """
    Client untuk Groq AI API
    - Token efficient: gunakan model kecil, batasi max_tokens
    - Simple queue: rate limiting otomatis
    - Error handling yang robust
    """
    
    # Model gratis Groq yang efisien
    MODELS = {
        'fast': 'llama-3.1-8b-instant',  # Paling cepat & hemat
        'balanced': 'llama-3.1-70b-versatile',  # Balance speed & quality
        'quality': 'llama-3.2-90b-text-preview',  # Quality terbaik
    }
    
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY tidak ditemukan di environment variable")
        
        # Simple queue untuk rate limiting (10 requests per menit untuk free tier)
        self.queue = SimpleQueue(max_requests_per_minute=10)
        
        # Default settings untuk efisiensi token
        self.default_model = self.MODELS['fast']  # Gunakan model paling efisien
        self.max_tokens = 300  # Batasi response untuk hemat token
        self.temperature = 0.7
    
    def _wait_if_needed(self):
        """Wait jika sudah mencapai rate limit"""
        retry_count = 0
        while not self.queue.can_process():
            if retry_count == 0:
                logger.info("Rate limit reached, waiting...")
            time.sleep(2)  # Wait 2 detik
            retry_count += 1
            if retry_count > 30:  # Max 1 menit waiting
                raise Exception("Queue timeout: terlalu banyak request")
    
    def chat_completion(self, messages, model=None, max_tokens=None, 
                       temperature=None, system_prompt=None):
        """
        Kirim chat completion request ke Groq
        
        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            model: Model name (default: llama-3.1-8b-instant)
            max_tokens: Max tokens untuk response (default: 300)
            temperature: Creativity level 0-1 (default: 0.7)
            system_prompt: System prompt untuk context (opsional)
        
        Returns:
            dict: Response dari Groq API
        """
        # Wait jika perlu (rate limiting)
        self._wait_if_needed()
        
        # Prepare messages
        final_messages = []
        if system_prompt:
            final_messages.append({
                "role": "system",
                "content": system_prompt
            })
        final_messages.extend(messages)
        
        # Prepare request
        payload = {
            "model": model or self.default_model,
            "messages": final_messages,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Track request untuk queue
            self.queue.add_request()
            
            # Send request
            logger.info(f"Sending request to Groq API (model: {payload['model']})")
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Log usage untuk monitoring
            if 'usage' in result:
                usage = result['usage']
                logger.info(
                    f"Groq API success - Tokens: {usage.get('total_tokens', 0)} "
                    f"(prompt: {usage.get('prompt_tokens', 0)}, "
                    f"completion: {usage.get('completion_tokens', 0)})"
                )
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Groq API error: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def simple_ask(self, question, context=None, model_preference='fast'):
        """
        Wrapper sederhana untuk tanya jawab
        
        Args:
            question: Pertanyaan user
            context: Context tambahan (opsional)
            model_preference: 'fast', 'balanced', atau 'quality'
        
        Returns:
            str: Jawaban dari AI
        """
        system_prompt = "Kamu adalah asisten inventory management yang membantu dalam bahasa Indonesia."
        
        if context:
            system_prompt += f"\n\nContext: {context}"
        
        messages = [
            {"role": "user", "content": question}
        ]
        
        model = self.MODELS.get(model_preference, self.MODELS['fast'])
        
        try:
            response = self.chat_completion(
                messages=messages,
                model=model,
                system_prompt=system_prompt
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Error in simple_ask: {str(e)}")
            return f"Maaf, terjadi kesalahan: {str(e)}"
    
    def get_inventory_insights(self, inventory_data, question):
        """
        Dapatkan insights dari data inventory menggunakan AI
        
        Args:
            inventory_data: Dict atau list data inventory
            question: Pertanyaan tentang inventory
        
        Returns:
            str: Insights dari AI
        """
        # Batasi data untuk hemat token
        data_str = json.dumps(inventory_data, indent=2)
        if len(data_str) > 2000:  # Batasi context size
            data_str = data_str[:2000] + "... (data dipotong untuk efisiensi)"
        
        context = f"Data Inventory:\n{data_str}"
        
        return self.simple_ask(question, context=context, model_preference='balanced')
