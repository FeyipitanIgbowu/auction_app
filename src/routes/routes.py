from flask import Blueprint, request, redirect, jsonify, render_template
from app.db import Database
from app.repositories import URLRepository
from app.services import URLService

bp = Blueprint('main', __name__)

db = Database()
repository = URLRepository(db)
service = URLService(repository)


@bp.route('/api/shorten', methods=['POST'])
def shorten():
    data = request.get_json() or {}
    original_url = data.get('url')
    if not original_url:
        return jsonify({"error": "Please provide a URL"}), 400

    try:
        short_id = service.shorten_url(original_url)
        short_url = request.host_url.rstrip('/') + '/' + short_id
        return jsonify({"short_url": short_url, "short_id": short_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<short_id>')
def redirect_to_url(short_id):
    original_url = service.get_original_url(short_id)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404


@bp.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    error = None
    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            error = 'Please provide a URL'
        else:
            try:
                short_id = service.shorten_url(original_url)
                short_url = request.host_url.rstrip('/') + '/' + short_id
            except Exception as e:
                error = str(e)

    return render_template('index.html', short_url=short_url, error=error)
