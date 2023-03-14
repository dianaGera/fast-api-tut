from fastapi import FastAPI

app = FastAPI()


def auth_required(handler):
    async def wrapper(*args, **kwargs):
        value = kwargs.get('value')

        # Do something with value

        value = 'test changed'
        return await handler(value)

    # Fix signature of wrapper
    import inspect
    wrapper.__signature__ = inspect.Signature(
        parameters = [
            # Use all parameters from handler
            *inspect.signature(handler).parameters.values(),

            # Skip *args and **kwargs from wrapper parameters:
            *filter(
                lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                inspect.signature(wrapper).parameters.values()
            )
        ],
        return_annotation = inspect.signature(handler).return_annotation,
    )

    return wrapper


def get_value():
    return 'test'


@app.get("/")
@auth_required
async def root(value:str=get_value()):
    return {"message": value}
