#AI 이미지 생성앱(python 3.10.11)

새로운 PC에서 다음 명령어 실행(cmd):
pip install flask flask_cors pillow torch torchvision torchaudio diffusers huggingface-hub transformers rembg onnxruntime accelerate
패키지 일괄다운로드
패키지가 다운로드되지 않았다면 터미널이 바로 죽는 오류 발생
이외의 경우 app.py를 파이썬으로 실행시키고 디버그 확인해볼것

GPU 사용시
cmd-> nvidia-smi 명령어 사용하여
맨오른쪽 상단 CUDA 버전 확인 (예: CUDA Version: 12.7 )

app.py 더블 클릭 하여 실행

!!절대 app.py를 IDLE로 실행하지말것.안돌아감

http://127.0.0.1:5000
접속