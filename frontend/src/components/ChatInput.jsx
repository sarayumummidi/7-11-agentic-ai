import React, { useState } from "react";

const ChatInput = ({ onSend }) => {
  const [text, setText] = useState("");

  const handleSend = () => {
    if(!text.trim()) return;
    if(onSend) {
      onSend(text.trim());
    } else {
      console.log("Sent:", text.trim());
    }
    setText("");
  };

  const handleKeyDown = (e) => {
    if(e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return ( 
    <div 
      style={{
        display: "flex",
        gap: "8px",
        padding: "12px",
        borderTop: "1px solid #ddd",
    }}
  >
    <textarea
      rows={1}
      value={text}
      onChange={(e) => setText(e.target.value)}
      onKeyDown={handleKeyDown}
      placeholder="Type a message..."
      style={{
        flex: 1,
        padding: "8px",
        borderRadius: "8px",
        border: "1px solid #ccc",
        resize: "none",
        fontSize: "15px",
      }}
    />
    <button
      onClick={handleSend}
      disabled={!text.trim()}
      style={{
        background: "#a34c46",
        color: "white",
        border: "none",
        borderRadius: "10px",
        padding: "10px",
        fontWeight: "600",
        cursor: "pointer",
        opacity: text.trim() ? 1 : 0.5,
      }}
    >
      Send
    </button>
   </div>
 );
};

export default ChatInput;
