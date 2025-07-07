from typing import Dict, Optional, Callable
from datetime import datetime, timedelta
import time
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import asyncio

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        calls: int = 100,
        period: timedelta = timedelta(minutes=1),
        identifier: Optional[Callable[[Request], str]] = None
    ):
        super().__init__(app)
        self.calls = calls
        self.period = period.total_seconds()
        self.identifier = identifier or self._default_identifier
        self.storage: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    def _default_identifier(self, request: Request) -> str:
        # Use IP address as default identifier
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "anonymous"
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        identifier = self.identifier(request)
        now = time.time()
        
        async with self._lock:
            # Clean old entries
            self.storage[identifier] = [
                timestamp for timestamp in self.storage[identifier]
                if timestamp > now - self.period
            ]
            
            # Check rate limit
            if len(self.storage[identifier]) >= self.calls:
                retry_after = int(self.period - (now - self.storage[identifier][0]))
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded",
                    headers={"Retry-After": str(retry_after)}
                )
            
            # Add current request
            self.storage[identifier].append(now)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.calls)
        response.headers["X-RateLimit-Remaining"] = str(
            self.calls - len(self.storage[identifier])
        )
        response.headers["X-RateLimit-Reset"] = str(int(now + self.period))
        
        return response

class AuthenticatedRateLimitMiddleware(RateLimitMiddleware):
    """Rate limiter that uses authenticated user ID when available"""
    
    def __init__(self, app, calls: int = 100, period: timedelta = timedelta(minutes=1)):
        super().__init__(app, calls, period, identifier=self._auth_identifier)
    
    def _auth_identifier(self, request: Request) -> str:
        # Try to get user ID from JWT token
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # In production, decode JWT to get user ID
            # For now, use the token itself as identifier
            return f"user:{auth_header[7:20]}"  # Use first part of token
        
        # Fall back to IP address
        return self._default_identifier(request)