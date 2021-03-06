# Greedy implementation

from dataclasses import dataclass
from enum import Enum
import math
from typing import Any, Dict, List, Tuple

@dataclass
class Worker():
    name: str
    skills: Dict[str, int]
    skill_level: int
    free: bool = True

@dataclass
class Project():
    name: str
    duration: int
    score: int
    bbefore: int
    roles: List[Tuple[str, int]]
    start_day: int = -1

@dataclass
class PlannedProject():
    name: str
    workers: List[str]

def input_data() -> Tuple[Dict[str, Worker], Dict[str, Project], Dict[str, List[Worker]]]:
    """
    Reads the input data.

    Returns
    -------
    dict of str and worker
        All workers stored
        key: worker name --- value: Worker
    dict of str and project
        All projects stored
        key: project name --- value: Project
    dict of str and list of workers
        Workers skills
        key: skill --- value: List of workers with that skill
    """
    first_line = input().split()
    n_workers = int(first_line[0])
    n_projects = int(first_line[1])
    skill_workers: Dict[str, List[Worker]] = {}
    workers: Dict[str, Worker] = {}
    for _ in range(n_workers):
        worker_line = input().split()
        name = worker_line[0]
        n_skills = int(worker_line[1])
        skills = {}
        skill_level = 0
        for _ in range(n_skills):
            skill_line = input().split()
            s_name = skill_line[0]
            s_level = int(skill_line[1])
            skills[s_name] = s_level
            skill_level += s_level
        w = Worker(name, skills, skill_level)
        for skill in w.skills:
            if skill in skill_workers:
                skill_workers[skill].append(w)
            else:
                skill_workers[skill] = [w]
        workers[name] = w
    
    projects: Dict[str, Project] = {}
    for _ in range(n_projects):
        proj_line = input().split()
        name = proj_line[0]
        duration = int(proj_line[1])
        score = int(proj_line[2])
        bbefore = int(proj_line[3])
        n_roles = int(proj_line[4])
        roles: List[Tuple[str, int]] = []
        for _ in range(n_roles):
            role_line = input().split()
            r_name = role_line[0]
            r_level = int(role_line[1])
            roles.append((r_name, r_level))
        if score > 0 and n_roles <= n_workers:
            p = Project(name, duration, score, bbefore, roles)
            projects[name] = p
    return (workers, projects, skill_workers)

def set_start_day(p: Project, day: int) -> Project:
    p.start_day = day
    return p

def maximum_project_points(project: Project, current_day: int) -> int:
    return max(0, (project.score+min(0, (project.bbefore-(current_day+project.duration)))))

def _ratio_skills_workers(project: Project, skill_workers: Dict[str, List[Worker]]) -> float:
    skilled_workers = 0
    for role in project.roles:
        if role[0] in skill_workers:
            skilled_workers += len(skill_workers[role[0]])
    cant_roles = len(project.roles)
    if cant_roles == 0:
        cant_roles = 1
    return  -(skilled_workers/cant_roles)

def calculate_means_and_ranges(projects: Dict[str, Project], skill_workers: Dict[str, List[Worker]], day: int) -> Tuple[float, float, float]:
    """
    Returns
    -------
    * mean_score: float
    * mean_duration: float
    * mean_ratio_skill_workers: float
    * range_score: float
    * range_duration: float
    * range_ratio_sk_w: float
    """
    ratio_sk_w = 0
    duration = 0
    score = 0
    min_ratio_sk_w = min_score = min_duration = math.inf
    max_ratio_sk_w = max_score = max_duration = 0
    for p_key in projects:
        project = projects[p_key]
        ratio_sk_w += _ratio_skills_workers(project, skill_workers)
        duration += project.duration
        score += maximum_project_points(project, day)
        if ratio_sk_w < min_ratio_sk_w:
            min_ratio_sk_w = ratio_sk_w
        if ratio_sk_w > max_ratio_sk_w:
            max_ratio_sk_w = ratio_sk_w
        if duration < min_duration:
            min_duration = duration
        if duration > max_duration:
            max_duration = duration
        if score < min_score:
            min_score = score
        if score > max_score:
            max_score = score
    c_projects = len(projects)
    ratio_sk_w /= c_projects
    duration /= c_projects
    score /= c_projects
    range_score = min(1, max_score - min_score)
    range_duration = min(1, max_duration - min_duration)
    range_ratio_sk_w = max_ratio_sk_w - min_ratio_sk_w
    if range_ratio_sk_w == 0:
        range_ratio_sk_w = 1
    return (score, duration, ratio_sk_w, range_score, range_duration, range_ratio_sk_w)

##############
#### Worker lookup methods
##############

def role_lookup_free_worker(skill_workers: Dict[str, List[Worker]], role: str, level: int,
        assigned: List[str], workers: Dict[str, Worker]) -> Tuple[str, bool]:
    if level == 0:
        for w_name in workers:
            worker = workers[w_name]
            if worker.free and worker.name not in assigned:
                return worker.name, True
    else:
        for worker in skill_workers[role]:
            if worker.free and worker.name not in assigned:
                if worker.skills[role] >= level:
                    return worker.name, True
    return None, False

def role_lookup_free_worker_dumbest_skill(skill_workers: Dict[str, List[Worker]], role: str,
        level: int, assigned: List[str], workers: Dict[str, Worker]) -> Tuple[str, bool]:
    min_level = math.inf
    worker_name = ""
    worker_found = False
    if level == 0:
        for w_name in workers:
            worker = workers[w_name]
            if worker.free and worker.name not in assigned:
                w_level = 0
                if role in worker.skills:
                    w_level = worker.skills[role]
                if min_level > w_level >= level:
                    min_level = w_level
                    worker_name = worker.name
                    worker_found = True
            if worker_found and min_level == 0:
                break
    else:
        for worker in skill_workers[role]:
            if worker.free and worker.name not in assigned:
                if min_level > worker.skills[role] >= level:
                    min_level = worker.skills[role]
                    worker_name = worker.name
                    worker_found = True
    if not worker_found:
        return None, False
    return worker_name, True

def role_lookup_free_worker_dumbest_general(skill_workers: Dict[str, List[Worker]], role: str,
        level: int, assigned: List[str], workers: Dict[str, Worker]) -> Tuple[str, bool]:
    min_level = math.inf
    worker_name = ""
    worker_found = False
    if level == 0:
        for w_name in workers:
            worker = workers[w_name]
            if worker.free and worker.name not in assigned:
                w_level = 0
                if role in worker.skills:
                    w_level = worker.skills[role]
                if w_level >= level and min_level > worker.skill_level:
                    min_level = worker.skill_level
                    worker_name = worker.name
                    worker_found = True
            if worker_found and min_level == 0:
                break
    else:
        for worker in skill_workers[role]:
            if worker.free and worker.name not in assigned:
                if worker.skills[role] >= level and min_level > worker.skill_level:
                    min_level = worker.skill_level
                    worker_name = worker.name
                    worker_found = True
    if not worker_found:
        return None, False
    return worker_name, True

SIMPLE_COLLAB: bool = True # When looking up a free worker, allow a lower level worker if possible for the already assigned workers for the project
MIN_LEVEL_COLLAB: int = 0 # Inferior level limit of collaboration. If equal to 0 it might affect performance.
MAX_LEVEL_COLLAB: int = math.inf # Superior level limit of collaboration.
REVERSE_SKILL_WORKERS: bool = False # Reverses all lists of skill_workers dictionary.
# Gives different outcome for some lookups, speciallt role_lookup_free_worker

def individual_role_lookup(project: Project, skill_workers: Dict[str, List[Worker]], workers: List[Worker]) -> Tuple[List[Worker], List[Tuple[str, int]], bool]:
    assigned_workers = []
    assigned_roles: List[Tuple[str, int]] = []
    project_possible = True
    for role in project.roles:
        level = role[1]
        is_mentor = False
        between_collab_limits = MIN_LEVEL_COLLAB <= (level-1) <= MAX_LEVEL_COLLAB
        if SIMPLE_COLLAB and between_collab_limits:
            for aname in assigned_workers:
                worker = workers[aname]
                if role[0] in worker.skills:
                    if worker.skills[role[0]] >= role[1]:
                        level -= 1
                        is_mentor = True
                        break
                if is_mentor:
                    break
        name, exists = role_lookup_free_worker_dumbest_general(skill_workers, role[0], level, assigned_workers, workers)
        if not exists:
            project_possible = False
            break
        assigned_workers.append(name)
        assigned_roles.append(role)
    return (assigned_workers, assigned_roles, project_possible)

############
#### Sorting methods
############

mean_score = mean_duration = mean_ratio_sk_w = 1

duration_range = ratio_sk_w_range = score_range = 1

def _norm_score(score: float) -> float:
    return SCORE_FACTOR * (score-mean_score)/score_range

def _norm_duration(duration: float) -> float:
    return DURATION_FACTOR * (duration-mean_duration)/duration_range

def _norm_ratio_sk_w(ratio_sk_w: float) -> float:
    return RATIO_SK_W_FACTOR * (ratio_sk_w-mean_ratio_sk_w)/ratio_sk_w_range

def sort_ratio_leftpoints_duration_less_first(name: str, projects: Dict[str, Project], day: int, _: Any) -> float:
    score = _norm_score(maximum_project_points(projects[name], day))
    duration  = _norm_duration(projects[name].duration)
    return score/duration

def sort_ratio_leftpoints_duration_bigger_first(name: str, projects: Dict[str, Project], day: int, _: Any) -> float:
    score = _norm_score(maximum_project_points(projects[name], day))
    duration  = _norm_duration(projects[name].duration)
    return -(score/duration)

def sort_ratio_leftpoints_duration_bigger_first_secondary_shortest(name: str, projects: Dict[str, Project], day: int, _: Any) -> Tuple[float, int]:
    score = _norm_score(maximum_project_points(projects[name], day))
    duration  = _norm_duration(projects[name].duration)
    return (-score/duration, duration)

def sort_leftpoints_bigger(name: str, projects: Dict[str, Project], day: int, _: Any) -> float:
    score = _norm_score(maximum_project_points(projects[name], day))
    return -score

def sort_substraction_leftpoints_bigger(name: str, projects: Dict[str, Project], day: int, _: Any) -> float:
    score = _norm_score(maximum_project_points(projects[name], day))
    duration  = _norm_duration(projects[name].duration)
    return -(score-duration)

def sort_shortest_first(name: str, projects: Dict[str, Project], day: Any, _: Any) -> float:
    return projects[name].duration

def sort_ratio_skills_workers_ratio_leftpoints_duration_bigger_first(name: str, projects: Dict[str, Project], day: int, skill_workers: Dict[str, List[Worker]]) -> float:
    project = projects[name]
    ratio_sk_w = _norm_ratio_sk_w(_ratio_skills_workers(project, skill_workers))
    score = _norm_score(maximum_project_points(projects[name], day))
    duration  = _norm_duration(projects[name].duration)
    return  -((ratio_sk_w*score)/duration)

def sort_ratio_skills_workers_bigger_first(name: str, projects: Dict[str, Project], day: int, skill_workers: Dict[str, List[Worker]]) -> float:
    project = projects[name]
    return _ratio_skills_workers(project, skill_workers)

SCORE_FACTOR = 1
DURATION_FACTOR = 1
RATIO_SK_W_FACTOR = 1

LEVEL_UP: bool = True # Workers level up
ZERO_PROJECTS: bool = True # Dinamically ignore the projects that won't give points.
SIMULATE_SKIP_BUG: bool = False # Accidental feature where if a project was accepted.
# the next project in the list was skipped. It was a bug but sometimes gave better results.
NORMALIZE_SORTING_PARAMS: bool = True # Normalize the ratios and sorting values so they all affect equally.

def main():
    workers, projects, skill_workers = input_data()
    order_projects = [p for p in projects]
    cant_free_workers = len(workers) # Amount of free (unoccupied) workers
    day = 0
    prev_num_projects = 0
    planned: List[PlannedProject] = []
    pending_projects: List[Project] = []
    score = 0
    global mean_score, mean_duration, mean_ratio_sk_w, score_range, duration_range, ratio_sk_w_range
    if NORMALIZE_SORTING_PARAMS:
        mean_score, mean_duration, mean_ratio_sk_w, score_range, duration_range, ratio_sk_w_range = calculate_means_and_ranges(projects, skill_workers, day)
    if REVERSE_SKILL_WORKERS:
        for skill in skill_workers:
            skill_workers[skill].reverse()
    while projects:
        #print(day)
        order_projects.sort(key=lambda x: sort_ratio_leftpoints_duration_bigger_first_secondary_shortest(x, projects, day, skill_workers))
        if prev_num_projects == len(order_projects) and cant_free_workers == len(workers):
            break
        prev_num_projects = len(order_projects)

        #####
        # Finish projects in progress (pending projects)
        #####
        # Check all in order to see if they are finished and we can recover the workers
        #print("Finishing projects...")
        removing_pends: List[str] = [] # List of recently finished projects
        for pend in pending_projects:
            if day >= pend.start_day + pend.duration:
                removing_pends.append(pend.name)
                plann = [p for p in planned if p.name == pend.name][0]
                for wk in plann.workers:
                    cant_free_workers += 1
                    workers[wk].free = True
                extra_score = max(0, pend.score + min(0, (pend.bbefore-day)))
                score += extra_score
        pending_projects = [p for p in pending_projects if p.name not in removing_pends]
        #print("Projects finished.")
        
        #####
        # Start the best projects that can be started
        #####
        starting_projects_names = []
        zero_projects: List[str] = [] # names of projects to be ignored
        prev_project_success = False
        accu_p_score = 0
        min_p_score = math.inf
        max_p_score = 0
        for p_key in order_projects:
            if SIMULATE_SKIP_BUG and prev_project_success:
                prev_project_success = False
                continue
            #print("Checking project:", p_key)
            project = projects[p_key]
            if ZERO_PROJECTS or NORMALIZE_SORTING_PARAMS:
                p_score = maximum_project_points(project, day)
            if ZERO_PROJECTS:
                # Check if the project wont give any points and we cant ignore it
                if p_score == 0:
                    zero_projects.append(p_key)
                    continue
            if len(project.roles) > cant_free_workers:
                continue
            assigned_workers, assigned_roles, project_possible = individual_role_lookup(project, skill_workers, workers)
            if project_possible:
                for ass_w_index, name in enumerate(assigned_workers):
                    cant_free_workers -= 1
                    workers[name].free = False
                    if LEVEL_UP:
                        role = assigned_roles[ass_w_index]
                        worker_level = 0
                        if role[0] in workers[name].skills:
                            worker_level = workers[name].skills[role[0]]
                        if worker_level <= role[1]:
                            if worker_level == 0:
                                workers[name].skills[role[0]] = 1
                            else:
                                workers[name].skills[role[0]] += 1
                                workers[name].skill_level += 1
                starting_projects_names.append(p_key)
                planned.append(PlannedProject(project.name, assigned_workers))
                prev_project_success = True
            elif NORMALIZE_SORTING_PARAMS:
                accu_p_score += p_score
                if p_score > max_p_score:
                    max_p_score = p_score
                if p_score < min_p_score:
                    min_p_score = p_score
        for p_key in starting_projects_names:
            order_projects.remove(p_key)
            pending_projects.append(set_start_day(projects[p_key], day))
        for p in zero_projects:
            order_projects.remove(p)
        if NORMALIZE_SORTING_PARAMS and len(order_projects) > 0:
            mean_score = accu_p_score/len(order_projects)
            score_range = max_p_score - min_p_score
            if score_range == 0:
                score_range = 1

        # Go forward enough days so something changes
        if pending_projects:
            min_days_proj = min([(p.start_day+p.duration)-day for p in pending_projects])
            day += min_days_proj
        else:
            day += 1

    print(score)
    print(len(planned))
    for plann in planned:
        print(plann.name)
        print(*plann.workers, sep=" ")


if __name__ == "__main__":
    main()