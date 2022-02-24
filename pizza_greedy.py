#!/usr/bin/env python3
# Author: Javier Gatón Herguedas.
# Pizza Hash Code Answer using a greedy approach.
# It deletes the client that collided with most ingredients.

from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Client():
    def __init__(self, id: str, client_likes: List[str], client_dislikes: List[str], num_collisions: int):
        self.id = id
        self.client_likes = client_likes
        self.client_dislikes = client_dislikes
        self.num_collisions = num_collisions

@dataclass
class Solution():
    def __init__(self, puntuacion: int, ingredients: List[str]):
        self.puntuacion = puntuacion
        self.ingredients = ingredients


def input_data() -> Tuple[Dict[str, List], Dict[str, List], List[Client]]:
    num_clients = int(input())
    likes: Dict[str, List] = {}
    dislikes: Dict[str, List] = {}
    clients: List[Client] = []

    for id in range(num_clients):
        like_line = input().split()
        n_likes = int(like_line[0])
        client_likes = []

        dislike_line = input().split()
        n_dislikes = int(dislike_line[0])
        client_dislikes = []

        num_collisions = 0

        # Check that its not a troll client
        troll = False
        for i in range(n_likes):
            food = like_line[i+1]
            for j in range(n_dislikes):
                dfood = dislike_line[j+1]
                if dfood == food:
                    troll = True
                    break
            if troll:
                break
        if troll:
            continue

        for i in range(n_likes):
            food = like_line[i+1]
            client_likes.append(food)
            if food in likes:
                likes[food].append(id)
            else:
                likes[food] = [id]
            if food in dislikes:
                ds = dislikes[food]
                for j in ds:
                    clients[j].num_collisions += 1
                num_collisions += len(dislikes[food])
        for i in range(n_dislikes):
            food = dislike_line[i+1]
            client_dislikes.append(food)
            if food in dislikes:
                dislikes[food].append(id)
            else:
                dislikes[food] = [id]
            if food in likes:
                ls = likes[food]
                for j in ls:
                    clients[j].num_collisions += 1
                num_collisions += len(likes[food])
        clients.append(Client(id, client_likes, client_dislikes, num_collisions))
    return likes, dislikes, clients

def get_non_collision_ingredients(likes: Dict[str, List], dislikes: Dict[str, List]) -> List[str]:
    foods = []
    for food in likes.keys():
        if not food in dislikes or len(dislikes[food]) == 0:
            foods.append(food)
    return foods

def main():
    likes, dislikes, clients = input_data()
    order_clients = [(clients[i].num_collisions, i) for i in range(len(clients))]
    order_clients.sort()
    puntuacion = sum(1 for c in clients if c.num_collisions == 0)
    ingredients = get_non_collision_ingredients(likes, dislikes)
    best_solution = Solution(puntuacion, ingredients)
    print(puntuacion)
    while order_clients:
        #print(order_clients)
        if not order_clients:
            print("Impossible!")
            break
        deleting_id = order_clients.pop()[1]
        lik_foods = clients[deleting_id].client_likes
        for food in lik_foods:
            likes[food].remove(deleting_id)
            if food in dislikes:
                for j in dislikes[food]:
                    clients[j].num_collisions -= 1
        dis_foods = clients[deleting_id].client_dislikes
        for food in dis_foods:
            dislikes[food].remove(deleting_id)
            if food in likes:
                for j in likes[food]:
                    clients[j].num_collisions -= 1
        order_clients = [(clients[oc[1]].num_collisions, oc[1]) for oc in order_clients]
        order_clients.sort()
        puntuacion = sum(1 for c in clients if c.num_collisions == 0)
        if puntuacion > best_solution.puntuacion:
            ingredients = get_non_collision_ingredients(likes, dislikes)
            best_solution = Solution(puntuacion, ingredients)
        #DO NOT DELETE THE CLIENT THAT WOULD BREAK IT
    print(puntuacion)
    print(len(best_solution.ingredients), *best_solution.ingredients)

if __name__ == "__main__":
    main()