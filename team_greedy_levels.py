# Greedy implementation

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Worker():
    name: str
    skills: Dict[str, int]

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

def input_data() -> Tuple[List[Worker], List[Project], Dict[str, List[Worker]]]:
    first_line = input().split()
    n_workers = int(first_line[0])
    n_projects = int(first_line[1])
    skill_workers: Dict[str, List[Worker]] = {}
    workers: List[Worker] = []
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
        workers.append(w)
    
    projects: List[Project] = []
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
            projects.append(p)
    return (workers, projects, skill_workers)

def set_start_day(p: Project, day: int) -> Project:
    p.start_day = day
    return p

def lookup_free_worker(free_workers: List[str], skill_workers: Dict[str, List[Worker]], role: str, level: int, assigned: List[str]) -> Tuple[Worker, bool]:
    for worker in skill_workers[role]:
        if worker.name in free_workers and worker.name not in assigned:
            if worker.skills[role] >= level:
                return worker, True
    return None, False

def main():
    workers, projects, skill_workers = input_data()
    free_workers = [w.name for w in workers]
    day = 0
    prev_num_projects = 0
    planned: List[PlannedProject] = []
    pending_projects: List[Project] = []
    score = 0
    while projects:
        #print(day)
        projects.sort(key=lambda x: (max(0, (x.score+min(0, (x.bbefore-(day+x.duration))))/x.duration), -x.duration), reverse=True)
        #print([(max(0, (x.score+min(0, (x.bbefore-(day+x.duration))))/x.duration), -x.duration) for x in projects])
        #print(projects)
        if prev_num_projects == len(projects) and len(free_workers) == len(workers):
            break
        prev_num_projects = len(projects)
        starting_projects_names = []
        ## VACIAMOS
        #print("a vaciar!")
        removing_pends: List[str] = []
        for pend in pending_projects:
            if day >= pend.start_day + pend.duration:
                removing_pends.append(pend.name)
                plann = [p for p in planned if p.name == pend.name][0]
                for wk in plann.workers:
                    free_workers.append(wk)
                extra_score = max(0, pend.score + min(0, (pend.bbefore-day)))
                #print(extra_score)
                score += extra_score
        pending_projects = [p for p in pending_projects if p.name not in removing_pends]
        #borrar projs de pends
        for project in projects:
            #print("vaciado")
            project_cant = False
            assigned_workers = []
            assigned_tuples: List[Tuple[Worker, str, int]] = []
            if len(project.roles) > len(free_workers):
                continue
            for role in project.roles:
                looked_worker, exists = lookup_free_worker(free_workers, skill_workers, role[0], role[1], assigned_workers)
                if not exists:
                    project_cant = True
                    break
                assigned_workers.append(looked_worker.name)
                assigned_tuples.append((looked_worker, role[0], role[1]))
                if project_cant:
                    break
            if not project_cant:
                for name in assigned_workers:
                    free_workers.remove(name)
                for tup in assigned_tuples:
                    if tup[0].skills[tup[1]] <= tup[2]:
                        tup[0].skills[tup[1]] += 1
                starting_projects_names.append(project.name)
                planned.append(PlannedProject(project.name, assigned_workers))
        pending_projects_new = [set_start_day(p, day) for p in projects if p.name in starting_projects_names]
        pending_projects += pending_projects_new
        projects = [p for p in projects if p.name not in starting_projects_names]
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