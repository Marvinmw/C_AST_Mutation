#!/usr/bin/env python
import shutil
import os
CWD = os.path.dirname(os.path.abspath(__file__))

import os, sys, subprocess, shutil, time, copy, fnmatch
from collections import defaultdict
import copy

CWD = os.path.dirname(os.path.abspath(__file__))

def executeCommand(args, debug=False):
    """ Executes a command and times it.
        Args:
             args: a list of strings that constitute the bash command.
             debug: boolean flag, if true, prints the output to the commandline
        Returns:
             out:  the output of running the command
             error: the error resulting from the command, if any.
             exec_time: the time spent to execute the command.
    """
    start_time = time.time()
    print(args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    end_time = time.time()
    out = decode(out)
    error = decode(err)
    if debug == True:
        print (str(args))
        print (out)
        print (error)
    exec_time = str(end_time - start_time)
    return out, error, exec_time


def decode(string):
    return string.decode('utf8', 'ignore')


from unidiff import PatchSet
import os
import json
def getChangedLines(patchfile, source_name):
    patch = PatchSet.from_filename(patchfile, encoding='utf-8')
    changed_lines = []
    for p in patch: #patchset
        fname = os.path.basename(p.source_file)
        if source_name in fname:
            for h in p: #hunk
                for line in h: #line
                    if line.is_added :
                        changed_lines.append(source_name+':'+str(line.target_line_no+1))

    return changed_lines

def mutate(compiler, ext, mutator, args, compiler_include_flags, src_indices, outputfolder, prefix="mutant"):
    new_args = copy.deepcopy(args)
    for index in src_indices:
        src_file = args[index]
        cov_info = getCoverageInfo(src_file)

        if not cov_info:
            print("no coverage info for the file: " + src_file + ", so assume wants to mutate all")
            cov_info = "all"
        command = mutator + " " + outputfolder + " "+prefix+" "+ src_file + " -coverage_info=" +  cov_info + " -- " + " ".join(args) + ' -I'  + compiler_include_flags.strip()
        print("THE ACTUAL COMMAND IS: " + command)
        out, err, my_time = executeCommand(command.split(), True)


def getCoverageInfo(src_file):
    print("THE CURRENT DIRECTORY IS: " + os.getcwd())
    file_name = os.path.basename(src_file) + ".cov"
    cov_file = os.path.join(getSummaryDir(), "coverage")    # Assume only one big coverage file, because only one tool at a time
    if not os.path.isfile(cov_file):
        return ""
    with open(cov_file, 'r') as in_file:
        lines = in_file.readlines()
    for line in lines:
        file_name = line.split(":")[0]
        if file_name != src_file:
            continue
        coverage = line.split(":")[1].strip(" ,\n")
        return coverage;


def getSummaryDir():
    # make the summary directory if does not exist
    # also makes the ir-coverage/ directory
    summaryDir = os.path.join(os.getenv("HOME"), ".srciror")
    if not os.path.exists(summaryDir):
        os.makedirs(summaryDir)
    return summaryDir

def write_code_area(changedlines, codefile):
    if not os.path.isfile('~/.srciror/coverage'):
        os.makedirs('~/.srciror', exist_ok=True)
    with open('~/.srciror/coverage', 'w') as fp :
         fp.write("{}:{}\n".format(codefile, ",".join(changedlines)))


def main():
    llvm_bin_dir = os.environ["SRCIROR_LLVM_BIN"]
    compiler_include_flags = os.environ["SRCIROR_LLVM_INCLUDES"] # Release+Asserts/lib/clang/3.8.0/include
    clang = os.path.join(llvm_bin_dir, 'clang')
    mutator = os.environ["SRCIROR_SRC_MUTATOR"] # path to build/mutator
    outputfolder = sys.argv[1]
    # print("patchfile  {}".format(patchfile))
    sourcefile = sys.argv[2]
    sourcecode = os.path.basename(sourcefile)
    print("sourcefile {}".format(sourcefile))

    srcdir = os.path.dirname(sourcefile)
    shutil.rmtree(os.path.join(srcdir, outputfolder), ignore_errors=True)
    os.makedirs(os.path.join(srcdir, outputfolder), exist_ok=True)

    # changedlines = getChangedLines(patchfile, sourcecode) if os.path.isfile(patchfile) else []
    # if len(changedlines) !=0 :
    #     write_code_area(changedlines, sourcefile)

    args = sys.argv[2:]

    if '-fstack-usage' in args: # TODO: What is -fstack-usage?
        args.remove('-fstack-usage')
    compiler = clang
    print('logging compile flags: ' + ' '.join(args))

    # if the build system is checking for the version flags, we don't mess it up, just delegate to the compiler
    if "--version" in args or "-V" in args:
        out, err, my_time = executeCommand([compiler] + args, True)
        return 1

    # mutate
    c_indices = [ i for i, word in enumerate(args) if word.endswith('.c')]  # Mutating only .c files
    if c_indices:
        ext = ".c"
        mutate(compiler, ext, mutator, args, compiler_include_flags, c_indices, outputfolder)

    #print('Looking to compile the original: ' + str([compiler] + args))
    #out, err, my_time = executeCommand([compiler] + args, True)
    return 1

if __name__ == '__main__':
    main()
