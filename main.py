from fastapi import FastAPI, Request
from tools.NmapWrapper import NmapWrapper
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

# NEW: POST endpoint for /scan/start
# noinspection D
@app.post("/scan/start")
async def start_scan(request: Request):
    body = await request.json()

    if body["tool"].lower() == "nmap":
        target = body.get("target")
        flags = body.get("flags", [])
        arguments = NmapWrapper.flags_to_arguments(flags)
        print(f"Running nmap with target={target} and arguments={arguments}")
        nmap = NmapWrapper()
        results = nmap.scan(target, arguments)
        return {"results": results}
    return {"error": "Unknown or unsupported tool"}