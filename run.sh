#!/bin/bash
workdir=$1
outputfolder=$2
filename=$3


sudo docker run --rm --mount type=bind,src=$workdir,dst=/work -it  maweimarvin/mutator_src \
                        bash -c "python3 /srciror/scripts/mutationClang.py  /work/$outputfolder /work/$filename -I/srciror/llvm-build/Release+Asserts/lib/clang/3.8.0/include"


