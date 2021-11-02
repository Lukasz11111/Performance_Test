import argparse
import json
JSON_RAPORT_PATH="./test/stress.json"

parser = argparse.ArgumentParser(description='Process some integers.')


parser.add_argument('-Recordings',  nargs='?')
parser.add_argument('-Trace_Span',  nargs='?')
parser.add_argument('-TotalJmeter',  nargs='?')

args=parser.parse_args().__dict__

filtered = {k: v for k, v in args.items() if v is not None}
args.clear()
args.update(filtered)


with open(JSON_RAPORT_PATH) as f:
    json_dict = json.load(f)


for key, value in args.items():
    json_dict[key]=value




with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
    json.dump(json_dict, x, ensure_ascii=False, indent=4)