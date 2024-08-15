cd protobuf

cd tasks
protoc --python_betterproto_out=. *.proto
cd ..

cd ticket
protoc --python_betterproto_out=. *.proto
cd ..

cd user
protoc --python_betterproto_out=. *.proto
cd ..

cd ..