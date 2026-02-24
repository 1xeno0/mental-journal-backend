from flask import Blueprint, jsonify, g
from app.models import Entry, db
from app.utils import login_required
from datetime import datetime, timedelta
from collections import Counter

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/weekly', methods=['GET'])
@login_required
def get_weekly_analytics():
    today = datetime.utcnow()
    one_week_ago = today - timedelta(days=7)

    entries = Entry.query.filter(
        Entry.user_id == g.user_id,
        Entry.created_at >= one_week_ago
    ).all()

    moods = [entry.mood for entry in entries]
    mood_counts = dict(Counter(moods))

    return jsonify(mood_counts)
