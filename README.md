# vision30

* pipfile을 이용한 설치

1. https://drive.google.com/drive/u/0/folders/1geTT_3rz5HH4DyFfy1HqmJMrwsJo9YDx 로 들어가 data.zip을 다운받는다.

2. 압축을 풀면 weights 파일들이 있을 텐데 이 파일들을 data폴더에 넣어준다. 

3. 터미널에서 keshavoct98로 경로 설정을 한 다음 pipenv install을 입력하면 가상환경에 필요한 라이브러리들이 다 깔린다.
(이 과정에서 오류가 날 수도 있을 것 같다. 이때는 오류를 하나하나 잡아가던가 해야...)

4. 3번까지 마쳤으면 pipenv run python demo_video.py --input inputs/test1.mp4 와 같은 명령어로 결과를 확인해보자.


* 수동 설치

1. https://drive.google.com/drive/u/0/folders/1geTT_3rz5HH4DyFfy1HqmJMrwsJo9YDx 로 들어가 data.zip을 다운받는다.

2. 압축을 풀면 weights 파일들이 있을 텐데 이 파일들을 data폴더에 넣어준다. 

3. https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe 에 들어가 python 3.7.9파일을 받은 다음 설치해 준다.

4. CUDA 9.2, CUDA 10.1 을 설치하고 각 CUDA에 맞는 버전의 cuDNN을 설치한다.

5. 터미널에서 keshavoct98 폴더로 이동한다(Pipfile, Pipfile.lock은 없어야 함).

6. 아래의 명령어를 차례대로 입력한다.

pipenv --python 3.7.9

pipenv run pip install opencv-python==4.2.0.34

pipenv run pip install tensorflow==2.2.0

pipenv run pip install easydict==1.9

pipenv run pip install keras_ocr==0.8.3

pipenv run pip install torch==1.4.0+cu92 torchvision==0.5.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html

pipenv run pip install easyocr

pipenv run pip install pytesseract

pipenv run pip install torch==1.7.0+cu101 torchvision==0.8.1+cu101 torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html)

7. pipenv run python demo_video.py --input inputs/test2.mp4 로 결과 확인

