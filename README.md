- download docker `sudo docker pull maweimarvin/mutator_src`
- mutator.cpp is based from https://github.com/TestingResearchIllinois/srciror
- first - fourth order mutantion operator
- 使用 `run.sh` 产生 mutanted source code
    * 使用举例子 `./run.sh $(pwd)/scripts output intra_class_example.c`
    * 参数 1. `$(pwd)/scripts` 是 工作目录, 必须是全路径。
    * 参数 2. `output` 是 保存  mutanted source code 的目录, 这个参数是相对于 参数1 的相对路径。
    * 参数 3. `intra_class_example.c` 是 要要改变的代码文件， 这个参数是相对于 参数1 的相对路径。
    * 参数2 和 参数3的相对路径， 前面不要使用 `./` 。
    
 ============================================================================================
 
 - 如果想在本地使用CMakeLists.txt编译，`sudo apt install llvm-3.9` , `sudo install clang-3.9`, g++编译器版本 `>=5`。
    
    
