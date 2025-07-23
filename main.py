import grpc
from concurrent import futures

from repository import BookRepository, connect_db
from controller import Library
from handler import LibraryGRPCHandler
from protogen import LibraryServicer, add_LibraryServicer_to_server


DEFAULT_PORT = 50051
DEBUG_PORT = 50052


def build_grpc_server(servicer: LibraryServicer) -> grpc.Server:
    """Builds the grpc server with the specified library servicer"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LibraryServicer_to_server(servicer, server)
    return server

def register_ports(server: grpc.Server, *args) -> tuple[int]:
    """Registers all ports provided by args and returns all ports assigned"""
    ports = []
    for port in args:
        ports.append(server.add_insecure_port(f'[::]:{port}'))
    return tuple(ports)


if __name__ == '__main__':
    try:
        # setup api stack
        db = connect_db()
        repo = BookRepository(db)
        controller = Library(repo)
        handler = LibraryGRPCHandler(controller)

        # create grpc server
        server = build_grpc_server(handler)
        ports = register_ports(server, DEFAULT_PORT, DEBUG_PORT)
        server.start()
        print(f'server listening on ports {ports}')
        server.wait_for_termination()

    except Exception as e:
        print('Application failed to start', e)

