import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";
import MessageWidget from "./components/MessageWidget";
import WeatherWidget from "./components/WeatherWidget";
import ClockWidget from "./components/ClockWidget";
import { useState } from "react";

function App() {
  const [widgets, setWidgets] = useState([
    { id: "clock", component: <ClockWidget /> },
    { id: "weather", component: <WeatherWidget /> },
    { id: "future1", component: <h2 className="text-xl font-bold">Future Widget 1</h2> },
    { id: "future2", component: <h2 className="text-xl font-bold">Future Widget 2</h2> },
    { id: "message", component: <MessageWidget /> },
    { id: "empty2", component: null },
    { id: "empty3", component: null },
    { id: "empty4", component: null },
  ]);

  const onDragEnd = (result) => {
    if (!result.destination) return;

    const newWidgets = [...widgets];

    // Swap places instead of shifting
    const sourceIndex = result.source.index;
    const destinationIndex = result.destination.index;
    [newWidgets[sourceIndex], newWidgets[destinationIndex]] = [newWidgets[destinationIndex], newWidgets[sourceIndex]];

    setWidgets(newWidgets);
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="h-screen w-screen bg-black text-white flex items-center justify-center">
        <Droppable droppableId="grid">
          {(provided) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className="grid grid-cols-3 grid-rows-3 gap-4 w-4/5 h-4/5"
            >
              {widgets.map((widget, index) => (
                <Draggable key={widget.id} draggableId={widget.id} index={index}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      className={`bg-gray-800 p-6 rounded-lg shadow-lg flex justify-center items-center cursor-grab transition-transform ${
                        snapshot.isDragging ? "scale-105" : "scale-100"
                      }`}
                    >
                      {widget.component}
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder} {/* <-- Ensure this is inside the Droppable div */}
            </div>
          )}
        </Droppable>
      </div>
    </DragDropContext>
  );
}

export default App;