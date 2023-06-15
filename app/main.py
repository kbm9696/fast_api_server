from fastapi import FastAPI, HTTPException, Request, Depends
import uvicorn
from fastapi.params import Path
from api.clients import ClientsApi, ClientApi
from api.users import SignUp, LogIn
from utils.firebase_auth import get_current_user
import logging
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

logging.basicConfig(level=logging.INFO)

app = FastAPI()
clients_resource = ClientsApi()
client_resource = ClientApi()
signup_resource = SignUp()
login_resource = LogIn()


@app.api_route("/client", methods=["GET", "POST"])
@app.api_route("/signup", methods=["POST"])
@app.api_route("/login", methods=["POST"])
async def handle_client_request(request: Request):
    method_name = request.method.lower()
    method = None
    if 'client' in request.url.path:
        await get_current_user(request.headers.get('authorization'))
        method = getattr(clients_resource, method_name)
    elif 'login' in request.url.path:
        method = getattr(login_resource, method_name)
    elif 'signup' in request.url.path:
        method = getattr(signup_resource, method_name)
    if method is None:
        raise HTTPException(status_code=405, detail="Method not allowed")
    if method_name in ['post', 'patch']:
        request_body = await request.json()
        return method(request_body)
    else:
        return method()


@app.api_route("/client/{cid}", methods=["GET", "PATCH", "DELETE"])
async def handle_client_instance_request(request: Request, cid: int = Path()):
    method_name = request.method.lower()
    await get_current_user(request.headers.get('authorization'))
    method = getattr(client_resource, method_name)
    if method is None:
        raise HTTPException(status_code=405, detail="Method not allowed")
    if method_name in ['post', 'patch']:
        request_body = await request.json()
        return method(request_body, cid)
    else:
        return method(cid)


# Generate the OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="fastapi with firebase authentication",
        version="1.0.0",
        description="Just a sample code which can be webserver using python fasiapi with sqlmodel and firebase authentication.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Serve the Swagger UI
@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="fastapi with firebase authentication",
    )


@app.get("/openapi.json", include_in_schema=False)
async def openapi_endpoint():
    return app.openapi()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
