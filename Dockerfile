FROM braintwister/ubuntu-18.04 
USER root
RUN  apt-get update && apt-get install python && git config --global http.sslVerify false && git clone https://github.com/EOSIO/eos --recursive
COPY 0001-Changed-build-script-to-also-include-extra-clang-too.patch /root/eos/
COPY 0002-Changed-eosiocpp-script-to-dump-command-db-compile_c.patch /root/eos/
COPY smartcontract.py /root/eos/
RUN  cd eos && git checkout tags/dawn-v4.2.0 &&
git checkout -b test &&
git apply 0001-Changed-build-script-to-also-include-extra-clang-too.patch &&
git apply 0002-Changed-eosiocpp-script-to-dump-command-db-compile_c.patch &&
./eosio_bulid.sh &&
cd &&
mkdir my-llvm &&
cd my-llvm &&
mv /tmp/llvm-compiler/ .
EXPOSE 19000
EXPOSE 19001
