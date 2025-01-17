from datetime import datetime, timedelta, tzinfo
import json
import os
from pathlib import Path
import sys
from time import tzname
from typing import List

from nadeo_event_api.api.structure.settings.plugin_settings import (
    QualifierPluginSettings,
)

from pytz import timezone, utc

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.structure.settings.script_settings import (
    CupSpecialScriptSettings,
    TimeAttackScriptSettings,
)
from nadeo_event_api.api.structure.settings.plugin_settings import QualifierPluginSettings
from nadeo_event_api.api.structure.round.qualifier import Qualifier, QualifierConfig
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.enums import LeaderboardType, ScriptType
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import (
    MatchParticipantMatchSpot,
    QualificationMatchSpot,
)
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.constants import CLUB_AUTO_EVENTS_STAGING


def get_round_config(
    map_pool: List[Map],
) -> RoundConfig:
    return RoundConfig(
        map_pool=map_pool,
        script=ScriptType.CUP_CLASSIC,
        max_players=4,
        script_settings=CupSpecialScriptSettings(
            points_repartition="10,6,4,3",
            points_limit=120,
            finish_timeout=15,
            rounds_per_map=4,
            number_of_winners=2,
            warmup_number=1,
            warmup_duration=60,
        ),
    )


def get_match_from_prev_round(
    prev_round: int,
    prev_first_seed_match: int,
    prev_first_seed_rank: int,
    prev_second_seed_match: int,
    prev_second_seed_rank: int,
    prev_third_seed_match: int,
    prev_third_seed_rank: int,
    prev_fourth_seed_match: int,
    prev_fourth_seed_rank: int,
) -> Match:
    return Match(
        spots=[
            MatchParticipantMatchSpot(
                prev_round, prev_first_seed_match, prev_first_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_second_seed_match, prev_second_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_third_seed_match, prev_third_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_fourth_seed_match, prev_fourth_seed_rank
            ),
        ]
    )


def get_match_with_round(
    prev_first_seed_round: int,
    prev_first_seed_match: int,
    prev_first_seed_rank: int,
    prev_second_seed_round: int,
    prev_second_seed_match: int,
    prev_second_seed_rank: int,
    prev_third_seed_round: int,
    prev_third_seed_match: int,
    prev_third_seed_rank: int,
    prev_fourth_seed_round: int,
    prev_fourth_seed_match: int,
    prev_fourth_seed_rank: int,
) -> Match:
    return Match(
        spots=[
            MatchParticipantMatchSpot(
                prev_first_seed_round, prev_first_seed_match, prev_first_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_second_seed_round, prev_second_seed_match, prev_second_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_third_seed_round, prev_third_seed_match, prev_third_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_fourth_seed_round, prev_fourth_seed_match, prev_fourth_seed_rank
            ),
        ]
    )


def get_match_from_quali(
    first_seed: int,
    second_seed: int,
    third_seed: int,
    fourth_seed: int,
) -> Match:
    return Match(
        spots=[
            QualificationMatchSpot(0, first_seed),
            QualificationMatchSpot(0, second_seed),
            QualificationMatchSpot(0, third_seed),
            QualificationMatchSpot(0, fourth_seed),
        ]
    )


def get_gs_round_1(
    quali_start_date: datetime,
    round_start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 1",
        start_date=round_start_date,
        end_date=round_start_date + timedelta(minutes=40),
        matches=[
            get_match_from_quali(1, 17, 48, 64),
            get_match_from_quali(8, 24, 41, 57),
            get_match_from_quali(9, 25, 40, 56),
            get_match_from_quali(16, 32, 33, 49),
            get_match_from_quali(2, 18, 47, 63),
            get_match_from_quali(7, 23, 42, 58),
            get_match_from_quali(10, 26, 39, 55),
            get_match_from_quali(15, 31, 34, 50),
            get_match_from_quali(3, 19, 46, 62),
            get_match_from_quali(6, 22, 43, 59),
            get_match_from_quali(11, 27, 38, 54),
            get_match_from_quali(14, 30, 35, 51),
            get_match_from_quali(4, 20, 45, 61),
            get_match_from_quali(5, 21, 44, 60),
            get_match_from_quali(12, 28, 37, 53),
            get_match_from_quali(13, 29, 36, 52),
        ],
        config=get_round_config(map_pool=map_pool),
        qualifier=Qualifier(
            name="Seeding Qualifier",
            start_date=quali_start_date,
            end_date=quali_start_date + timedelta(minutes=40),
            leaderboard_type=LeaderboardType.SUMSCORE,
            config=QualifierConfig(
                map_pool=map_pool,
                script=ScriptType.TIME_ATTACK,
                plugin_settings=QualifierPluginSettings(
                    use_playlist_complete=True,
                ),
                script_settings=TimeAttackScriptSettings(
                    warmup_number=1,
                    warmup_duration=20,
                    time_limit=360,
                ),
            ),
        ),
    )


def get_gs_round_2(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 2",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[
            get_match_from_prev_round(0, 0, 1, 1, 2, 2, 1, 3, 2),
            get_match_from_prev_round(0, 0, 2, 1, 1, 2, 2, 3, 1),
            get_match_from_prev_round(0, 0, 3, 1, 4, 2, 3, 3, 4),
            get_match_from_prev_round(0, 0, 4, 1, 3, 2, 4, 3, 3),
            get_match_from_prev_round(0, 4, 1, 5, 2, 6, 1, 7, 2),
            get_match_from_prev_round(0, 4, 2, 5, 1, 6, 2, 7, 1),
            get_match_from_prev_round(0, 4, 3, 5, 4, 6, 3, 7, 4),
            get_match_from_prev_round(0, 4, 4, 5, 3, 6, 4, 7, 3),
            get_match_from_prev_round(0, 8, 1, 9, 2, 10, 1, 11, 2),
            get_match_from_prev_round(0, 8, 2, 9, 1, 10, 2, 11, 1),
            get_match_from_prev_round(0, 8, 3, 9, 4, 10, 3, 11, 4),
            get_match_from_prev_round(0, 8, 4, 9, 3, 10, 4, 11, 3),
            get_match_from_prev_round(0, 12, 1, 13, 2, 14, 1, 15, 2),
            get_match_from_prev_round(0, 12, 2, 13, 1, 14, 2, 15, 1),
            get_match_from_prev_round(0, 12, 3, 13, 4, 14, 3, 15, 4),
            get_match_from_prev_round(0, 12, 4, 13, 3, 14, 4, 15, 3),
        ],
        config=get_round_config(map_pool=map_pool),
    )


def get_gs_round_3(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 3",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[
            get_match_from_prev_round(1, 0, 1, 0, 2, 1, 1, 1, 2),
            get_match_from_prev_round(1, 0, 3, 1, 4, 2, 1, 3, 2),
            get_match_from_prev_round(1, 0, 4, 1, 3, 2, 2, 3, 1),
            get_match_from_prev_round(1, 4, 1, 4, 2, 5, 1, 5, 2),
            get_match_from_prev_round(1, 4, 3, 5, 4, 6, 1, 7, 2),
            get_match_from_prev_round(1, 4, 4, 5, 3, 6, 2, 7, 1),
            get_match_from_prev_round(1, 8, 1, 8, 2, 9, 1, 9, 2),
            get_match_from_prev_round(1, 8, 3, 9, 4, 10, 1, 11, 2),
            get_match_from_prev_round(1, 8, 4, 9, 3, 10, 2, 11, 1),
            get_match_from_prev_round(1, 12, 1, 12, 2, 13, 1, 13, 2),
            get_match_from_prev_round(1, 12, 3, 13, 4, 14, 1, 15, 2),
            get_match_from_prev_round(1, 12, 4, 13, 3, 14, 2, 15, 1),
        ],
        config=get_round_config(map_pool=map_pool),
    )


def get_gs_round_4(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="GS - Round 4",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[
            get_match_from_prev_round(2, 1, 1, 1, 2, 2, 1, 2, 2),
            get_match_from_prev_round(2, 4, 1, 4, 2, 5, 1, 5, 2),
            get_match_from_prev_round(2, 7, 1, 7, 2, 8, 1, 8, 2),
            get_match_from_prev_round(2, 10, 1, 10, 2, 11, 1, 11, 2),
        ],
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_1(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 1",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[
            get_match_with_round(2, 0, 3, 2, 9, 4, 3, 2, 1, 3, 1, 2),
            get_match_with_round(2, 3, 3, 2, 6, 4, 3, 3, 1, 3, 0, 2),
            get_match_with_round(2, 6, 3, 2, 3, 4, 3, 0, 1, 3, 3, 2),
            get_match_with_round(2, 9, 3, 2, 0, 4, 3, 1, 1, 3, 2, 2),
        ],
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_2(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 2",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[
            get_match_with_round(4, 0, 1, 4, 1, 2, 4, 2, 2, 4, 3, 1),
            get_match_with_round(4, 0, 2, 4, 1, 1, 4, 2, 1, 4, 3, 2),
            get_match_with_round(4, 0, 3, 4, 1, 4, 4, 2, 4, 4, 3, 3),
            get_match_with_round(4, 0, 4, 4, 1, 3, 4, 2, 3, 4, 3, 4),
        ],
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_3(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 3",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[
            get_match_with_round(5, 0, 3, 5, 1, 4, 5, 2, 1, 5, 3, 2),
            get_match_with_round(5, 0, 4, 5, 1, 3, 5, 2, 2, 5, 3, 1),
        ],
        config=get_round_config(map_pool=map_pool),
    )


def get_swiss_round_4(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Swiss - Round 4",
        start_date=start_date,
        end_date=start_date + timedelta(minutes=40),
        matches=[], # CD will add the matches if necessary as tie breaker
        config=get_round_config(map_pool=map_pool),
    )


### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "PATC Qualifier"
club_id = 68298 
campaign_id = 58789  # Uses maps from a campaign

registration_start = datetime.utcnow() + timedelta(minutes=1)
gs_r1_quali_start = datetime(2024, 1, 27, 21, 0)
gs_r1_start = datetime(2024, 1, 27, 21, 45)
gs_r2_start = datetime(2024, 1, 27, 22, 30)
gs_r3_start = datetime(2024, 1, 27, 23, 15)
gs_r4_start = datetime(2024, 1, 28, 0, 0)
swiss_r1_start = datetime(2024, 1, 28, 21, 0)
swiss_r2_start = datetime(2024, 1, 28, 21, 45)
swiss_r3_start = datetime(2024, 1, 28, 22, 30)
swiss_r4_start = datetime(2024, 1, 28, 23, 15)
### NOTE END ###

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

gs_r1 = get_gs_round_1(gs_r1_quali_start, gs_r1_start, map_pool)
gs_r2 = get_gs_round_2(gs_r2_start, map_pool)
gs_r3 = get_gs_round_3(gs_r3_start, map_pool)
gs_r4 = get_gs_round_4(gs_r4_start, map_pool)
swiss_r1 = get_swiss_round_1(swiss_r1_start, map_pool)
swiss_r2 = get_swiss_round_2(swiss_r2_start, map_pool)
swiss_r3 = get_swiss_round_3(swiss_r3_start, map_pool)
swiss_r4 = get_swiss_round_4(swiss_r4_start, map_pool)

# Create and post the event
event = Event(
    name=event_name,
    club_id=club_id,
    registration_start_date=registration_start,
    registration_end_date=gs_r1_quali_start,
    rounds=[gs_r1, gs_r2, gs_r3, gs_r4, swiss_r1, swiss_r2, swiss_r3, swiss_r4],
)
event.post()
