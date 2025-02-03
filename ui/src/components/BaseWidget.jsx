import { Draggable } from "react-beautiful-dnd";

const BaseWidget = ({ id, index, children }) => {
  return (
    <Draggable draggableId={id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className="bg-gray-800 p-6 rounded-lg shadow-lg flex justify-center items-center cursor-grab"
        >
          {children}
        </div>
      )}
    </Draggable>
  );
};

export default BaseWidget;