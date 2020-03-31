#!/usr/bin/env python
import os
CWD = os.path.dirname(os.path.abspath(__file__))

import os, sys, subprocess, shutil, time
import copy


def executeCommand(args, shell=False, debug=False):
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
    p = subprocess.Popen(args, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


def getChangedLines(patchfile, source_name):
    patch = PatchSet.from_filename(patchfile, encoding='utf-8')
    changed_lines = []
    for p in patch: #patchset
        fname = os.path.basename(p.source_file)
        if source_name in fname:
            for h in p: #hunk
                for line in h: #line
                    if line.is_added :
                        changed_lines.append(str(line.target_line_no+1))

    return changed_lines

def mutate(compiler, ext, mutator, args, compiler_include_flags, src_indices, outputfolder, prefix, cov_info=None):
    new_args = copy.deepcopy(args)
    for index in src_indices:
        src_file = args[index]
        #cov_info = getCoverageInfo(src_file)

        if not cov_info:
            print("no coverage info for the file: " + src_file + ", so assume wants to mutate all")
            cov_info = "all"
        command = mutator + " " + outputfolder + " " + prefix +" "+ src_file + " -coverage_info=" +  cov_info + " -- " + " ".join(args) + ' -I'  + compiler_include_flags.strip()
        print("THE ACTUAL COMMAND IS: " + command)
        out, err, my_time = executeCommand(command.split(),shell=False, debug= True)
        print(out)
        print(err)


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


def read_source_folder(workdir):
    source_srclist = []
    for f in  os.listdir(workdir):
        source_srclist.append(os.path.join(workdir, f))
    return source_srclist


def changeFilePathinPatch(patch, buggroup):
    with open(patch, 'r+', encoding='utf-8') as file:
        result = ''
        for line in file:
            if line.startswith('---'):
        # result += '--- ' + program + '\n'
               result += '--- ' + buggroup + '_tmp.c' + '\n'
            elif line.startswith('+++'):
        # result += '+++ ' + fixedFile + '\n'
               result += '+++ ' + buggroup +'_tmp.c' + '\n'
            else:
               result += line
    with open(patch, 'w', encoding='utf-8') as file:
        file.writelines(result)

def main():
    llvm_bin_dir = os.environ["SRCIROR_LLVM_BIN"] #/usr/lib/llvm-3.9/bin
    compiler_include_flags = os.environ["SRCIROR_LLVM_INCLUDES"] # Release+Asserts/lib/clang/3.8.0/include #
    clang = os.path.join(llvm_bin_dir, 'clang')
    mutator = os.environ["SRCIROR_SRC_MUTATOR"] # path to build/mutator
    work_dir = sys.argv[1]
    program_name = sys.argv[2]
    args_org = sys.argv[3:]
    source_srclist = read_source_folder(work_dir)

    for srcfolder in source_srclist:
        outputfolder = os.path.join(srcfolder, "mutation_patched")
        outputpatchesfolder = os.path.join(srcfolder, "mutation_patches")
        # print("patchfile  {}".format(patchfile))
        sourcefile = os.path.join(srcfolder, program_name+".c")
        args = [os.path.join(srcfolder, program_name+"_tmp.c")] + args_org

        shutil.rmtree( outputfolder, ignore_errors=True)
        os.makedirs(outputfolder, exist_ok=True)
        shutil.rmtree( outputpatchesfolder, ignore_errors=True)
        os.makedirs(outputpatchesfolder, exist_ok=True)
        shutil.copy(sourcefile,  os.path.join(srcfolder, program_name+"_tmp.c"))
        for patch_file in os.listdir(os.path.join(srcfolder, "patches")):
            patch_file_path = os.path.join(srcfolder,"patches", patch_file)
            changeFilePathinPatch(patch_file_path, program_name)
            shutil.copy(sourcefile,  os.path.join(srcfolder, program_name+"_tmp.c"))
            out, error, exec_time = executeCommand("cd "+srcfolder+" && " + 'patch --ignore-whitespace -p0 < ' + '\"' + patch_file_path + '\"', shell=True)
           # print(out)
            assert error is not None, print(error)
            changedlines = getChangedLines(patch_file_path, program_name)
            src_cov = ",".join(changedlines).strip(" ,\n")
            print(src_cov)
            #if len(changedlines) !=0 :
            #    write_code_area(changedlines, sourcefile)

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
                mutate(compiler, ext, mutator, args, compiler_include_flags, c_indices, outputfolder, patch_file, cov_info=src_cov)

            #print('Looking to compile the original: ' + str([compiler] + args))
            #out, err, my_time = executeCommand([compiler] + args, True)
            #return 1

        for gsrc in os.listdir(outputfolder):
            gsrc_path = os.path.join(outputfolder, gsrc)
            gpath  = os.path.join(outputpatchesfolder, gsrc)
            executeCommand("diff -u "+sourcefile+" "+gsrc_path+"  >  "+gpath+".patch", shell=True)


if __name__ == '__main__':
    main()
