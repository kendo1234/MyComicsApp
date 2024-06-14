from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/comics', methods=['GET'])
def get_comics():
    return jsonify(comics_data)


@app.route('/comics/title/<title>', methods=['GET'])
def get_comic_by_title(title):
    title = title.strip().lower()
    comics = [comic for comic in comics_data if 'Title' in comic and comic['Title'].strip().lower() == title]
    if comics:
        return jsonify(comics)
    else:
        return jsonify({"error": "Comics not found"}), 404


@app.route('/comics/volume/<volume>', methods=['GET'])
def get_comic_by_volume(volume):
    try:
        volume = int(volume)
        comics = [comic for comic in comics_data if 'Volume' in comic and comic['Volume'] == volume]
        if comics:
            return jsonify(comics)
        else:
            return jsonify({"error": "Comics not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid volume format"}), 400


@app.route('/comics/writer/<writer>', methods=['GET'])
def get_comic_by_writer(writer):
    writer = writer.strip().lower()
    comics = [comic for comic in comics_data if 'Writer' in comic and comic['Writer'].strip().lower() == writer]
    if comics:
        return jsonify(comics)
    else:
        return jsonify({"error": "Comics not found"}), 404


@app.route('/comics', methods=['POST'])
def add_comic():
    new_comic = request.json
    comics_data.append(new_comic)

    # Append new comic to the DataFrame
    df_new_comic = pd.DataFrame([new_comic])
    df_new_comic.columns = df_new_comic.columns.str.capitalize()  # Ensure column names match the Excel format
    global df
    df = pd.concat([df, df_new_comic], ignore_index=True)

    # Write the updated DataFrame back to the Excel file
    df.to_excel('Comics.xlsx', index=False)

    return jsonify(new_comic), 201


@app.route('/comics/title/<title>', methods=['DELETE'])
def delete_comic_by_title(title):
    title = title.strip().lower()
    global comics_data
    new_comics_data = [comic for comic in comics_data if
                       'Title' not in comic or comic['Title'].strip().lower() != title]

    if len(new_comics_data) == len(comics_data):
        return jsonify({"error": "Comic not found"}), 404

    comics_data = new_comics_data

    # Update the DataFrame and write to Excel
    global df
    df = pd.DataFrame(comics_data)
    df.columns = df.columns.str.capitalize()  # Ensure column names match the Excel format
    df.to_excel('Comics.xlsx', index=False)

    return jsonify({"message": "Comic deleted successfully"}), 200


if __name__ == '__main__':
    df = pd.read_excel('Comics.xlsx')
    comics_data = df.to_dict(orient='records')

    # Convert all keys to strings
    comics_data = [{str(key): value for key, value in comic.items()} for comic in comics_data]

    # Normalize the data
    for comic in comics_data:
        if 'title' in comic:
            comic['title'] = comic['title'].strip().lower()
        if 'writer' in comic:
            comic['writer'] = comic['writer'].strip().lower()
        if 'artist' in comic:
            comic['artist'] = comic['artist'].strip().lower()

    app.run(debug=True)
