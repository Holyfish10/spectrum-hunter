from typing import Union

from annotated_types.test_cases import cases
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def read_root():
    return {"message": "pong"}


@app.get("/scans/{tool}")
def read_item(tool: str):
        response = ""
        match tool:
            case "nmap":
                from tools.NmapWrapper import NmapWrapper as nmap
                nmap.scan()
                response = {"message":"nmap scan started"}
            case "zap":
                response = {"message": "zap"}
            case "whois":
                response = {"message": "whois"}
        return response
