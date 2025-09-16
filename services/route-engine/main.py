from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import math
from typing import List, Tuple
import os

app = FastAPI(
    title="LogiChain Route Engine",
    description="Dijkstra Algorithm for Route Optimization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    start_lat: float
    start_lng: float
    stops: List[Tuple[float, float]]
    vehicle_capacity: int = 1000

class RouteEngine:
    def __init__(self):
        self.cache = {}
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate Haversine distance between two points"""
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def dijkstra_shortest_path(self, graph: dict, start: int, end: int) -> Tuple[List[int], float]:
        """Implement Dijkstra's algorithm"""
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        previous = {}
        unvisited = set(graph.keys())
        
        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            
            if current == end:
                break
                
            unvisited.remove(current)
            
            for neighbor, weight in graph[current].items():
                distance = distances[current] + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
        
        # Reconstruct path
        path = []
        current = end
        while current in previous:
            path.append(current)
            current = previous[current]
        path.append(start)
        path.reverse()
        
        return path, distances[end]
    
    def create_graph_from_coordinates(self, coordinates: List[Tuple[float, float]]) -> dict:
        """Create a weighted graph from coordinates"""
        graph = {}
        n = len(coordinates)
        
        for i in range(n):
            graph[i] = {}
            for j in range(n):
                if i != j:
                    lat1, lng1 = coordinates[i]
                    lat2, lng2 = coordinates[j]
                    distance = self.calculate_distance(lat1, lng1, lat2, lng2)
                    graph[i][j] = distance
        
        return graph
    
    def solve_vrp_dijkstra(self, start_point: Tuple[float, float], stops: List[Tuple[float, float]]) -> dict:
        """Solve Vehicle Routing Problem using Dijkstra algorithm"""
        # Create list of all points (start + stops)
        all_points = [start_point] + stops
        graph = self.create_graph_from_coordinates(all_points)
        
        # Use nearest neighbor heuristic with Dijkstra for shortest paths
        route = [0]  # Start at depot (index 0)
        unvisited = set(range(1, len(all_points)))
        current_node = 0
        total_distance = 0
        
        while unvisited:
            # Find nearest unvisited node using Dijkstra
            nearest_node = None
            shortest_distance = float('infinity')
            
            for node in unvisited:
                path, distance = self.dijkstra_shortest_path(graph, current_node, node)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_node = node
            
            if nearest_node is not None:
                route.append(nearest_node)
                unvisited.remove(nearest_node)
                total_distance += shortest_distance
                current_node = nearest_node
        
        # Return to start
        return_path, return_distance = self.dijkstra_shortest_path(graph, current_node, 0)
        route.append(0)
        total_distance += return_distance
        
        return {
            "routes": [route],
            "total_distance": round(total_distance, 2),
            "estimated_time": round(total_distance * 2.5, 0),  # Assume 2.5 minutes per km
            "algorithm": "dijkstra",
            "optimized": True,
            "coordinates": all_points
        }

route_engine = RouteEngine()

@app.get("/")
async def root():
    return {
        "service": "LogiChain Route Engine",
        "algorithm": "Dijkstra",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "route-engine",
        "algorithm": "dijkstra",
        "features": ["vrp_solving", "shortest_path", "real_coordinates"]
    }

@app.post("/optimize")
async def optimize_route(request: RouteRequest):
    """Optimize delivery route using Dijkstra algorithm"""
    try:
        # Validate input
        if not request.stops:
            raise HTTPException(status_code=400, detail="No stops provided")
        
        # Check cache
        cache_key = f"route_{hash(str(request.dict()))}"
        if cache_key in route_engine.cache:
            cached_result = route_engine.cache[cache_key]
            cached_result["cached"] = True
            return cached_result
        
        # Calculate optimal route using Dijkstra
        result = route_engine.solve_vrp_dijkstra(
            (request.start_lat, request.start_lng),
            request.stops
        )
        
        # Cache result
        route_engine.cache[cache_key] = result
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route optimization failed: {str(e)}")

@app.get("/demo/optimize")
async def demo_optimize():
    """Demo route optimization with sample data"""
    sample_request = RouteRequest(
        start_lat=40.7128,
        start_lng=-74.0060,
        stops=[
            (40.7589, -73.9851),  # Central Park
            (40.6892, -74.0445),  # Statue of Liberty area
            (40.7505, -73.9934),  # Times Square
            (40.7061, -74.0087)   # Brooklyn Bridge
        ],
        vehicle_capacity=1000
    )
    
    return await optimize_route(sample_request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
