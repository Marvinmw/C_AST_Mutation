FROM ubuntu:16.04
RUN apt-get update
RUN apt-get --yes install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
RUN apt-get --yes install  python \
                           python-pip  \
                           python3     \
                           python3-pip     \
                           lib32z1-dev     \
                           git            \
                           make           \
                           vim            \
                           wget           \
                           gcc            \
                           g++
RUN pip install unidiff
RUN git clone https://github.com/TestingResearchIllinois/srciror.git
WORKDIR srciror
RUN ls
RUN rm -rf Demo && rm -rf Examples && rm -rf IRMutation && rm -rf PythonWrappers && rm -rf SRCMutation
COPY src ./
COPY example ./
COPY mutationClang.py ./
COPY Makefile ./
RUN chmod +x llvm-build.sh && ./llvm-build.sh

ENV SRCIROR_LLVM_BIN=$(pwd)/llvm-build/Release+Asserts/bin/
ENV SRCIROR_LLVM_INCLUDES=$(pwd)/llvm-build/Release+Asserts/lib/clang/3.8.0/include/
#RUN make
#ENV SRCIROR_SRC_MUTATOR=$(pwd)/build/mutator
