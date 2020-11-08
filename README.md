# vision30

1. https://drive.google.com/drive/u/0/folders/1geTT_3rz5HH4DyFfy1HqmJMrwsJo9YDx 로 들어가 data.zip을 다운받는다.

2. 압축을 풀면 weights 파일들이 있을 텐데 이 파일들을 data폴더에 넣어준다. 

3. 터미널에서 keshavoct98로 경로 설정을 한 다음 pipenv install을 입력하면 가상환경에 필요한 라이브러리들이 다 깔린다.
(이 과정에서 오류가 날 수도 있을 것 같다. 이때는 오류를 하나하나 잡아가던가 해야...)

4. 3번까지 마쳤으면 pipenv run python demo_video.py --input inputs/test1.mp4 와 같은 명령어로 결과를 확인해보자.
