from app import app
from utils.constants import ASTEROID_ROOT, DECODER_ROOT


def test_routing():
    response = app.test_client().get(ASTEROID_ROOT)
    assert response.status_code == 200

    response = app.test_client().get(DECODER_ROOT)
    assert response.status_code == 200
