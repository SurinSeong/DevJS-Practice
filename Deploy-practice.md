# Docker

## 사용해보기

- [Docker Hub](https://hub.docker.com/)에서 Docker 이미지를 다운로드 받아 Container 실행하는 예제
- **Docker Hub** : Docker 이미지 저장소
- **Docker Image** : 애플리케이션 실행에 필요한 모든 것 (애플리케이션 구성 파일, 라이브러리, 설정 정보 등)을 포함한 소프트웨어 패키지
- **Docker Container** : Docker 이미지를 기반으로 실행되는 독립적인 애플리케이션 환경

### terminal 기능 활성화

- Docker Desktop에서 Terminal 기능을 제공해준다. (하지만 꼭 쓰지 않아도 된다. cmd 사용 가능)
    - 원하는 명령어 인터페이스를 선택해 사용할 수 있다.
 
### Docker 이미지를 다운받아 Container 실행

- Tomcat 이미지를 다운 받아 Container로 띄우는 예제 진행하기
    - Docker Hub에서 Tomcat 이미지 다운로드
    - Terminal에서 설치
    - Tomcat 이미지 실행
        - Tomcat : 아파치 소프트웨어 재단에서 개발한 동적 웹을 구동할 수 있도록 해주는 웹 서버 & 서블릿 컨테이너
        - 기본적으로 웹페이지가 정상적으로 띄워졌는지 알 수 있도록 예제 웹 리소스를 제공해주는데 해당 예제 웹 리소스의 위치는 `tomcat/webapp/` 위치에 존재
