"""
Google Gemini AI Client with Token Efficiency and Simple Queue System
Support for Gemini 1.5 Flash & Pro models
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
    def __init__(self, max_requests_per_minute=15):
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


class GeminiClient:
    """
    Client untuk Google Gemini API
    - Token efficient: gunakan model flash untuk speed
    - Simple queue: rate limiting otomatis
    - Error handling yang robust
    """
    
    # Model Gemini yang tersedia (gratis) - Updated 2026
    MODELS = {
        'fast': 'gemini-2.5-flash',           # Recommended: Balance speed & quality
        'balanced': 'gemini-2.5-flash',       # Same as fast
        'quality': 'gemini-2.5-pro',          # Best quality
        'fastest': 'gemini-2.5-flash-lite',   # Highest volume, lowest latency
    }
    
    API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variable")
        
        # Detect API key type and adjust endpoint if needed
        if self.api_key.startswith('AQ.'):
            # This is a Cloud API key, might need different endpoint or v1 instead of v1beta
            logger.info("Detected Cloud API key format (AQ.*)")
        
        # Simple queue untuk rate limiting (15 requests per menit untuk free tier)
        self.queue = SimpleQueue(max_requests_per_minute=15)
        
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
        Kirim chat completion request ke Gemini
        
        Args:
            messages: List of message dicts [{"role": "user", "content": "..."}]
            model: Model name (default: gemini-1.5-flash)
            max_tokens: Max tokens untuk response (default: 300)
            temperature: Creativity level 0-2 (default: 0.7)
            system_prompt: System prompt untuk context (opsional)
        
        Returns:
            dict: Response dari Gemini API
        """
        # Wait jika perlu (rate limiting)
        self._wait_if_needed()
        
        # Prepare messages - Gemini format
        contents = []
        
        # For v1 API (Cloud keys), add system prompt as first user message
        # For v1beta, use systemInstruction
        use_v1_api = self.api_key.startswith('AQ.')
        
        # Convert messages to Gemini format
        if system_prompt and use_v1_api:
            # For v1: prepend system prompt to first user message
            first_user_msg = None
            for i, msg in enumerate(messages):
                if msg["role"] == "user":
                    first_user_msg = i
                    break
            
            if first_user_msg is not None:
                messages[first_user_msg]["content"] = f"{system_prompt}\n\n{messages[first_user_msg]['content']}"
        
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        # Prepare request
        model_name = model or self.default_model
        
        # Try different API versions and endpoints based on key type
        use_v1_api = self.api_key.startswith('AQ.')
        if use_v1_api:
            # Use v1 stable for Cloud API keys
            url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={self.api_key}"
        else:
            # Use v1beta for standard API keys (AIzaSy...)
            url = f"{self.API_BASE_URL}/{model_name}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature if temperature is not None else self.temperature,
                "maxOutputTokens": max_tokens or self.max_tokens,
                "topP": 0.95,
                "topK": 40
            }
        }
        
        # Add system instruction only for v1beta (not v1)
        if system_prompt and not use_v1_api:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        
        try:
            # Track request untuk queue
            self.queue.add_request()
            
            # Send request
            logger.info(f"Sending request to Gemini API (model: {model_name})")
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Log usage untuk monitoring
            if 'usageMetadata' in result:
                usage = result['usageMetadata']
                logger.info(
                    f"Gemini API success - Tokens: {usage.get('totalTokenCount', 0)} "
                    f"(prompt: {usage.get('promptTokenCount', 0)}, "
                    f"response: {usage.get('candidatesTokenCount', 0)})"
                )
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
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
        system_prompt = "Kamu adalah asisten inventory management yang membantu dalam bahasa Indonesia. Berikan jawaban yang singkat, jelas, dan praktis."
        
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
            
            # Extract text from Gemini response
            if 'candidates' in response and len(response['candidates']) > 0:
                candidate = response['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text']
            
            return "Maaf, tidak ada response dari AI."
            
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
