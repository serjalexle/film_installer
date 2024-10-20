# run main program (main.py) with the following command:
# python run.py

import uvicorn as uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)
