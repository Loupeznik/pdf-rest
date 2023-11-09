from PyPDF2 import PdfMerger, PdfReader
from fastapi import UploadFile
from typing import List
from os import path, mkdir, remove
import uuid

tempdir = '/tmp/merger'


async def merge(files: List[UploadFile]) -> str:
    merger = PdfMerger()
    filename = '{}.pdf'.format(uuid.uuid1())
    tempfiles = []

    if not path.exists(tempdir):
        mkdir(tempdir)

    await save_files(files)

    for file in files:
        merger.append(PdfReader('{}/{}'.format(tempdir, file.filename)))
        tempfiles.append(file.filename)

    await clean_files(tempfiles)

    return_path = '{}/{}'.format(tempdir, filename)
    merger.write(return_path)
    return return_path


async def save_files(files: List[UploadFile]):
    for file in files:
        with open('{}/{}'.format(tempdir, file.filename), 'wb+') as temp:
            temp.write(file.file.read())


async def clean_files(files: List[str]):
    for filename in files:
        remove('{}/{}'.format(tempdir, filename))
