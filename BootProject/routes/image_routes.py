from flask import Blueprint, request, jsonify, send_file
from PIL import Image
import io
from diffusers import StableDiffusionPipeline
import torch
from rembg import remove

# Blueprint 생성
image_bp = Blueprint("image", __name__)

# Stable Diffusion 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32
pipeline = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2",
    torch_dtype=torch_dtype
)
pipeline.to(device)
pipeline.enable_attention_slicing()

def resize_to_divisible_by_8(image: Image.Image) -> Image.Image:
    """이미지를 8로 나누어떨어지는 크기로 조정"""
    width, height = image.size
    new_width = (width // 8) * 8
    new_height = (height // 8) * 8
    return image.resize((new_width, new_height), Image.LANCZOS)

@image_bp.route("/process-image/", methods=["POST"])
def process_image():
    try:
        # 업로드된 파일 가져오기
        file = request.files.get("file")
        prompt = request.form.get("prompt", "기본 배경")
        
        if not file or not file.filename.lower().endswith(("png", "jpg", "jpeg")):
            return jsonify({"error": "유효한 이미지 파일을 업로드해주세요."}), 400

        # 원본 이미지 열기
        original_image = Image.open(file).convert("RGB")
        
        # 이미지 크기 조정 (8로 나누어떨어지도록)
        original_image = resize_to_divisible_by_8(original_image)

        # 이미지 바이트로 변환
        image_bytes = io.BytesIO()
        original_image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # 전경 이미지 생성
        foreground_bytes = remove(image_bytes.getvalue())
        foreground_image = Image.open(io.BytesIO(foreground_bytes)).convert("RGBA")

        # Stable Diffusion으로 새로운 배경 생성
        generated_image = pipeline(prompt).images[0]

        # 배경 이미지 크기를 원본 이미지 크기에 맞게 조정
        generated_image = generated_image.resize(
            (foreground_image.width, foreground_image.height), 
            Image.LANCZOS
        ).convert("RGBA")

        # 전경과 배경 합성
        combined_image = Image.alpha_composite(generated_image, foreground_image)

        # 결과 반환
        output = io.BytesIO()
        combined_image.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype="image/png")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
