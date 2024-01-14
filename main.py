from flask import Flask, render_template, request, redirect, url_for
import string
import random

app = Flask(__name__)

# Dictionary to store mappings of short URLs to original URLs
url_mapping = {}

def generate_short_url():
    # Generate a random short URL of length 6
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']

    # Check if the URL has already been shortened
    short_url = next((short for short, url in url_mapping.items() if url == original_url), None)

    if not short_url:
        # Generate a new short URL
        short_url = generate_short_url()

        # Store the mapping in the dictionary
        url_mapping[short_url] = original_url

    return render_template('result.html', short_url=short_url, original_url=original_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    # Redirect to the original URL if the short URL is found
    original_url = url_mapping.get(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return render_template('result.html', error='URL not found')

if __name__ == '__main__':
    app.run(debug=True)
