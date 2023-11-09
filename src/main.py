from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from typing import List
from func import ocrworker, pdfmerger

app = FastAPI(
    title='PDF REST',
    description='REST API for manipulating PDF files',
    version='1.0.0',
    license_info={
        'name': 'MIT',
        'url': 'https://github.com/Loupeznik/pdf-rest/blob/master/LICENSE'
    }
)

responses = {
    400: {'error': 'Bad file type'},
    200: {'content': {'application/pdf': {}}}
}


@app.post('/ocr-pdf', name='Run OCR', description='Performs OCR on a file', responses={**responses})
async def ocr(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail='Bad file type')
    filepath = await ocrworker.scan(file)
    return FileResponse(filepath)


@app.post('/merge-pdf', name='Merge multiple files', description='Merge multiple PDF files', responses={**responses})
async def merge(files: List[UploadFile] = File(...)):
    for file in files:
        if file.content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail='Bad file type')
        else:
            continue
    filepath = await pdfmerger.merge(files)
    return FileResponse(filepath)
