from flask import Flask, render_template
from flask_cors import CORS
import logging
from routes.image_routes import image_bp
from routes.home_routes import home_bp

def create_app():
    app = Flask(__name__)

    # CORS 설정 (Permissions-Policy 경고 해결)
    CORS(app, expose_headers=["Permissions-Policy"])

    # Blueprint 등록
    app.register_blueprint(image_bp, url_prefix="/api")  # 이미지 처리 관련
    app.register_blueprint(home_bp)  # 메인 페이지 관련

    # Permissions-Policy 설정
    @app.after_request
    def set_permissions_policy(response):
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"  # 필요 없는 정책 제거
        return response

    # 에러 처리
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Error: 서버 내부 오류 발생 - {error}")
        return render_template("500.html"), 500

    # 로깅 설정
    logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
