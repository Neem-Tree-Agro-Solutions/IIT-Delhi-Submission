from fastapi import FastAPI, UploadFile, File
import uvicorn
from starlette.responses import RedirectResponse
from predict import predict, read_imagefile

app = FastAPI()

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post('/api/predict')
async def predict_image(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    predictions =  predict(image)
    return predictions


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='127.0.0.1')