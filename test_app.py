import pytest
from flask import Flask, jsonify, request
from app import app, comics_data


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the index endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Comics API" in response.data


def test_get_comics(client):
    """Test the get all comics endpoint"""
    response = client.get('/comics')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_comic_by_title(client):
    """Test the get comic by title endpoint"""
    title = comics_data[0]['title']
    response = client.get(f'/comics/title/{title}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['title'].lower() == title.lower()


def test_get_comic_by_volume(client):
    """Test the get comic by volume endpoint"""
    volume = comics_data[0]['volume']
    response = client.get(f'/comics/volume/{volume}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['volume'] == volume


def test_get_comic_by_writer(client):
    """Test the get comic by writer endpoint"""
    writer = comics_data[0]['writer']
    response = client.get(f'/comics/writer/{writer}')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data[0]['writer'].lower() == writer.lower()


def test_post_comic(client):
    """Test the add comic endpoint"""
    new_comic = {
        "title": "Test Title",
        "volume": 1,
        "writer": "Test Writer",
        "artist": "Test Artist"
    }
    response = client.post('/comics', json=new_comic)
    assert response.status_code == 201
    data = response.get_json()
    assert data == new_comic


def test_get_nonexistent_comic(client):
    """Test getting a comic that doesn't exist"""
    response = client.get('/comics/title/Nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Comics not found"
