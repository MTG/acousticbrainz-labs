import yaml
import json
import os
import sys

def main(dirname):
    count = 0
    for root, dirs, files in os.walk(dirname):
        for f in files:
            if f.endswith("yaml"):
                continue
            count += 1
            if count % 500 == 0:
                print count
            fullpath = os.path.join(root, f)
            n, ex = os.path.splitext(fullpath)
            yamlpath = "%s.yaml" % n
            #print fullpath, "->", yamlpath
            if os.path.exists(yamlpath):
                continue
            with open(fullpath) as jfp:
                try:
                    j = json.load(jfp)
                    del j["metadata"]
                    with open(yamlpath, "w") as yfp:
                        yaml.safe_dump(j, yfp, encoding='utf-8', allow_unicode=True, default_flow_style=False)
                except ValueError:
                    print "Error loading json file"
                    print "", fullpath


if __name__ == "__main__":
    main(sys.argv[1])
