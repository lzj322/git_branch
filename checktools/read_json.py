import os
import time
import json

import argparse

parser = argparse.ArgumentParser(description = 'read and transcribe regression test')

#parser.add_argument('-i','--input_file', type=str, default='D:/data/temp/first_765.json',
parser.add_argument('-i','--input_file', type=str, default='D:/TDownloads/Jenny_QU_Outputs_765.txt',
    help='input file')
parser.add_argument('-o','--output_file', type=str, default='D:/data/temp/regression765.tsv',
    help='output file')
parser.add_argument('-b','--badlines_file', type=str, default='D:/data/temp/badquerys.tsv',
    help='output file')
#parser.add_argument('--interval', type=int, default='30',
#    help='print intervals')
args=parser.parse_args()

def main():
    interval =30
    cnt = 0
    start_time = time.time()
    last_time = time.time()
    with open(args.output_file, 'w') as fout:
        with open(args.badlines_file, 'w') as fbad:
            with open(args.input_file, 'r') as fin:
                load_dict = json.load(fin)
                # 1. outputs
                outputs = load_dict['outputs']
                # 2. outputs has N arrays
                # 3. each output has 4 keys: 'Keys','Context','LogBlob','DebugBlob'
                for object in outputs:
                    cnt += 1
                    Context = object['Context']
                    # 4. context has 63 keys:
                    QuInput = Context['QuInput'] 
                    Rawquery = QuInput['RawQuery']
                    NormalizedQuery = QuInput['NormalizedQuery']
                    EncodedQueryFeatures = Context['EncodedQueryFeatures']
                    # EncodedVector
                    if len(EncodedQueryFeatures)==0:
                        wline = Rawquery.replace("\n","\\n") + '\t' + NormalizedQuery + '\n'
                        fbad.write(wline)
                        continue
                    EncodedVector = EncodedQueryFeatures['2']['EncodedVector']
                    Vector = str(EncodedVector)[1:-1]
                    wline = NormalizedQuery + '\t'+ Vector + '\n'
                    # elapse times
                    if cnt % interval == 0:
                        elapsed = int(time.time()-last_time)
                        print('== {} lines processed. || {:.2f} s per  ====='
	                                                    .format(cnt,elapsed))
                        last_time = time.time()
                    fout.write(wline)
                
def totalline():
    with open(args.input_file, 'r') as fin:
        load_dict = json.load(fin)
        outputs = load_dict['outputs']
        print(len(outputs))

if __name__ == "__main__":
    main()
    #totalline()