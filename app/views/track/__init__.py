from fastapi import APIRouter
from fastapi.params import Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_502_BAD_GATEWAY,
)

from app.schemas.base import (
    APIErrorResponse,
    APIResponse,
    APIResponsePaginated
)
from app.schemas.cargo import (
    CargoResponseAlreadyDelivered,
    CargoResponseNotFound
)
from app.schemas.location import LocationResponseNotFound
from app.schemas.track import (
    TrackRequest,
    TrackResponse,
    TrackResponseDuplicated,
    TrackResponseNotDeletable,
    TrackResponseNotFound
)
from app.schemas.vessel import VesselResponseNotFound
from app.views.track.create_track import create_track
from app.views.track.delete_track import delete_track
from app.views.track.get_track import get_track
from app.views.track.list_tracks import list_tracks
from app.views.track.update_track import update_track

TAG = 'tracks'

tracks_router = APIRouter()

tracks_router.add_api_route(
    endpoint=create_track,
    methods=['POST'],
    name='create_track',
    path='',
    response_model=APIResponse[TrackResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[
                CargoResponseNotFound
                |LocationResponseNotFound
                |VesselResponseNotFound
            ]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[
                CargoResponseAlreadyDelivered
                |TrackResponseDuplicated
            ]
        },
    },
    status_code=HTTP_201_CREATED,
    summary='Create new tracking information',
    tags=[TAG]
)

tracks_router.add_api_route(
    endpoint=get_track,
    methods=['GET'],
    name='get_track',
    path='/{track_id}',
    response_model=APIResponse[TrackResponse],
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[TrackResponseNotFound]
        }
    },
    status_code=HTTP_200_OK,
    summary='Retrieve track info by ID.',
    tags=[TAG]
)

tracks_router.add_api_route(
    endpoint=list_tracks,
    methods=['GET'],
    name='list_tracks',
    path='',
    response_model=APIResponsePaginated[TrackResponse],
    status_code=HTTP_200_OK,
    summary='Retrieves tracks applying filters.',
    tags=[TAG]
)

tracks_router.add_api_route(
    endpoint=delete_track,
    methods=['DELETE'],
    name='delete_track',
    path='/{track_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[TrackResponseNotFound]
        },
        HTTP_409_CONFLICT: {
            'model': APIErrorResponse[TrackResponseNotDeletable]
        }
    },
    summary='Deletes a specific track by ID.',
    tags=[TAG]
)

tracks_router.add_api_route(
    endpoint=update_track,
    methods=['PATCH'],
    name='update_track',
    path='/{track_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {
            'model': APIErrorResponse[TrackResponseNotFound]
        }
    },
    summary='Updates an existing track',
    tags=[TAG]
)
