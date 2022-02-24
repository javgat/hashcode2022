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
    print(workers)
    print(projects)

if __name__ == "__main__":
    main()