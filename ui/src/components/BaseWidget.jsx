import { Draggable } from "react-beautiful-dnd";
import { useEffect, useState } from "react";

const BaseWidget = ({ id, index, extraClass, children }) => {
  const [column, setColumn] = useState(index % 3); // Initial column

  useEffect(() => {
    setColumn(index % 3); // Update column whenever index changes
  }, [index]);
  // Determine alignment based on column index

  const alignmentClass =
  column === 0 ? "justify-start text-left" : column === 1 ? "justify-center text-center" : "justify-end text-right";


  return (
    <Draggable draggableId={id} index={index}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={`bg-black p-6 rounded-lg shadow-lg flex cursor-grab transition-transform} ${alignmentClass} ${extraClass}`}
        >
          {children}
        </div>
      )}
    </Draggable>
  );
};

export default BaseWidget;