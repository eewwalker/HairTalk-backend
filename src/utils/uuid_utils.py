import uuid

def parse_uuid(user_id):
    """
    Convert a string to UUID, handling different formats.
    Returns UUID object if valid, raises ValueError if invalid
    """
    try:
        if user_id is None:
            raise ValueError("user_id cannot be None")
    # Convert to string first in case it's passed as another type
        user_uuid = uuid.UUID(str(user_id))
        return user_uuid

    except (ValueError, AttributeError, TypeError) as e:
        # Raise the error instead of just printing
        print('Error parsing uuid ', e)
        raise ValueError(f"Invalid UUID format for user_id: {user_id}. Error: {str(e)}")