# import heapq
# import math
# from typing import override

# from aegis import (
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
# from aegis.common.location import Location

# from agent import BaseAgent, Brain, LogLevels


# class ExampleAgent(Brain):
#     def __init__(self) -> None:
#         super().__init__()
#         self._agent: BaseAgent = BaseAgent.get_base_agent()
#         # Initialize movement tracking
#         self.current_surround_info = None  # Store the latest surround info
#         self.saved_survivors = []  # List to track saved survivors
#         self.survivor_location = None  # Class variable to store survivor location

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
#     def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"SEND_MESSAGE_RESULT: {smr}")
#         BaseAgent.log(LogLevels.Test, f"{smr}")
#         BaseAgent.log(LogLevels.Always, f"Received message from Agent {smr.from_agent_id}: '{smr.msg}'")

#         # Parse and log location
#         if "My location is" in smr.msg:
#             location = smr.msg.split("My location is")[-1].split(";")[0].strip()
#             BaseAgent.log(LogLevels.Always, f"Received location of Agent {smr.from_agent_id}: {location}")

#         # Parse and log energy
#         if "Energy:" in smr.msg:
#             energy = smr.msg.split("Energy:")[-1].split(";")[0].strip()
#             BaseAgent.log(LogLevels.Always, f"Received energy of Agent {smr.from_agent_id}: {energy}")

#         # Parse and log survivor location
#         if "Survivor location:" in smr.msg:
#             survivor_location = smr.msg.split("Survivor location:")[-1].split(";")[0].strip()
#             BaseAgent.log(LogLevels.Always, f"Received survivor location from Agent {smr.from_agent_id}: {survivor_location}")

#         # Parse and log rubble details
#         if "Rubble at" in smr.msg:
#             rubble_details = smr.msg.split("Rubble at")[-1].split(";")[0].strip()
#             BaseAgent.log(LogLevels.Always, f"Received rubble details from Agent {smr.from_agent_id}: {rubble_details}")

#     @override
#     def handle_move_result(self, mr: MOVE_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"MOVE_RESULT: {mr}")
#         BaseAgent.log(LogLevels.Test, f"{mr}")
#         # Store the latest surround info
#         self.current_surround_info = mr.surround_info

#     @override
#     def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"OBSERVER_RESULT: {ovr}")
#         BaseAgent.log(LogLevels.Test, f"{ovr}")
#         #print("#--- You need to implement handle_observe_result function! ---#")

#     @override
#     def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"SAVE_SURV_RESULT: {ssr}")
#         BaseAgent.log(LogLevels.Test, f"{ssr}")
#         self.current_surround_info = ssr.surround_info

#     @override
#     def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"PREDICT_RESULT: {prd}")
#         BaseAgent.log(LogLevels.Test, f"{prd}")

#     @override
#     def handle_sleep_result(self, sr: SLEEP_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"SLEEP_RESULT: {sr}")
#         BaseAgent.log(LogLevels.Test, f"{sr}")
#         #print("#--- You need to implement handle_sleep_result function! ---#")

#     @override
#     def handle_team_dig_result(self, tdr: TEAM_DIG_RESULT) -> None:
#         BaseAgent.log(LogLevels.Always, f"TEAM_DIG_RSULT: {tdr}")
#         BaseAgent.log(LogLevels.Test, f"{tdr}")
#         self.current_surround_info = tdr.surround_info

#     @override
#     def think(self) -> None:
#         BaseAgent.log(LogLevels.Always, "Thinking")

#         # Send a message to other agents in my group.
#         current_location = self._agent.get_location()
#         current_energy = self._agent.get_energy_level()
#         message = f"My location is {current_location}; Energy: {current_energy}"
        
#         # Include survivor location if known
#         if hasattr(self, 'survivor_location') and self.survivor_location is not None:
#             message += f"; Survivor location: {self.survivor_location}"

#         # Check for rubble in the current cell
#         current_cell = self.get_world().get_cell_at(current_location)
#         if current_cell and isinstance(current_cell.get_top_layer(), Rubble):
#             rubble = current_cell.get_top_layer()
#             rubble_details = f"Rubble at {current_location}: Energy={rubble.json()['arguments']['remove_energy']}, Agents={rubble.json()['arguments']['remove_agents']}"
#             message += f"; {rubble_details}"

#         self._agent.send(SEND_MESSAGE(AgentIDList(), message))
#         BaseAgent.log(LogLevels.Always, f"Message sent: {message}")
        
#         # Empty AgentIDList will send to group members.
#         # Update the world with latest surround info
#         if self.current_surround_info is not None:
#             self.update_surround(self.current_surround_info)

#         # Retrieve the current state of the world.
#         world = self.get_world()
#         if world is None:
#             self.send_and_end_turn(MOVE(Direction.CENTER))
#             return

#         # Fetch the cell at the agent’s current location. If the location is outside the world’s bounds,
#         # return a default move action and end the turn.
#         cell = world.get_cell_at(self._agent.get_location())
#         if cell is None:
#             self.send_and_end_turn(MOVE(Direction.CENTER))
#             return

#         # Get the top layer at the agent’s current location.
#         top_layer = cell.get_top_layer()

#         # If a survivor is present, save it and end the turn.
#         if isinstance(top_layer, Survivor):
#             self.send_and_end_turn(SAVE_SURV())
#             BaseAgent.log(LogLevels.Always, f"Survivor saved at location: {cell.location}")
#             return
        
#         # If rubble is present, clear it and end the turn.
#         if isinstance(top_layer, Rubble) and cell.location == self.survivor_location:
#             self.send_and_end_turn(TEAM_DIG())
#             BaseAgent.log(LogLevels.Always, f"Digging rubble at location: {cell.location}")
#             return

#         # No more survivors or rubble at this location, mark it as saved
#         if cell.location == self.survivor_location and cell.location not in self.saved_survivors:
#             self.saved_survivors.append(cell.location)
#             BaseAgent.log(LogLevels.Always, f"Location {cell.location} marked as saved.")

#         # # If a survivor is present and has not been saved before, save it and end the turn.
#         # if isinstance(top_layer, Survivor) and cell.location not in self.saved_survivors:
#         #     self.send_and_end_turn(SAVE_SURV())
#         #     print ("survivor saved at location: ", cell.location)
#         #     self.saved_survivors.append(cell.location)  # Mark the survivor as saved
#         #     return

#         # # If rubble is present, clear it and end the turn.
#         # if isinstance(top_layer, Rubble) and cell.location == self.survivor_location and cell.location not in self.saved_survivors:
#         #     self.send_and_end_turn(TEAM_DIG())
#         #     return

#         survivor_location = self.find_survivor_location(world)
#         if survivor_location is None:
#             # No survivors left to save; end turn or implement other logic
#             BaseAgent.log(LogLevels.Always, "No more survivors to save.")
#             self.send_and_end_turn(END_TURN())
#             return

#         # Run A* search to get the best direction to move towards the survivor
#         direction = self.run_a_star(world, survivor_location)

#         if direction:
#             self.send_and_end_turn(MOVE(direction))
#             return
#         else:
#             # Move east and reset north movement
#             BaseAgent.log(LogLevels.Always, "Moving EAST")
#             self.send_and_end_turn(MOVE(Direction.EAST))

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


# #    def find_survivor_location(self, world):
# #        grid_array = world.get_world_grid() 
# #        
# #        for x in range(len(grid_array)):
# #            for y in range(len(grid_array[x])):
# #                grid_cell = grid_array[x][y]  
# #
# #                grid_location = Location(x, y)
# #                # Check if the grid cell contains survivor and if it hasn't been saved
# #                if grid_cell and grid_cell.survivor_chance > 0 and grid_location not in self.saved_survivors:
# #                    BaseAgent.log(LogLevels.Always, f"Survivor found at row: {x}, col: {y}")
# #                    self.survivor_location = grid_location  # Set the class variable
# #                    return Location(x, y)  # Return the location of the survivor#
# #
# #        BaseAgent.log(LogLevels.Always, "No survivor found in the grid.")
# #        self.survivor_location = None  # If no survivor found, set the class variable to None
# #        return None 

#     def find_survivor_location(self, world):
#         grid_array = world.get_world_grid()
#         closest_survivor_location = None
#         closest_distance = float('inf')  # Start with a very large distance
        
#         for x in range(len(grid_array)):
#             for y in range(len(grid_array[x])):
#                 grid_cell = grid_array[x][y]
#                 grid_location = Location(x, y)

#                 # Check if the grid cell contains a survivor and hasn't been saved
#                 if grid_cell and grid_cell.survivor_chance > 0 and grid_location not in self.saved_survivors:
#                     # Calculate the Euclidean distance from the agent's current location to the survivor
#                     distance = self.calculate_distance(self._agent.get_location(), grid_location)
                    
#                     # Check if this survivor is the closest so far
#                     if distance < closest_distance:
#                         # You can add accessibility checks here if needed
#                         closest_survivor_location = grid_location
#                         closest_distance = distance
        
#         if closest_survivor_location:
#             BaseAgent.log(LogLevels.Always, f"Closest survivor found at {closest_survivor_location}")
#             self.survivor_location = closest_survivor_location
#             return closest_survivor_location  # Return the closest survivor location
#         else:
#             BaseAgent.log(LogLevels.Always, "No accessible survivor found.")
#             self.survivor_location = None  # If no survivor found, set the class variable to None
#             return None

#     def calculate_distance(self, current_location, target_location):
#         """Calculates the Euclidean distance between two locations."""
#         dx = target_location.x - current_location.x
#         dy = target_location.y - current_location.y
#         return math.sqrt(dx ** 2 + dy ** 2) 
    
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
#                 neighbor_grid_cell = world.get_cell_at(neighbor_location)

#                 # If the neighbor is out of bounds or already visited then skip it
#                 if neighbor_location in visited or neighbor_grid_cell is None or neighbor_grid_cell.is_killer_cell() or neighbor_grid_cell.is_fire_cell() or neighbor_grid_cell.is_on_fire():
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
















































import heapq
import math
from typing import override

from aegis import (
    CONNECT_OK,
    END_TURN,
    SEND_MESSAGE_RESULT,
    MOVE,
    MOVE_RESULT,
    OBSERVE_RESULT,
    PREDICT_RESULT,
    SAVE_SURV,
    SAVE_SURV_RESULT,
    SEND_MESSAGE,
    SLEEP_RESULT,
    TEAM_DIG,
    TEAM_DIG_RESULT,
    AgentCommand,
    AgentIDList,
    Direction,
    Rubble,
    SurroundInfo,
    Survivor,
)
from aegis.common.location import Location

from agent import BaseAgent, Brain, LogLevels


class ExampleAgent(Brain):
    def __init__(self) -> None:
        super().__init__()
        self._agent: BaseAgent = BaseAgent.get_base_agent()
        self.current_surround_info = None
        self.saved_survivors = []
        self.survivor_location = None
        self.team_number = None
        self.other_agent_locations = {}
        self.other_agent_energies = {}
        self.team_survivor_locations = {}

    @override
    def handle_connect_ok(self, connect_ok: CONNECT_OK) -> None:
        BaseAgent.log(LogLevels.Always, "CONNECT_OK")
        self.team_number = self._agent.get_agent_id().id % 3

    @override
    def handle_disconnect(self) -> None:
        BaseAgent.log(LogLevels.Always, "DISCONNECT")

    @override
    def handle_dead(self) -> None:
        BaseAgent.log(LogLevels.Always, "DEAD")

    @override
    def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"SEND_MESSAGE_RESULT: {smr}")
        BaseAgent.log(LogLevels.Test, f"{smr}")
        BaseAgent.log(LogLevels.Always, f"Received message from Agent {smr.from_agent_id}: '{smr.msg}'")

        other_agent_id = smr.from_agent_id.id
        other_agent_team = other_agent_id % 3

        # Parse location value
        if "My location is" in smr.msg:
            loc_str = smr.msg.split("My location is")[-1].split(";")[0].strip()
            # Parse format "( X 2 , Y 8 )" to get coordinates
            try:
                x = int(loc_str.split(",")[0].split("X")[1].strip())
                y = int(loc_str.split(",")[1].split("Y")[1].strip().rstrip(")"))
                self.other_agent_locations[other_agent_id] = Location(x, y)
                BaseAgent.log(LogLevels.Always, f"Received location of Agent {smr.from_agent_id}: Location({x}, {y})")
            except:
                BaseAgent.log(LogLevels.Always, f"Failed to parse location from: {loc_str}")

        # Parse energy value
        if "Energy:" in smr.msg:
            try:
                energy = int(smr.msg.split("Energy:")[-1].split(";")[0].strip())
                self.other_agent_energies[other_agent_id] = energy
                BaseAgent.log(LogLevels.Always, f"Received energy of Agent {smr.from_agent_id}: {energy}")
            except:
                BaseAgent.log(LogLevels.Always, "Failed to parse energy value")

        # Parse survivor location
        if "Survivor location:" in smr.msg:
            surv_loc_str = smr.msg.split("Survivor location:")[-1].split(";")[0].strip()
            try:
                x = int(surv_loc_str.split(",")[0].split("X")[1].strip())
                y = int(surv_loc_str.split(",")[1].split("Y")[1].strip().rstrip(")"))
                if other_agent_team == self.team_number:
                    self.team_survivor_locations[f"{x},{y}"] = Location(x, y)
                BaseAgent.log(LogLevels.Always, f"Received survivor location from Agent {smr.from_agent_id}: Location({x}, {y})")
            except:
                BaseAgent.log(LogLevels.Always, f"Failed to parse survivor location from: {surv_loc_str}")

    @override
    def handle_move_result(self, mr: MOVE_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"MOVE_RESULT: {mr}")
        BaseAgent.log(LogLevels.Test, f"{mr}")
        self.current_surround_info = mr.surround_info

    @override
    def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"OBSERVER_RESULT: {ovr}")
        BaseAgent.log(LogLevels.Test, f"{ovr}")

    @override
    def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"SAVE_SURV_RESULT: {ssr}")
        BaseAgent.log(LogLevels.Test, f"{ssr}")
        self.current_surround_info = ssr.surround_info

    @override
    def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"PREDICT_RESULT: {prd}")
        BaseAgent.log(LogLevels.Test, f"{prd}")

    @override
    def handle_sleep_result(self, sr: SLEEP_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"SLEEP_RESULT: {sr}")
        BaseAgent.log(LogLevels.Test, f"{sr}")

    @override
    def handle_team_dig_result(self, tdr: TEAM_DIG_RESULT) -> None:
        BaseAgent.log(LogLevels.Always, f"TEAM_DIG_RESULT: {tdr}")
        BaseAgent.log(LogLevels.Test, f"{tdr}")
        self.current_surround_info = tdr.surround_info

    @override
    def think(self) -> None:
        BaseAgent.log(LogLevels.Always, "Thinking")

        current_location = self._agent.get_location()
        current_energy = self._agent.get_energy_level()
        
        # Enhanced status message with team information
        message = f"My location is {current_location}; Energy: {current_energy}; Team: {self.team_number}"
        
        if hasattr(self, 'survivor_location') and self.survivor_location is not None:
            message += f"; Survivor location: {self.survivor_location}"

        # Check for rubble and include team coordination info
        current_cell = self.get_world().get_cell_at(current_location)
        if current_cell and isinstance(current_cell.get_top_layer(), Rubble):
            rubble = current_cell.get_top_layer()
            rubble_details = f"Rubble at {current_location}: Energy={rubble.json()['arguments']['remove_energy']}, Agents={rubble.json()['arguments']['remove_agents']}"
            message += f"; {rubble_details}"

        self._agent.send(SEND_MESSAGE(AgentIDList(), message))
        BaseAgent.log(LogLevels.Always, f"Message sent: {message}")

        # Update world info
        if self.current_surround_info is not None:
            self.update_surround(self.current_surround_info)

        world = self.get_world()
        if world is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        cell = world.get_cell_at(current_location)
        if cell is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        top_layer = cell.get_top_layer()

        # Handle survivor rescue
        if isinstance(top_layer, Survivor):
            self.send_and_end_turn(SAVE_SURV())
            BaseAgent.log(LogLevels.Always, f"Survivor saved at location: {cell.location}")
            if cell.location not in self.saved_survivors:
                self.saved_survivors.append(cell.location)
            return

        # Handle rubble with team coordination
        if isinstance(top_layer, Rubble) and cell.location == self.survivor_location:
            # Try to dig even if alone, but prefer team coordination
            nearby_team_members = sum(1 for agent_id, loc in self.other_agent_locations.items() 
                                    if agent_id % 3 == self.team_number 
                                    and self.calculate_distance(current_location, loc) <= 2)
            
            # Always dig if at survivor location, regardless of team members
            self.send_and_end_turn(TEAM_DIG())
            BaseAgent.log(LogLevels.Always, f"Digging rubble at location: {cell.location}" + 
                        (" with team" if nearby_team_members >= 1 else " alone"))
            return

        # Find closest survivor based on team assignment
        survivor_location = self.find_survivor_location(world)
        if survivor_location is None:
            BaseAgent.log(LogLevels.Always, "No more survivors to save.")
            self.send_and_end_turn(END_TURN())
            return

        # Move toward survivor
        direction = self.run_a_star(world, survivor_location)
        if direction:
            self.send_and_end_turn(MOVE(direction))
        else:
            BaseAgent.log(LogLevels.Always, "Moving EAST")
            self.send_and_end_turn(MOVE(Direction.EAST))

    def send_and_end_turn(self, command: AgentCommand):
        BaseAgent.log(LogLevels.Always, f"SENDING {command}")
        self._agent.send(command)
        self._agent.send(END_TURN())

    def update_surround(self, surround_info: SurroundInfo):
        world = self.get_world()
        if world is None:
            return

        for dir in Direction:
            cell_info = surround_info.get_surround_info(dir)
            if cell_info is None:
                continue

            cell = world.get_cell_at(cell_info.location)
            if cell is None:
                continue

            cell.move_cost = cell_info.move_cost
            cell.set_top_layer(cell_info.top_layer)

    def find_survivor_location(self, world):
        grid_array = world.get_world_grid()
        closest_survivor_location = None
        closest_distance = float('inf')
        
        world_width = len(grid_array)
        section_width = max(1, world_width // 3)
        
        # First try to find survivors in assigned section
        for x in range(len(grid_array)):
            for y in range(len(grid_array[x])):
                grid_cell = grid_array[x][y]
                grid_location = Location(x, y)

                if grid_cell and grid_cell.survivor_chance > 0 and grid_location not in self.saved_survivors:
                    # Check if survivor is in team's section
                    survivor_section = x // section_width
                    if survivor_section == self.team_number:
                        distance = self.calculate_distance(self._agent.get_location(), grid_location)
                        if distance < closest_distance:
                            closest_survivor_location = grid_location
                            closest_distance = distance
        
        # If no survivors found in assigned section, look anywhere
        if closest_survivor_location is None:
            for x in range(len(grid_array)):
                for y in range(len(grid_array[x])):
                    grid_cell = grid_array[x][y]
                    grid_location = Location(x, y)

                    if grid_cell and grid_cell.survivor_chance > 0 and grid_location not in self.saved_survivors:
                        distance = self.calculate_distance(self._agent.get_location(), grid_location)
                        if distance < closest_distance:
                            closest_survivor_location = grid_location
                            closest_distance = distance

        if closest_survivor_location:
            BaseAgent.log(LogLevels.Always, f"Closest survivor found at {closest_survivor_location}")
            self.survivor_location = closest_survivor_location
            return closest_survivor_location
        else:
            BaseAgent.log(LogLevels.Always, "No accessible survivor found.")
            self.survivor_location = None
            return None

    def calculate_distance(self, current_location, target_location):
        dx = target_location.x - current_location.x
        dy = target_location.y - current_location.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def get_heuristic(self, current, destination):
        x_distance = (destination.x - current.x) ** 2
        y_distance = (destination.y - current.y) ** 2
        euclidean_distance = x_distance + y_distance
        return math.sqrt(euclidean_distance)

    def run_a_star(self, world, goal):
        start = self._agent.get_location()
        priority_queue = []
        path_trace = {}
        heapq.heapify(priority_queue)
        g_costs = {start: 0}
        visited = set()

        heapq.heappush(priority_queue, (0, start))

        while priority_queue:
            _, current_cell = heapq.heappop(priority_queue)

            if current_cell in visited:
                continue

            visited.add(current_cell)

            if current_cell == goal:
                return self.get_first_step_of_path(path_trace, start, goal)

            for direction in Direction:
                neighbor_location = current_cell.add(direction)
                neighbor_grid_cell = world.get_cell_at(neighbor_location)

                if neighbor_location in visited or neighbor_grid_cell is None or neighbor_grid_cell.is_killer_cell() or neighbor_grid_cell.is_fire_cell() or neighbor_grid_cell.is_on_fire():
                    continue

                current_g_cost = g_costs[current_cell] + neighbor_grid_cell.move_cost

                if neighbor_location not in g_costs or current_g_cost < g_costs[neighbor_location]:
                    g_costs[neighbor_location] = current_g_cost
                    h_cost = self.get_heuristic(neighbor_location, goal)
                    f_cost = current_g_cost + h_cost

                    path_trace[neighbor_location] = (current_cell, direction)
                    heapq.heappush(priority_queue, (f_cost, neighbor_location))

        return None

    def get_first_step_of_path(self, came_from, start, goal):
        first_step = None

        current = goal
        while current != start:
            previous, direction = came_from[current]
            if previous == start:
                return direction
            current = previous
        return first_step