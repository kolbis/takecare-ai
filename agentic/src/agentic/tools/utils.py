# Lazy container to avoid circular import at module load
def get_container():
    from app.src.app import get_container as _get_container
    return _get_container()
