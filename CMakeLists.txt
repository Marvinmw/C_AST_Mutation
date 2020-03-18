cmake_minimum_required(VERSION 3.10)
project(mutator)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_COMPILER g++)
find_package(LLVM 3.9 CONFIG REQUIRED)
set(Clang_DIR /usr/share/llvm-3.9/cmake)
set(CLANG_INSTALL_PREFIX /usr/lib/llvm-3.9)
set(CLANG_EXPORTED_TARGETS "clangBasic;clangLex;clangParse;clangAST;clangDynamicASTMatchers;clangASTMatchers;clangSema;clangCodeGen;clangAnalysis;clangEdit;clangRewrite;clangARCMigrate;clangDriver;clangSerialization;clangRewriteFrontend;clangFrontend;clangFrontendTool;clangToolingCore;clangTooling;clangIndex;clangStaticAnalyzerCore;clangStaticAnalyzerCheckers;clangStaticAnalyzerFrontend;clangFormat;clangApplyReplacements;clangRename;clangTidy;clangTidyPlugin;clangTidyBoostModule;clangTidyCERTModule;clangTidyLLVMModule;clangTidyCppCoreGuidelinesModule;clangTidyGoogleModule;clangTidyMiscModule;clangTidyModernizeModule;clangTidyPerformanceModule;clangTidyReadabilityModule;clangTidyUtils;clangQuery;clangIncludeFixer;findAllSymbols;libclang")
set(CLANG_CMAKE_DIR "${CLANG_INSTALL_PREFIX}/lib/cmake/clang")

# Provide all our library targets to users.
include("${CLANG_CMAKE_DIR}/ClangTargets.cmake")
message("Clang Include DIRS ${CLANG_INCLUDE_DIRS}")
message("CMAKE CLANG_INSTALL_PREFIX path ${CLANG_INSTALL_PREFIX}")

# Compile Options
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -fpic -Wall -Wextra -fno-rtti" )
add_definitions(${LLVM_DEFINITIONS})

message("SRCIROR_LLVM_BIN ${LLVM_BIN}")
message("SRCIROR_LLVM_INCLUDES ${LLVM_INCLUDES}")

message("CMAKE CLANG_INSTALL_PREFIX path ${CLANG_INSTALL_PREFIX}")

execute_process(
		COMMAND export SRCIROR_LLVM_BIN=$(/usr/bin/llvm-config-3.9 --libdir)
		OUTPUT_VARIABLE LLVM_BIN
		OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
		COMMAND export SRCIROR_LLVM_INCLUDES=$( /usr/bin/llvm-config-3.9 --includedir)
		OUTPUT_VARIABLE LLVM_INCLUDES
		OUTPUT_STRIP_TRAILING_WHITESPACE
)

#set(SRCIROR_LLVM_BIN ${LLVM_BIN})
#set(SRCIROR_LLVM_INCLUDES ${LLVM_INCLUDES})

execute_process(
        COMMAND /usr/bin/llvm-config-3.9 --cxxflags
        OUTPUT_VARIABLE LLVM_CXXFLAGS
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
        COMMAND /usr/bin/llvm-config-3.9 --ldflags  --libs  --system-libs
        OUTPUT_VARIABLE LLVM_LDFLAGS
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

include_directories(${CLANG_INCLUDEDIR})
add_executable(mutator src/mutator.cpp)
#set_target_properties(mutator PROPERTIES COMPILE_FLAGS "${LLVM_CXXFLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${LLVM_CXXFLAGS}")
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)
#set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${LLVM_CXXFLAGS}")
message("LLVM_LDFLAGS ${LLVM_LDFLAGS}")
#set_target_properties(mutator PROPERTIES COMPILE_FLAGS "${LLVM_CXXFLAGS}")
llvm_map_components_to_libnames(llvm_libs support core irreader)
target_link_libraries(mutator
		clangAnalysis
		clangBasic
		clangDriver
		clangEdit
		clangFrontend
		clangFrontendTool
		clangLex
		clangParse
		clangSema
		clangEdit
		clangASTMatchers
		clangRewrite
		clangRewriteFrontend
		clangStaticAnalyzerFrontend
		clangStaticAnalyzerCheckers
		clangStaticAnalyzerCore
		clangSerialization
		clangToolingCore
		clangTooling
		LLVM
		)
#target_link_libraries(mutator
#		LLVMSupport
#		)
