from flask import Blueprint, render_template

bp = Blueprint('policies', __name__)

@bp.route('/')
def index():
    return render_template('policies.html')  


