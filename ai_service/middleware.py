"""
Simple Anti-Hacker Middleware
Proteksi sederhana untuk aplikasi
"""
import logging
from django.http import HttpResponseForbidden
from django.core.cache import cache
import re

logger = logging.getLogger(__name__)


class SimpleSecurityMiddleware:
    """
    Middleware keamanan sederhana:
    - Blokir SQL injection patterns
    - Blokir XSS patterns
    - Rate limiting per IP
    """
    
    # Pattern berbahaya yang harus diblokir
    DANGEROUS_PATTERNS = [
        r'(\%27)|(\')|(\-\-)|(\%23)|(#)',  # SQL injection
        r'((\%3C)|<)((\%2F)|\/)*[a-z0-9\%]+((\%3E)|>)',  # XSS
        r'((\%3C)|<)((\%69)|i|(\%49))((\%6D)|m|(\%4D))((\%67)|g|(\%47))',  # IMG tag
        r'exec(\s|\+)+(s|x)p\w+',  # SQL exec
        r'union.*select',  # SQL union
        r'<script',  # XSS script
        r'javascript:',  # XSS javascript
        r'onerror\s*=',  # XSS event
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) 
                                 for pattern in self.DANGEROUS_PATTERNS]
    
    def __call__(self, request):
        # Rate limiting sederhana per IP
        if not self._check_rate_limit(request):
            logger.warning(f"Rate limit exceeded for IP: {self._get_client_ip(request)}")
            return HttpResponseForbidden("Too many requests. Please try again later.")
        
        # Check untuk pattern berbahaya
        if self._has_dangerous_content(request):
            logger.warning(f"Dangerous pattern detected from IP: {self._get_client_ip(request)}")
            return HttpResponseForbidden("Suspicious activity detected.")
        
        response = self.get_response(request)
        return response
    
    def _get_client_ip(self, request):
        """Dapatkan IP address client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _check_rate_limit(self, request):
        """
        Simple rate limiting: max 100 requests per minute per IP
        """
        ip = self._get_client_ip(request)
        cache_key = f'rate_limit_{ip}'
        
        request_count = cache.get(cache_key, 0)
        
        if request_count >= 100:  # Max 100 requests per minute
            return False
        
        cache.set(cache_key, request_count + 1, 60)  # Expire in 60 seconds
        return True
    
    def _has_dangerous_content(self, request):
        """Check apakah request mengandung pattern berbahaya"""
        # Check GET parameters
        for key, value in request.GET.items():
            if self._is_dangerous(value):
                return True
        
        # Check POST parameters
        for key, value in request.POST.items():
            if self._is_dangerous(str(value)):
                return True
        
        # Check path
        if self._is_dangerous(request.path):
            return True
        
        return False
    
    def _is_dangerous(self, text):
        """Check apakah text mengandung pattern berbahaya"""
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
        return False
