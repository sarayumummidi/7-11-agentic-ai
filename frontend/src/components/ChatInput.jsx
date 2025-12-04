import React, { useState } from 'react'
import SendButton from './SendButton'

const ChatInput = ({ onSend }) => {
  const [text, setText] = useState('')

  const handleSend = () => {
    if (!text.trim()) return
    if (onSend) {
      onSend(text.trim())
    } else {
      console.log('Sent:', text.trim())
    }
    setText('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div
      style={{
        display: 'flex',
        gap: '4px',
        padding: '12px',
        backgroundColor: 'rgba(255, 255, 255, 0.5)',
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
          padding: '8px',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          backgroundColor: 'rgba(255, 255, 255, 0.45)',
          backdropFilter: 'blur(10px) saturate(180%)',
          fontSize: '15px',
          resize: 'none',
          color: '#333',
          fontFamily: 'Manrope, "Segoe UI", sans-serif',
          outline: 'none',
        }}
      />
      <SendButton disabled={!text.trim()} onClick={handleSend} />
    </div>
  )
}

export default ChatInput
