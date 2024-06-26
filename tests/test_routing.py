from app import app
from utils.constants import LAB_WORK_ROOT


def test_routing():
    response = app.test_client().get(LAB_WORK_ROOT)
    assert response.status_code == 200
