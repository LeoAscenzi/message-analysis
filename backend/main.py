import polars as pl
import asyncio
import json
from fastapi import FastAPI, File, HTTPException, UploadFile
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import utils

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pl.DataFrame(schema= {"name": str, "date": pl.Datetime(time_unit="ms"), "message": str})
    app.state.user_list = set()
    app.state.df_lock = asyncio.Lock()
    print("Starting App")

    yield

    print("Shutting down App")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def healthcheck():
    print("App is up!")
    return "App is up!"

@app.get("/clear-data")
def clear_data():
    try:
        app.state.df = pl.DataFrame(schema= {"name": str, "date": pl.Datetime(time_unit="ms"), "message": str})
        app.state.user_list = set()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "Data Cleared!"

@app.get("/get-users")
def get_users():
    return [val for val in app.state.user_list]

@app.get("/get-dashboard")
def get_dashboard():
    print(app.state.df)
    return app.state.df.head(10).write_json()

@app.get("/get-top-messages")
def get_top_messages(username: str, n: int):
    return utils.getTopMessages(app.state.df, username, n).write_json()

@app.get("/get-longest-messages")
def get_longest_messages(username: str, n: int):
    return utils.getLongestMessages(app.state.df, username, n).write_json()

@app.post("/upload-messages-json/")
async def upload_messages_json(files: list[UploadFile] = File(...)):
    success_files = []
    failed_files = []
    rows_added = 0
    dfs_to_combine = []
    try:
        results = await asyncio.gather(*[parse_messages_file(file) for file in files])
        for result in results:
            if(result["status"] == "success"):
                success_files.append(result["filename"])
                dfs_to_combine.append(result["data"])
                rows_added += result["rows"]
                app.state.user_list.update(result["users"])
            else:
                failed_files.append(result["filename"])
        
        for frame in dfs_to_combine:
            async with app.state.df_lock:
                app.state.df = pl.concat([app.state.df, frame])
        
        return {"rows_added": rows_added, "total_rows": app.state.df.shape[0], "success_files": success_files, "failed_files": failed_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def parse_messages_file(file: UploadFile) -> dict:
    try:
        contents = await file.read()
        data = json.loads(contents.decode('utf-8'))
        messages = data['messages']
        users = [participant["name"] for participant in data['participants']]
        df_part = utils.parseJsonMessagesToDf(messages)
        return {"rows": df_part.shape[0], "filename": file.filename, "status": "success", "data": df_part, "users": users}
    
    except Exception as e:
        print(e)
        return {"rows": 0, "filename": file.filename, "status": "failed"}
    finally:
        await file.close()