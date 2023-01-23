### Build
```shell
docker build -t bgremover .
```
### Run
```shell
docker run -d -p 5000:5000 bgremover
```

### Test
```shell
curl -XPOST -H'content-type: application/json' -d'{"url":"https://eg.jumia.is/unsafe/fit-in/680x680/filters:fill(white)/product/55/373622/1.jpg?2661"}' http://localhost:5000/ > output.jpg
```