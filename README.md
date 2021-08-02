# 숨고 크롤러
숨고에서 본인이 받은 요청들을 google sheet로 자동으로 옮겨주는 프로그램입니다.

## 사용법
1. `pip install -r requirements.txt` 로 필요한 라이브러리들을 설치해줍니다.
2. `python main.py --help`를 실행하여, 필요한 인자들을 확인합니다.
```bash
$ python main.py --help
usage: main.py [-h] --credential-json CREDENTIAL_JSON --spreadsheet-key SPREADSHEET_KEY --chromedriver CHROMEDRIVER --sumgo-id SUMGO_ID --sumgo-pw SUMGO_PW

optional arguments:
  -h, --help            show this help message and exit
  --credential-json CREDENTIAL_JSON
                        Path to google api credential json file.
  --spreadsheet-key SPREADSHEET_KEY
                        Google spreadsheet key.
  --chromedriver CHROMEDRIVER
                        Path to chromedriver (Default: ./chromedriver).
  --sumgo-id SUMGO_ID   Sumgo ID.
  --sumgo-pw SUMGO_PW   Sumgo password.
```
3. 인자들을 추가하여, `main.py`를 실행합니다.

## 인자 설명
- `--chromedriver`: 먼저 chrome을 설치한다. 그리고 설치한 chrome과 동일한 버전의 chromedriver를 https://sites.google.com/a/chromium.org/chromedriver/downloads 에서 다운받는다. 그리고 그 경로를 `--chromedriver <경로>`의 형태로 추가한다.
- `--credential-json`: https://cloud.google.com/ai-platform/training/docs/python-client-library?hl=ko 를 통해 json 키 파일을 생성한다. 그리고 그 파일의 경로를 `--credential-json <경로>`의 형태로 추가한다. 부가적으로, 링크를 통해 추가한 프로젝트에서 google sheet, google drive api를 허용해줘야한다.
- `--spreadsheet-key`: 숨고 받은요청들을 저장할 google spread sheet의 키 값을 전달받는 인자이다.
- `--sumgo-id`, `--sumgo-pw`: 본인의 숨고 사이트 아이디, 비번을 추가한다.
