# Lazy container to avoid circular import at module load
def get_container():
    from app.src.app import get_container
    return get_container()
