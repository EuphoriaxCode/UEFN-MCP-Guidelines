import sys,json
from mcp import call
def tool(ts,name,args=None):
    p={"tool_name":name,"arguments":args or {}}
    if ts: p["toolset_name"]=ts
    out=call("tools/call",{"name":"call_tool","arguments":p})
    j=json.loads(out)
    if "error" in j: return "ERR "+json.dumps(j["error"])
    r=j["result"]; s="\n".join(c.get("text",str(c)) for c in r.get("content",[]))
    return ("ISERROR " if r.get("isError") else "")+s
def describe(ts):
    j=json.loads(call("tools/call",{"name":"describe_toolset","arguments":{"toolset_name":ts}}))
    return "\n".join(c.get("text","") for c in j["result"]["content"])
if __name__=="__main__":
    if sys.argv[1]=="d": print(describe(sys.argv[2]))
    else:
        a=json.load(open(sys.argv[3],encoding="utf-8")) if len(sys.argv)>3 else {}
        print(tool(sys.argv[1],sys.argv[2],a))
