import time

from fastapi import FastAPI, HTTPException, Request
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from authorization.logic.autorization_logic import JWTLogic, UserSchema
from settings import middleware
from authorization.controllers.auth_controllers import user_manager
from database import redis_client


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.jwt_logic = JWTLogic()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in middleware.excluded_path_auth:
            return await call_next(request)
        headers = request.headers.get("Authorization")
        print(request.headers)
        if not headers:
            return JSONResponse(status_code=401, content={"detail": "Access Token is missing"})
        try:
            access_token = headers.split(" ")[1]
        except IndexError:
            return JSONResponse(status_code=401, content={"Authorization header is malformed"})
        refresh_token = request.headers.get("refresh-token")
        if refresh_token:
            if redis_client.get(refresh_token):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Unauthorized"}
                )
        else:
            return JSONResponse(status_code=401, content={"Refresh Token is missing"})
        try:
            access_payload = self.jwt_logic.verify_expire_token(access_token, "access")
            user = await user_manager.get_user(user_id=access_payload.get("user_id"))
            user = user.scalars().first()
            if not user:
                return JSONResponse({"detail": "User is not found"}, status_code=401)
            request.state.user = access_payload
            response = await  call_next(request)
        except HTTPException as ex:
            try:
                refresh_payload = self.jwt_logic.verify_expire_token(refresh_token, "refresh")
                user = await user_manager.get_user(user_id=refresh_payload.get("user_id"))
                user = user.scalars().first()
                if not user:
                    return JSONResponse({"detail": "user is not found"}, status_code=401)
                user_schema: UserSchema = UserSchema(user_id=user.user_id, role=user.role)
                new_access_token = self.jwt_logic.create_access_token(user_schema)
                response = JSONResponse(
                content={"detail": "Access token has been refreshed"},
                headers={"Authorization": f"Bearer {new_access_token}"}
                )
            except HTTPException as refresh_exc:
                return JSONResponse({"detail": str(refresh_exc)}, status_code=401)
        return response


class PrometheusMiddleware(BaseHTTPMiddleware):
    REQUEST_COUNT: Counter = Counter(
        "http_requests_total",
        "Total number of HTTP requests",
        ["method", "endpoint", "http_status"]
    )

    REQUEST_LATENCY: Histogram = Histogram(
        "http_request_duration_seconds",
        "HTTP request latency in seconds",
        ["method", "endpoint"]
    )

    EXCEPTION_COUNT: Counter = Counter(
        "http_exceptions_total",
        "Total number of exceptions",
        ["exception_type"]
    )
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path

        start_time = time.time()

        try:
            response = await call_next(request)
            status_code = response.status_code
            self.REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
        except Exception as e:
            self.EXCEPTION_COUNT.labels(exception_type=type(e).__name__).inc()
            raise e
        finally:
            self.REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(time.time() - start_time)

        return response






