FROM braintwister/ubuntu-18.04 
USER root
RUN  cd /root && apt-get update && apt-get install apt-utils && apt-get install -y python && git config --global http.sslVerify false && git clone https://github.com/EOSIO/eos --recursive && grep -rl "7000" /root/eos/scripts | xargs sed -i 's/7000/3000/g' 
COPY 0001-Changed-build-script-to-also-include-extra-clang-too.patch /root/eos/
COPY 0002-Changed-eosiocpp-script-to-dump-command-db-compile_c.patch /root/eos/
COPY smartcontract.py /root/eos/
RUN  cd /root && cd eos && git checkout -f tags/dawn-v4.2.0 && git checkout -f -b test && git apply 0001-Changed-build-script-to-also-include-extra-clang-too.patch && git apply 0002-Changed-eosiocpp-script-to-dump-command-db-compile_c.patch && ./eosio_bulid.sh && cd && mkdir my-llvm && cd my-llvm && mv /tmp/llvm-compiler/ .
EXPOSE 19000
EXPOSE 19001
