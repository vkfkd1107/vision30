from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
from .forms import UploadForm
from .models import FileUpload

from django.conf import settings

import os

# *********************************************************
#                   html파일 나타내는 view
# *********************************************************

# 인덱스 템플릿
def index(request):
    return render(request,'index.html',{})

# 파일 업로드 페이지
def upload_file(request):
    reset(request)
    if request.method=='POST':
        print("request.post: ",request.POST, "request.files: " , request.FILES)        
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            print('*'*30)
            print('form valid')
            form.save()
            print("form.cleaned_data: ", form.cleaned_data)
            return redirect('file_list')
    else:
        print('*'*30)
        print('else')
        form=UploadForm()
    return render(request,'upload.html',{
        'form':form
    })
# from .extract_wav import extract_wav
# from .storage_upload import upload_blob
# from .video_transcripts import transcribe_model_selection_gcs

# ***********************************************************************
# 파이썬파일(번호판 인식) 부르는 코드
# from .detect import main
# Create your views here.
# 차량 번호판을 인식하는 파이썬 파일: demo_video2.py
# 일단 demo_video2.py 가 실행한번하는데 하루종일 걸리므로 detect로 먼저 연결하기
# 지금 시도 하는 방식은 detect.py의 파일의 main함수를 import하여 실행시키는 것을 시도중
# >> no module named 'core' 에러남
# ***********************************************************************

# 로딩페이지
def loading(request):
    print('*'*30)
    print('loading')
    files =FileUpload.objects.all()
    file = files[0]
    file_path=file.pic.path

    file_name = file.pic
    # file_name = str(file_name).split('.')[0]

    print(file_path)
    print(file_name)
    # print('##########',file_name)
    # gs_uri = f'gs://team8_hackathon/{file_name}'

    # path_to_wav = extract_wav(file_path)
    # path_to_mediadir = path_to_wav.split(file_name)[0]
    # print('########extract_wav completed')

    # upload_blob(bucket_name='team8_hackathon', source_file_name=path_to_wav, destination_blob_name=file_name)

    # print('########upload to storage completed')

    # transcribe_model_selection_gcs(path_to_mediadir, file_name, gs_uri, 'video')
    # print('########script completed')
    # return render(request,'list.html')

# 파일 업로드 시 리스트 보여주는 페이지
from .connect import connect

def file_list(request):

# **************************************************************
# 모델연결하기
# **************************************************************
    print('*'*30)
    print('file list')
    print('*'*30)
    # loading(request)
    files=FileUpload.objects.all()
    file = files[0]
    file_path=file.pic.path
    file_name = file.pic
    mediadir = file_path.split(str(file_name))[0]
    # file_name = str(file_name).split('.')[0]

    print('file_path: ',file_path)
    print('mediadir: ',mediadir)
    print('file_name: ',file_name)
    
    connect(file_path, mediadir, file_name)
    print('*'*30)
    print("analysis complete")
    print('*'*30)
    files = os.listdir(str(r'C:\Users\NA\Desktop\AI_School\Main_project\deployment\first_django\firstproject\results'))
    print("media list: ", files)
    file_list = []
    # for file in files:
    #     if (file.split('.')[-1] == 'csv'):
    #         file_list.append(file)
    context={
        'files': files,
    }
    return render(request,'list.html',context)




# *********************************************************
#                   내부에서 작동하는 코드
# *********************************************************

# 내부의 필요없는 파일을 삭제해주는 함수
def reset(request):
    print('*'*30)
    print('reset')
    files=FileUpload.objects.all()
    files.delete()

    return redirect('upload_file')

# file_list의 파일 클릭 시 다운하는 함수
def down(request,selected_file):
    # file=FileUpload.objects.get(pk=file_pk)
    # file_path=file.pic.path
    # print(file_path)    
    # response=FileResponse(open(file_path,'rb'))
    # return response
    print('*'*30)
    print('down')
    files=FileUpload.objects.all()
    file = files[0]
    file_path = file.pic.path
    print('file_path: ', file_path)
    file_name = file.pic
    print('file_name: ', file_name)
    mediadir = 'results/'
    print(selected_file)

    import mimetypes 
    import urllib
    file_path = mediadir + str(selected_file)
    print('download path: ', file_path)
    with open(file_path, 'rb') as fh: 
        response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0]) 
        response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_name 
        return response

# 출처: https://www.devoops.kr/69 [데브웁스]
#     content = open(mediadir + str(selected_file)).read()
#     response = HttpResponse(open(content, 'rb'), content_type='text/css')
#     response['Content-Disposition'] = 'attachment; filename="file.css"'
#     return response