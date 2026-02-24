from flask import Blueprint, request, jsonify, g
from app.models import Entry, db
from app.utils import login_required
from app.ai_service import get_vibe_check
from datetime import datetime

entries_bp = Blueprint('entries', __name__)

@entries_bp.route('/', methods=['POST'])
@login_required
def create_entry():
    data = request.get_json()
    mood = data.get('mood')
    note = data.get('note')
    tags = data.get('tags', [])

    if not mood or not note:
        return jsonify({'error': 'Mood and note are required', 'code': 'MISSING_FIELDS'}), 400

    if len(note) < 50:
         return jsonify({'error': 'Note must be at least 50 characters', 'code': 'NOTE_TOO_SHORT'}), 400

    ai_response = get_vibe_check(note)

    new_entry = Entry(
        user_id=g.user_id,
        mood=mood,
        note=note,
        tags=tags,
        ai_response=ai_response
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify(new_entry.to_dict()), 201

@entries_bp.route('/', methods=['GET'])
@login_required
def get_entries():
    from_date_str = request.args.get('from')
    to_date_str = request.args.get('to')

    query = Entry.query.filter_by(user_id=g.user_id)

    if from_date_str:
        try:
            from_date = datetime.fromisoformat(from_date_str)
            query = query.filter(Entry.created_at >= from_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format (ISO 8601 expected)', 'code': 'INVALID_DATE'}), 400
    
    if to_date_str:
        try:
            to_date = datetime.fromisoformat(to_date_str)
            query = query.filter(Entry.created_at <= to_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format (ISO 8601 expected)', 'code': 'INVALID_DATE'}), 400

    entries = query.order_by(Entry.created_at.desc()).all()
    return jsonify([entry.to_dict() for entry in entries])

@entries_bp.route('/<entry_id>', methods=['GET'])
@login_required
def get_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id, user_id=g.user_id).first()
    if not entry:
        return jsonify({'error': 'Entry not found', 'code': 'ENTRY_NOT_FOUND'}), 404
    return jsonify(entry.to_dict())

@entries_bp.route('/<entry_id>', methods=['PUT'])
@login_required
def update_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id, user_id=g.user_id).first()
    if not entry:
        return jsonify({'error': 'Entry not found', 'code': 'ENTRY_NOT_FOUND'}), 404

    data = request.get_json()
    mood = data.get('mood')
    note = data.get('note')
    tags = data.get('tags')

    if mood:
        entry.mood = mood
    
    if tags is not None:
        entry.tags = tags
    
    if note:
        if len(note) < 50:
             return jsonify({'error': 'Note must be at least 50 characters', 'code': 'NOTE_TOO_SHORT'}), 400
        
        if note != entry.note:
            entry.note = note
            entry.ai_response = get_vibe_check(note)

    db.session.commit()
    return jsonify(entry.to_dict())

@entries_bp.route('/<entry_id>', methods=['DELETE'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id, user_id=g.user_id).first()
    if not entry:
        return jsonify({'error': 'Entry not found', 'code': 'ENTRY_NOT_FOUND'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'success': True})
