import subprocess
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def list_models():
    """
    List available Ollama models installed locally.
    """

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True,
        )

        lines = result.stdout.strip().split("\n")

        # Skip header line from ollama output
        models = []

        for line in lines[1:]:
            parts = line.split()

            if parts:
                models.append(parts[0])

        return {"models": models}

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Ollama is not installed or not available in PATH.",
        )

    except subprocess.CalledProcessError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve models: {exc}",
        )
