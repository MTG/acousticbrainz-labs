import msgpack
import json
import sys

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

if __name__=="__main__":
    filename = sys.argv[1]
    json_data = open(filename).read()
    data = json.loads(json_data)
    data = convert(data)
    msg_data = msgpack.packb(data)
    open("output.msgpack","w").write(msg_data)
    
