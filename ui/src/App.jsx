import { DragDropContext, Droppable } from "react-beautiful-dnd";
import { useState } from "react";
import BaseWidget from "./components/BaseWidget";
import MessageWidget from "./components/MessageWidget";
import WeatherWidget from "./components/WeatherWidget";
import ClockWidget from "./components/ClockWidget";
import CalendarWidget from "./components/CalendarWidget";

function App() {
  const [widgets, setWidgets] = useState([
    { id: "clock", component: <ClockWidget /> },
    { id: "weather", component: <WeatherWidget /> },
    { id: "calendar", component: <CalendarWidget /> },
    { id: "future2", component: <h2 className="text-xl font-bold">Future Widget 2</h2> },
    { id: "message", component: <MessageWidget />, extraClass: "col-span-3" },
    { id: "empty2", component: null },
    { id: "empty3", component: null },
    { id: "empty4", component: null },
  ]);

  const onDragEnd = (result) => {
    if (!result.destination) return;

    const newWidgets = [...widgets];
    const sourceIndex = result.source.index;
    const destinationIndex = result.destination.index;

    // Swap elements instead of shifting
    [newWidgets[sourceIndex], newWidgets[destinationIndex]] = [newWidgets[destinationIndex], newWidgets[sourceIndex]];

    setWidgets(newWidgets);
};


  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="w-screen h-screen bg-black text-white flex">

        <Droppable droppableId="grid">
          {(provided) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className="w-screen h-screen grid grid-cols-3 grid-rows-3 gap-4 w-4/5 h-4/5"
            >
              {widgets.map((widget, index) => (
                <BaseWidget key={widget.id} id={widget.id} index={index} extraClass={widget.extraClass}>
                  {widget.component}
                </BaseWidget>
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