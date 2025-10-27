import pytest
from app import create_app, db
from models import User
from utils import calculate_daily_calories

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_calculate_daily_calories_male():
    result = calculate_daily_calories(weight=70, height=175, age=25, gender='Чоловік')
    assert 1600 < result < 1900

def test_calculate_daily_calories_female():
    result = calculate_daily_calories(weight=60, height=165, age=25, gender='Жінка')
    assert 1300 < result < 1700

def test_user_registration(client):
    response = client.post('/', data={
        'name': 'test',
        'email': 'test@example.com',
        'password_hash': '1234',
        'age': '25',
        'height': '175',
        'weight': '70',
        'gender': 'Чоловік'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'test' in response.data

    with client.application.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.name == 'test'