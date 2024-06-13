# Comics API

This is a simple Flask API for managing a collection of comics. The API allows you to retrieve all comics, get comics by title, volume, or writer, and add new comics.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository or download the code.
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Run app 
```bash
python app.py
```

## Api Endpoints
- `GET /comics`: Retrieve all comics.
- `GET /comics/title/<title>`: Retrieve comics by title.
- `GET /comics/volume/<volume>`: Retrieve comics by volume.
- `GET /comics/writer/<writer>`: Retrieve comics by writer.
- `POST /comics`: Add a new comic. Send a JSON body with `title`, `volume`, `writer`, and `artist`.

## Example JSON for POST /comics

```json
{
  "title": "New Title",
  "volume": 1,
  "writer": "New Writer",
  "artist": "New Artist"
}
```
