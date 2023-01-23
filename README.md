### Build
```shell
docker build -t bgremover .
```
### Run
```shell
docker run -d -p 5000:5000 bgremover
```

### Test
This should take about 20 seconds on a cpu.
```shell
curl -XPOST -H'content-type: application/json' -d'{"url":"https://eg.jumia.is/unsafe/fit-in/680x680/filters:fill(white)/product/55/373622/1.jpg?2661"}' http://localhost:5000/ > output.jpg
```

### Process images in bulk outside a container
Assuming that:

- Requirements are satisfied
- Images are stored in `./sample` directory, which contains one directory with images
per product

The output will be placed in `./no_bg` directory with the same structure as `./sample`.

```shell
python bulk_processing.py
```