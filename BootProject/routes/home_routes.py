from flask import Blueprint, render_template

# Blueprint 생성
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """
    메인 HTML 페이지 렌더링.
    """
    return render_template('index.html')  # 'templates/index.html' 경로의 HTML 파일 렌더링
