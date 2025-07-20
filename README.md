# Autonomous RC Car MCP Server

This is a comprehensive Model Context Protocol (MCP) server that provides autonomous navigation capabilities for an RC car. The system integrates with a Flask server running on a QNX Pi to control physical motors and camera hardware.

## 🚗 System Overview

The autonomous RC car system consists of:

1. **MCP Server** (`mcp_server.py`) - Provides LLM interface for autonomous navigation
2. **Flask Server** (`flask_motor_control.py`) - Controls physical hardware on QNX Pi
3. **Camera System** - Takes photos and analyzes them with AI
4. **Motor Control** - Controls forward, backward, left, and right movements

## 🛠️ Available Tools

### Movement Tools

#### `move_forward(duration: float = 0.3)`

- **Purpose**: Move the RC car forward
- **Duration**: 0.1-1.0 seconds (default: 0.3s)
- **Use Cases**: Approaching targets, moving toward objectives
- **Precision**: Shorter durations (0.2-0.4s) for fine control

#### `move_backward(duration: float = 0.3)`

- **Purpose**: Move the RC car backward
- **Duration**: 0.1-1.0 seconds (default: 0.3s)
- **Use Cases**: Backing away from obstacles, repositioning
- **Safety**: Useful for avoiding collisions

#### `turn_left(duration: float = 0.3)`

- **Purpose**: Turn the RC car left (rotate in place)
- **Duration**: 0.1-1.0 seconds (default: 0.3s)
- **Use Cases**: Changing direction, aligning with targets
- **Control**: Shorter durations for fine adjustments

#### `turn_right(duration: float = 0.3)`

- **Purpose**: Turn the RC car right (rotate in place)
- **Duration**: 0.1-1.0 seconds (default: 0.3s)
- **Use Cases**: Changing direction, aligning with targets
- **Control**: Shorter durations for fine adjustments

#### `stop_car()`

- **Purpose**: Immediately stop all movement
- **Use Cases**: Safety, pausing movement, reassessing situation
- **Response**: Instant halt of all motors

### Sensing Tools

#### `take_photo_and_analyze(goal_description: str)`

- **Purpose**: Take a photo and analyze it for navigation
- **Input**: Description of what the car is trying to find
- **Output**: AI analysis with recommended next actions
- **Analysis Codes**:
  - `GOAL_ACHIEVED`: Target is centered and reached
  - `MOVE_LEFT`: Target visible on left side
  - `MOVE_RIGHT`: Target visible on right side
  - `MOVE_FORWARD`: Target visible but too far
  - `MOVE_BACKWARD`: Target too close
  - `TURN_LEFT`: Target not visible, search left
  - `TURN_RIGHT`: Target not visible, search right
  - `NOT_FOUND`: Target completely absent

### System Tools

#### `get_car_status()`

- **Purpose**: Get system health and status information
- **Returns**: Connection status, available tools, configuration
- **Use Cases**: Debugging, monitoring system health

## 🧠 Autonomous Navigation Strategy

### Core Principles

1. **Continuous Assessment**: Always take photos to understand current position
2. **Incremental Movement**: Use short, controlled movements (0.2-0.4s)
3. **Visual Feedback**: Analyze each photo to determine next action
4. **Goal-Oriented**: Keep the objective in mind with every decision
5. **Safety First**: Avoid obstacles and use conservative movements

### Navigation Workflow

1. **Initial Assessment**: Take photo to understand current situation
2. **Analysis**: AI analyzes photo based on goal description
3. **Decision**: Choose appropriate movement based on analysis
4. **Execution**: Execute movement with appropriate duration
5. **Reassessment**: Take new photo and repeat process
6. **Goal Achievement**: Continue until target is reached

### Movement Guidelines

- **Forward**: Use for approaching targets or moving toward objectives
- **Backward**: Use for backing away from obstacles or repositioning
- **Left/Right Turns**: Use for changing direction or aligning with targets
- **Fine Adjustments**: Use 0.2-0.3s durations for precise positioning
- **Search Patterns**: Use systematic turns when target is not visible

## 🔧 Configuration

### Network Configuration

```python
BASE_URL = "http://10.33.35.1:5000"  # Flask server on QNX Pi
LAPTOP_IP = "10.33.49.88"  # Laptop IP for processing
LAPTOP_PORT = 8000  # Laptop port for processing
```

### Movement Parameters

```python
DEFAULT_DURATION = 0.3  # Default movement duration
MAX_DURATION = 1.0      # Maximum safe duration
MIN_DURATION = 0.1      # Minimum duration
```

## 🚀 Usage Examples

### Basic Movement

```python
# Move forward for 0.3 seconds
move_forward(duration=0.3)

# Turn left for 0.2 seconds (fine adjustment)
turn_left(duration=0.2)

# Stop all movement
stop_car()
```

### Autonomous Navigation

```python
# Take photo and analyze for goal
result = take_photo_and_analyze("Find a red ball on the ground")

# Based on analysis, execute appropriate movement
if "MOVE_LEFT" in result["analysis_result"]:
    turn_left(duration=0.2)
elif "MOVE_FORWARD" in result["analysis_result"]:
    move_forward(duration=0.3)
```

### Complete Navigation Loop

```python
goal = "Find a keychain object on the ground"

# Initial assessment
photo_result = take_photo_and_analyze(goal)

# Navigation loop
while "GOAL_ACHIEVED" not in photo_result["analysis_result"]:
    # Execute movement based on analysis
    if "MOVE_LEFT" in photo_result["analysis_result"]:
        turn_left(duration=0.2)
    elif "MOVE_RIGHT" in photo_result["analysis_result"]:
        turn_right(duration=0.2)
    elif "MOVE_FORWARD" in photo_result["analysis_result"]:
        move_forward(duration=0.3)
    elif "TURN_LEFT" in photo_result["analysis_result"]:
        turn_left(duration=0.4)
    elif "TURN_RIGHT" in photo_result["analysis_result"]:
        turn_right(duration=0.4)

    # Reassess
    photo_result = take_photo_and_analyze(goal)
```

## 🧪 Testing

### Test Script

Run the comprehensive test suite:

```bash
python test_mcp_server.py
```

### Individual Tests

- Flask server connection
- Movement endpoints
- Photo capture and analysis
- Movement sequences
- Duration control
- Autonomous navigation simulation

## 🔒 Safety Considerations

1. **Duration Limits**: Never use durations longer than 1.0 seconds
2. **Movement Validation**: All durations are clamped to safe ranges
3. **Error Handling**: All requests include timeout and error handling
4. **Stop Function**: Always available for emergency stopping
5. **Conservative Movements**: Default to shorter durations for safety

## 📋 System Requirements

### Hardware

- QNX Pi with motor control hardware
- Camera system for photo capture
- Network connectivity between components

### Software

- Python 3.7+
- FastMCP library
- Requests library
- Flask server running on QNX Pi

### Network

- Flask server accessible at `http://10.33.35.1:5000`
- Laptop processing available at `10.33.49.88:8000`

## 🎯 Best Practices

1. **Frequent Photos**: Take photos often to maintain situational awareness
2. **Short Movements**: Use 0.2-0.4s durations for precise control
3. **Systematic Search**: Use systematic patterns when target is not visible
4. **Goal Focus**: Always keep the objective in mind
5. **Safety First**: Prioritize safety over speed
6. **Error Recovery**: Handle errors gracefully and retry when appropriate

## 🔍 Troubleshooting

### Common Issues

1. **Connection Errors**: Check network connectivity to Flask server
2. **Photo Failures**: Verify camera system is working
3. **Movement Issues**: Check motor connections and power
4. **Analysis Errors**: Verify AI processing system is available

### Debug Commands

```python
# Check system status
status = get_car_status()

# Test individual movements
move_forward(duration=0.1)
stop_car()

# Test photo system
photo_result = take_photo_and_analyze("Test goal")
```

## 📞 Support

For issues or questions:

1. Check the test script output
2. Verify network connectivity
3. Test individual components
4. Review system logs

The autonomous RC car system is designed to be robust, safe, and capable of navigating to find specific objects or locations based on visual feedback and AI analysis.
