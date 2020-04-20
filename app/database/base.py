# Import all the models, so that Base has them before being
# imported by Alembic
from .base_class import Base
from ..models.recording import Recording  # noqa
from ..models.result import Result  # noqa
from ..models.run import Run  # noqa
from ..models.value import Value  # noqa
from ..models.participant import Participant  # noqa
from ..models.song import Song  # noqa
from ..models.playlist import Playlist  # noqa
from ..models.sensor import Sensor  # noqa
from ..models.file import File  # noqa
