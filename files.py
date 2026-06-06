from typing import Annotated

from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()


@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()]
):
    return {
        "file_size": len(file)
    }

#recommended approach

@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[
        UploadFile,
        File()
    ]
):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type" : file.content_type
    }

#Multiple Files 

@app.post("/file/")
async def upload_files(
    files: Annotated[
        list[UploadFile],
        File()
    ]
):
    return {
        "filenames": [
            file.filename
            for file in files
        ]
    }


#Request Form and Files

@app.post("/resume/")
async def upload_resume(
    student_id: Annotated[str, Form()],
    name: Annotated[str, Form()],
    resume: Annotated[UploadFile, File()],
):
    return {
        "student_id": student_id,
        "name": name,
        "filename": resume.filename
    }

@app.post("/assignment/")
async def upload_assignment(
    student_id: Annotated[str,Form()],
    subject:Annotated[str,Form()],
    file:Annotated[UploadFile,File()]
):
    return{
        "student_id": student_id,
        "subject":subject,
        "filename": file.filename
    }