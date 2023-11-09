import ocrmypdf
import uuid
from fastapi import UploadFile, HTTPException
from os import path, mkdir

tempdir = '/tmp/ocr'


async def scan(file: UploadFile) -> str:
    input_filename = '{}.pdf'.format(uuid.uuid1())
    output_filename = '{}.pdf'.format(uuid.uuid1())

    if not path.exists(tempdir):
        mkdir(tempdir)

    with open(get_full_path(input_filename), 'wb+') as temp:
        temp.write(file.file.read())

    try:
        ocrmypdf.ocr(get_full_path(input_filename), get_full_path(output_filename), deskew=True, language='ces')
    except ocrmypdf.PriorOcrFoundError as ex:
        raise HTTPException(status_code=400, detail=ex.message)

    return get_full_path(output_filename)


def get_full_path(filename: str) -> str:
    return '{}/{}'.format(tempdir, filename)
