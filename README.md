# FastAPI Learning

This repository contains my FastAPI learning examples and practice code.


# creation of a vitual environment named as "myenv" :

>>python -m venv myenv

# Activate the created vitual environment myenv :

>>source myenv/bin/activate

# To see the installed libraries/packages in myenv :

>>pip list

# Deactivate the created vitual environment myenv :

>>deactivate

# Installing FastApi and Uvicorn (the ASGI web server)

>> pip install fastapi uvicorn

# To start the uvicorn web server and show the output on webpage ( CTRL+C  to stop )

>>uvicorn pythonfilename:FastapiObjectname --reload
>>uvicorn main:app --reload


#   Pydantic is mainly used for data validation in Fastapi