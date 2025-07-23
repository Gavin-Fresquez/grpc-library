.PHONY: gen-proto-exports

PROTO_SRC = $(wildcard proto/*)
PROTO_OUTPUT_DIR = protogen
SCRIPTS_DIR = scripts

compile-proto: gen-proto-exports
	@echo "Compiling protobuf files..."
	@$(foreach file,$(PROTO_SRC), python -m grpc_tools.protoc -Iproto --python_out=protogen --pyi_out=protogen --grpc_python_out=protogen $(file))
	@echo "Fixing imports in generated gRPC files..."
	@sed -i'' -e 's/^import \(.*_pb2\)/from . import \1/' protogen/*_pb2_grpc.py
	@echo "Creating __init__.py in .proto directory..."

gen-proto-exports:
	@: > $(PROTO_OUTPUT_DIR)/__init__.py
	@python $(SCRIPTS_DIR)/gen-proto-exports.py $(shell find $(PROTO_SRC) -maxdepth 1 -type f -print0 | xargs -0)
	@echo "" >> $(PROTO_OUTPUT_DIR)/__init__.py

