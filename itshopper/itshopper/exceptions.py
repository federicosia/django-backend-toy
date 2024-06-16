from ninja.errors import ValidationError
from ninja import NinjaAPI

api = NinjaAPI(title="IT-Shopper", description="Backend documentation", version="0.1")


@api.exception_handler(ValidationError)
def validation_errors(request, exception: ValidationError):
    result: dict = dict()
    for index, error in enumerate(exception.errors):
        result[index] = dict()
        match error.get("type"):
            case "missing":
                result[index]["error_type"] = "missing param"
                result[index]["field"] = error.get("loc")[-1]
            case _:
                return "Something went wrong with formatting ValidationError..."
    print(f"Eccezione: {exception.errors}")
    print(f"Risultato parsato: {result}")
    return api.create_response(request, {"details": result}, status=422)
