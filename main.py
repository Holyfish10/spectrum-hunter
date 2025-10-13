from fastapi import FastAPI, Request
from pydantic.v1.utils import to_lower_camel
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
@app.post("/scan/start")
async def start_scan(request: Request):
    body = await request.json()
    print("Received scan start POST request with body:", body)
    match body["tool"].lower():
        case "nmap":
            data = await request.json()
            scan = data.get("scan", {})
            target = scan.get("target")
            arguments = ""
            # If arguments is a dict or JSON string, parse/convert as needed
            if scan.get("arguments"):
                if isinstance(scan["arguments"], str):
                    import json
                    try:
                        arg_data = json.loads(scan["arguments"])
                        if arg_data.get("ports"):
                            arguments += f"-p {arg_data['ports']} "
                    except Exception:
                        arguments = scan["arguments"]  # Use as-is if not JSON
                elif isinstance(scan["arguments"], dict):
                    arg_data = scan["arguments"]
                    if arg_data.get("ports"):
                        arguments += f"-p {arg_data['ports']} "
                    # Add more logic as above
            else:
                arguments = '-n -sP'  # default scan?

            # Actually run the scan
            from tools.NmapWrapper import NmapWrapper as NmapWrapper
            nmap = NmapWrapper()
            print(f"Running nmap with target={target}, arguments={arguments}")
            results = nmap.scan(target, arguments)
            return {"results": results}
    return None