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
    roles: Dict[str, List[int]]

@dataclass
class PlannedProject():
    name: str
    workers: List[str]

def input_data() -> Tuple[List[Worker], List[Project]]:
    first_line = input().split()
    n_workers = int(first_line[0])
    n_projects = int(first_line[1])
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
        workers.append(w)
    
    projects: List[Project] = []
    for _ in range(n_projects):
        proj_line = input().split()
        name = proj_line[0]
        duration = int(proj_line[1])
        score = int(proj_line[2])
        bbefore = int(proj_line[3])
        n_roles = int(proj_line[4])
        roles: Dict[str, List[int]] = {}
        for _ in range(n_roles):
            role_line = input().split()
            r_name = role_line[0]
            r_level = int(role_line[1])
            if r_name in roles:
                roles[r_name].append(r_level)
            else:
                roles[r_name] = [r_level]
        p = Project(name, duration, score, bbefore, roles)
        projects.append(p)
    return (workers, projects)

def main():
    workers, projects = input_data()
    free_workers = [w.name for w in workers]
    day = 0
    projects.sort(key=lambda x: min(0, (x.score+min(0, (x.bbefore-(day+x.duration))))/x.duration))
    prev_num_projects = 0
    while projects:
        if prev_num_projects == len(projects) and len(free_workers) == len(workers):
            break
        prev_num_projects = len(projects)
        starting_projects_names = []
        for project in projects:
            project_cant = False
            assigned_workers = []
            for role in project.roles:
                for level in project.roles[role]:
                    name, exists = lookup_free_worker(free_workers, workers, role, level)
                    assigned_workers.append(name)
                    if not exists:
                        project_cant = True
                        break
                if project_cant:
                    break
            for name in assigned_workers:
                free_workers.remove(name)
            starting_projects_names.append(project.name)
        projects = [p for p in projects if p.name not in starting_projects_names]
            
            


    #print(workers)
    #print(projects)


if __name__ == "__main__":
    main()