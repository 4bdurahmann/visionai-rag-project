"""Root route: OK-status + project metadata from core config."""

from fastapi import APIRouter

from core.config import get_settings

router = APIRouter()


@router.get("/")
def root() -> dict:
    app_settings = get_settings()
    return {
        "status": "success",
        "message": "Server is running smoothly and fully operational.",
        "project_details": {
            "name": app_settings.PROJECT_NAME,
            "event": app_settings.PROJECT_EVENT,
            "organizers": [name for name in app_settings.PROJECT_ORGANIZERS],
            "instructors": [name for name in app_settings.PROJECT_INSTRUCTORS],
        },
        "supervision": {
            "team": app_settings.SUPERVISOR_TEAM,
            "members": [name for name in app_settings.SUPERVISOR_MEMBER],
        },
        "timestamp": app_settings.PROJECT_DATE,
    }