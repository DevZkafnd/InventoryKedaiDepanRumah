"""
AI Service Views
API endpoints untuk fitur AI
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
import logging

from .groq_client import GroqClient

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_ask(request):
    """
    Endpoint untuk tanya jawab dengan AI
    
    POST /api/ai/ask/
    Body: {
        "question": "Pertanyaan Anda",
        "context": "Context opsional",
        "model": "fast|balanced|quality" (opsional, default: fast)
    }
    """
    try:
        if not (
            request.user.groups.filter(name="managers").exists()
            or request.user.groups.filter(name="owners").exists()
        ):
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )
        question = request.data.get('question')
        if not question:
            return Response(
                {'error': 'Question is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Rate limiting per user (max 20 requests per hour)
        user_id = request.user.id
        cache_key = f'ai_rate_limit_user_{user_id}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= 20:
            return Response(
                {'error': 'Rate limit exceeded. Maximum 20 requests per hour.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Process request
        context = request.data.get('context')
        model_pref = request.data.get('model', 'fast')
        
        client = GroqClient()
        answer = client.simple_ask(
            question=question,
            context=context,
            model_preference=model_pref
        )
        
        # Update rate limit counter
        cache.set(cache_key, request_count + 1, 3600)  # 1 hour
        
        return Response({
            'question': question,
            'answer': answer,
            'model': model_pref,
            'requests_remaining': 20 - request_count - 1
        })
        
    except Exception as e:
        logger.error(f"Error in ai_ask: {str(e)}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_inventory_insights(request):
    """
    Endpoint untuk mendapatkan insights dari inventory data
    
    POST /api/ai/inventory-insights/
    Body: {
        "inventory_data": {...},
        "question": "Apa insight dari data ini?"
    }
    """
    try:
        if not (
            request.user.groups.filter(name="managers").exists()
            or request.user.groups.filter(name="owners").exists()
        ):
            return Response(
                {"error": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )
        inventory_data = request.data.get('inventory_data')
        question = request.data.get('question')
        
        if not inventory_data or not question:
            return Response(
                {'error': 'inventory_data and question are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Rate limiting
        user_id = request.user.id
        cache_key = f'ai_insights_rate_limit_user_{user_id}'
        request_count = cache.get(cache_key, 0)
        
        if request_count >= 10:  # Lebih ketat karena data lebih besar
            return Response(
                {'error': 'Rate limit exceeded. Maximum 10 insights requests per hour.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        client = GroqClient()
        insights = client.get_inventory_insights(inventory_data, question)
        
        cache.set(cache_key, request_count + 1, 3600)
        
        return Response({
            'question': question,
            'insights': insights,
            'requests_remaining': 10 - request_count - 1
        })
        
    except Exception as e:
        logger.error(f"Error in ai_inventory_insights: {str(e)}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_status(request):
    """
    Check status AI service dan quota
    
    GET /api/ai/status/
    """
    if not (
        request.user.groups.filter(name="managers").exists()
        or request.user.groups.filter(name="owners").exists()
    ):
        return Response(
            {"error": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
        )
    user_id = request.user.id
    
    # Check rate limits
    ask_key = f'ai_rate_limit_user_{user_id}'
    insights_key = f'ai_insights_rate_limit_user_{user_id}'
    
    ask_count = cache.get(ask_key, 0)
    insights_count = cache.get(insights_key, 0)
    
    return Response({
        'status': 'active',
        'model_default': 'llama-3.1-8b-instant',
        'quota': {
            'ask': {
                'used': ask_count,
                'limit': 20,
                'remaining': 20 - ask_count
            },
            'insights': {
                'used': insights_count,
                'limit': 10,
                'remaining': 10 - insights_count
            }
        }
    })
