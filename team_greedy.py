# Greedy implementation

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple

@dataclass
class Worker():
    name: str
    skills: Dict[str, int]
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
        for _ in range(n_skills):
            skill_line = input().split()
            s_name = skill_line[0]
            s_level = int(skill_line[1])
            skills[s_name] = s_level
        w = Worker(name, skills)
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

def lookup_free_worker(skill_workers: Dict[str, List[Worker]], role: str, level: int, assigned: List[str]) -> Tuple[str, bool]:
    for worker in skill_workers[role]:
        if worker.free and worker.name not in assigned:
            if worker.skills[role] >= level:
                return worker.name, True
    return None, False

def maximum_project_points(project: Project, current_day: int) -> int:
    return max(0, (project.score+min(0, (project.bbefore-(current_day+project.duration)))))

def sort_ratio_leftpoints_duration_less_first(name: str, projects: Dict[str, Project], day: int) -> float:
    return maximum_project_points(projects[name], day)/projects[name].duration

def sort_ratio_leftpoints_duration_bigger_first(name: str, projects: Dict[str, Project], day: int) -> float:
    return -(maximum_project_points(projects[name], day)/projects[name].duration)

def sort_ratio_leftpoints_duration_bigger_first_secondary_shortest(name: str, projects: Dict[str, Project], day: int) -> Tuple[float, int]:
    return (-maximum_project_points(projects[name], day)/projects[name].duration, projects[name].duration)

LEVEL_UP: bool = True # Workers level up
ZERO_PROJECTS: bool = True # Dinamically ignore the projects that won't give points.
SIMULATE_SKIP_BUG: bool = True # Accidental feature where if a project was accepted.
# the next project in the list was skipped. It was a bug but sometimes gave better results.

def main():
    workers, projects, skill_workers = input_data()
    order_projects = [p for p in projects]
    cant_free_workers = len(workers) # Amount of free (unoccupied) workers
    day = 0
    prev_num_projects = 0
    planned: List[PlannedProject] = []
    pending_projects: List[Project] = []
    score = 0
    while projects:
        #print(day)
        order_projects.sort(key=lambda x: sort_ratio_leftpoints_duration_bigger_first(x, projects, day))
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
        for p_key in order_projects:
            if SIMULATE_SKIP_BUG and prev_project_success:
                prev_project_success = False
                continue
            #print("Checking project:", p_key)
            project = projects[p_key]
            if ZERO_PROJECTS:
                # Check if the project wont give any points and we cant ignore it
                p_score = maximum_project_points(project, day)
                if p_score == 0:
                    zero_projects.append(p_key)
                    continue
            project_cant = False
            assigned_workers = []
            assigned_roles: List[Tuple[str, int]] = []
            if len(project.roles) > cant_free_workers:
                continue
            for role in project.roles:
                name, exists = lookup_free_worker(skill_workers, role[0], role[1], assigned_workers)
                if not exists:
                    project_cant = True
                    break
                assigned_workers.append(name)
                assigned_roles.append(role)
                if project_cant:
                    break
            if not project_cant:
                for ass_w_index, name in enumerate(assigned_workers):
                    cant_free_workers -= 1
                    workers[name].free = False
                    if LEVEL_UP:
                        role = assigned_roles[ass_w_index]
                        if workers[name].skills[role[0]] <= role[1]:
                            workers[name].skills[role[0]] += 1
                starting_projects_names.append(p_key)
                planned.append(PlannedProject(project.name, assigned_workers))
                prev_project_success = True
        for p_key in starting_projects_names:
            order_projects.remove(p_key)
            pending_projects.append(set_start_day(projects[p_key], day))
        for p in zero_projects:
            order_projects.remove(p)

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