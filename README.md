# Build image

```bash
docker build -t uploader .
```


```bash
docker run -dp 5000:5000 --name uploader --env-file ./.env uploader
```
