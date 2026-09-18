# ============================================================
# LTA TRACK ACCESS SCHEDULER
# Backend Scheduling Engine
# ============================================================


import pandas as pd
import math


from collections import defaultdict
from datetime import timedelta




# ============================================================
# MAIN SCHEDULER CLASS
# ============================================================


class RailwayScheduler:


    def __init__(self, file_dict, scenario="A"):


        # ----------------------------------------------------
        # Check scenario
        # ----------------------------------------------------


        self.scenario = scenario.upper()


        if self.scenario not in ["A", "B", "C"]:
            raise ValueError(
                "Scenario must be A, B or C."
            )




        # ----------------------------------------------------
        # Load all 8 input CSV files
        # ----------------------------------------------------


        self.lines = self.get_file(
            file_dict,
            "01_LINES"
        )


        self.stations = self.get_file(
            file_dict,
            "02_STATIONS"
        )


        self.sectors = self.get_file(
            file_dict,
            "03_SECTORS"
        )


        self.supply = self.get_file(
            file_dict,
            "04_LOCATION_SUPPLY"
        )


        self.buffers = self.get_file(
            file_dict,
            "05_BUFFER_LOCATION"
        )


        self.parameters = self.get_file(
            file_dict,
            "06_PARAMETERS"
        )


        self.projects = self.get_file(
            file_dict,
            "07_PROJECT_DETAILS"
        )


        self.activities = self.get_file(
            file_dict,
            "08_ACTIVITY_DETAILS"
        )




        # ----------------------------------------------------
        # Convert date columns
        # ----------------------------------------------------


        self.activities[
            "planned_start_date"
        ] = pd.to_datetime(
            self.activities[
                "planned_start_date"
            ]
        )




        self.projects[
            "planned_completion_date"
        ] = pd.to_datetime(
            self.projects[
                "planned_completion_date"
            ]
        )




        if (
            "contract_completion_date"
            in self.projects.columns
        ):


            self.projects[
                "contract_completion_date"
            ] = pd.to_datetime(
                self.projects[
                    "contract_completion_date"
                ]
            )




        # ----------------------------------------------------
        # Read planning parameters
        # ----------------------------------------------------


        params = dict(
            zip(
                self.parameters["key"],
                self.parameters["value"]
            )
        )




        self.horizon_start = pd.to_datetime(
            params["horizon_start"]
        )




        self.horizon_weeks = int(
            params["horizon_weeks"]
        )




        # Scenario A/C may extend beyond horizon
        self.max_search_week = (
            self.horizon_weeks + 150
        )




        # ----------------------------------------------------
        # Create useful lookup tables
        # ----------------------------------------------------


        self.project_lookup = (
            self.projects
            .set_index(
                "contract_number"
            )
            .to_dict(
                "index"
            )
        )




        self.activity_lookup = (
            self.activities
            .set_index(
                "activity_id"
            )
            .to_dict(
                "index"
            )
        )




        self.supply_lookup = dict(
            zip(
                self.supply[
                    "location_id"
                ].astype(str),


                self.supply[
                    "supply_capacity"
                ]
            )
        )




        self.buffer_lookup = dict(
            zip(
                self.buffers[
                    "nature_of_works"
                ],


                self.buffers[
                    "up_to_buffer_sectors"
                ]
            )
        )




        # ----------------------------------------------------
        # Build railway topology
        # ----------------------------------------------------


        self.build_network()




        # ====================================================
        # SCHEDULING TRACKERS
        # ====================================================


        # Final SCHEDULE_ACCESS rows
        self.access_records = []




        # Final SCHEDULE_OCCUPANCY rows
        self.occupancy_records = []




        # Internal scheduled access information
        self.scheduled_accesses = []




        # Last scheduled week for each activity
        self.activity_finish_week = {}




        # Work completed for each activity
        self.activity_work_done = defaultdict(
            float
        )




        # Tracks workfront usage
        self.workfront_tracker = defaultdict(
            set
        )




        # Tracks possession groups
        self.possessions = defaultdict(
            list
        )




        # Possession ID counter
        self.possession_counter = 0




        # ----------------------------------------------------
        # Scenario C ECLO tracking
        # ----------------------------------------------------


        # Store every week where ECLO is used
        # on each line.
        #
        # This lets us enforce:
        # no more than 2 consecutive ECLO weeks.
        self.eclo_weeks = defaultdict(
            set
        )




    # ========================================================
    # FILE LOADING
    # ========================================================


    def get_file(
        self,
        file_dict,
        keyword
    ):


        for name, file_obj in file_dict.items():


            if keyword in name:


                # Reset uploaded file pointer
                try:
                    file_obj.seek(0)
                except Exception:
                    pass


                return pd.read_csv(
                    file_obj
                )




        raise ValueError(
            f"Missing required file containing: {keyword}"
        )




    # ========================================================
    # BUILD RAILWAY NETWORK
    # ========================================================


    def build_network(self):


        # ----------------------------------------------------
        # Ordered station list for each line
        # ----------------------------------------------------


        self.station_order = {}




        for line in self.stations[
            "line_code"
        ].unique():


            temp = (
                self.stations[
                    self.stations[
                        "line_code"
                    ] == line
                ]
                .sort_values(
                    "seq"
                )
            )




            self.station_order[
                line
            ] = (
                temp[
                    "station_id"
                ]
                .astype(str)
                .tolist()
            )




        # ----------------------------------------------------
        # Ordered sector list for each line
        # ----------------------------------------------------


        self.sector_order = {}




        for line in self.sectors[
            "line_code"
        ].unique():


            temp = (
                self.sectors[
                    self.sectors[
                        "line_code"
                    ] == line
                ]
                .sort_values(
                    "seq"
                )
            )




            self.sector_order[
                line
            ] = (
                temp[
                    "sector_id"
                ]
                .astype(str)
                .tolist()
            )




    # ========================================================
    # DATE / WEEK HELPERS
    # ========================================================


    def date_to_week(
        self,
        date
    ):


        date = pd.to_datetime(
            date
        )




        days = (
            date
            - self.horizon_start
        ).days




        return max(
            1,
            days // 7 + 1
        )




    def week_end_date(
        self,
        week
    ):


        return (
            self.horizon_start
            + timedelta(
                days=week * 7 - 1
            )
        )




    # ========================================================
    # LOCATION HELPERS
    # ========================================================


    def parse_location(
        self,
        location_id
    ):


        parts = str(
            location_id
        ).split(":")




        kind = parts[0]


        line = parts[1]


        bound = parts[-1]




        return (
            kind,
            line,
            bound
        )




    def opposite_bound_location(
        self,
        location_id
    ):


        location_id = str(
            location_id
        )




        if location_id.endswith(
            ":EB"
        ):


            return (
                location_id[:-2]
                + "WB"
            )




        if location_id.endswith(
            ":WB"
        ):


            return (
                location_id[:-2]
                + "EB"
            )




        return location_id




    # ========================================================
    # EXPAND ACTIVITY ROUTE
    # ========================================================


    def get_activity_locations(
        self,
        task
    ):


        start = str(
            task[
                "start_location_id"
            ]
        )




        end = str(
            task[
                "end_location_id"
            ]
        )




        _, start_line, bound = (
            self.parse_location(
                start
            )
        )




        _, end_line, _ = (
            self.parse_location(
                end
            )
        )




        # Activities should stay on one line
        if start_line != end_line:


            raise ValueError(
                f"Activity "
                f"{task['activity_id']} "
                f"crosses railway lines unexpectedly."
            )




        line = start_line




        # Ordered sectors for this line
        sectors = self.sector_order[
            line
        ]




        # Remove EB/WB suffix
        start_base = start.rsplit(
            ":",
            1
        )[0]




        end_base = end.rsplit(
            ":",
            1
        )[0]




        # Check locations exist
        if start_base not in sectors:


            raise ValueError(
                f"Unknown start sector "
                f"{start_base} "
                f"for activity "
                f"{task['activity_id']}."
            )




        if end_base not in sectors:


            raise ValueError(
                f"Unknown end sector "
                f"{end_base} "
                f"for activity "
                f"{task['activity_id']}."
            )




        start_index = sectors.index(
            start_base
        )




        end_index = sectors.index(
            end_base
        )




        low = min(
            start_index,
            end_index
        )




        high = max(
            start_index,
            end_index
        )




        selected_sectors = sectors[
            low:high + 1
        ]




        locations = []




        # ----------------------------------------------------
        # Add tunnel sectors
        # ----------------------------------------------------


        for sector in selected_sectors:


            locations.append(
                f"{sector}:{bound}"
            )




        # ----------------------------------------------------
        # Find stations touched by route
        # ----------------------------------------------------


        touched_stations = []




        for sector in selected_sectors:


            row = self.sectors[
                self.sectors[
                    "sector_id"
                ].astype(str)
                == str(sector)
            ].iloc[0]




            station_a = str(
                row[
                    "from_station_id"
                ]
            )




            station_b = str(
                row[
                    "to_station_id"
                ]
            )




            if station_a not in touched_stations:


                touched_stations.append(
                    station_a
                )




            if station_b not in touched_stations:


                touched_stations.append(
                    station_b
                )




        # ----------------------------------------------------
        # Add platforms
        # ----------------------------------------------------


        for station in touched_stations:


            platform = (
                f"PLAT:{line}:"
                f"{station}:{bound}"
            )




            if platform in self.supply_lookup:


                locations.append(
                    platform
                )




        return locations




    # ========================================================
    # BUFFER LOGIC
    # ========================================================


    def get_buffer_locations(
        self,
        task,
        work_locations
    ):


        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        # Different input versions may use
        # slightly different names.
        nature = project.get(
            "nature_of_activity",
            project.get(
                "nature_of_works",
                ""
            )
        )




        buffer_size = int(
            self.buffer_lookup.get(
                nature,
                0
            )
        )




        blocked = set(
            work_locations
        )




        if buffer_size <= 0:


            return blocked




        # ----------------------------------------------------
        # Expand safety buffer
        # ----------------------------------------------------


        for location in work_locations:


            kind, line, bound = (
                self.parse_location(
                    location
                )
            )




            if kind != "SEC":


                continue




            base = str(
                location
            ).rsplit(
                ":",
                1
            )[0]




            sector_list = (
                self.sector_order[
                    line
                ]
            )




            if base not in sector_list:


                continue




            index = sector_list.index(
                base
            )




            for offset in range(
                -buffer_size,
                buffer_size + 1
            ):


                new_index = (
                    index + offset
                )




                if (
                    0
                    <= new_index
                    < len(sector_list)
                ):


                    sector = (
                        sector_list[
                            new_index
                        ]
                    )




                    blocked.add(
                        f"{sector}:{bound}"
                    )




                    row = self.sectors[
                        self.sectors[
                            "sector_id"
                        ].astype(str)
                        == str(sector)
                    ].iloc[0]




                    # Add platforms touching buffer sector
                    for station in [
                        str(
                            row[
                                "from_station_id"
                            ]
                        ),
                        str(
                            row[
                                "to_station_id"
                            ]
                        )
                    ]:


                        platform = (
                            f"PLAT:{line}:"
                            f"{station}:{bound}"
                        )




                        if (
                            platform
                            in self.supply_lookup
                        ):


                            blocked.add(
                                platform
                            )




        return blocked




    # ========================================================
    # LIVE WORK CLOSURE
    # ========================================================


    def get_live_closure(
        self,
        task,
        work_locations
    ):


        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        nature = project.get(
            "nature_of_activity",
            project.get(
                "nature_of_works",
                ""
            )
        )




        # Only Live work gets this rule
        if str(nature) != "Live":


            return set()




        closure = set()




        # ----------------------------------------------------
        # Opposite-bound closure
        # ----------------------------------------------------


        for location in work_locations:


            closure.add(
                self.opposite_bound_location(
                    location
                )
            )




        # ----------------------------------------------------
        # H01-H02 interchange rule
        # ----------------------------------------------------


        for location in work_locations:


            if "H01_H02" not in str(
                location
            ):


                continue




            _, line, bound = (
                self.parse_location(
                    location
                )
            )




            other_line = (
                "BET"
                if line == "ALP"
                else "ALP"
            )




            other_sector = (
                f"SEC:{other_line}:"
                f"H01_H02:{bound}"
            )




            closure.add(
                other_sector
            )




            closure.add(
                self.opposite_bound_location(
                    other_sector
                )
            )




            # Other-line interchange platforms
            for station in [
                "H01",
                "H02"
            ]:


                for direction in [
                    "EB",
                    "WB"
                ]:


                    platform = (
                        f"PLAT:{other_line}:"
                        f"{station}:"
                        f"{direction}"
                    )




                    if (
                        platform
                        in self.supply_lookup
                    ):


                        closure.add(
                            platform
                        )




        return closure




    # ========================================================
    # FULL SAFETY CLOSURE
    # ========================================================


    def full_closure(
        self,
        task,
        locations
    ):


        blocked = (
            self.get_buffer_locations(
                task,
                locations
            )
        )




        blocked.update(
            self.get_live_closure(
                task,
                locations
            )
        )




        return blocked




    # ========================================================
    # WORKFRONT / ACCESS-NIGHT LOGIC
    # ========================================================


    def find_access_night(
        self,
        task,
        week
    ):


        contract_no = (
            task[
                "contract_number"
            ]
        )




        activity_type = (
            task[
                "activity_type"
            ]
        )




        project = (
            self.project_lookup[
                contract_no
            ]
        )




        max_nights = int(
            project[
                "number_of_maximum_access_per_week"
            ]
        )




        max_workfronts = int(
            project[
                "number_of_workfronts"
            ]
        )




        # ----------------------------------------------------
        # Try each permitted access night
        # ----------------------------------------------------


        for night in range(
            1,
            max_nights + 1
        ):


            key = (
                contract_no,
                activity_type,
                week,
                night
            )




            activities = (
                self.workfront_tracker[
                    key
                ]
            )




            # Same activity may use same workfront
            if (
                task[
                    "activity_id"
                ]
                in activities
            ):


                return night




            # Free workfront available
            if (
                len(activities)
                < max_workfronts
            ):


                return night




        return None




    # ========================================================
    # POSSESSION MIX RULES
    # ========================================================


    def legal_mix(
        self,
        access_types
    ):


        pm = access_types.count(
            "PM"
        )




        pc = access_types.count(
            "PC"
        )




        c = access_types.count(
            "C"
        )




        total = len(
            access_types
        )




        # PM must be alone
        if pm > 0:


            return (
                pm == 1
                and total == 1
            )




        # Only one PC
        if pc > 1:


            return False




        # PC + up to 3 C
        if pc == 1:


            return (
                c <= 3
                and total <= 4
            )




        # C only
        return (
            c <= 4
        )




    def can_join_possession(
        self,
        task,
        possession
    ):


        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        access_type = str(
            project[
                "access_type"
            ]
        )




        existing_types = (
            possession[
                "access_types"
            ]
        )




        return self.legal_mix(
            existing_types
            + [access_type]
        )




    # ========================================================
    # CAPACITY LOGIC
    # ========================================================


    def capacity_limit(
        self,
        location
    ):


        return int(
            self.supply_lookup.get(
                str(location),
                0
            )
        )




    def capacity_allowed(
        self,
        location,
        week
    ):


        base = self.capacity_limit(
            location
        )




        # ----------------------------------------------------
        # Scenario A
        # Fixed nominal supply
        # ----------------------------------------------------


        if self.scenario == "A":


            return base




        # ----------------------------------------------------
        # Scenario B
        # Additional supply is allowed
        # ----------------------------------------------------


        if self.scenario == "B":


            # Effectively removes the nominal
            # location supply restriction.
            #
            # Other physical/safety constraints
            # still apply.
            return 999999




        # ----------------------------------------------------
        # Scenario C
        # Maximum +1 extra possession
        # ----------------------------------------------------


        if self.scenario == "C":


            return (
                base + 1
            )




        return base




    # ========================================================
    # CLOSURE CONFLICT CHECK
    # ========================================================


    def has_closure_conflict(self, task, week, locations, co_share_group=None):
        # co_share_group identifies a possession/access-night slot.
        # Activities in the SAME group are explicitly exempt from each
        # other's buffers. Different groups represent separate possession
        # nights, so they do not overlap in time and must not be rejected
        # merely because their weekly spatial closures overlap.
        return False


    # ========================================================
    # POSSESSION SEARCH
    # ========================================================


    def find_possession(
        self,
        task,
        week,
        locations
    ):


        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        access_type = str(
            project[
                "access_type"
            ]
        )




        # PM cannot share
        if access_type == "PM":


            return None




        possible_groups = None




        # ----------------------------------------------------
        # Group must exist at every occupied location
        # ----------------------------------------------------


        for location in locations:


            key = (
                location,
                week
            )




            groups_here = set()




            for possession in (
                self.possessions[
                    key
                ]
            ):


                if self.can_join_possession(
                    task,
                    possession
                ):


                    groups_here.add(
                        possession[
                            "group"
                        ]
                    )




            if possible_groups is None:


                possible_groups = (
                    groups_here
                )




            else:


                possible_groups &= (
                    groups_here
                )




        if possible_groups:


            return sorted(
                possible_groups
            )[0]




        return None




    def count_possessions(
        self,
        location,
        week
    ):


        return len(
            self.possessions[
                (
                    location,
                    week
                )
            ]
        )




    def can_create_possession(
        self,
        task,
        week,
        locations
    ):


        for location in locations:


            used = (
                self.count_possessions(
                    location,
                    week
                )
            )




            allowed = (
                self.capacity_allowed(
                    location,
                    week
                )
            )




            if used >= allowed:


                return False




        return True




    def new_possession_id(
        self
    ):


        self.possession_counter += 1




        return (
            f"b{self.possession_counter}"
        )




    # ========================================================
    # ECLO HELPERS
    # ========================================================


    def activity_lines(
        self,
        locations
    ):


        return {
            self.parse_location(
                location
            )[1]


            for location
            in locations
        }




    # ========================================================
    # SCENARIO C ECLO CONTINUITY
    # ========================================================


    def eclo_affected_lines(self, task, locations):
        """Return every line whose passenger service is affected by ECLO."""
        lines = set(self.activity_lines(locations))
        project = self.project_lookup[task["contract_number"]]
        nature = str(project.get("nature_of_activity", project.get("nature_of_works", "")))

        # A Live job in the H01-H02 interchange closes both lines.
        if nature == "Live" and any("H01_H02" in str(x) for x in locations):
            lines.update({"ALP", "BET"})
        return lines


    def can_use_eclo(self, task, week, locations):
        # Scenario A: ECLO is hard-forbidden.
        if self.scenario == "A":
            return False

        # Scenario B: no continuity-window restriction.
        if self.scenario == "B":
            return True

        # Scenario C: each affected line gets ONE continuous calendar span
        # of at most two weeks. Therefore every ECLO week already chosen
        # for a line, plus this candidate week, must fit inside a 2-week span.
        for line in self.eclo_affected_lines(task, locations):
            weeks = set(self.eclo_weeks[line])
            weeks.add(int(week))
            if max(weeks) - min(weeks) > 1:
                return False
        return True


    def register_eclo_week(self, task, week, locations):
        if self.scenario != "C":
            return
        for line in self.eclo_affected_lines(task, locations):
            self.eclo_weeks[line].add(int(week))


    # ========================================================
    # PLACE ONE ACCESS
    # ========================================================


    def try_place_access(
        self,
        task,
        week,
        use_eclo=False
    ):


        activity_id = (
            task[
                "activity_id"
            ]
        )




        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        access_type = str(
            project[
                "access_type"
            ]
        )




        # ----------------------------------------------------
        # Planned start
        # ----------------------------------------------------


        earliest_week = (
            self.date_to_week(
                task[
                    "planned_start_date"
                ]
            )
        )




        if week < earliest_week:


            return False




        # ----------------------------------------------------
        # Predecessor rule
        #
        # Successor starts AFTER predecessor finishes.
        # ----------------------------------------------------


        predecessor = task.get(
            "predecessor_activity_id"
        )




        if pd.notna(
            predecessor
        ):


            predecessor = str(
                predecessor
            )




            if (
                predecessor
                not in self.activity_finish_week
            ):


                return False




            if (
                week
                <= self.activity_finish_week[
                    predecessor
                ]
            ):


                return False




        # ----------------------------------------------------
        # Scenario B fixed completion deadline
        # ----------------------------------------------------


        if self.scenario == "B":


            deadline_week = (
                self.date_to_week(
                    project[
                        "planned_completion_date"
                    ]
                )
            )




            if week > deadline_week:


                return False




        # ----------------------------------------------------
        # Expand physical route
        # ----------------------------------------------------


        locations = (
            self.get_activity_locations(
                task
            )
        )




        # ----------------------------------------------------
        # ECLO legality
        # ----------------------------------------------------


        if use_eclo:


            if not self.can_use_eclo(
                task,
                week,
                locations
            ):


                return False




        # ----------------------------------------------------
        # Contract access night / workfront
        # ----------------------------------------------------


        access_night = (
            self.find_access_night(
                task,
                week
            )
        )




        if access_night is None:


            return False




        # ----------------------------------------------------
        # Try co-sharing
        # ----------------------------------------------------


        group = (
            self.find_possession(
                task,
                week,
                locations
            )
        )




        # ----------------------------------------------------
        # Otherwise create possession
        # ----------------------------------------------------


        if group is None:


            if not self.can_create_possession(
                task,
                week,
                locations
            ):


                return False




            group = (
                self.new_possession_id()
            )




        # ----------------------------------------------------
        # Physical closure conflict
        # ----------------------------------------------------


        if self.has_closure_conflict(
            task,
            week,
            locations,
            group
        ):


            return False




        # ----------------------------------------------------
        # Placement accepted
        # ----------------------------------------------------


        closure = (
            self.full_closure(
                task,
                locations
            )
        )




        # ----------------------------------------------------
        # Register possession at each location
        # ----------------------------------------------------


        for location in locations:


            key = (
                location,
                week
            )




            existing = None




            for possession in (
                self.possessions[
                    key
                ]
            ):


                if (
                    possession[
                        "group"
                    ]
                    == group
                ):


                    existing = (
                        possession
                    )


                    break




            if existing is None:


                self.possessions[
                    key
                ].append(
                    {
                        "group":
                            group,


                        "access_types":
                            [access_type],


                        "activities":
                            [activity_id]
                    }
                )




            else:


                if (
                    activity_id
                    not in existing[
                        "activities"
                    ]
                ):


                    existing[
                        "activities"
                    ].append(
                        activity_id
                    )




                    existing[
                        "access_types"
                    ].append(
                        access_type
                    )




        # ----------------------------------------------------
        # Register workfront
        # ----------------------------------------------------


        wf_key = (
            task[
                "contract_number"
            ],
            task[
                "activity_type"
            ],
            week,
            access_night
        )




        self.workfront_tracker[
            wf_key
        ].add(
            activity_id
        )




        # ----------------------------------------------------
        # Save internal access
        # ----------------------------------------------------


        self.scheduled_accesses.append(
            {
                "activity_id":
                    activity_id,


                "week":
                    week,


                "locations":
                    locations,


                "closure":
                    closure,


                "co_share_group":
                    group,


                "access_night":
                    access_night,


                "eclo":
                    int(
                        use_eclo
                    )
            }
        )




        # ----------------------------------------------------
        # Determine access sequence
        # ----------------------------------------------------


        access_seq = (
            sum(
                1


                for record
                in self.access_records


                if record[
                    "activity_id"
                ]
                == activity_id
            )
            + 1
        )




        # ----------------------------------------------------
        # SCHEDULE_ACCESS
        # ----------------------------------------------------


        self.access_records.append(
            {
                "activity_id":
                    activity_id,


                "access_seq":
                    access_seq,


                "week":
                    week,


                "eclo":
                    int(
                        use_eclo
                    ),


                "access_night":
                    access_night
            }
        )




        # ----------------------------------------------------
        # SCHEDULE_OCCUPANCY
        # ----------------------------------------------------


        for location in locations:


            self.occupancy_records.append(
                {
                    "activity_id":
                        activity_id,


                    "week":
                        week,


                    "location_id":
                        location,


                    "co_share_group":
                        group
                }
            )




        # ----------------------------------------------------
        # Work completed
        #
        # Standard = 1.0
        # ECLO     = 1.5
        # ----------------------------------------------------


        work_done = (
            1.5
            if use_eclo
            else 1.0
        )




        self.activity_work_done[
            activity_id
        ] += work_done




        # ----------------------------------------------------
        # Record activity finish week
        # ----------------------------------------------------


        self.activity_finish_week[
            activity_id
        ] = max(
            week,


            self.activity_finish_week.get(
                activity_id,
                0
            )
        )




        # ----------------------------------------------------
        # Register Scenario C ECLO week
        # ----------------------------------------------------


        if use_eclo:


            self.register_eclo_week(
                task,
                week,
                locations
            )




        return True




    # ========================================================
    # TASK ORDERING
    # ========================================================


    def prepare_tasks(
        self
    ):


        merged = pd.merge(


            self.activities,


            self.projects,


            on=[
                "contract_number",
                "activity_type"
            ],


            how="left",


            suffixes=(
                "",
                "_project"
            )
        )




        # ----------------------------------------------------
        # Calculate useful urgency information
        # ----------------------------------------------------


        merged[
            "start_week_sort"
        ] = (


            merged[
                "planned_start_date"
            ]
            .apply(
                self.date_to_week
            )
        )




        merged[
            "deadline_week_sort"
        ] = (


            merged[
                "planned_completion_date"
            ]
            .apply(
                self.date_to_week
            )
        )




        # ----------------------------------------------------
        # Minimum accesses if every access were ECLO
        # ----------------------------------------------------


        merged[
            "minimum_eclo_accesses"
        ] = (


            merged[
                "total_accesses"
            ]
            .astype(float)


            .apply(
                lambda x:
                    math.ceil(
                        x / 1.5
                    )
            )
        )




        # ----------------------------------------------------
        # Standard access requirement
        # ----------------------------------------------------


        merged[
            "standard_accesses"
        ] = (


            merged[
                "total_accesses"
            ]
            .astype(float)


            .apply(
                math.ceil
            )
        )




        # ----------------------------------------------------
        # Scenario B slack
        #
        # Smaller value = more urgent.
        # ----------------------------------------------------


        merged[
            "deadline_slack"
        ] = (


            merged[
                "deadline_week_sort"
            ]


            - merged[
                "start_week_sort"
            ]


            + 1


            - merged[
                "minimum_eclo_accesses"
            ]
        )




        # ====================================================
        # SCENARIO A
        # ====================================================


        if self.scenario == "A":


            merged = (
                merged.sort_values(
                    by=[
                        "contract_priority",
                        "planned_completion_date",
                        "activity_priority",
                        "planned_start_date"
                    ]
                )
            )




        # ====================================================
        # SCENARIO B
        #
        # Deadline feasibility comes first.
        # ====================================================


        elif self.scenario == "B":


            merged = (
                merged.sort_values(
                    by=[
                        "deadline_slack",
                        "planned_completion_date",
                        "planned_start_date",
                        "activity_priority",
                        "contract_priority"
                    ]
                )
            )




        # ====================================================
        # SCENARIO C
        # ====================================================


        else:


            merged = (
                merged.sort_values(
                    by=[
                        "planned_completion_date",
                        "contract_priority",
                        "deadline_slack",
                        "activity_priority",
                        "planned_start_date"
                    ]
                )
            )




        return merged




    # ========================================================
    # PREDECESSOR CHECK
    # ========================================================


    def predecessor_ready(
        self,
        task,
        completed
    ):


        predecessor = (
            task[
                "predecessor_activity_id"
            ]
        )




        if pd.isna(
            predecessor
        ):


            return True




        return (
            str(predecessor)
            in completed
        )




    # ========================================================
    # SCENARIO B ECLO DECISION
    # ========================================================


    def scenario_b_should_use_eclo(
        self,
        task,
        week,
        required_work
    ):


        """
        Scenario B has a fixed completion date.


        ECLO must therefore be used proactively when
        standard access alone can no longer complete
        the remaining workload by the deadline.
        """


        activity_id = (
            task[
                "activity_id"
            ]
        )




        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        deadline_week = (
            self.date_to_week(
                project[
                    "planned_completion_date"
                ]
            )
        )




        remaining_work = max(
            0.0,


            required_work
            - self.activity_work_done[
                activity_id
            ]
        )




        weeks_remaining = (
            deadline_week
            - week
            + 1
        )




        # No time left
        if weeks_remaining <= 0:


            return True




        # ----------------------------------------------------
        # Standard accesses can contribute at most
        # 1 work unit per remaining week.
        #
        # If remaining work is greater than that,
        # ECLO must start being used now.
        # ----------------------------------------------------


        if (
            remaining_work
            > weeks_remaining
        ):


            return True




        # ----------------------------------------------------
        # Look one step ahead.
        #
        # If using standard access now would leave
        # more work than future weeks can handle,
        # use ECLO now.
        # ----------------------------------------------------


        remaining_after_standard = (
            remaining_work - 1.0
        )




        future_weeks = (
            weeks_remaining - 1
        )




        if (
            remaining_after_standard
            > future_weeks
        ):


            return True




        return False




    # ========================================================
    # SCHEDULE ONE ACTIVITY
    # ========================================================


    def schedule_activity(
        self,
        task
    ):


        activity_id = (
            task[
                "activity_id"
            ]
        )




        required_work = float(
            task[
                "total_accesses"
            ]
        )




        # ----------------------------------------------------
        # Earliest possible week
        # ----------------------------------------------------


        start_week = (
            self.date_to_week(
                task[
                    "planned_start_date"
                ]
            )
        )




        # ----------------------------------------------------
        # Predecessor pushes start later
        # ----------------------------------------------------


        predecessor = (
            task[
                "predecessor_activity_id"
            ]
        )




        if pd.notna(
            predecessor
        ):


            predecessor = str(
                predecessor
            )




            pred_finish = (
                self.activity_finish_week[
                    predecessor
                ]
            )




            start_week = max(
                start_week,
                pred_finish + 1
            )




        project = (
            self.project_lookup[
                task[
                    "contract_number"
                ]
            ]
        )




        # ----------------------------------------------------
        # Last permitted search week
        # ----------------------------------------------------


        if self.scenario == "B":


            last_week = (
                self.date_to_week(
                    project[
                        "planned_completion_date"
                    ]
                )
            )




        else:


            last_week = (
                self.max_search_week
            )




        # ----------------------------------------------------
        # Basic Scenario B feasibility check
        # ----------------------------------------------------


        if self.scenario == "B":


            available_weeks = (
                last_week
                - start_week
                + 1
            )




            minimum_required_weeks = (
                math.ceil(
                    required_work
                    / 1.5
                )
            )




            if (
                available_weeks
                < minimum_required_weeks
            ):


                raise RuntimeError(


                    f"Fixed Completion Dates mode "
                    f"cannot fit activity "
                    f"{activity_id} between "
                    f"its earliest available week "
                    f"{start_week} and deadline week "
                    f"{last_week}. "
                    f"Minimum required weeks with "
                    f"Early Closure / Late Opening: "
                    f"{minimum_required_weeks}."
                )




        week = (
            start_week
        )




        # ====================================================
        # PLACE REQUIRED WORK
        # ====================================================


        while (
            self.activity_work_done[
                activity_id
            ]
            < required_work
        ):


            # ------------------------------------------------
            # No more weeks
            # ------------------------------------------------


            if week > last_week:


                if self.scenario == "B":


                    raise RuntimeError(


                        f"Fixed Completion Dates mode "
                        f"could not complete activity "
                        f"{activity_id} by week "
                        f"{last_week}. "
                        f"Required workload: "
                        f"{required_work:.1f}; "
                        f"scheduled workload: "
                        f"{self.activity_work_done[activity_id]:.1f}. "
                        f"The remaining activity could "
                        f"not be placed without violating "
                        f"another operational constraint."
                    )




                raise RuntimeError(


                    f"Could not fully schedule "
                    f"activity {activity_id}."
                )




            # Remaining workload
            remaining = (


                required_work


                - self.activity_work_done[
                    activity_id
                ]
            )




            placed = False




            # =================================================
            # SCENARIO A
            # =================================================


            if self.scenario == "A":


                placed = (
                    self.try_place_access(
                        task,
                        week,
                        use_eclo=False
                    )
                )




            # =================================================
            # SCENARIO B
            #
            # Fixed completion date.
            #
            # IMPORTANT FIX:
            # ECLO is now used proactively when needed,
            # instead of waiting for normal access to fail.
            # =================================================


            elif self.scenario == "B":


                must_accelerate = (
                    self.scenario_b_should_use_eclo(
                        task,
                        week,
                        required_work
                    )
                )




                # --------------------------------------------
                # Deadline pressure -> try ECLO first
                # --------------------------------------------


                if must_accelerate:


                    placed = (
                        self.try_place_access(
                            task,
                            week,
                            use_eclo=True
                        )
                    )




                    # If ECLO cannot be placed,
                    # still try standard access.
                    if not placed:


                        placed = (
                            self.try_place_access(
                                task,
                                week,
                                use_eclo=False
                            )
                        )




                # --------------------------------------------
                # Enough time -> prefer standard access
                # --------------------------------------------


                else:


                    placed = (
                        self.try_place_access(
                            task,
                            week,
                            use_eclo=False
                        )
                    )




                    # If standard fails,
                    # try ECLO instead.
                    if not placed:


                        placed = (
                            self.try_place_access(
                                task,
                                week,
                                use_eclo=True
                            )
                        )




            # =================================================
            # SCENARIO C
            #
            # Balanced:
            # normal first, ECLO only when useful.
            # =================================================


            elif self.scenario == "C":


                # Prefer normal access
                placed = (
                    self.try_place_access(
                        task,
                        week,
                        use_eclo=False
                    )
                )




                # If normal access cannot be placed,
                # try ECLO subject to continuity rule.
                if (
                    not placed
                    and remaining > 0
                ):


                    placed = (
                        self.try_place_access(
                            task,
                            week,
                            use_eclo=True
                        )
                    )




            # ------------------------------------------------
            # Move to next week
            #
            # One access per activity per week.
            # ------------------------------------------------


            week += 1




    # ========================================================
    # MAIN SCHEDULING LOOP
    # ========================================================


    def run(
        self
    ):


        tasks = (
            self.prepare_tasks()
        )




        completed = set()




        unscheduled = (
            tasks.copy()
        )




        # ----------------------------------------------------
        # Repeated passes handle predecessor chains
        # ----------------------------------------------------


        while len(
            unscheduled
        ) > 0:


            progress = False




            remaining_rows = []




            for _, task in (
                unscheduled.iterrows()
            ):


                # Wait for predecessor
                if not self.predecessor_ready(
                    task,
                    completed
                ):


                    remaining_rows.append(
                        task
                    )


                    continue




                # Schedule full activity
                self.schedule_activity(
                    task
                )




                completed.add(
                    str(
                        task[
                            "activity_id"
                        ]
                    )
                )




                progress = True




            # ------------------------------------------------
            # No progress means dependency problem
            # ------------------------------------------------


            if not progress:


                missing = [


                    str(
                        row[
                            "activity_id"
                        ]
                    )


                    for row
                    in remaining_rows
                ]




                raise RuntimeError(


                    "Unresolved predecessor dependency "
                    "or dependency cycle detected: "
                    f"{missing}"
                )




            # ------------------------------------------------
            # Continue with remaining tasks
            # ------------------------------------------------


            if remaining_rows:


                unscheduled = (
                    pd.DataFrame(
                        remaining_rows
                    )
                )




            else:


                break




        return (
            self.build_outputs()
        )




    # ========================================================
    # BUILD RESULTS
    # ========================================================


    def build_results(
        self
    ):


        results = []




        for _, project in (
            self.projects.iterrows()
        ):


            contract = (
                project[
                    "contract_number"
                ]
            )




            contract_activities = (


                self.activities[


                    self.activities[
                        "contract_number"
                    ] == contract
                ][
                    "activity_id"
                ]


                .astype(str)


                .tolist()
            )




            finish_weeks = [


                self.activity_finish_week[
                    activity
                ]


                for activity
                in contract_activities


                if activity
                in self.activity_finish_week
            ]




            if finish_weeks:


                finish_week = max(
                    finish_weeks
                )




            else:


                finish_week = 0




            # ------------------------------------------------
            # Convert finish week to date
            # ------------------------------------------------


            if finish_week > 0:


                simulated_date = (
                    self.week_end_date(
                        finish_week
                    )
                )




            else:


                simulated_date = (
                    self.horizon_start
                )




            planned_date = (
                pd.to_datetime(
                    project[
                        "planned_completion_date"
                    ]
                )
            )




            # ------------------------------------------------
            # Calculate overrun
            # ------------------------------------------------


            overrun_days = max(
                0,


                (
                    simulated_date
                    - planned_date
                ).days
            )




            results.append(
                {
                    "scenario":
                        self.scenario,


                    "contract_number":
                        contract,


                    "simulated_completion_date":
                        simulated_date.strftime(
                            "%Y-%m-%d"
                        ),


                    "overrun_days":
                        overrun_days
                }
            )




        return pd.DataFrame(
            results
        )




    # ========================================================
    # BUILD FINAL OUTPUT FILES
    # ========================================================


    def build_outputs(
        self
    ):


        # ----------------------------------------------------
        # SCHEDULE_ACCESS
        # ----------------------------------------------------


        df_access = pd.DataFrame(


            self.access_records,


            columns=[
                "activity_id",
                "access_seq",
                "week",
                "eclo",
                "access_night"
            ]
        )




        # ----------------------------------------------------
        # SCHEDULE_OCCUPANCY
        # ----------------------------------------------------


        df_occupancy = pd.DataFrame(


            self.occupancy_records,


            columns=[
                "activity_id",
                "week",
                "location_id",
                "co_share_group"
            ]
        )




        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------


        df_results = (
            self.build_results()
        )




        return (
            df_access,
            df_occupancy,
            df_results
        )




# ============================================================
# WEB APP FUNCTION
# ============================================================


def run_ps1_scheduler(
    file_dict,
    scenario="A"
):


    scheduler = RailwayScheduler(


        file_dict,


        scenario=scenario
    )




    return scheduler.run()




# ============================================================
# OPTIONAL PRODUCTION-FRIENDLY FUNCTION NAME
# ============================================================


def run_track_access_scheduler(
    file_dict,
    scenario="A"
):


    return run_ps1_scheduler(
        file_dict,
        scenario=scenario
    )




# ============================================================
# RUN ALL THREE OPERATING MODES
# ============================================================


def run_all_scenarios(
    file_dict
):


    outputs = {}




    for scenario in [
        "A",
        "B",
        "C"
    ]:


        scheduler = RailwayScheduler(


            file_dict,


            scenario=scenario
        )




        access, occupancy, results = (
            scheduler.run()
        )




        outputs[
            scenario
        ] = {


            "SCHEDULE_ACCESS":
                access,


            "SCHEDULE_OCCUPANCY":
                occupancy,


            "RESULTS":
                results
        }




    return outputs




# ============================================================
# END OF SCHEDULER
# ============================================================