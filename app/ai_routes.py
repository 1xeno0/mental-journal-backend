from flask import Blueprint, request, jsonify
from app.ai_service import get_vibe_check
from app.utils import login_required

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/vibe-check', methods=['POST'])
@login_required
def vibe_check():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required', 'code': 'INVALID_REQUEST'}), 400
        
    note = data.get('note')

    if not note:
        return jsonify({'error': 'Note is required', 'code': 'MISSING_NOTE'}), 400

    if len(note) < 50:
        return jsonify({'error': 'Note must be at least 50 characters', 'code': 'NOTE_TOO_SHORT'}), 400

    response = get_vibe_check(note)
    return jsonify({'ai_response': response})
