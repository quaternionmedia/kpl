from kpl import kpl
import krpc
from math import sqrt
from time import time
from pydantic import BaseModel
from typing import List, Tuple

floats = [ 'angle_of_attack',  'atmosphere_density', 'bedrock_altitude', 'dynamic_pressure', 'elevation', 'equivalent_air_speed', 'g_force', 'heading', 'horizontal_speed', 'latitude', 'longitude', 'mach', 'mean_altitude', 'pitch', 'roll',  'sideslip_angle', 'speed', 'speed_of_sound',  'static_air_temperature', 'static_pressure', 'static_pressure_at_msl', 'surface_altitude', 'terminal_velocity',  'total_air_temperature', 'true_air_speed', 'vertical_speed']
vectors = ['aerodynamic_force', 'center_of_mass', 'direction', 'drag', 'lift', 'velocity']
quaternions = ['rotation']

class Flight(BaseModel):
    angle_of_attack: float
    atmosphere_density: float
    bedrock_altitude: float
    dynamic_pressure: float
    elevation: float
    equivalent_air_speed: float
    g_force: float
    heading: float
    horizontal_speed: float
    latitude: float
    longitude: float
    mach: float
    mean_altitude: float
    pitch: float
    roll: float
    sideslip_angle: float
    speed: float
    speed_of_sound: float
    static_air_temperature: float
    static_pressure: float
    static_pressure_at_msl: float
    surface_altitude: float
    terminal_velocity: float
    total_air_temperature: float
    true_air_speed: float
    vertical_speed: float
    aerodynamic_force: Tuple[float]
    center_of_mass: Tuple[float]
    direction: Tuple[float]
    drag: Tuple[float]
    lift: Tuple[float]
    velocity: Tuple[float]
    rotation: Tuple[float] # quaternion

class Vessel(BaseModel):
    angular_velocity: Tuple[float]
    auto_pilot: float
    available_control_surface_torque: Tuple[Tuple[float]]
    available_engine_torque: Tuple[Tuple[float]]
    available_other_torque: Tuple[Tuple[float]]
    available_rcs_torque: Tuple[Tuple[float]]
    available_reaction_wheel_torque: Tuple[Tuple[float]]
    available_thrust: float
    available_torque: Tuple[Tuple[float]]
    biome: str
    bounding_box: Tuple[Tuple[float]]
    comms: float
    control: float
    # crew: List[krpc.SpaceCenter.CrewMember]
    crew_capacity: int
    crew_count: int
    direction: Tuple[float]
    dry_mass: float
    inertia_tensor: List[float]
    kerbin_sea_level_specific_impulse: float
    mass: float
    max_thrust: float
    max_vacuum_thrust: float
    met: float # mission elapsed time
    moment_of_inertia: Tuple[float]
    name: str
    # orbital_reference_frame:
    # parts: float
    position: Tuple[float]
    recoverable: bool
    # reference_frame:
    # resources: List[krpc.Resources]
    rotation: Tuple[float] # quaternion
    # situation: krpc.VesselSituation
    specific_impulse: float
    # surface_reference_frame:
    # surface_velocity_reference_frame:
    thrust: float
    # type: krpc.VesselType
    vacuum_specific_impulse: float
    velocity: Tuple[float]

class Orbit(BaseModel):
    apoapsis: float
    apoapsis_altitude: float
    argument_of_periapsis: float
    # body: krpc.CelestialBody
    eccentric_anomaly: float
    eccentricity: float
    epoch: float
    inclination: float
    # list_closest_approaches: List(List(float))
    longitude_of_ascending_node: float
    mean_anomaly: float
    # next_orbit: krpc.Orbit
    orbital_speed: float
    periapsis: float
    periapsis_altitude: float
    period: float
    radius: float
    reference_plane_direction: float
    reference_plane_normal: float
    relative_inclination: float
    semi_major_axis: float
    semi_minor_axis: float
    speed: float
    time_of_closest_approach: float
    time_to_apoapsis: float
    time_to_periapsis: float
    time_to_soi_change: float
    true_anomaly: float

class Control(BaseModel):
    abort: bool
    add_node: float
    antennas: bool
    brakes: bool
    cargo_bays: bool
    current_stage: int
    forward: float
    gear: bool
    get_action_group: float
    input_mode: float
    intakes: bool
    legs: bool
    lights: bool
    nodes: float
    parachutes: bool
    pitch: float
    radiators: bool
    rcs: bool
    reaction_wheels: bool
    remove_nodes: float
    resource_harvesters: bool
    resource_harvesters_active: bool
    right: float
    roll: float
    sas: bool
    # sas_mode: SASMode
    set_action_group: float
    solar_panels: bool
    # source: ControlSource
    # speed_mode: SpeedMode
    # state: ControlState
    throttle: float
    toggle_action_group: float
    up: float
    wheel_steering: float
    wheel_throttle: float
    wheels: bool
    yaw: float
    # nodes: List[Nodes]

# class Comms(BaseModel):
#
# class AutoPilot(BaseModel):
#
# class CrewMember(BaseModel):
#
# class CrewMemberType(BaseModel):


vessel = kpl.conn.space_center.active_vessel
refframe = vessel.orbit.body.reference_frame
ranges = []

def symlog(n):
    if n < 0: return -sqrt(sqrt(-n))
    else: return sqrt(sqrt(n))
    # return n/1000000000

def getStats():
    s = flightStats()
    j = {i: round(getattr(s, i), 2) for i in floats}

    v = {i: getattr(s, i) for i in vectors}
    w = {i: (round(v[i][0], 2), round(v[i][1], 2), round(v[i][2], 2)) for i in vectors}
    j['time'] = round(time(), 2)
    return {**j, **w}

flightStats = kpl.conn.add_stream(vessel.flight, refframe)
# print('init stats with:', stats[-1])

def getBodyNames():
    return list(kpl.conn.space_center.bodies.keys())

def getPositions(n, refName):
    print('getting positions from', refName)
    refframe = kpl.conn.space_center.bodies[refName].reference_frame
    bodies = []
    for k, b in kpl.conn.space_center.bodies.items():
        body = {
            'name': k,
            'satellites': [s.name for s in b.satellites],
            'mass': b.mass,
            'position': b.position(refframe),
            'size': b.equatorial_radius,
            }
        if not b.orbit: body['radius'] = 0
        else: body['radius']  = b.orbit.radius
        bodies.append(body)
        # body_names.append(k)
    # pprint(bodies)

    vessels = []
    n = 0
    for i in kpl.conn.space_center.vessels:
        vessels.append({
            'name': str(n) + i.name,
            'orbiting': i.orbit.body.name,
            'radius': i.orbit.radius,
            'position': i.position(refframe),
            'mass': i.mass,
            'satellites': '',
            })
        n += 1
    # pprint(vessels)


    elements = [ { 'data': {
                    'id':i['name'],
                    'label': i['name']},
                'position':{
                    'x': int(2*symlog(i['position'][0])),
                    'y': int(2*symlog(i['position'][2]))
                },} for i in bodies+vessels]
    # pprint(elements)

    for b in bodies:
        if len(b['satellites']) > 0:
            for s in b['satellites']:
                # optional add parents for each satellite
                # elements[body_names.index(s)]['data']['parent'] = b['name']
                # add edge from body to satellite
                elements.append({'data':{'source': b['name'], 'target': s}})
                # print('making edge: ', b['name'], s)
    for v in vessels:
        elements.append({'data':{'source': v['name'], 'target': v['orbiting']}})
    # pprint(elements)
    return elements
