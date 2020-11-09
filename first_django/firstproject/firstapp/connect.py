from detect import detect_connect

def connect(file_path,file_name,mediadir):
    print('*'*50)
    print('connect')
    print('*'*50)

    print(file_path)
    print(file_name)
    print(mediadir)

    detect_connect(file_path,file_name,mediadir)