# DJANGO_ELECTRON_v1.00
  - 일단 고생해서 짠 코드니 남겨 놓기는 하겠다만, Django 백엔드에 Electron Frontend 는 별로 좋은 생각이 아닌 것 같다. 
  - 도대체 돌려야 하는 Subprocess 가 몇 개인가? 그냥 PyQT 나 PySide6 로 짜는 게 정신건강에 이롭다.

 # 설치 및 실행
   - 실행하려면 Node 가 필요하다. 사실 python 처럼 이 저장소에 다 포함하려고 했으나, 깃허브 업로드 용량 제한 문제로 따로 다운로드해 주어야 한다.
   - https://nodejs.org/en/download 에서 다운로드 받은 "Windows Binary" 파일의 압축을 풀어 node 폴더에 넣어 주면 된다. (node.exe 파일이 node 폴더에 있으면 됨.)

 # Notice
   - Electron 의 main.ts 에서 Django 를 서브프로세스로 실행한다.
   - 문제는 이 서브프로세스를 Kill 해도 Django 가 꺼지지 않는다. Django 는 cmd 에서 ctrl+c 를 눌러야 꺼지기 때문이다.
   - 사실 Python manage.py runserver 를 하면 manage.py 가 Django 를 서브프로세스로 실행하는데, main.ts 가 종료될 시 subprocess 를 kill 할 경우, manage.py 만 꺼지고 Django 는 꺼지지 않는 것이다.
   - 그래서 Django 를 돌리는 manage.py 를 돌리는 runserver.py 를 돌리는 run.py 를 main.ts 에서 돌리도록 했다. main.ts 가 run.py 및 runserver.py 를 돌릴 때는 자기 자신의 PID 값을 인수로 넘겨준다. main.ts 가 종료되면 run.py 는 자동으로 kill 되며 runserver.py 는 종료되지 않는데, runserver.py 는 주기적으로 main.ts 의 PID 와 일치하는 프로세스가 존재하는 지 체크하고, 없으면 ctrl+C Signal 을 manage.py 에 보내고 끝낸다. 이렇게 모든 subprocess 가 회수될 수 있도록 하였다.