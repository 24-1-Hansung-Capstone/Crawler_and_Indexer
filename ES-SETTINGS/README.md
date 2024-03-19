## es 명령
### 인덱스 생성
- curl 명령, settings.json과 같은 디렉터리에 있어야 함
```bash
$ curl -XPUT "http://ES_IP:9200/인덱스명" -H "Content-Type: application/json" -d @settings.json
$ curl -XPUT "http://ES_IP:9200/인덱스명/_mappings" -H "Content-Type: application/json" -d @mapping.json
```
- postman
  - PUT 명령
  - http://ES_IP:9200/인덱스명
  - body에 settings.json 복붙

#### send 후 결과값 200 및 acknowladge : true인지 확인!!
