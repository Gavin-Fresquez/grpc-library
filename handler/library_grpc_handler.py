from uuid import uuid4
from grpc import ServicerContext, StatusCode

from protogen import LibraryServicer, UpsertBookRequest, UpsertBookResponse, Error, ErrorCode
from mapper import book, bookProtoToModel, bookModelToProto
from controller import Library


class LibraryGRPCHandler(LibraryServicer):
    """LibraryServicer gRPC server implementation"""

    def __init__(self, controller: Library) -> None:
        self._library_controller = controller

    def CreateBook(
        self,
        request: UpsertBookRequest,
        context: ServicerContext
    ) -> UpsertBookResponse:
        if not request.book:
            err = Error('Invalid request', ErrorCode.ERR_CODE_BAD_REQUEST)
            context.set_code(StatusCode.INVALID_ARGUMENT)
            return UpsertBookResponse(err=err)
        if not request.book.uuid:
            request.book.uuid = str(uuid4())
        inserted_id = self._library_controller.add_book(bookProtoToModel(request.book))
        if not inserted_id:
            err = Error('Failed to add book', ErrorCode.ERR_CODE_INTERNAL_MALFUNCTION)
            context.set_code(StatusCode.INTERNAL)
            return UpsertBookResponse(err=err)
        return UpsertBookResponse(uuid=inserted_id)

    def UpdateBook(
        self,
        request: UpsertBookRequest,
        context: ServicerContext
    ):
        if not request.book:
            err = Error('Invalid request', ErrorCode.ERR_CODE_BAD_REQUEST)
            context.set_code(StatusCode.INVALID_ARGUMENT)
            return UpsertBookResponse(err=err)
        inserted_id = self._library_controller.update_book(bookProtoToModel(request.book))
        if not inserted_id:
            err = Error('Failed to update book', ErrorCode.ERR_CODE_INTERNAL_MALFUNCTION)
            context.set_code(StatusCode.INTERNAL)
            return UpsertBookResponse(err=err)
        return UpsertBookResponse(inserted_id)

    def CheckoutBook(self, request, context):
        return super().CheckoutBook(request, context)

    def ReturnBook(self, request, context):
        return super().ReturnBook(request, context)

    def GetBook(self, request, context):
        return super().GetBook(request, context)

    def ListBooks(self, request, context):
        return super().ListBooks(request, context)

    def DeleteBook(self, request, context):
        return super().DeleteBook(request, context)


