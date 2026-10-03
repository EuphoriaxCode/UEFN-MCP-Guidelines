import json,sys,urllib.request,os
URL="http://127.0.0.1:8000/mcp"
SF=os.path.join(os.path.dirname(__file__),"sid.txt")
def post(body,sid=None):
    h={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"]=sid
    r=urllib.request.urlopen(urllib.request.Request(URL,json.dumps(body).encode(),h),timeout=600)
    return r.headers.get("Mcp-Session-Id"),r.read().decode("utf-8","replace")
def sid():
    if os.path.exists(SF): return open(SF).read().strip()
    s,_=post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cc","version":"1"}}})
    post({"jsonrpc":"2.0","method":"notifications/initialized"},s)
    open(SF,"w").write(s); return s
def call(method,params):
    s=sid()
    try: _,b=post({"jsonrpc":"2.0","id":2,"method":method,"params":params},s)
    except Exception as e:
        os.remove(SF); s=sid(); _,b=post({"jsonrpc":"2.0","id":2,"method":method,"params":params},s)
    return b
if __name__=="__main__":
    m=sys.argv[1]
    p=json.loads(sys.argv[2]) if (len(sys.argv)>2 and m!="tool") else {}
    if m=="tool":
        args=json.load(open(sys.argv[3],encoding="utf-8")) if len(sys.argv)>3 else {}
        out=call("tools/call",{"name":sys.argv[2],"arguments":args})
        try:
            j=json.loads(out)
            for c in j.get("result",{}).get("content",[]): print(c.get("text",c))
            if "error" in j: print(j["error"])
            if j.get("result",{}).get("isError"): print("ISERROR")
        except Exception: print(out)
    else: print(call(m,p))
