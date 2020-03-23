#!/bin/bash
workdir=$1
prgname=$2

#example ./run_new.sh ./introclass3 smallest
sudo docker run --rm --mount type=bind,src=$workdir,dst=/work -it --user 1000:1000   maweimarvin/mutator_src \
                       bash -c "python3 /srciror/scripts/mutationClang_intraclass.py  /work ${prgname} -I/srciror/llvm-build/Release+Asserts/lib/clang/3.8.0/include"


#/home/wei/CLionProjects/C_AST_Mutation/introclass3 smallest  -I/usr/include/clang/3.9.1/include -I/usr/lib/llvm-3.9/include -I/usr/lib/llvm-3.9/include