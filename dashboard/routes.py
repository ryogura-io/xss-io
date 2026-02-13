from flask import Blueprint, render_template, jsonify
from dashboard.analytics import AnalyticsService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def index():
    total_attacks = AnalyticsService.get_total_attacks()
    recent_attacks = AnalyticsService.get_recent_attacks()
    return render_template('dashboard.html', total_attacks=total_attacks, recent_attacks=recent_attacks)

@dashboard_bp.route('/stats')
def stats():
    distribution = AnalyticsService.get_attack_distribution()
    return jsonify(distribution)

@dashboard_bp.route('/attacks')
def attacks():
    attacks = AnalyticsService.get_recent_attacks(limit=50)
    return render_template('admin.html', attacks=attacks)
