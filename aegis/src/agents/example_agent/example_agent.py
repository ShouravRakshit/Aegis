# from typing import override
# import heapq
# import math
# from aegis.common.location import Location

# from aegis import (
#     AgentID,
#     CONNECT_OK,
#     END_TURN,
#     SEND_MESSAGE_RESULT,
#     MOVE,
#     MOVE_RESULT,
#     OBSERVE_RESULT,
#     PREDICT_RESULT,
#     SAVE_SURV,
#     SAVE_SURV_RESULT,
#     SEND_MESSAGE,
#     SLEEP_RESULT,
#     TEAM_DIG,
#     TEAM_DIG_RESULT,
#     AgentCommand,
#     AgentIDList,
#     Direction,
#     Rubble,
#     SurroundInfo,
#     Survivor,
# )
# from agent import BaseAgent, Brain, LogLevels


# class ExampleAgent(Brain):
#     def __init__(self) -> None:
#         super().__init__()
#         self._agent: BaseAgent = BaseAgent.get_base_agent()
#         self.receive_messages = []

#     @override
#     def handle_connect_ok(self, connect_ok: CONNECT_OK) -> None:
#         BaseAgent.log(LogLevels.Always, "CONNECT_OK")

#     @override
#     def handle_disconnect(self) -> None:
#         BaseAgent.log(LogLevels.Always, "DISCONNECT")

#     @override
#     def handle_dead(self) -> None:
#         BaseAgent.log(LogLevels.Always, "DEAD")

#     @override
#     def handle_messages_start(self, num_messages: int) -> None:
#         BaseAgent.log(LogLevels.Always, f"Starting to receive {num_messages} messages")
#         self.received_messages = []

#     @override
#     def handle_message(self, id_from: AgentID, msg: str) -> None:
#         BaseAgent.log(LogLevels.Always, f"Received message from {id_from}: {msg}")
#         self.received_messages.append((id_from, msg))

#     @override
#     def handle_messages_end(self) -> None:
#         BaseAgent.log(LogLevels.Always, "Finished receiving messages")

#     @override
#     def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"SEND_MESSAGE_RESULT: {smr}")

#     @override
#     def handle_move_result(self, mr: MOVE_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"MOVE_RESULT: {mr}")
#         BaseAgent.log(LogLevels.Test, f"{mr}")
#         print("#--- You need to implement handle_move_result function! ---#")
#         self.update_surround(mr.surroundings)


#     @override
#     def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"OBSERVER_RESULT: {ovr}")
#         BaseAgent.log(LogLevels.Test, f"{ovr}")
#         print("#--- You need to implement handle_observe_result function! ---#")


#     @override
#     def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"SAVE_SURV_RESULT: {ssr}")
#         BaseAgent.log(LogLevels.Test, f"{ssr}")
#         # Update world state
#         self.update_surround(ssr.surroundings)

#     @override
#     def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"PREDICT_RESULT: {prd}")
#         BaseAgent.log(LogLevels.Test, f"{prd}")

#     @override
#     def handle_sleep_result(self, sr: SLEEP_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"SLEEP_RESULT: {sr}")
#         BaseAgent.log(LogLevels.Test, f"{sr}")
#         print("#--- You need to implement handle_sleep_result function! ---#")
#         self.update_surround(sr.surroundings)


#     @override
#     def handle_team_dig_result(self, tdr: TEAM_DIG_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"TEAM_DIG_RSULT: {tdr}")
#         BaseAgent.log(LogLevels.Test, f"{tdr}")
#         print("#--- You need to implement handle_team_dig_result function! ---#")
#         self.update_surround(tdr.surroundings)

#     @override
#     def think(self) -> None:
#         BaseAgent.log(LogLevels.Always, "Thinking")
#         BaseAgent.log(LogLevels.Always, f"Agent location: {self._agent.get_location()}")
#         # At the start of the first round, send a request for surrounding information
#         # by moving to the center of the current grid. This will help initiate pathfinding.
#         if self._agent.get_round_number() == 1:
#             self.send_and_end_turn(MOVE(Direction.CENTER))
#             return

#         # Retrieve the current state of the world.
#         world = self.get_world()
#         if world is None:
#             self.send_and_end_turn(MOVE(Direction.CENTER))
#             return

#         # Fetch the grid at the agent’s current location. If the location is outside the world’s bounds,
#         # return a default move action and end the turn.

#         grid = world.get_grid_at(self._agent.get_location())
#         if grid is None:
#             self.send_and_end_turn(MOVE(Direction.CENTER))
#             return

#         # Get the top layer at the agent’s current location.
#         # If a survivor is present, save it and end the turn.
#         top_layer = grid.get_top_layer()
#         if top_layer:
#             self.send_and_end_turn(SAVE_SURV())
#             return

#         survivor_location = self.find_survivor_location(world)

#         # Run A* search to get the best direction to move towards the survivor
#         direction = self.run_a_star(world, survivor_location)

#         if direction:
#             self.send_and_end_turn(MOVE(direction))
#             return

#         # Default action
#         self.send_and_end_turn(MOVE(Direction.CENTER))
#         #self.send_and_end_turn(MOVE(Direction.NORTH))
#         return
    
#     def find_survivor_location(self, world):
#         grid_array = world.get_world_grid() 
        
#         for x in range(len(grid_array)):
#             for y in range(len(grid_array[x])):
#                 grid_cell = grid_array[x][y]  
                
#                 # Check if the grid cell contains survivor
#                 if grid_cell and grid_cell.percent_chance > 0:
#                     BaseAgent.log(LogLevels.Always, f"Survivor found at row: {x}, col: {y}")
#                     return Location(x, y)  # Return the location of the survivor

#         BaseAgent.log(LogLevels.Always, "No survivor found in the grid.")
#         return None

#     def run_a_star(self, world, goal):
#         start = self._agent.get_location()
#         priority_queue = []
#         path_trace = {}
#         heapq.heapify(priority_queue)
#         g_costs = {start: 0}
#         visited = set()

#         # Initialize the open list with the current location
#         heapq.heappush(priority_queue, (0, start))

#         while priority_queue:
#             #Ignore fcost, get current cell
#             _, current_cell = heapq.heappop(priority_queue)

#             if current_cell in visited:
#                 continue

#             visited.add(current_cell)

#             # If we have reached the goal, determine the direction
#             if current_cell == goal:
#                 return self.get_first_step_of_path(path_trace, start, goal)

#             for direction in Direction:
#                 neighbor_location = current_cell.add(direction)
#                 neighbor_grid_cell = world.get_grid_at(neighbor_location)

#                 # If the neighbor is out of bounds or already visited then skip it
#                 if neighbor_location in visited or neighbor_grid_cell is None or neighbor_grid_cell.is_killer_grid() or neighbor_grid_cell.is_on_fire():
#                     continue

#                 # Calculate g(n) - the movement cost to move into this neighboring cell
#                 current_g_cost = g_costs[current_cell] + neighbor_grid_cell.move_cost

#                 # If this neighbor is not in g_costs or a better path was discovered, update fields
#                 if neighbor_location not in g_costs or current_g_cost < g_costs[neighbor_location]:
#                     g_costs[neighbor_location] = current_g_cost
#                     h_cost = self.get_heuristic(neighbor_location, goal)
#                     f_cost = current_g_cost + h_cost

#                     # Record the path and push the neighbor onto the open list
#                     path_trace [neighbor_location] = (current_cell, direction)
#                     heapq.heappush(priority_queue, (f_cost, neighbor_location))

#         # If no path to the target is found
#         return None
    
#     def get_heuristic(self, current, destination):
#         x_distance = (destination.x - current.x) ** 2
#         y_distance = (destination.y - current.y) ** 2
#         euclidean_distance = x_distance + y_distance
#         return math.sqrt(euclidean_distance)

#     def get_first_step_of_path(self, came_from, start, goal):
#         first_step = None

#         current = goal
#         while current != start:
#             previous, direction = came_from[current]
#             if previous == start:
#                 return direction
#             current = previous
#         return first_step  

#     # @override
#     # def think(self) -> None:
#     #     BaseAgent.log(LogLevels.Always, "Thinking")

#     #     # Check if any messages have been received
#     #     if not self.received_messages:
#     #         BaseAgent.log(LogLevels.Always, "No other agents detected. Proceeding alone.")
#     #         # Send a message to other agents
#     #         self._agent.send(
#     #             SEND_MESSAGE(
#     #                 AgentIDList(), f"Hello from agent {self._agent.get_agent_id().id}"
#     #             )
#     #         )
#     #     else:
#     #         BaseAgent.log(LogLevels.Always, "Other agents detected. Proceeding alone for this challenge.")

#     #     # Proceed with acting alone
#     #     self.act_alone()

            
#         # def act_alone(self):
#         #     # Retrieve the current state of the world.
#         #     world = self.get_world()
#         #     if world is None:
#         #         self.send_and_end_turn(MOVE(Direction.CENTER))
#         #         return

        

#         # Fetch the cell at the agent’s current location. If the location is outside the world’s bounds,
#         # return a default move action and end the turn.
#             # cell = world.get_cell_at(self._agent.get_location())
#         #     if cell is None:
#         #         self.send_and_end_turn(MOVE(Direction.CENTER))
#         #         return

#         # # Get the top layer at the agent’s current location.
#         #     top_layer = cell.get_top_layer()

#         #     # If a survivor is present, save it and end the turn.
#         #     if isinstance(top_layer, Survivor):
#         #         self.send_and_end_turn(SAVE_SURV())
#         #         return

#         #     # If rubble is present, clear it and end the turn.
#         #     if isinstance(top_layer, Rubble):
#         #         self.send_and_end_turn(TEAM_DIG())
#         #         return

#         #     # Default action: Move the agent north if no other specific conditions are met.
#         #     self.send_and_end_turn(MOVE(Direction.NORTH))

#     def send_and_end_turn(self, command: AgentCommand):
#         """Send a command and end your turn."""
#         BaseAgent.log(LogLevels.Always, f"SENDING {command}")
#         self._agent.send(command)
#         self._agent.send(END_TURN())

#     def update_surround(self, surround_info: SurroundInfo):
#         """
#         Updates the current and surrounding cells of the agent.

#         You can check assignment 1 to figure out how to use this function.
#         """
#         world = self.get_world()
#         if world is None:
#             return

#         for dir in Direction:
#             cell_info = surround_info.get_surround_info(dir)
#             if cell_info is None:
#                 continue

#             cell = world.get_cell_at(cell_info.location)
#             if cell is None:
#                 continue

#             cell.move_cost = cell_info.move_cost
#             cell.set_top_layer(cell_info.top_layer)







import heapq
import math
from typing import override

from aegis.common import Direction
from aegis.common.commands.aegis_commands import MOVE_RESULT, SAVE_SURV_RESULT
from aegis.common.commands.agent_command import AgentCommand
from aegis.common.commands.agent_commands import (
    END_TURN,
    MOVE,
    SAVE_SURV,
)
from aegis.common.location import Location
from aegis.common.world.cell import Cell
# from aegis.common.world.info import SurroundInfo, SurvivorInfo, WorldObjectInfo
from aegis.common.world.objects import Survivor
from agent.base_agent import BaseAgent
from agent.brain import Brain
from agent.log_levels import LogLevels


class ExampleAgent(Brain):
    def __init__(self) -> None:
        super().__init__()
        self._agent = BaseAgent.get_base_agent()

    @override
    def handle_move_result(self, mr: MOVE_RESULT) -> None:
        self.update_surround(mr.surround_info)

    @override
    def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
        self.update_surround(ssr.surround_info)

    @override
    def think(self) -> None:
        BaseAgent.log(LogLevels.Always, "Thinking")
        BaseAgent.log(LogLevels.Always, f"Agent location: {self._agent.get_location()}")
        # At the start of the first round, send a request for surrounding information
        # by moving to the center of the current grid. This will help initiate pathfinding.
        if self._agent.get_round_number() == 1:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Retrieve the current state of the world.
        world = self.get_world()
        if world is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Fetch the grid at the agent’s current location. If the location is outside the world’s bounds,
        # return a default move action and end the turn.

        grid = world.get_grid_at(self._agent.get_location())
        if grid is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Get the top layer at the agent’s current location.
        # If a survivor is present, save it and end the turn.
        top_layer = grid.get_top_layer()
        if top_layer:
            self.send_and_end_turn(SAVE_SURV())
            return

        survivor_location = self.find_survivor_location(world)

        # Run A* search to get the best direction to move towards the survivor
        direction = self.run_a_star(world, survivor_location)

        if direction:
            self.send_and_end_turn(MOVE(direction))
            return

        # Default action
        self.send_and_end_turn(MOVE(Direction.CENTER))
        #self.send_and_end_turn(MOVE(Direction.NORTH))
        return

    def find_survivor_location(self, world):
        grid_array = world.get_world_grid() 
        
        for x in range(len(grid_array)):
            for y in range(len(grid_array[x])):
                grid_cell = grid_array[x][y]  
                
                # Check if the grid cell contains survivor
                if grid_cell and grid_cell.percent_chance > 0:
                    BaseAgent.log(LogLevels.Always, f"Survivor found at row: {x}, col: {y}")
                    return Location(x, y)  # Return the location of the survivor

        BaseAgent.log(LogLevels.Always, "No survivor found in the grid.")
        return None  
    
    def run_a_star(self, world, goal):
        start = self._agent.get_location()
        priority_queue = []
        path_trace = {}
        heapq.heapify(priority_queue)
        g_costs = {start: 0}
        visited = set()

        # Initialize the open list with the current location
        heapq.heappush(priority_queue, (0, start))

        while priority_queue:
            #Ignore fcost, get current cell
            _, current_cell = heapq.heappop(priority_queue)

            if current_cell in visited:
                continue

            visited.add(current_cell)

            # If we have reached the goal, determine the direction
            if current_cell == goal:
                return self.get_first_step_of_path(path_trace, start, goal)

            for direction in Direction:
                neighbor_location = current_cell.add(direction)
                neighbor_grid_cell = world.get_grid_at(neighbor_location)

                # If the neighbor is out of bounds or already visited then skip it
                if neighbor_location in visited or neighbor_grid_cell is None or neighbor_grid_cell.is_killer_grid() or neighbor_grid_cell.is_on_fire():
                    continue

                # Calculate g(n) - the movement cost to move into this neighboring cell
                current_g_cost = g_costs[current_cell] + neighbor_grid_cell.move_cost

                # If this neighbor is not in g_costs or a better path was discovered, update fields
                if neighbor_location not in g_costs or current_g_cost < g_costs[neighbor_location]:
                    g_costs[neighbor_location] = current_g_cost
                    h_cost = self.get_heuristic(neighbor_location, goal)
                    f_cost = current_g_cost + h_cost

                    # Record the path and push the neighbor onto the open list
                    path_trace [neighbor_location] = (current_cell, direction)
                    heapq.heappush(priority_queue, (f_cost, neighbor_location))

        # If no path to the target is found
        return None

    def get_heuristic(self, current, destination):
        x_distance = (destination.x - current.x) ** 2
        y_distance = (destination.y - current.y) ** 2
        euclidean_distance = x_distance + y_distance
        return math.sqrt(euclidean_distance)

    def get_first_step_of_path(self, came_from, start, goal):
        first_step = None

        current = goal
        while current != start:
            previous, direction = came_from[current]
            if previous == start:
                return direction
            current = previous
        return first_step    

    def send_and_end_turn(self, command: AgentCommand):
        """Send a command and end your turn."""
        BaseAgent.log(LogLevels.Always, f"SENDING {command}")
        self._agent.send(command)
        self._agent.send(END_TURN())

    def update_surround(self, surround_info: SurroundInfo):
        """Updates the current and surrounding grid cells of the agent."""
        world = self.get_world()
        if world is None:
            return

        for dir in Direction:
            grid_info = surround_info.get_surround_info(dir)
            if grid_info is None:
                continue

            grid = world.get_grid_at(grid_info.location)
            if grid is None:
                continue

            grid.move_cost = grid_info.move_cost
            self.update_top_layer(grid, grid_info.top_layer_info)

    def update_top_layer(self, grid: Cell, top_layer: WorldObjectInfo):
        """Updates the top layer of the grid. Converting WorldObjectInfo to WorldObject"""
        if isinstance(top_layer, SurvivorInfo):
            layer = Survivor(
                top_layer.id,
                top_layer.energy_level,
                top_layer.damage_factor,
                top_layer.body_mass,
                top_layer.mental_state,
            )
            grid.set_top_layer(layer)
