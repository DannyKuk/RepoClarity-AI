from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get("/")
def list_models(request: Request):
    services = request.app.state.services

    try:
        models = services.llm.list_models()
        return {"models": models}

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )